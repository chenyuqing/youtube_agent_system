"""初始化系统目录结构"""

import os
from pathlib import Path

def create_directory_structure():
    """创建系统所需的目录结构"""
    base_dir = Path(__file__).parent.parent.parent

    # 定义目录结构
    directories = [
        # assets目录结构
        'assets/images/thumbnails',
        'assets/images/backgrounds',
        'assets/videos/raw',
        'assets/videos/edited',
        'assets/audio/music',
        'assets/audio/sfx',
        'assets/cache',
        'assets/temp',
        'assets/logs',
        
        # credentials目录
        'credentials',
    ]

    # 创建目录
    for directory in directories:
        dir_path = base_dir / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        # 创建.gitkeep文件以保持目录结构
        if not any(dir_path.iterdir()):
            (dir_path / '.gitkeep').touch()

    print("目录结构已创建完成。")
    return True

if __name__ == "__main__":
    create_directory_structure()
