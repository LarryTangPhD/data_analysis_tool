"""
可视化页面模块
负责高级数据可视化功能
"""

import streamlit as st
import pandas as pd
import numpy as np
from src.utils.visualization_helpers import (
    create_bar_chart, create_line_chart, create_scatter_chart, 
    create_pie_chart, create_histogram, create_box_chart, 
    create_correlation_heatmap
)
from src.utils.data_processing import calculate_correlation_matrix
from src.utils.ai_assistant_utils import get_smart_ai_assistant
from src.utils.session_manager import SessionManager


def render_visualization_page():
    """渲染可视化页面"""
    st.markdown('<h2 class="sub-header">📈 高级可视化</h2>', unsafe_allow_html=True)
    
    # 获取会话管理器
    session_manager = SessionManager()
    
    # 检查是否有数据
    if not session_manager.has_data():
        st.warning("⚠️ 请先上传数据文件")
        return
    
    data = session_manager.get_data()
    
    st.subheader("📊 图表类型选择")
    chart_type = st.selectbox(
        "选择图表类型",
        ["柱状图", "折线图", "散点图", "饼图", "直方图", "箱线图", "热力图"]
    )
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if chart_type == "柱状图":
        x_col = st.selectbox("选择X轴列", data.columns.tolist())
        y_col = st.selectbox("选择Y轴列", numeric_cols)
        if x_col and y_col:
            fig = create_bar_chart(data, x_col, y_col, title=f'{y_col} vs {x_col}')
            st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "散点图":
        x_col = st.selectbox("选择X轴列", numeric_cols)
        y_col = st.selectbox("选择Y轴列", numeric_cols)
        color_col = st.selectbox("选择颜色列（可选）", [None] + categorical_cols)
        if x_col and y_col:
            fig = create_scatter_chart(data, x_col, y_col, color_col, title=f'{y_col} vs {x_col}')
            st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "直方图":
        col_name = st.selectbox("选择要分析的列", numeric_cols)
        if col_name:
            fig = create_histogram(data, col_name, title=f'{col_name} 分布直方图')
            st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "箱线图":
        x_col = st.selectbox("选择分组列", categorical_cols)
        y_col = st.selectbox("选择数值列", numeric_cols)
        if x_col and y_col:
            fig = create_box_chart(data, x_col, y_col, title=f'{y_col} 按 {x_col} 分组的箱线图')
            st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "热力图":
        if len(numeric_cols) > 1:
            correlation_matrix = calculate_correlation_matrix(data)
            fig = create_correlation_heatmap(correlation_matrix)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("需要至少2个数值型列来创建热力图")
    
    # AI智能可视化建议
    st.subheader("🤖 AI智能可视化建议")
    
    # 检查AI助手是否可用
    ai_assistant = get_smart_ai_assistant()
    
    if ai_assistant is None:
        st.warning("⚠️ AI助手不可用，请检查API配置")
    else:
        # 选择分析目标
        analysis_goal = st.selectbox(
            "选择分析目标",
            ["trend_analysis", "distribution_comparison", "correlation_analysis", "pattern_detection"],
            format_func=lambda x: {
                "trend_analysis": "趋势分析",
                "distribution_comparison": "分布比较",
                "correlation_analysis": "相关性分析",
                "pattern_detection": "模式检测"
            }[x]
        )
        
        if st.button("🤖 获取AI可视化建议", type="primary"):
            with st.spinner("AI正在分析可视化方案..."):
                try:
                    viz_advice = ai_assistant.suggest_visualization(data, analysis_goal)
                    
                    st.success("✅ AI可视化建议完成！")
                    st.markdown("### 🤖 AI可视化建议")
                    st.markdown(viz_advice)
                    
                except Exception as e:
                    st.error(f"❌ AI建议失败：{str(e)}")
        
        # AI智能问答
        st.write("**💡 有可视化问题？问问AI助手：**")
        user_question = st.text_area(
            "请输入您的问题：",
            placeholder="例如：如何选择合适的图表类型？如何优化图表效果？",
            height=80,
            key="viz_question"
        )
        
        if st.button("🤖 获取AI回答", key="viz_ai_answer") and user_question.strip():
            with st.spinner("AI正在思考..."):
                try:
                    data_context = f"数据集包含{len(data)}行{len(data.columns)}列，数值型列{len(numeric_cols)}个，分类型列{len(categorical_cols)}个"
                    answer = ai_assistant.answer_data_question(user_question, data_context, "高级可视化")
                    
                    st.success("✅ AI回答完成！")
                    st.markdown("### 🤖 AI回答")
                    st.markdown(answer)
                    
                except Exception as e:
                    st.error(f"❌ AI回答失败：{str(e)}")
