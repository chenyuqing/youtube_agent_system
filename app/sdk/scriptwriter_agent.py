import os
import requests
from dotenv import load_dotenv

load_dotenv()

class ScriptwriterAgent:
    def __init__(self):
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
        self.OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")
        if not self.OPENROUTER_API_KEY or not self.OPENROUTER_MODEL:
            raise ValueError("OPENROUTER_API_KEY or OPENROUTER_MODEL not found in .env file")

        self.base_url = "https://openrouter.ai/api/v1"

    def _get_duration_range(self, duration: str) -> str:
        duration_ranges = {
            "short": "不超过10分钟",
            "medium": "10~15分钟",
            "long": "15分钟以上"
        }
        return duration_ranges.get(duration, "10~15分钟")

    def generate_script(self, topic_title: str, research_summary: str, style: str = "理性分析", duration: str = "medium"):
        duration_range = self._get_duration_range(duration)
        prompt = f"""
你是一名专业政经类视频编剧，帮助YouTuber撰写可口语化的视频脚本。

请根据以下【选题标题】和【研究摘要】，输出一个{duration_range}的口播脚本。风格参考："{style}"。

要求：
1. 口语化表达，避免书面腔；
2. 结构清晰：引入 → 事件展开 → 双方观点 → 数据支撑 → 结尾总结；
3. 字数控制：
   - 10分钟以下：1200-1500字
   - 10-15分钟：1500-2000字
   - 15分钟以上：2000-2500字
4. 每段不超过500字，适合口播；
5. 最后一段加入引导观众评论、订阅的句子。

【选题标题】
{topic_title}

【研究摘要】
{research_summary}

请开始生成脚本：
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

# === 示例运行（调试/独立运行用）===
if __name__ == "__main__":
    agent = ScriptwriterAgent()
    topic = "宁德时代在香港二次上市的影响与前景"
    try:
        summary = open("research_summary.txt", "r", encoding="utf-8").read()
    except FileNotFoundError:
        summary = "这是一个关于宁德时代在香港二次上市的虚拟研究摘要，用于测试脚本生成功能。"
        print("Warning: research_summary.txt not found. Using dummy summary for testing.")

    script = agent.generate_script(
        topic, 
        summary, 
        style="理性分析 + 隐含批评",
        duration="medium"
    )
    print("\n--- 视频脚本 ---\n")
    print(script)

    with open("scriptwriter_summary.txt", "w", encoding="utf-8") as f:
        f.write(script)
