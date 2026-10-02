"""
AI Agent.

This module implements a simple OpenAI Function Calling loop.

The agent can:

1. Receive a user request
2. Decide whether a tool is needed
3. Execute the selected tool
4. Send the tool output back to the LLM
5. Generate a final response

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

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


# ==========================================================
# TOOL REGISTRY
# ==========================================================
#
# Maps tool names to Python functions.
# The agent uses this registry to execute
# the tool selected by the model.
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
    Executes a complete Function Calling workflow.

    Workflow:

        User Request
              ↓
        OpenAI Model
              ↓
        Tool Selection
              ↓
        Tool Execution
              ↓
        Tool Result
              ↓
        Final Response

    Args:
        user_message (str):
            User request.

    Returns:
        str:
            Final assistant response.
    """
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
                    "Use tools whenever they help answer the request."
                )
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        # ==================================================
        # FIRST MODEL CALL
        # ==================================================
        #
        # OpenAI decides whether a tool is required.
        #
        # ==================================================

        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            tools=OPENAI_TOOLS,
            tool_choice="auto"
        )

        response_message = (
            response.choices[0].message
        )

        # ==================================================
        # NO TOOL REQUIRED
        # ==================================================

        if not response_message.tool_calls:

            return (
                response_message.content
                or "No response generated."
            )

        # ==================================================
        # TOOL CALL DETECTED
        # ==================================================

        tool_call = response_message.tool_calls[0]

        tool_name = tool_call.function.name

        tool_arguments = json.loads(
            tool_call.function.arguments
        )

        # ==================================================
        # VALIDATE TOOL
        # ==================================================

        if tool_name not in TOOL_REGISTRY:

            return (
                f"Unknown tool requested: "
                f"{tool_name}"
            )

        tool_function = TOOL_REGISTRY[
            tool_name
        ]

        # ==================================================
        # EXECUTE TOOL
        # ==================================================

        tool_result = tool_function(
            **tool_arguments
        )

        # ==================================================
        # ADD TOOL CALL TO CONVERSATION
        # ==================================================

        messages.append(response_message)

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

        # ==================================================
        # FINAL MODEL CALL
        # ==================================================
        #
        # Model receives tool output and generates
        # a human-readable answer.
        #
        # ==================================================

        final_response = (
            client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages
            )
        )

        return (
            final_response
            .choices[0]
            .message
            .content
            or "No response generated."
        )

    except Exception as ex:

        return (
            f"Agent execution error: {str(ex)}"
        )