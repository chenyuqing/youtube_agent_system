from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import (
    strategy,
    research,
    script,
    review,
    editor,
    config,
    thumbnail,
    publishing,
    analytics
)
from .core.initialize import create_directory_structure
from .core.config import settings

app = FastAPI(title="YouTube Multi-Agent System API")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化系统目录
create_directory_structure()

# 验证配置
config_status = settings.verify_settings()
if not config_status["is_valid"]:
    print("警告: 配置不完整")
    print(f"缺少的配置项: {config_status['missing_keys']}")
else:
    print("配置验证通过")

# 注册路由
app.include_router(strategy.router, tags=["Strategy"])
app.include_router(research.router, tags=["Research"])
app.include_router(script.router, tags=["Script"])
app.include_router(review.router, tags=["Review"])
app.include_router(editor.router, tags=["Editor"])
app.include_router(config.router, tags=["Config"])
app.include_router(thumbnail.router, tags=["Thumbnail"])
app.include_router(publishing.router, tags=["Publishing"])
app.include_router(analytics.router, tags=["Analytics"])

@app.get("/")
async def root():
    return {
        "message": "YouTube Multi-Agent System API is running",
        "version": "1.0.0",
        "config_status": config_status,
        "endpoints": [
            "/strategy - 生成内容策略",
            "/research - 生成研究报告",
            "/script - 生成视频脚本",
            "/review - 审查和改写脚本",
            "/editor - 剪辑助手",
            "/config - 系统配置",
            "/thumbnail - 生成缩略图设计",
            "/publish - 视频发布管理",
            "/analytics - 数据分析与优化"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
