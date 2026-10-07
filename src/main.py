"""
Main FastAPI application.

Endpoints:
- GET /health
- POST /agent/chat
- POST /agent/process-document
"""

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from fastapi import UploadFile
from fastapi import File

from pathlib import Path

from src.agent import run_agent

from src.tools import (
    parse_document_tool,
    db_transport_tool
)

from src.database import init_db

from src.schemas import (
    AgentChatRequest,
    AgentChatResponse,
    ProcessDocumentRequest,
    ProcessDocumentResponse
)


# ==========================================================
# APPLICATION STARTUP
# ==========================================================

app = FastAPI(
    title="Smart Logistics Agent",
    description=(
        "Multi-Tool AI Agent for Freight & Logistics"
    ),
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================================
# DATABASE INITIALIZATION
# ==========================================================

init_db()


# ==========================================================
# HEALTH CHECK
# ==========================================================

@app.get("/health")
def health_check():
    """
    Simple application health endpoint.
    """

    return {
        "status": "healthy"
    }


# ==========================================================
# AGENT CHAT
# ==========================================================

@app.post(
    "/agent/chat",
    response_model=AgentChatResponse
)
def chat_with_agent(
    request: AgentChatRequest
):
    """
    Send a natural language request
    to the AI agent.
    """

    try:

        response = run_agent(
            request.message
        )

        return AgentChatResponse(
            response=response
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )


# ==========================================================
# DOCUMENT PROCESSING
# ==========================================================

@app.post(
    "/agent/process-document",
    response_model=ProcessDocumentResponse
)
def process_document(
    request: ProcessDocumentRequest
):
    """
    Parse a shipment PDF document
    and return structured data.
    """

    try:

        result = parse_document_tool(
            request.file_path
        )

        return ProcessDocumentResponse(
            result=result
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )
        
# ==========================================================
# ANALYTICS
# ==========================================================

@app.get("/analytics")
def analytics():
    """
    Returns high-level logistics metrics.
    """

    return {
        "total_shipments": db_transport_tool(
            "count",
            {}
        ),

        "average_cost": db_transport_tool(
            "average_cost",
            {}
        ),

        "countries": db_transport_tool(
            "list_countries",
            {}
        ),

        "transport_modes": db_transport_tool(
            "list_transport_modes",
            {}
        )
    }

# ==========================================================
# SHIPMENTS
# ==========================================================

@app.get("/shipments")
def get_shipments():
    """
    Return all shipments.
    """

    return db_transport_tool(
        action="list",
        payload={}
    )
    
# ==========================================================
# PDF UPLOAD
# ==========================================================

@app.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...)
):
    """
    Upload and analyze a PDF document.
    """

    upload_dir = Path("uploads")

    upload_dir.mkdir(
        exist_ok=True
    )

    file_path = (
        upload_dir / file.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        content = await file.read()

        buffer.write(content)

    result = parse_document_tool(
        str(file_path)
    )

    return {
        "filename": file.filename,
        "result": result
    }
    
# ==========================================================
# SAVE SHIPMENT
# ==========================================================

@app.post("/save-shipment")
def save_shipment(
    shipment_data: dict
):
    """
    Save a shipment into the database.
    """

    result = db_transport_tool(
        action="create",
        payload=shipment_data
    )

    return result
     
# ==========================================================
# VERSION
# ==========================================================
    
@app.get("/version")
def version():
    """
    Application version.
    """

    return {
        "application": "smart-logistics-agent",
        "version": "1.0.0"
    }