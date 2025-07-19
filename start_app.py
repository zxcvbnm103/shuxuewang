#!/usr/bin/env python3
"""
启动脚本 - 数学笔记智能搜索系统
"""
import subprocess
import sys
import os
from pathlib import Path

def main():
    """启动Streamlit应用"""
    print("数学笔记智能搜索系统")
    print("=" * 50)
    
    # 检查当前目录
    current_dir = Path.cwd()
    app_file = current_dir / "app.py"
    
    if not app_file.exists():
        print(f"错误：找不到 app.py 文件")
        print(f"当前目录：{current_dir}")
        print("请确保在项目根目录下运行此脚本")
        return 1
    
    print(f"项目目录：{current_dir}")
    print(f"启动应用：{app_file}")
    print()
    
    # 检查依赖
    try:
        import streamlit
        print(f"Streamlit 版本：{streamlit.__version__}")
    except ImportError:
        print(f"错误：未安装 Streamlit")
        print("请运行：pip install -r requirements.txt")
        return 1
    
    # 启动应用
    print("\n启动Web应用...")
    print("应用将在浏览器中自动打开")
    print("访问地址：http://localhost:8501")
    print("\n按 Ctrl+C 停止应用")
    print("=" * 50)
    
    try:
        # 使用subprocess启动streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ]
        
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        print("\n\n应用已停止")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\n启动失败：{e}")
        return 1
    except Exception as e:
        print(f"\n未知错误：{e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())