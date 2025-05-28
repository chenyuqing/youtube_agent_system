from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal
from ..sdk.strategy_agent import StrategyAgent, TimeRange

router = APIRouter()

class StrategyRequest(BaseModel):
    topic: str
    source: Literal["news", "youtube"]
    category_id: str | None = None
    query: str | None = None
    region: str | None = None  # For YouTube trending videos
    time_range: Literal["MONTHS_3", "YEAR_1", "YEARS_2"] = "MONTHS_3"  # 默认为近3个月

class StrategyResponse(BaseModel):
    recommendation: str

@router.post("/strategy", response_model=StrategyResponse)
async def get_strategy_recommendation(request: StrategyRequest):
    try:
        # 将字符串时间范围转换为TimeRange枚举
        time_range = TimeRange[request.time_range]
        
        agent = StrategyAgent()
        
        # 构造文章列表（实际应该从新闻API或YouTube API获取）
        articles = [
            {
                "title": f"{request.topic} 相关新闻",
                "url": "https://example.com/article"
            }
        ]
        
        recommendation = agent.generate_topic_suggestions(
            articles=articles,
            time_range=time_range
        )
        
        if not recommendation:
            raise HTTPException(
                status_code=500,
                detail="未能生成选题建议"
            )
            
        return StrategyResponse(recommendation=recommendation)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
