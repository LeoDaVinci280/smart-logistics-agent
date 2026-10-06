"""
AI Agent.

This module implements a multi-step OpenAI Function Calling loop.

The agent can:

1. Receive a user request
2. Decide whether one or more tools are needed
3. Execute the requested tools
4. Send tool outputs back to the LLM
5. Continue the workflow if additional tools are required
6. Generate a final response

Available tools:
- parse_document_tool
- db_transport_tool
- calculate_duty_and_currency_tool
"""

import json

from openai import OpenAI

from src.config import settings

from src.tools import (
    OPENAI_TOOLS,
    parse_document_tool,
    db_transport_tool,
    calculate_duty_and_currency_tool
)


# ==========================================================
# OPENAI CLIENT
# ==========================================================
#
# Centralized OpenAI client used by the agent.
#
# ==========================================================

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


# ==========================================================
# TOOL REGISTRY
# ==========================================================
#
# Maps tool names to Python functions.
#
# Example:
#
# "db_transport_tool"
#           ↓
# db_transport_tool(...)
#
# This allows the agent to dynamically execute
# the tool selected by GPT.
#
# ==========================================================

TOOL_REGISTRY = {
    "parse_document_tool": parse_document_tool,
    "db_transport_tool": db_transport_tool,
    "calculate_duty_and_currency_tool":
        calculate_duty_and_currency_tool
}


# ==========================================================
# AGENT EXECUTION
# ==========================================================

def run_agent(user_message: str) -> str:
    """
    Execute a complete multi-step Function Calling workflow.

    The agent may execute:

    - No tool
    - One tool
    - Several tools sequentially

    Example:

        User Request
              ↓
          Tool #1
              ↓
          Tool #2
              ↓
          Tool #3
              ↓
        Final Answer

    Args:
        user_message (str):
            User request.

    Returns:
        str:
            Final assistant response.
    """

    # ======================================================
    # VALIDATE CONFIGURATION
    # ======================================================

    if not settings.OPENAI_API_KEY:
        return "OpenAI API key is not configured."

    try:

        # ==================================================
        # INITIAL CONVERSATION
        # ==================================================

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a freight and logistics AI assistant. "
                    "You specialize in shipment management, "
                    "customs duty calculations, freight invoicing, "
                    "transport document analysis and logistics operations. "
                    "You may use multiple tools whenever necessary "
                    "to accomplish the user's request. "
                    "Always complete the requested workflow "
                    "before responding."
                )
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        # ==================================================
        # INITIAL MODEL CALL
        # ==================================================
        #
        # GPT decides:
        #
        # - Answer directly
        # - Use one tool
        # - Use several tools
        #
        # ==================================================

        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            tools=OPENAI_TOOLS,
            tool_choice="auto"
        )

        # ==================================================
        # MULTI-STEP TOOL EXECUTION LOOP
        # ==================================================
        #
        # Continue until GPT produces
        # a final answer without requesting tools.
        #
        # ==================================================

        while True:

            response_message = (
                response.choices[0].message
            )

            # ==============================================
            # WORKFLOW COMPLETE
            # ==============================================
            #
            # No tools requested anymore.
            #
            # Return the final answer.
            #
            # ==============================================

            if not response_message.tool_calls:

                return (
                    response_message.content
                    or "No response generated."
                )

            # ==============================================
            # STORE THE ASSISTANT MESSAGE
            # ==============================================

            messages.append(response_message)

            # ==============================================
            # EXECUTE ALL REQUESTED TOOLS
            # ==============================================

            for tool_call in response_message.tool_calls:

                tool_name = (
                    tool_call.function.name
                )

                tool_arguments = json.loads(
                    tool_call.function.arguments
                )

                # ==========================================
                # VALIDATE TOOL
                # ==========================================

                if tool_name not in TOOL_REGISTRY:

                    raise ValueError(
                        f"Unknown tool requested: "
                        f"{tool_name}"
                    )

                tool_function = TOOL_REGISTRY[
                    tool_name
                ]

                # ==========================================
                # EXECUTE TOOL
                # ==========================================

                tool_result = tool_function(
                    **tool_arguments
                )

                # ==========================================
                # STORE TOOL RESULT
                # ==========================================
                #
                # GPT receives the output and can decide
                # whether another tool is required.
                #
                # ==========================================

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(
                            tool_result,
                            indent=2,
                            default=str
                        )
                    }
                )

            # ==============================================
            # ASK GPT WHAT TO DO NEXT
            # ==============================================
            #
            # GPT can:
            #
            # - Call another tool
            # - Call multiple tools
            # - Produce the final answer
            #
            # ==============================================

            response = (
                client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    messages=messages,
                    tools=OPENAI_TOOLS,
                    tool_choice="auto"
                )
            )

    except Exception as ex:

        # ==================================================
        # GLOBAL ERROR HANDLING
        # ==================================================

        return (
            f"Agent execution error: {str(ex)}"
        )