"""
数据洞察页面模块
负责数据洞察功能
"""

import streamlit as st
import pandas as pd
import numpy as np
from src.utils.session_manager import SessionManager


def render_insights_page():
    """渲染数据洞察页面"""
    st.markdown('<h2 class="sub-header">👁️ 数据洞察</h2>', unsafe_allow_html=True)
    
    # 获取会话管理器
    session_manager = SessionManager()
    
    # 检查是否有数据
    if not session_manager.has_data():
        st.warning("⚠️ 请先上传数据文件")
        return
    
    data = session_manager.get_data()
    
    # 数眸品牌介绍
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px rgba(30, 64, 175, 0.3);
    ">
        <h3 style="color: white; margin-bottom: 20px; text-align: center;">👁️ 数眸 - 专业数据洞察平台</h3>
        <p style="font-size: 18px; line-height: 1.8; margin-bottom: 20px; text-align: center;">
            <strong>💡 基于业界标准工具：</strong><br>
            集成YData Profiling、Sweetviz等专业数据分析工具，提供企业级数据洞察能力。
        </p>
        <div style="display: flex; gap: 25px; margin-bottom: 20px;">
            <div style="flex: 1; background: rgba(255,255,255,0.15); padding: 20px; border-radius: 12px; backdrop-filter: blur(10px);">
                <h4 style="color: #FDE68A; margin-bottom: 15px;">📊 YData Profiling</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 15px;">
                    <li>全面数据质量评估</li>
                    <li>智能相关性分析</li>
                    <li>缺失值模式识别</li>
                    <li>专业统计报告</li>
                </ul>
            </div>
            <div style="flex: 1; background: rgba(255,255,255,0.15); padding: 20px; border-radius: 12px; backdrop-filter: blur(10px);">
                <h4 style="color: #A7F3D0; margin-bottom: 15px;">🍯 Sweetviz</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 15px;">
                    <li>数据集对比分析</li>
                    <li>训练测试集比较</li>
                    <li>特征分布对比</li>
                    <li>数据漂移检测</li>
                </ul>
            </div>
            <div style="flex: 1; background: rgba(255,255,255,0.15); padding: 20px; border-radius: 12px; backdrop-filter: blur(10px);">
                <h4 style="color: #FECACA; margin-bottom: 15px;">⚡ 快速洞察</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 15px;">
                    <li>一键生成报告</li>
                    <li>交互式可视化</li>
                    <li>多格式导出</li>
                    <li>专业级分析</li>
                </ul>
            </div>
        </div>
        <p style="font-size: 16px; margin: 0; text-align: center; opacity: 0.9;">
            <strong>🎯 专业使命：</strong> 让专业数据分析触手可及，洞察数据背后的真相
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 专业洞察类型选择
    insight_type = st.selectbox(
        "选择专业洞察工具",
        [
            "📊 YData Profiling - 全面分析",
            "🍯 Sweetviz - 对比分析", 
            "⚡ 快速数据洞察",
            "🔍 数据质量评估",
            "🎯 综合数据洞察"
        ],
        help="选择您想要使用的专业数据分析工具"
    )
    

    
    # 检查工具可用性
    from src.utils.insights_helpers import check_tool_availability
    tool_status = check_tool_availability()
    
    # 显示工具状态
    col1, col2, col3 = st.columns(3)
    with col1:
        if tool_status["ydata_profiling"]:
            st.success("✅ YData Profiling 可用")
        else:
            st.error("❌ YData Profiling 不可用")
    with col2:
        if tool_status["sweetviz"]:
            st.success("✅ Sweetviz 可用")
        else:
            st.error("❌ Sweetviz 不可用")
    with col3:
        if tool_status["streamlit_profiling"]:
            st.success("✅ Streamlit Profiling 可用")
        else:
            st.error("❌ Streamlit Profiling 不可用")
    
    # 根据选择的洞察类型执行相应功能
    from src.utils.insights_helpers import (
        render_ydata_profiling_insights,
        render_sweetviz_insights,
        render_quick_insights,
        render_data_quality_assessment,
        render_comprehensive_insights
    )
    
    if insight_type == "📊 YData Profiling - 全面分析":
        render_ydata_profiling_insights(data)
    elif insight_type == "🍯 Sweetviz - 对比分析":
        render_sweetviz_insights(data)
    elif insight_type == "⚡ 快速数据洞察":
        render_quick_insights(data)
    elif insight_type == "🔍 数据质量评估":
        render_data_quality_assessment(data)
    elif insight_type == "🎯 综合数据洞察":
        render_comprehensive_insights(data)
