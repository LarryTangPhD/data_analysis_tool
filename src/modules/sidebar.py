"""
侧边栏模块
负责渲染应用的侧边栏功能
"""

import streamlit as st
from src.utils.session_manager import SessionManager
from src.modules.mode_manager import ModeManager


def render_sidebar():
    """渲染侧边栏"""
    with st.sidebar:
        st.markdown("## 🎛️ 控制面板")
        
        # 数据状态显示
        _render_data_status()
        
        # 模式切换
        _render_mode_switcher()
        
        # 快速操作
        _render_quick_actions()
        
        # 设置选项
        _render_settings()
        
        # 帮助信息
        _render_help_info()


def _render_data_status():
    """渲染数据状态"""
    st.markdown("### 📊 数据状态")
    
    session_manager = SessionManager()
    
    if session_manager.has_data():
        data = session_manager.get_data()
        data_info = session_manager.get_data_info()
        
        st.success("✅ 数据已加载")
        st.write(f"**行数：** {data_info['rows']}")
        st.write(f"**列数：** {data_info['columns']}")
        st.write(f"**内存：** {data_info['memory_usage']:.2f} MB")
        
        if session_manager.has_cleaned_data():
            st.success("✅ 数据已清洗")
        else:
            st.info("ℹ️ 数据未清洗")
    else:
        st.warning("⚠️ 未加载数据")
    
    st.markdown("---")


def _render_mode_switcher():
    """渲染模式切换器"""
    st.markdown("### 🎯 分析模式")
    
    mode_manager = ModeManager()
    current_mode = mode_manager.get_current_mode()
    
    # 显示当前模式信息
    mode_info = mode_manager.get_mode_info(current_mode)
    if mode_info:
        st.write(f"**当前模式：** {mode_info['name']}")
        st.write(f"**描述：** {mode_info['description']}")
        
        st.write("**功能特性：**")
        for feature in mode_info['features']:
            st.write(f"• {feature}")
    
    # 模式切换按钮
    if st.button("🔄 切换模式"):
        st.session_state.current_page = "🎯 模式选择"
        st.rerun()
    
    st.markdown("---")


def _render_quick_actions():
    """渲染快速操作"""
    st.markdown("### ⚡ 快速操作")
    
    session_manager = SessionManager()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📁 上传数据", use_container_width=True):
            st.session_state.current_page = "📁 数据上传"
            st.rerun()
        
        if st.button("🧹 数据清洗", use_container_width=True):
            st.session_state.current_page = "🧹 数据清洗"
            st.rerun()
    
    with col2:
        if st.button("📊 数据分析", use_container_width=True):
            st.session_state.current_page = "🔍 自动数据分析"
            st.rerun()
        
        if st.button("📈 可视化", use_container_width=True):
            st.session_state.current_page = "📈 高级可视化"
            st.rerun()
    
    if st.button("🤖 机器学习", use_container_width=True):
        st.session_state.current_page = "🤖 机器学习"
        st.rerun()
    
    if st.button("📋 生成报告", use_container_width=True):
        st.session_state.current_page = "📋 报告生成"
        st.rerun()
    
    st.markdown("---")


def _render_settings():
    """渲染设置选项"""
    st.markdown("### ⚙️ 设置")
    
    # 性能设置
    st.write("**性能设置：**")
    cache_enabled = st.checkbox("启用缓存", value=True, help="启用数据缓存以提高性能")
    
    # 显示设置
    st.write("**显示设置：**")
    show_animations = st.checkbox("显示动画", value=True, help="显示加载动画和过渡效果")
    
    # 数据设置
    st.write("**数据设置：**")
    auto_save = st.checkbox("自动保存", value=True, help="自动保存分析结果")
    
    if st.button("💾 保存设置"):
        st.success("✅ 设置已保存")
    
    st.markdown("---")


def _render_help_info():
    """渲染帮助信息"""
    st.markdown("### ❓ 帮助")
    
    # 快速帮助
    with st.expander("📖 使用指南"):
        st.markdown("""
        **快速开始：**
        1. 📁 上传数据文件
        2. 🧹 清洗数据（可选）
        3. 📊 进行数据分析
        4. 📈 创建可视化图表
        5. 📋 生成分析报告
        
        **支持格式：** CSV, Excel, JSON, Parquet
        **最大文件：** 100MB
        """)
    
    # 快捷键
    with st.expander("⌨️ 快捷键"):
        st.markdown("""
        - `Ctrl+U`: 上传数据
        - `Ctrl+C`: 数据清洗
        - `Ctrl+A`: 数据分析
        - `Ctrl+V`: 可视化
        - `Ctrl+R`: 生成报告
        """)
    
    # 联系信息
    with st.expander("📞 联系我们"):
        st.markdown("""
        **技术支持：**
        - 📧 Email: support@shumou.com
        - 💬 在线客服: 工作日 9:00-18:00
        - 📱 微信: shumou_support
        
        **反馈建议：**
        欢迎提出宝贵意见，帮助我们改进产品！
        """)
    
    # 版本信息
    st.markdown("---")
    st.markdown("**版本：** v3.0.0 (重构版)")
    st.markdown("**更新：** 2024-01-15")
