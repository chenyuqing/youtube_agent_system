"""核心配置管理模块"""

import os
from typing import Dict, Any
# from pydantic_settings import BaseSettings

# 尝试导入python-dotenv，如果没有安装则跳过
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("警告: python-dotenv未安装，使用系统环境变量")

class Settings():
    """系统配置类"""
    # API密钥
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY", "")
    
    # 认证文件路径
    YOUTUBE_CLIENT_SECRETS_FILE: str = os.getenv(
        "YOUTUBE_CLIENT_SECRETS_FILE", 
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                    "credentials", "client_secret.json")  # 注意这里是client_secret.json，不是client_secrets.json
    )
    
    # API锁定状态
    API_LOCK: bool = False
    
    # 数据目录
    ASSETS_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets")
    CREDENTIALS_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "credentials")
    
    class Config:
        case_sensitive = True

    def verify_settings(self) -> Dict[str, Any]:
        """验证配置是否完整"""
        missing_keys = []
        if not self.DEEPSEEK_API_KEY:
            missing_keys.append("DEEPSEEK_API_KEY")
        if not self.YOUTUBE_API_KEY:
            missing_keys.append("YOUTUBE_API_KEY")
        if not os.path.exists(self.YOUTUBE_CLIENT_SECRETS_FILE):
            missing_keys.append("YOUTUBE_CLIENT_SECRETS_FILE")
            
        return {
            "is_valid": len(missing_keys) == 0,
            "missing_keys": missing_keys,
            "credentials_dir_exists": os.path.exists(self.CREDENTIALS_DIR),
            "assets_dir_exists": os.path.exists(self.ASSETS_DIR)
        }

# 创建全局配置实例
settings = Settings()

# 确保必要的目录存在
os.makedirs(settings.CREDENTIALS_DIR, exist_ok=True)
os.makedirs(settings.ASSETS_DIR, exist_ok=True)
