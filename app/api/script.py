from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..sdk.scriptwriter_agent import ScriptwriterAgent

router = APIRouter()

class ScriptRequest(BaseModel):
    topic_title: str
    research_summary: str
    style: str = "理性分析"
    duration: str = "medium"  # short: <10min, medium: 10-15min, long: >15min

class ScriptResponse(BaseModel):
    script: str

@router.post("/script", response_model=ScriptResponse)
async def generate_video_script(request: ScriptRequest):
    try:
        agent = ScriptwriterAgent()
        script = agent.generate_script(
            topic_title=request.topic_title,
            research_summary=request.research_summary,
            style=request.style,
            duration=request.duration
        )
        return ScriptResponse(script=script)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
