from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from typing import List, Dict, Any
from ..sdk.editor_assistant import EditorAssistantAgent # Updated import

router = APIRouter()

class EditorRequest(BaseModel):
    script_segment: str

class EditorResponse(BaseModel):
    keywords: List[str]
    pexels_results: List[Dict[str, Any]]
    ai_image_prompt: Dict[str, str]

class ExportCsvRequest(BaseModel):
    assets: EditorResponse # Expecting the output of the /editor endpoint
    csv_path: str = "fcp_labels.csv"
    segment_duration: int = 10

@router.post("/editor", response_model=EditorResponse)
async def get_editor_recommendations(request: EditorRequest):
    try:
        agent = EditorAssistantAgent()
        recommendations = agent.recommend_assets_for_segment(request.script_segment)
        return EditorResponse(**recommendations)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@router.post("/editor/export-csv")
async def export_editor_assets_to_csv(request: ExportCsvRequest):
    try:
        agent = EditorAssistantAgent()
        # The export_csv_for_fcp method prints to console, but for API,
        # we might want to return the file or a success message.
        # For simplicity, let's just return a success message for now.
        # The file will be created on the server.
        agent.export_csv_for_fcp(request.assets.model_dump(), request.csv_path, request.segment_duration)
        return {"message": f"CSV exported successfully to {request.csv_path}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
