import os
import requests
from typing import Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class YouTubeStrategyAgent:
    def __init__(self):
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
        self.OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")
        if not self.OPENROUTER_API_KEY or not self.OPENROUTER_MODEL:
            raise ValueError("OPENROUTER_API_KEY or OPENROUTER_MODEL not found in .env file")

        self.base_url = "https://openrouter.ai/api/v1"

    def _get_date_range(self, months_back: int = 3) -> tuple[str, str]:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30 * months_back)
        return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

    def _call_api(self, prompt: str) -> str:
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

    def generate_topic_suggestions_from_youtube(
        self,
        topic: str,
        category_id: Optional[str] = None,
        region: str = "US",
        months_back: int = 3
    ) -> str:
        start_date, end_date = self._get_date_range(months_back)
        prompt = f"""
你是一位资深的YouTube内容策略顾问，请基于{start_date}至{end_date}期间的YouTube趋势为以下主题提供专业的选题建议。

【主题方向】
{topic}

【内容分类】
{category_id or "不限"}

【目标地区】
{region}

【时间范围】
{start_date} 至 {end_date}

请提供以下内容：

1. 标题建议
   - 主标题（引人注目且SEO友好）
   - 2-3个备选标题
   - SEO优化建议

2. 内容策略
   - 视频内容重点
   - 目标受众定位
   - 建议时长范围
   - 必须覆盖的要点

3. 差异化建议
   - 竞品分析
   - 独特卖点
   - 创新角度

4. 发布策略
   - 最佳发布时间
   - Tag建议（包含时效性标签）
   - 封面要点
   - 互动引导

请特别关注近期（最近一个月内）的热点话题和趋势。建议以结构化的方式输出，并标注信息的时效性。
"""
        return self._call_api(prompt)

    def generate_topic_suggestions_from_news(
        self,
        topic: str,
        category_id: Optional[str] = None,
        query: Optional[str] = None,
        months_back: int = 3
    ) -> str:
        start_date, end_date = self._get_date_range(months_back)
        prompt = f"""
你是一位资深的YouTube内容策略顾问，请基于{start_date}至{end_date}期间的新闻热点为以下主题提供专业的选题建议。

【主题方向】
{topic}

【新闻分类】
{category_id or "不限"}

【关键词】
{query or "不限"}

【时间范围】
{start_date} 至 {end_date}

请提供以下内容：

1. 标题建议
   - 主标题（新闻时效性强且引人注目）
   - 2-3个备选标题
   - SEO优化建议

2. 内容策略
   - 视频内容重点（特别关注最近一个月内的发展动态）
   - 目标受众定位
   - 建议时长范围
   - 必须覆盖的要点

3. 差异化建议
   - 同类内容分析
   - 独特视角（基于最新发展）
   - 深度拓展方向

4. 发布策略
   - 最佳发布时间（考虑新闻时效性）
   - Tag建议（包含时效性标签）
   - 封面要点
   - 互动引导

请特别关注近期（最近一个月内）的热点新闻。建议以结构化的方式输出，并标注新闻的发布时间和时效性。
"""
        return self._call_api(prompt)

# === 示例运行（调试/独立运行用）===
if __name__ == "__main__":
    agent = YouTubeStrategyAgent()
    
    # 测试YouTube趋势选题
    youtube_strategy = agent.generate_topic_suggestions_from_youtube(
        topic="人工智能发展趋势",
        region="US",
        months_back=3
    )
    print("\n=== YouTube趋势选题 ===\n")
    print(youtube_strategy)
    
    # 测试新闻热点选题
    news_strategy = agent.generate_topic_suggestions_from_news(
        topic="人工智能发展趋势",
        query="ChatGPT",
        months_back=3
    )
    print("\n=== 新闻热点选题 ===\n")
    print(news_strategy)
