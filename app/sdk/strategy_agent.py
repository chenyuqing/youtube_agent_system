import requests
import os
from typing import Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

class TimeRange(Enum):
    MONTHS_3 = 3    # 近3个月
    YEAR_1 = 12    # 近1年
    YEARS_2 = 24   # 近2年

class StrategyAgent:
    def __init__(self):
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
        self.OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")
        if not self.OPENROUTER_API_KEY or not self.OPENROUTER_MODEL:
            raise ValueError("OPENROUTER_API_KEY or OPENROUTER_MODEL not found in .env file")

        self.base_url = "https://openrouter.ai/api/v1"

    def _get_date_range(self, time_range: TimeRange) -> tuple[str, str]:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30 * time_range.value)
        return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

    def generate_topic_suggestions(self, articles, time_range: TimeRange = TimeRange.MONTHS_3):
        """根据文章生成选题建议，支持不同的时间范围"""
        start_date, end_date = self._get_date_range(time_range)
        news_summaries = "".join([f"- {a['title']} ({a['url']})\n" for a in articles])

        time_range_text = {
            TimeRange.MONTHS_3: "近3个月",
            TimeRange.YEAR_1: "近1年",
            TimeRange.YEARS_2: "近2年"
        }[time_range]

        prompt = f"""
你是一个为政经类YouTube频道策划选题的AI助手。
根据以下{time_range_text}（{start_date}至{end_date}）的新闻标题和链接，生成5个具备时效性、独特性和观众吸引力的视频选题建议：

新闻标题及链接：
{news_summaries}

每个选题请包含：
1. 标题建议
2. 背景说明（包含信息的时效性）
3. 推荐关键词
4. 是否具争议性（是/否）
5. 参考新闻链接 (请列出所有相关的原始新闻链接)

提示：
- 对于近3个月的内容，重点关注当前热点
- 对于近1年的内容，关注重要趋势和发展
- 对于近2年的内容，注重长期影响和历史对比
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

# === 主流程 ===
if __name__ == "__main__":
    agent = StrategyAgent()
    articles = [
        {"title": "宁德时代香港上市：全球电池霸主的新野心？", "url": "https://example.com/article1"},
        {"title": "全球芯片短缺对电动车行业的影响", "url": "https://example.com/article2"}
    ]

    # 测试不同时间范围
    for time_range in TimeRange:
        print(f"\n=== {time_range.name} 选题建议 ===")
        suggestions = agent.generate_topic_suggestions(articles, time_range)
        print(suggestions)
        print("\n" + "="*50)
