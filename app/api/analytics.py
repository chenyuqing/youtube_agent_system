from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from ..sdk.analytics_agent import AnalyticsAgent

router = APIRouter()

class PerformanceRequest(BaseModel):
    video_id: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    metrics: Optional[str] = None

class AudienceRequest(BaseModel):
    video_id: str

class OptimizationRequest(BaseModel):
    video_id: str
    metrics: Dict[str, Any]
    audience_data: Dict[str, Any]
    video_metadata: Dict[str, Any]

class KeywordTrackingRequest(BaseModel):
    video_id: str
    keywords: List[str]

class ABTestRequest(BaseModel):
    video_id: str
    current_metrics: Dict[str, Any]

class PerformanceResponse(BaseModel):
    metrics: Dict[str, Any]

class AudienceResponse(BaseModel):
    insights: Dict[str, Any]

class OptimizationResponse(BaseModel):
    suggestions: str

class KeywordTrackingResponse(BaseModel):
    performance: Dict[str, float]

class ABTestResponse(BaseModel):
    suggestions: List[Dict[str, str]]

@router.post("/analytics/performance", response_model=PerformanceResponse)
async def get_video_performance(request: PerformanceRequest):
    try:
        agent = AnalyticsAgent()
        metrics = agent.get_performance_metrics(
            video_id=request.video_id,
            start_date=request.start_date,
            end_date=request.end_date
        )
        return PerformanceResponse(metrics=metrics)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@router.post("/analytics/audience", response_model=AudienceResponse)
async def get_audience_insights(request: AudienceRequest):
    try:
        agent = AnalyticsAgent()
        insights = agent.get_audience_insights(video_id=request.video_id)
        return AudienceResponse(insights=insights)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@router.post("/analytics/optimize", response_model=OptimizationResponse)
async def get_optimization_suggestions(request: OptimizationRequest):
    try:
        agent = AnalyticsAgent()
        suggestions = agent.generate_optimization_suggestions(
            metrics=request.metrics,
            audience_data=request.audience_data,
            video_metadata=request.video_metadata
        )
        return OptimizationResponse(suggestions=suggestions)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@router.post("/analytics/keywords", response_model=KeywordTrackingResponse)
async def track_keyword_performance(request: KeywordTrackingRequest):
    try:
        agent = AnalyticsAgent()
        performance = agent.track_keyword_performance(
            video_id=request.video_id,
            keywords=request.keywords
        )
        return KeywordTrackingResponse(performance=performance)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@router.post("/analytics/ab-test", response_model=ABTestResponse)
async def get_ab_test_suggestions(request: ABTestRequest):
    try:
        agent = AnalyticsAgent()
        suggestions = agent.generate_ab_test_suggestions(
            video_id=request.video_id,
            current_metrics=request.current_metrics
        )
        return ABTestResponse(suggestions=suggestions)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
