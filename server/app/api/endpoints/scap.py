from fastapi import APIRouter, Response, HTTPException, Depends
from fastapi.responses import FileResponse
import os
from app.core.security import get_current_agent

router = APIRouter()

SCAP_CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))), "scap", "content")

@router.get("/content/{content_id}")
async def download_scap_content(content_id: str, current_agent: int = Depends(get_current_agent)):
    # Ensure directory exists
    os.makedirs(SCAP_CONTENT_DIR, exist_ok=True)
    
    file_path = os.path.join(SCAP_CONTENT_DIR, content_id)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/xml")
        
    # Mock returning an XML datastream if not found, to keep agent working in beta tests
    mock_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<data-stream id="{content_id}">
    <!-- Stubbed SCAP Content -->
</data-stream>
"""
    return Response(content=mock_xml, media_type="application/xml")
