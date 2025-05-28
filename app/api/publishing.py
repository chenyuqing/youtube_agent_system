from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from ..sdk.publishing_agent import PublishingAgent

router = APIRouter()

class SEOMetadataRequest(BaseModel):
    title: str
    description: str
    transcript: str
    category: str = "Education"

class PublishRequest(BaseModel):
    video_file: str
    metadata: Dict[str, Any]
    thumbnail_file: Optional[str] = None
    publish_time: Optional[datetime] = None

class OptimalTimeRequest(BaseModel):
    category: str
    target_regions: List[str] = ["US", "GB", "AU"]

class CardsEndscreenRequest(BaseModel):
    video_id: str
    related_videos: List[str]

class SEOMetadataResponse(BaseModel):
    metadata: Dict[str, Any]

class PublishResponse(BaseModel):
    video_id: str
    status: str
    publish_time: str
    upload_status: str

class OptimalTimeResponse(BaseModel):
    optimal_time: datetime

class CardsEndscreenResponse(BaseModel):
    success: bool
    message: str = ""

@router.post("/publish/seo", response_model=SEOMetadataResponse)
async def generate_seo_metadata(request: SEOMetadataRequest):
    try:
        agent = PublishingAgent()
        metadata = agent.generate_seo_metadata(
            title=request.title,
            description=request.description,
            transcript=request.transcript,
            category=request.category
        )
        return SEOMetadataResponse(metadata=metadata)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@router.post("/publish/schedule", response_model=PublishResponse)
async def schedule_video_upload(request: PublishRequest):
    try:
        agent = PublishingAgent()
        result = agent.schedule_upload(
            video_file=request.video_file,
            metadata=request.metadata,
            thumbnail_file=request.thumbnail_file,
            publish_time=request.publish_time
        )
        return PublishResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@router.post("/publish/optimal-time", response_model=OptimalTimeResponse)
async def get_optimal_publish_time(request: OptimalTimeRequest):
    try:
        agent = PublishingAgent()
        optimal_time = agent.get_optimal_publish_time(
            category=request.category,
            target_regions=request.target_regions
        )
        return OptimalTimeResponse(optimal_time=optimal_time)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@router.post("/publish/cards-endscreen", response_model=CardsEndscreenResponse)
async def setup_cards_and_endscreen(request: CardsEndscreenRequest):
    try:
        agent = PublishingAgent()
        success = agent.setup_cards_and_endscreen(
            video_id=request.video_id,
            related_videos=request.related_videos
        )
        return CardsEndscreenResponse(
            success=success,
            message="已成功设置卡片和片尾画面" if success else "设置失败"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
