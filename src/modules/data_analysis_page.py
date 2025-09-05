"""
数据分析页面模块
负责自动数据分析和统计功能
"""

import streamlit as st
import pandas as pd
import numpy as np
from src.utils.data_processing import (
    calculate_data_quality_score, get_data_info,
    calculate_correlation_matrix
)
from src.utils.visualization_helpers import create_correlation_heatmap, create_histogram
from src.utils.ai_assistant_utils import get_smart_ai_assistant
from src.utils.session_manager import SessionManager


def render_data_analysis_page():
    """渲染数据分析页面"""
    st.markdown('<h2 class="sub-header">🔍 自动数据分析</h2>', unsafe_allow_html=True)
    
    # 获取会话管理器
    session_manager = SessionManager()
    
    # 检查是否有数据
    if not session_manager.has_data():
        st.warning("⚠️ 请先上传数据文件")
        return
    
    data = session_manager.get_data()
    
    st.subheader("📊 数据概览")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("行数", len(data))
    with col2:
        st.metric("列数", len(data.columns))
    with col3:
        st.metric("缺失值", data.isnull().sum().sum())
    with col4:
        st.metric("重复行", data.duplicated().sum())
    
    # 基础统计分析
    st.subheader("📈 描述性统计")
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        st.dataframe(data[numeric_cols].describe(), use_container_width=True)
    else:
        st.info("数据中没有数值型列")
    
    # 相关性分析
    if len(numeric_cols) > 1:
        st.subheader("🔗 相关性分析")
        correlation_matrix = calculate_correlation_matrix(data)
        fig = create_correlation_heatmap(correlation_matrix)
        st.plotly_chart(fig, use_container_width=True)
    
    # 数据分布分析
    st.subheader("📊 数据分布分析")
    if len(numeric_cols) > 0:
        selected_col = st.selectbox("选择要分析的列", numeric_cols)
        if selected_col:
            fig = create_histogram(data, selected_col, title=f"{selected_col} 分布直方图")
            st.plotly_chart(fig, use_container_width=True)
    
    # AI智能分析解释
    st.subheader("🤖 AI智能分析解释")
    
    # 检查AI助手是否可用
    ai_assistant = get_smart_ai_assistant()
    
    if ai_assistant is None:
        st.warning("⚠️ AI助手不可用，请检查API配置")
    else:
        # 收集分析结果
        analysis_results = {
            "数据规模": f"{len(data)}行 × {len(data.columns)}列",
            "数值型列数": len(numeric_cols),
            "缺失值情况": data.isnull().sum().sum(),
            "重复行数": data.duplicated().sum(),
            "数据质量评分": calculate_data_quality_score(data)
        }
        
        if len(numeric_cols) > 0:
            analysis_results["描述性统计"] = data[numeric_cols].describe().to_dict()
        
        if st.button("🤖 获取AI分析解释", type="primary"):
            with st.spinner("AI正在解释分析结果..."):
                try:
                    interpretation = ai_assistant.interpret_auto_analysis(data, analysis_results)
                    
                    st.success("✅ AI分析解释完成！")
                    st.markdown("### 🤖 AI分析结果解释")
                    st.markdown(interpretation)
                    
                except Exception as e:
                    st.error(f"❌ AI解释失败：{str(e)}")
        
        # AI智能问答
        st.write("**💡 有数据分析问题？问问AI助手：**")
        user_question = st.text_area(
            "请输入您的问题：",
            placeholder="例如：这个分析结果说明了什么？如何进一步分析？",
            height=80,
            key="analysis_question"
        )
        
        if st.button("🤖 获取AI回答", key="analysis_ai_answer") and user_question.strip():
            with st.spinner("AI正在思考..."):
                try:
                    data_context = f"数据集包含{len(data)}行{len(data.columns)}列，数值型列{len(numeric_cols)}个，数据质量评分{calculate_data_quality_score(data):.1f}分"
                    answer = ai_assistant.answer_data_question(user_question, data_context, "自动数据分析")
                    
                    st.success("✅ AI回答完成！")
                    st.markdown("### 🤖 AI回答")
                    st.markdown(answer)
                    
                except Exception as e:
                    st.error(f"❌ AI回答失败：{str(e)}")
