from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..sdk.research_agent import ResearchAgent

router = APIRouter()

class ResearchRequest(BaseModel):
    topic: str
    source: str
    time_range: int

class ResearchResponse(BaseModel):
    report: str

@router.post("/research", response_model=ResearchResponse)
async def get_research_report(request: ResearchRequest):
    try:
        agent = ResearchAgent()
        report = agent.generate_research_report(
            topic=request.topic,
            source=request.source,
            time_range=request.time_range
        )
        return ResearchResponse(report=report)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
