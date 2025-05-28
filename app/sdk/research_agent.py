import requests
import os
from typing import List, Dict
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class ResearchAgent:
    def __init__(self):
        self.SERPER_API_KEY = os.getenv("SERPER_API_KEY")
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
        self.OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")

        if not self.SERPER_API_KEY:
            raise ValueError("SERPER_API_KEY not found in .env file")
        if not self.OPENROUTER_API_KEY or not self.OPENROUTER_MODEL:
            raise ValueError("OPENROUTER_API_KEY or OPENROUTER_MODEL not found in .env file")

        self.base_url = "https://openrouter.ai/api/v1"

    def _get_date_range(self, months_back: int = 3) -> str:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30 * months_back)
        return f"qdr:m{months_back}"  # 使用Google搜索的时间范围参数

    # === Step 1: 使用 Serper.dev 搜索观点与链接 ===
    def search_articles(self, query: str, num_results: int = 5) -> List[Dict]:
        url = "https://google.serper.dev/search"
        
        # 添加时间限制到查询
        time_range = self._get_date_range(3)  # 默认搜索最近3个月
        search_query = f"{query} when:{time_range}"
        
        headers = {
            "X-API-KEY": self.SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        
        params = {
            "q": search_query,
            "num": num_results * 2,  # 多获取一些结果以防部分结果不合适
            "gl": "us",  # 设置地区为美国以获得更多英文结果
            "hl": "en",  # 设置语言为英文
            "tbs": time_range  # 时间范围参数
        }

        try:
            response = requests.post(url, headers=headers, json=params)
            response.raise_for_status()  # 检查请求是否成功
            response_json = response.json()
            
            # 获取搜索结果
            results = response_json.get("organic", [])
            
            # 筛选有效结果
            valid_results = []
            for result in results:
                if ('title' in result and 'link' in result and 
                    result['title'].strip() and result['link'].strip()):
                    valid_results.append({
                        'title': result['title'],
                        'link': result['link'],
                        'snippet': result.get('snippet', '')
                    })
                
                if len(valid_results) >= num_results:
                    break
            
            if not valid_results:
                print("Warning: No valid search results found")
                return []
                
            return valid_results

        except requests.exceptions.RequestException as e:
            print(f"Error during search request: {str(e)}")
            return []
        except Exception as e:
            print(f"Unexpected error during search: {str(e)}")
            return []

    # === Step 2: 使用 OpenRouter 总结观点与数据 ===
    def generate_research_report(self, query: str) -> str:
        articles = self.search_articles(query)
        if not articles:
            return "未找到相关内容。请尝试修改搜索关键词或放宽时间限制。"

        articles_text = "\n\n".join([
            f"标题: {a['title']}\n链接: {a['link']}\n摘要: {a.get('snippet', '无摘要')}"
            for a in articles
        ])

        prompt = f"""
你是一名专业的研究分析师，负责为 YouTube 频道生成深度研究报告。请基于以下搜索结果进行分析：

搜索主题：{query}

搜索结果：
{articles_text}

请提供一份结构化的研究报告，包含以下内容：

1. 主要发现
   - 核心观点总结
   - 各方立场对比
   - 关键事实陈述

2. 数据支持
   - 重要统计数据
   - 关键指标分析
   - 市场/行业数据

3. 趋势分析
   - 当前发展趋势
   - 未来预测
   - 潜在影响

4. 参考来源
   - 按时间顺序列出所有引用的新闻来源
   - 标注每个来源的发布时间（如有）

请使用 Markdown 格式输出，确保内容客观、专业，并注明信息的时效性。
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

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error generating research report: {str(e)}")
            return f"生成研究报告时出错: {str(e)}"

# === 主流程（调试/独立运行用）===
if __name__ == "__main__":
    import traceback
    debug_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "debug")
    os.makedirs(debug_dir, exist_ok=True)
    
    def log_debug(message):
        print(message)
        with open(os.path.join(debug_dir, "debug_log.txt"), "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    
    try:
        log_debug("开始初始化 ResearchAgent...")
        agent = ResearchAgent()
        log_debug("初始化完成")
        
        query = "最新AI技术发展趋势"
        
        # 测试搜索功能
        log_debug("开始测试搜索功能...")
        search_results = agent.search_articles(query, num_results=5)
        log_debug(f"找到 {len(search_results)} 条搜索结果")
        with open(os.path.join(debug_dir, "debug_search.txt"), "w", encoding="utf-8") as f:
            f.write(str(search_results))
        log_debug("搜索结果已保存")
        
        # 测试研究报告生成
        log_debug("开始测试研究报告生成...")
        report = agent.generate_research_report(query)
        with open(os.path.join(debug_dir, "debug_report.txt"), "w", encoding="utf-8") as f:
            f.write(report)
        log_debug("研究报告已保存")
        
    except Exception as e:
        error_msg = f"错误: {str(e)}\n{traceback.format_exc()}"
        log_debug(error_msg)
