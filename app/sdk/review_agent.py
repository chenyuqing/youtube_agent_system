import os
import requests
from dotenv import load_dotenv

load_dotenv()

class ReviewerAgent:
    def __init__(self):
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
        self.OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")
        if not self.OPENROUTER_API_KEY or not self.OPENROUTER_MODEL:
            raise ValueError("OPENROUTER_API_KEY or OPENROUTER_MODEL not found in .env file")

        self.base_url = "https://openrouter.ai/api/v1"

    def review_script(self, script_text: str, style: str = "政经理性") -> str:
        prompt = f"""
你是一名政经类内容的专业审稿员。请对以下脚本进行内容审查，并输出以下维度：

1. 逻辑合理性：是否存在跳跃推理或因果混乱；
2. 立场平衡性：是否存在明显倾向或激进语言；
3. 数据与事实准确性：是否存在来源不明或数据被误解；
4. 引用来源判断：是否真实、具权威；
5. 改进建议：如何改写更平衡、可信、适合{style}风格；

【原始脚本】
{script_text}
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

        return response.json()["choices"][0]["message"]["content"].strip()

    def rewrite_script(self, script_text: str, review_summary: str, style: str = "政经理性") -> str:
        prompt = f"""
你是一位政经类YouTube频道的AI编剧。请根据以下【脚本草稿】和【审稿建议】对内容进行改写，使其更可信、理性、风格统一。

要求：
- 删除激进或绝对化措辞
- 补充必要背景与因果逻辑
- 表述口语化，适合3~5分钟口播
- 风格参考：“{style}”

【审稿建议】
{review_summary}

【脚本草稿】
{script_text}

请输出改写后的完整脚本。
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

        return response.json()["choices"][0]["message"]["content"].strip()

    def revise_script_workflow(self, script_text: str, style: str = "政经理性") -> str:
        print("🕵️ 正在审稿...")
        review = self.review_script(script_text, style)
        print("✍️ 正在改写...")
        revised = self.rewrite_script(script_text, review, style)
        return revised

# === 示例用法（调试/独立运行用）===
if __name__ == "__main__":
    agent = ReviewerAgent()
    try:
        raw_script = open("scriptwriter_summary.txt", "r", encoding="utf-8").read()
    except FileNotFoundError:
        raw_script = "这是一个虚拟的脚本草稿，用于测试审稿和改写功能。"
        print("Warning: scriptwriter_summary.txt not found. Using dummy script for testing.")

    final_script = agent.revise_script_workflow(raw_script)
    with open("rewritten_script.txt", "w", encoding="utf-8") as f:
        f.write(final_script)
    print("✅ 脚本改写完成，保存在 rewritten_script.txt")
