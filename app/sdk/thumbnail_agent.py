import os
import requests
from dotenv import load_dotenv

load_dotenv()

class ThumbnailAgent:
    def __init__(self):
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
        self.OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")
        if not self.OPENROUTER_API_KEY or not self.OPENROUTER_MODEL:
            raise ValueError("OPENROUTER_API_KEY or OPENROUTER_MODEL not found in .env file")

        self.base_url = "https://openrouter.ai/api/v1"

    def generate_thumbnail_design(self, title: str, script_excerpt: str, style: str = "modern") -> dict:
        prompt = f"""
作为一位专业的YouTube缩略图设计师，请为以下视频设计一个引人注目的缩略图方案。

【视频标题】
{title}

【内容摘要】
{script_excerpt}

【风格要求】
{style}

请提供以下设计方案：

1. 构图布局：
   - 主体元素位置
   - 文字布局
   - 背景处理

2. 配色方案：
   - 主色调
   - 辅助色
   - 文字颜色
   - 背景色

3. 关键视觉元素：
   - 图标/符号建议
   - 图片素材建议
   - 特效处理建议

4. 文字处理：
   - 主标题处理
   - 副标题建议
   - 字体推荐
   - 大小层级

5. 优化建议：
   - 点击率优化建议
   - A/B测试方案
   - 移动端适配建议

请以JSON格式输出，便于后续处理。
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
    agent = ThumbnailAgent()
    design = agent.generate_thumbnail_design(
        title="宁德时代香港上市：全球电池霸主的新野心？",
        script_excerpt="本视频深入分析宁德时代选择在港股二次上市的战略意义...",
        style="modern business"
    )
    print("\n=== 缩略图设计方案 ===\n")
    print(design)
