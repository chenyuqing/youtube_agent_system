import os
import requests
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class PublishingAgent:
    def __init__(self):
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
        self.OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")
        if not self.OPENROUTER_API_KEY or not self.OPENROUTER_MODEL:
            raise ValueError("OPENROUTER_API_KEY or OPENROUTER_MODEL not found in .env file")

        self.base_url = "https://openrouter.ai/api/v1"

    def generate_seo_metadata(
        self,
        title: str,
        description: str,
        transcript: str,
        category: str = "Education"
    ) -> Dict[str, any]:
        prompt = f"""
作为YouTube SEO专家，请为以下视频内容生成优化的元数据。

【视频标题】
{title}

【视频描述】
{description}

【视频文字稿】
{transcript[:500]}...

【视频类别】
{category}

请提供以下SEO优化建议：

1. SEO标题建议：
   - 主标题（考虑关键词）
   - 3-5个备选标题
   - 标题优化说明

2. 描述文案：
   - 首段重点内容
   - 关键信息点
   - 时间戳建议
   - CTA设计

3. 标签组合：
   - 主要标签（5-7个）
   - 相关标签（10-15个）
   - 趋势标签建议

4. 分类设置：
   - 主分类建议
   - 次分类建议
   - 播放列表建议

5. 发布优化：
   - 最佳发布时间
   - 首发推广建议
   - 互动引导设计

请以JSON格式输出，确保包含所有必要的元数据字段。
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
    agent = PublishingAgent()
    metadata = agent.generate_seo_metadata(
        title="宁德时代香港上市：全球电池霸主的新野心？",
        description="深度解析宁德时代二次上市的战略意义和全球布局",
        transcript="这是一个示例文字稿...",
        category="Business"
    )
    print("\n=== SEO元数据 ===\n")
    print(metadata)
