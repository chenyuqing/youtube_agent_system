import os
import requests
import json
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# 设置YouTube API的范围
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
CLIENT_SECRETS_FILE = 'credentials/client_secret.json'

class AnalyticsAgent:
    def __init__(self):
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
        self.OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")
        if not self.OPENROUTER_API_KEY or not self.OPENROUTER_MODEL:
            raise ValueError("OPENROUTER_API_KEY or OPENROUTER_MODEL not found in .env file")

        self.base_url = "https://openrouter.ai/api/v1"
        self.youtube_api = None
        
    def _get_authenticated_service(self):
        """获取已认证的YouTube API服务"""
        try:
            # 检查是否存在已保存的凭据
            if os.path.exists('credentials/youtube_token.json'):
                with open('credentials/youtube_token.json', 'r') as token_file:
                    credentials_data = json.load(token_file)
                    credentials = google.oauth2.credentials.Credentials.from_authorized_user_info(credentials_data)
            else:
                # 如果没有保存的凭据，则进行OAuth2认证流程
                flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                    CLIENT_SECRETS_FILE, SCOPES)
                credentials = flow.run_local_server(port=8080)
                
                # 保存凭据以便下次使用
                with open('credentials/youtube_token.json', 'w') as token_file:
                    token_file.write(credentials.to_json())
            
            # 构建YouTube API客户端
            return googleapiclient.discovery.build(
                API_SERVICE_NAME, API_VERSION, credentials=credentials)
        except Exception as e:
            print(f"认证服务创建失败: {e}")
            return None
            
    def get_performance_metrics(self, video_id: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> Dict[str, any]:
        """获取视频性能指标"""
        # 如果未提供日期，默认使用过去30天
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()
            
        # 确保YouTube API客户端已初始化
        if not self.youtube_api:
            self.youtube_api = self._get_authenticated_service()
            
        if not self.youtube_api:
            # 如果API客户端初始化失败，返回模拟数据
            print("YouTube API客户端初始化失败，返回模拟数据")
            return self._get_mock_performance_metrics()
            
        try:
            # 获取视频基本信息
            video_response = self.youtube_api.videos().list(
                part="snippet,statistics",
                id=video_id
            ).execute()
            
            if not video_response.get('items'):
                raise ValueError(f"未找到ID为{video_id}的视频")
                
            video_info = video_response['items'][0]
            snippet = video_info['snippet']
            statistics = video_info['statistics']
            
            # 构建性能指标
            metrics = {
                "title": snippet.get('title', ''),
                "published_at": snippet.get('publishedAt', ''),
                "views": int(statistics.get('viewCount', 0)),
                "likes": int(statistics.get('likeCount', 0)),
                "comments": int(statistics.get('commentCount', 0)),
                "favorites": int(statistics.get('favoriteCount', 0)),
                # 以下数据需要YouTube Analytics API，这里简化处理
                "watch_time": self._estimate_watch_time(int(statistics.get('viewCount', 0))),
                "avg_view_duration": self._estimate_avg_view_duration(),
                "ctr": self._estimate_ctr(),
                "avg_view_percentage": self._estimate_avg_view_percentage()
            }
            
            return metrics
        except googleapiclient.errors.HttpError as e:
            print(f"YouTube API请求失败: {e}")
            return self._get_mock_performance_metrics()
        except Exception as e:
            print(f"获取性能指标时出错: {e}")
            return self._get_mock_performance_metrics()
    
    def get_audience_insights(self, video_id: str) -> Dict[str, any]:
        """获取受众洞察"""
        # 实际实现中，这需要YouTube Analytics API的更高权限
        # 这里返回模拟数据
        return {
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
    
    def track_keyword_performance(self, video_id: str, keywords: List[str]) -> Dict[str, float]:
        """跟踪关键词性能"""
        # 模拟数据
        return {keyword: round(0.1 + 0.8 * (i / len(keywords)), 2) for i, keyword in enumerate(keywords)}
    
    def generate_ab_test_suggestions(self, video_id: str, current_metrics: Dict[str, any]) -> List[Dict[str, str]]:
        """生成A/B测试建议"""
        # 模拟数据
        return [
            {"element": "缩略图", "suggestion": "尝试使用更鲜艳的颜色和更大的文字"},
            {"element": "标题", "suggestion": "在标题开头添加数字或问号"},
            {"element": "描述", "suggestion": "在描述的前两行添加明确的CTA"}
        ]
    
    # 辅助方法：估算指标
    def _estimate_watch_time(self, views: int) -> int:
        """估算观看时间（秒）"""
        avg_duration = self._estimate_avg_view_duration()
        return int(views * avg_duration)
    
    def _estimate_avg_view_duration(self) -> int:
        """估算平均观看时长（秒）"""
        return 180  # 假设平均3分钟
    
    def _estimate_ctr(self) -> float:
        """估算点击率"""
        return 0.05  # 假设5%
    
    def _estimate_avg_view_percentage(self) -> float:
        """估算平均观看百分比"""
        return 0.65  # 假设65%
    
    def _get_mock_performance_metrics(self) -> Dict[str, any]:
        """获取模拟性能指标"""
        return {
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
