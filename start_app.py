#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据分析应用快速启动脚本
支持主应用启动和依赖安装
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_dependencies():
    """检查依赖包是否已安装"""
    try:
        import streamlit
        import pandas
        import numpy
        import plotly
        print("✅ 核心依赖包检查通过")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖包: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def start_main_app():
    """启动主应用"""
    print("🚀 启动数据分析应用主程序...")
    print("📱 支持三种模式: 新手模式、中级模式、专业模式")
    print("🌐 应用将在浏览器中打开: http://localhost:8501")
    print("-" * 50)
    print("💡 提示: 在应用中选择'新手模式'即可体验专为初学者设计的功能")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

def install_dependencies():
    """安装依赖包"""
    print("📦 安装项目依赖包...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ 依赖包安装完成")
    except Exception as e:
        print(f"❌ 安装失败: {e}")

def show_info():
    """显示项目信息"""
    print("=" * 60)
    print("📊 数据分析应用 - 核心版本")
    print("=" * 60)
    print("🎯 功能特性:")
    print("  • 三种分析模式: 新手、中级、专业")
    print("  • Material Design 3 现代化界面")
    print("  • AI助手智能分析建议")
    print("  • 完整的数据分析流程")
    print("  • 交互式可视化图表")
    print("  • 自动报告生成")
    print()
    print("📁 项目结构:")
    print("  • app.py - 主应用程序")
    print("  • src/ - 源代码目录")
    print("  • 新手模式已集成在主应用中")
    print()
    print("🚀 启动方式:")
    print("  • python start_app.py - 启动主应用")
    print("  • python start_app.py --install - 安装依赖")
    print("  • streamlit run app.py - 直接启动")
    print()
    print("🎯 新手模式使用:")
    print("  1. 启动应用后选择'新手模式'")
    print("  2. 享受专为初学者设计的引导式体验")
    print("  3. 逐步学习数据分析技能")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="数据分析应用启动器")
    parser.add_argument("--install", action="store_true", help="安装依赖包")
    parser.add_argument("--info", action="store_true", help="显示项目信息")
    
    args = parser.parse_args()
    
    if args.info:
        show_info()
        return
    
    if args.install:
        install_dependencies()
        return
    
    # 检查依赖
    if not check_dependencies():
        print("💡 提示: 运行 'python start_app.py --install' 安装依赖包")
        return
    
    # 启动主应用
    start_main_app()

if __name__ == "__main__":
    main()
