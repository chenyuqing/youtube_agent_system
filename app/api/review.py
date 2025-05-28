from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..sdk.review_agent import ReviewerAgent

router = APIRouter()

class ReviewRequest(BaseModel):
    script_text: str
    style: str = "政经理性"

class ReviewResponse(BaseModel):
    revised_script: str

@router.post("/review", response_model=ReviewResponse)
async def review_and_rewrite_script(request: ReviewRequest):
    try:
        agent = ReviewerAgent()
        revised_script = agent.revise_script_workflow(
            script_text=request.script_text,
            style=request.style
        )
        return ReviewResponse(revised_script=revised_script)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
