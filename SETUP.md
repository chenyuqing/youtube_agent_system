# YouTube Multi-Agent System 设置指南

## 1. 安装依赖

```bash
# 创建并激活虚拟环境（可选但推荐）
python -m venv venv
source venv/bin/activate  # Unix/macOS
# 或者
.\venv\Scripts\activate  # Windows

# 安装依赖包
pip install -r requirements.txt
```

## 2. API密钥配置

1. **复制环境变量模板**:
```bash
cp .env.example .env
```

2. **填写 .env 文件**:
```env
# Deepseek API密钥
DEEPSEEK_API_KEY=你的deepseek密钥

# YouTube API认证
YOUTUBE_API_KEY=你的YouTube API密钥
YOUTUBE_CLIENT_SECRETS_FILE=client_secrets.json的完整路径
```

## 3. YouTube API 设置

1. **创建 Google Cloud 项目**:
   - 访问 [Google Cloud Console](https://console.cloud.google.com/)
   - 创建新项目或选择现有项目
   - 启用 YouTube Data API v3

2. **获取认证文件**:
   - 转到 [API和服务 > 凭据](https://console.cloud.google.com/apis/credentials)
   - 点击 "创建凭据" -> "OAuth 客户端 ID"
   - 选择应用类型：桌面应用
   - 下载 JSON 文件并重命名为 `client_secrets.json`
   - 将文件移动到项目目录（建议：`youtube_agent_system/credentials/client_secrets.json`）

3. **更新 .env 文件**:
```env
YOUTUBE_CLIENT_SECRETS_FILE=/你的完整路径/youtube_agent_system/credentials/client_secrets.json
```

4. **设置 OAuth 2.0 授权界面**:
   - 转到 [OAuth同意屏幕](https://console.cloud.google.com/apis/credentials/consent)
   - 选择"外部"用户类型
   - 填写必要信息
   - 添加以下范围：
     * `https://www.googleapis.com/auth/youtube.readonly`
     * `https://www.googleapis.com/auth/youtube.upload`
     * `https://www.googleapis.com/auth/youtube.force-ssl`

## 4. 验证设置

1. **检查环境变量**:
```python
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('YOUTUBE_API_KEY:', bool(os.getenv('YOUTUBE_API_KEY'))); print('CLIENT_SECRETS_FILE:', os.path.exists(os.getenv('YOUTUBE_CLIENT_SECRETS_FILE')))"
```

2. **验证 YouTube API 访问**:
```python
python -c "from youtube_agent_system.app.sdk.youtube_strategy_agent import YouTubeStrategyAgent; agent = YouTubeStrategyAgent(); print('YouTube API 连接成功')"
```

## 5. 常见问题

1. **ModuleNotFoundError: No module named 'google_auth_oauthlib'**
   ```bash
   pip install google-auth-oauthlib
   ```

2. **client_secrets.json not found**
   - 确保文件路径在 .env 中设置正确
   - 路径应该是绝对路径

3. **API quota exceeded**
   - 检查 [Google Cloud Console](https://console.cloud.google.com/) 的配额使用情况
   - 考虑申请配额提升

4. **认证错误**
   - 确保已添加正确的 OAuth 2.0 范围
   - 检查凭据是否启用
   - 删除旧的令牌文件，重新认证

## 6. 开发建议

1. **API 配额管理**:
   - 使用缓存减少 API 调用
   - 实现请求限制
   - 监控配额使用情况

2. **安全考虑**:
   - 不要将认证文件提交到版本控制
   - 使用环境变量而不是硬编码
   - 定期轮换密钥

3. **调试**:
   - 启用详细日志记录
   - 使用测试账号进行开发
   - 实现错误重试机制

## 7. 运行系统

```bash
# 启动 FastAPI 服务器
uvicorn youtube_agent_system.app.main:app --reload

# 访问 API 文档
open http://localhost:8000/docs
