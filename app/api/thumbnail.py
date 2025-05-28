from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from ..sdk.thumbnail_agent import ThumbnailAgent

router = APIRouter()

class ThumbnailRequest(BaseModel):
    title: str
    script_excerpt: str
    style: str = "modern"

class ThumbnailResponse(BaseModel):
    design: Dict[str, Any]
    asset_suggestions: list[str]

@router.post("/thumbnail", response_model=ThumbnailResponse)
async def generate_thumbnail_design(request: ThumbnailRequest):
    try:
        agent = ThumbnailAgent()
        design = agent.generate_thumbnail_design(
            title=request.title,
            script_excerpt=request.script_excerpt,
            style=request.style
        )
        
        suggestions = agent.get_asset_suggestions(design)
        
        return ThumbnailResponse(
            design=design,
            asset_suggestions=suggestions
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
