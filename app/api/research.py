from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..sdk.research_agent import ResearchAgent

router = APIRouter()

class ResearchRequest(BaseModel):
    query: str

class ResearchResponse(BaseModel):
    report: str

@router.post("/research", response_model=ResearchResponse)
async def get_research_report(request: ResearchRequest):
    try:
        agent = ResearchAgent()
        report = agent.generate_research_report(request.query)
        return ResearchResponse(report=report)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
