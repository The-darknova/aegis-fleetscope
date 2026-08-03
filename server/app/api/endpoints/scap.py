from fastapi import APIRouter, Response

router = APIRouter()

@router.get("/content/{content_id}")
async def download_scap_content(content_id: str):
    # Mock returning an XML datastream
    mock_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<data-stream id="{content_id}">
    <!-- Stubbed SCAP Content -->
</data-stream>
"""
    return Response(content=mock_xml, media_type="application/xml")
