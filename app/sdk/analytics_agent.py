import os
import requests
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

class AnalyticsAgent:
    def __init__(self):
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
        self.OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")
        if not self.OPENROUTER_API_KEY or not self.OPENROUTER_MODEL:
            raise ValueError("OPENROUTER_API_KEY or OPENROUTER_MODEL not found in .env file")

        self.base_url = "https://openrouter.ai/api/v1"

    def generate_optimization_suggestions(
        self,
        metrics: Dict[str, any],
        audience_data: Dict[str, any],
        video_metadata: Dict[str, any]
    ) -> str:
        prompt = f"""
作为YouTube频道优化专家，请根据以下数据分析视频表现并提供优化建议。

【性能指标】
{metrics}

【受众数据】
{audience_data}

【视频元数据】
{video_metadata}

请提供以下方面的分析和建议：

1. 整体表现分析：
   - 关键指标评估
   - 与行业标准对比
   - 异常数据分析

2. 受众分析：
   - 核心受众画像
   - 观看行为分析
   - 互动模式分析

3. 内容优化建议：
   - 标题/缩略图优化
   - 视频节奏调整
   - 关键时间点优化

4. 涨粉策略：
   - 订阅者增长分析
   - 粉丝互动建议
   - 留存优化方案

5. 变现建议：
   - 收益优化方向
   - 广告投放建议
   - 合作机会分析

请输出详细的优化报告，重点关注可执行的具体建议。
"""

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.OPENROUTER_API_KEY}"
        }

        data = {
            "model": self.OPENROUTER_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 2000,
        }

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data
        )

        if response.status_code != 200:
            raise Exception(f"OpenRouter API请求失败: {response.text}")

        return response.json()["choices"][0]["message"]["content"]

# === 示例运行（调试/独立运行用）===
if __name__ == "__main__":
    agent = AnalyticsAgent()
    metrics = {
        "views": 10000,
        "watch_time": 50000,
        "avg_view_duration": 300,
        "likes": 500,
        "comments": 100,
        "shares": 50,
        "subscribers_gained": 20,
        "impressions": 20000,
        "ctr": 0.05,
        "avg_view_percentage": 0.65
    }
    audience_data = {
        "demographics": {
            "age_groups": {"18-24": 0.3, "25-34": 0.4, "35-44": 0.2},
            "genders": {"male": 0.6, "female": 0.4},
            "locations": {"US": 0.4, "GB": 0.2, "IN": 0.1}
        },
        "viewer_behavior": {
            "traffic_sources": {
                "suggested": 0.4,
                "browse": 0.3,
                "search": 0.2
            },
            "devices": {
                "mobile": 0.6,
                "desktop": 0.3,
                "tablet": 0.1
            }
        },
        "engagement": {
            "peak_times": ["14:00", "20:00"],
            "retention_drops": [
                {"time": "0:30", "percentage": 0.2},
                {"time": "2:45", "percentage": 0.3}
            ]
        }
    }
    video_metadata = {"title": "测试视频", "tags": ["tag1", "tag2"]}
    suggestions = agent.generate_optimization_suggestions(metrics, audience_data, video_metadata)
    print("\n=== 优化建议 ===\n")
    print(suggestions)
