"""
API schemas.

This module contains the request and response
models used by FastAPI.
"""

from pydantic import BaseModel


class AgentChatRequest(BaseModel):
    """
    User chat request.
    """

    message: str


class AgentChatResponse(BaseModel):
    """
    Agent response.
    """

    response: str


class ProcessDocumentRequest(BaseModel):
    """
    PDF processing request.
    """

    file_path: str


class ProcessDocumentResponse(BaseModel):
    """
    Shipment extraction result.
    """

    result: dict
