from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal, List, Union
from ..sdk.strategy_agent import StrategyAgent, TimeRange
from ..sdk.youtube_strategy_agent import YouTubeStrategyAgent

router = APIRouter()

class StrategyRequest(BaseModel):
    topic: str
    source: Literal["news", "youtube"]
    category_id: str | None = None
    query: str | None = None
    region: Union[str, List[str], None] = None  # 支持单个区域或区域列表
    time_range: Literal["MONTHS_3", "YEAR_1", "YEARS_2"] = "MONTHS_3"  # 默认为近3个月

class StrategyResponse(BaseModel):
    recommendation: str

@router.post("/strategy", response_model=StrategyResponse)
async def get_strategy_recommendation(request: StrategyRequest):
    try:
        # 将字符串时间范围转换为TimeRange枚举
        time_range = TimeRange[request.time_range]
        months_back = time_range.value
        
        # 根据来源选择不同的代理
        if request.source == "youtube":
            agent = YouTubeStrategyAgent()
            
            # 处理区域参数
            region_param = request.region
            if isinstance(region_param, list):
                # 如果是区域列表，生成多个区域的建议并合并
                recommendations = []
                for region in region_param:
                    rec = agent.generate_topic_suggestions_from_youtube(
                        topic=request.topic,
                        category_id=request.category_id,
                        region=region,
                        months_back=months_back
                    )
                    recommendations.append(f"## {region} 地区建议\n\n{rec}")
                
                recommendation = "\n\n".join(recommendations)
            else:
                # 单个区域或默认区域
                region = region_param if region_param else "US"
                recommendation = agent.generate_topic_suggestions_from_youtube(
                    topic=request.topic,
                    category_id=request.category_id,
                    region=region,
                    months_back=months_back
                )
        else:  # news
            agent = YouTubeStrategyAgent()
            recommendation = agent.generate_topic_suggestions_from_news(
                topic=request.topic,
                category_id=request.category_id,
                query=request.query,
                months_back=months_back
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
