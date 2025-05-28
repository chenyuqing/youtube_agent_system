import os
import requests
import re
import json
from dotenv import load_dotenv
from urllib.parse import urlencode
from pathlib import Path

load_dotenv()

class EditorAssistantAgent:
    def __init__(self):
        self.PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
        if not self.PEXELS_API_KEY:
            raise ValueError("PEXELS_API_KEY not found in .env file")

        self.PEXELS_SEARCH_URL = "https://api.pexels.com/videos/search"
        self.PEXELS_HEADERS = {"Authorization": self.PEXELS_API_KEY}
        self.DOWNLOAD_DIR = "./assets/pexels/"

        os.makedirs(self.DOWNLOAD_DIR, exist_ok=True)

    # === Step 1: 提取关键词（简化版） ===
    def extract_keywords(self, text):
        hint_words = [
            "中国", "企业", "工厂", "香港", "投资", "全球化", "制裁", "政策", "议员", "电动车", "芯片", "能源", "会议"
        ]
        return [kw for kw in hint_words if kw in text]

    # === Step 2: 调用 Pexels API 搜索素材 ===
    def search_pexels_videos(self, query, per_page=3):
        params = {"query": query, "per_page": per_page}
        response = requests.get(self.PEXELS_SEARCH_URL, headers=self.PEXELS_HEADERS, params=params)
        if response.status_code != 200:
            print(f"[PEXELS ERROR] {response.status_code}: {response.text}")
            return []
        return response.json().get("videos", [])

    # === Step 3: 下载视频缩略图或封面图（供剪辑预览） ===
    def download_thumbnail(self, video_data):
        video_id = video_data.get("id")
        image_url = video_data.get("image")
        if not video_id or not image_url:
            return None
        file_path = os.path.join(self.DOWNLOAD_DIR, f"pexels_{video_id}.jpg")
        try:
            img = requests.get(image_url)
            with open(file_path, "wb") as f:
                f.write(img.content)
            return file_path
        except Exception as e:
            print(f"Error downloading thumbnail {image_url}: {e}")
            return None

    # === Step 4: AI 图像 Prompt 推荐 ===
    def generate_ai_prompt(self, text):
        return {
            "prompt": f"realistic political economic scene: {text[:50]}...",
            "style": "realism",
            "negative_prompt": "blurry, watermark, distorted, ugly, cartoon, sketch"
        }

    # === 主调度函数 ===
    def recommend_assets_for_segment(self, script_segment: str):
        keywords = self.extract_keywords(script_segment)
        all_videos = []
        thumbnails = [] # This variable is not used in the return, but kept for consistency with original
        for kw in keywords:
            vids = self.search_pexels_videos(kw)
            for v in vids:
                thumb_path = self.download_thumbnail(v)
                thumbnails.append(thumb_path)
                all_videos.append({
                    "keyword": kw,
                    "title": v.get("url"),
                    "thumbnail": thumb_path
                })
        ai_prompt = self.generate_ai_prompt(script_segment)
        return {
            "keywords": keywords,
            "pexels_results": all_videos,
            "ai_image_prompt": ai_prompt
        }

# === 示例用法（调试/独立运行用）===
if __name__ == "__main__":
    agent = EditorAssistantAgent()
    sample_text = "宁德时代这次募资的50%将投向海外，比如匈牙利和印尼的超级工厂。"
    assets = agent.recommend_assets_for_segment(sample_text)
    print(json.dumps(assets, indent=2, ensure_ascii=False))
