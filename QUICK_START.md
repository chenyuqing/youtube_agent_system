# YouTube Multi-Agent System 快速开始指南

## 环境要求

```bash
# 推荐的Python版本
Python 3.8 - 3.10（推荐3.10）

# 操作系统支持
- macOS
- Linux
- Windows
```

## 1. 设置虚拟环境

```bash
# 创建虚拟环境
python3.10 -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
.\venv\Scripts\activate
```

## 2. 安装项目和依赖

```bash
# 升级pip
pip install --upgrade pip

# 进入项目目录（如果还没有）
cd youtube_agent_system

# 首先安装必要的基础依赖
pip install python-dotenv requests fastapi uvicorn

# 然后安装项目（开发模式）
pip install -e .

# 如果遇到依赖问题，可以尝试手动安装其他依赖
pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
pip install numpy==1.24.3 pandas==1.5.3
pip install openai==1.3.7
pip install python-jose passlib bcrypt
pip install "pydantic>=1.10.0,<2.0.0"
```

## 3. 配置认证

1. **创建凭据目录**:
```bash
mkdir -p credentials
```

2. **获取 YouTube API 认证文件**:
   - 访问 [Google Cloud Console](https://console.cloud.google.com/)
   - 创建项目或选择现有项目
   - 启用 YouTube Data API v3
   - 创建 OAuth 2.0 客户端凭据
   - 下载 JSON 文件并重命名为 `client_secret.json`（注意：不是client_secrets.json）
   - 将文件移动到 `credentials` 目录

3. **设置环境变量**:
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑环境变量文件
# macOS/Linux:
nano .env
# Windows:
notepad .env
```

在.env中填写:
```env
DEEPSEEK_API_KEY=your_deepseek_api_key
YOUTUBE_API_KEY=your_youtube_api_key
YOUTUBE_CLIENT_SECRETS_FILE=/absolute/path/to/credentials/client_secret.json
```

## 4. 启动服务

```bash
# 确保在项目根目录下
cd youtube_agent_system

# 启动FastAPI服务器
uvicorn app.main:app --reload

# 访问API文档
open http://localhost:8000/docs
```

## 5. 验证安装

```bash
# 测试环境变量配置
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('配置检查:', all([os.getenv('DEEPSEEK_API_KEY'), os.getenv('YOUTUBE_API_KEY'), os.getenv('YOUTUBE_CLIENT_SECRETS_FILE')]))"

# 测试YouTube API连接
python -c "from app.sdk.youtube_strategy_agent import YouTubeStrategyAgent; agent = YouTubeStrategyAgent(); print('YouTube API 连接成功')"
```

## 常见问题

1. **ModuleNotFoundError: No module named 'dotenv'**
```bash
pip install python-dotenv
```

2. **ModuleNotFoundError: No module named 'xyz'**
```bash
# 确保在项目根目录
pwd  # 应该显示 .../youtube_agent_system

# 重新安装所有依赖
pip install -r requirements.txt
pip install -e .
```

3. **ImportError: numpy/pandas版本问题**
```bash
# 卸载并重新安装指定版本
pip uninstall numpy pandas -y
pip install numpy==1.24.3 pandas==1.5.3
```

4. **认证文件错误**
```bash
# 检查文件路径
ls -l credentials/client_secret.json
# 确保文件权限正确
chmod 600 credentials/client_secret.json
```

5. **配置不完整错误**
```
警告: 配置不完整
缺少的配置项: ['YOUTUBE_CLIENT_SECRETS_FILE']
```

这通常是因为系统找不到YouTube API认证文件。请确保：
- 文件名是`client_secret.json`（注意是单数形式，不是client_secrets.json）
- 文件位于`credentials`目录中
- 在.env文件中设置了正确的路径
- 文件有正确的读取权限

## 使用示例

1. **生成选题策略**:
```python
from app.sdk.youtube_strategy_agent import YouTubeStrategyAgent

agent = YouTubeStrategyAgent()
strategy = agent.generate_strategy(
    topic="AI发展趋势",
    source="youtube",
    region="US"
)
print(strategy)
```

2. **生成研究报告**:
```python
from app.sdk.research_agent import ResearchAgent

agent = ResearchAgent()
report = agent.generate_research("AI在医疗领域的应用")
print(report)
```

更多示例请参考 `frame.md` 中的完整文档。

## 更新日志

参考 SETUP.md 获取完整的设置指南和最新更新。
