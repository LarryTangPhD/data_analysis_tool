"""
数据清洗页面模块
负责数据清洗和预处理功能
"""

import streamlit as st
import pandas as pd
import numpy as np
from src.utils.data_processing import (
    calculate_data_quality_score, get_data_info,
    handle_missing_values, handle_duplicates, handle_outliers
)
from src.utils.ai_assistant_utils import get_smart_ai_assistant
from src.utils.session_manager import SessionManager


def render_data_cleaning_page():
    """渲染数据清洗页面"""
    st.markdown('<h2 class="sub-header">🧹 数据清洗</h2>', unsafe_allow_html=True)
    
    # 获取会话管理器
    session_manager = SessionManager()
    
    # 检查是否有数据
    if not session_manager.has_data():
        st.warning("⚠️ 请先上传数据文件")
        return
    
    data = session_manager.get_data()
    
    # 添加整洁数据说明
    _render_tidy_data_guide()
    
    # 数据概览
    _render_data_overview(data, session_manager)
    
    # 数据清洗功能
    _render_cleaning_functions(data, session_manager)
    
    # 显示清洗结果
    _render_cleaning_results(data, session_manager)
    
    # AI智能清洗建议
    _render_ai_cleaning_advice(data)


def _render_tidy_data_guide():
    """渲染整洁数据指南"""
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    ">
        <h3 style="color: white; margin-bottom: 15px;">📊 整洁数据（Tidy Data）指南</h3>
        <p style="font-size: 16px; line-height: 1.6; margin-bottom: 15px;">
            <strong>💡 什么是整洁数据？</strong><br>
            整洁数据是一种标准化的数据格式，遵循"每行一个观测值，每列一个变量"的原则，让数据分析变得更加高效和准确。
        </p>
        <div style="display: flex; gap: 20px; margin-bottom: 15px;">
            <div style="flex: 1; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                <h4 style="color: #ff6b6b; margin-bottom: 10px;">❌ 避免这样的数据格式</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 14px;">
                    <li>变量信息混合在列名中</li>
                    <li>相同类型的变量分散在不同列</li>
                    <li>一个单元格包含多个值</li>
                    <li>列名不清晰或不一致</li>
                </ul>
            </div>
            <div style="flex: 1; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                <h4 style="color: #51cf66; margin-bottom: 10px;">✅ 推荐这样的数据格式</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 14px;">
                    <li>每行代表一个观测值</li>
                    <li>每列代表一个变量</li>
                    <li>每个单元格只包含一个值</li>
                    <li>变量名清晰明确</li>
                </ul>
            </div>
        </div>
        <p style="font-size: 14px; margin: 0; opacity: 0.9;">
            <strong>🎯 为什么重要？</strong> 整洁数据让统计分析、可视化和机器学习变得更加简单高效！
        </p>
    </div>
    """, unsafe_allow_html=True)


def _render_data_overview(data, session_manager):
    """渲染数据概览"""
    st.subheader("📋 数据概览")
    data_info = get_data_info(data)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("总行数", data_info['rows'])
    with col2:
        st.metric("总列数", data_info['columns'])
    with col3:
        st.metric("缺失值总数", data_info['missing_values'])
    with col4:
        st.metric("重复行数", data_info['duplicate_rows'])
    
    # 数据质量评分
    quality_score = calculate_data_quality_score(data)
    st.write(f"**数据质量评分：** {quality_score:.1f}/100")


def _render_cleaning_functions(data, session_manager):
    """渲染数据清洗功能"""
    st.subheader("🔧 数据清洗")
    
    # 缺失值处理
    st.write("**1. 缺失值处理**")
    missing_strategy = st.selectbox(
        "选择缺失值处理策略",
        ["删除行", "删除列", "均值填充", "中位数填充", "众数填充", "前向填充", "后向填充"]
    )
    
    if st.button("处理缺失值", type="primary"):
        with st.spinner("正在处理缺失值..."):
            data_cleaned = data.copy()
            data_cleaned = handle_missing_values(data_cleaned, missing_strategy)
            session_manager.set_cleaned_data(data_cleaned)
            st.success("✅ 数眸缺失值处理完成！")
    
    # 重复值处理
    st.write("**2. 重复值处理**")
    if st.button("删除重复行"):
        with st.spinner("正在删除重复行..."):
            if session_manager.has_cleaned_data():
                data_cleaned = session_manager.get_cleaned_data()
            else:
                data_cleaned = data.copy()
            data_cleaned = handle_duplicates(data_cleaned)
            session_manager.set_cleaned_data(data_cleaned)
            st.success("✅ 数眸重复值处理完成！")
    
    # 异常值处理
    st.write("**3. 异常值处理**")
    outlier_strategy = st.selectbox(
        "选择异常值处理策略",
        ["IQR方法", "Z-score方法", "百分位法"]
    )
    
    if st.button("处理异常值"):
        with st.spinner("正在处理异常值..."):
            if session_manager.has_cleaned_data():
                data_cleaned = session_manager.get_cleaned_data()
            else:
                data_cleaned = data.copy()
            data_cleaned = handle_outliers(data_cleaned, outlier_strategy)
            session_manager.set_cleaned_data(data_cleaned)
            st.success("✅ 数眸异常值处理完成！")


def _render_cleaning_results(data, session_manager):
    """渲染清洗结果对比"""
    if session_manager.has_cleaned_data():
        st.subheader("📊 清洗结果对比")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**原始数据：**")
            st.write(f"行数：{len(data)}")
            st.write(f"列数：{len(data.columns)}")
            st.write(f"缺失值：{data.isnull().sum().sum()}")
            st.write(f"重复行：{data.duplicated().sum()}")
        
        with col2:
            cleaned_data = session_manager.get_cleaned_data()
            st.write("**清洗后数据：**")
            st.write(f"行数：{len(cleaned_data)}")
            st.write(f"列数：{len(cleaned_data.columns)}")
            st.write(f"缺失值：{cleaned_data.isnull().sum().sum()}")
            st.write(f"重复行：{cleaned_data.duplicated().sum()}")


def _render_ai_cleaning_advice(data):
    """渲染AI智能清洗建议"""
    st.subheader("🤖 AI智能清洗建议")
    
    # 检查AI助手是否可用
    ai_assistant = get_smart_ai_assistant()
    
    if ai_assistant is None:
        st.warning("⚠️ AI助手不可用，请检查API配置")
    else:
        # 选择清洗问题类型
        cleaning_issue = st.selectbox(
            "选择需要AI建议的清洗问题",
            ["missing_values", "duplicates", "outliers", "data_types"],
            format_func=lambda x: {
                "missing_values": "缺失值处理",
                "duplicates": "重复值处理", 
                "outliers": "异常值处理",
                "data_types": "数据类型转换"
            }[x]
        )
        
        if st.button("🤖 获取AI清洗建议", type="primary"):
            with st.spinner("AI正在分析清洗策略..."):
                try:
                    cleaning_advice = ai_assistant.suggest_cleaning_strategy(data, cleaning_issue)
                    
                    st.success("✅ 数眸AI清洗建议完成！")
                    st.markdown("### 🤖 数眸AI清洗策略建议")
                    st.markdown(cleaning_advice)
                    
                except Exception as e:
                    st.error(f"❌ 数眸AI建议失败：{str(e)}")
        
        # AI智能问答
        st.write("**💡 有数据清洗问题？问问数眸AI助手：**")
        user_question = st.text_area(
            "请输入您的问题：",
            placeholder="例如：如何处理这个数据集的缺失值？异常值检测用什么方法？",
            height=80,
            key="cleaning_question"
        )
        
        if st.button("🤖 获取AI回答", key="cleaning_ai_answer") and user_question.strip():
            with st.spinner("AI正在思考..."):
                try:
                    data_context = f"数据集包含{len(data)}行{len(data.columns)}列，缺失值{data.isnull().sum().sum()}个，重复行{data.duplicated().sum()}个"
                    answer = ai_assistant.answer_data_question(user_question, data_context, "数据清洗")
                    
                    st.success("✅ 数眸AI回答完成！")
                    st.markdown("### 🤖 数眸AI回答")
                    st.markdown(answer)
                    
                except Exception as e:
                    st.error(f"❌ 数眸AI回答失败：{str(e)}")
