"""
统计分析页面模块
负责统计分析功能
"""

import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
from src.utils.session_manager import SessionManager


def render_statistics_page():
    """渲染统计分析页面"""
    st.markdown('<h2 class="sub-header">📊 统计分析</h2>', unsafe_allow_html=True)
    
    # 获取会话管理器
    session_manager = SessionManager()
    
    # 检查是否有数据
    if not session_manager.has_data():
        st.warning("⚠️ 请先上传数据文件")
        return
    
    data = session_manager.get_data()
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numeric_cols:
        st.warning("⚠️ 数据中没有数值型列，无法进行统计分析")
        return
    
    # 描述性统计
    st.subheader("📈 描述性统计")
    selected_cols = st.multiselect("选择要分析的列", numeric_cols, default=numeric_cols[:3])
    
    if selected_cols:
        desc_stats = data[selected_cols].describe()
        st.dataframe(desc_stats, use_container_width=True)
        
        # 添加更多统计指标
        additional_stats = pd.DataFrame({
            '偏度': data[selected_cols].skew(),
            '峰度': data[selected_cols].kurtosis(),
            '变异系数': data[selected_cols].std() / data[selected_cols].mean(),
            'Q1': data[selected_cols].quantile(0.25),
            'Q3': data[selected_cols].quantile(0.75),
            'IQR': data[selected_cols].quantile(0.75) - data[selected_cols].quantile(0.25)
        })
        st.write("**额外统计指标：**")
        st.dataframe(additional_stats, use_container_width=True)
    
    # 假设检验
    st.subheader("🔬 假设检验")
    test_type = st.selectbox("选择检验类型", ["正态性检验", "t检验", "方差分析", "相关性检验", "卡方检验"])
    
    if test_type == "正态性检验":
        col_name = st.selectbox("选择要检验的列", numeric_cols)
        if st.button("进行正态性检验"):
            statistic, p_value = stats.shapiro(data[col_name].dropna())
            st.write(f"**Shapiro-Wilk 正态性检验结果：**")
            st.write(f"统计量：{statistic:.4f}")
            st.write(f"p值：{p_value:.4f}")
            if p_value > 0.05:
                st.success("✅ 数据符合正态分布 (p > 0.05)")
            else:
                st.warning("⚠️ 数据不符合正态分布 (p ≤ 0.05)")
    
    elif test_type == "t检验":
        col1, col2 = st.columns(2)
        with col1:
            col_name = st.selectbox("选择要检验的列", numeric_cols)
        with col2:
            group_col = st.selectbox("选择分组列", data.select_dtypes(include=['object', 'category']).columns.tolist())
        
        if st.button("进行t检验"):
            groups = data[group_col].unique()
            if len(groups) == 2:
                group1 = data[data[group_col] == groups[0]][col_name].dropna()
                group2 = data[data[group_col] == groups[1]][col_name].dropna()
                statistic, p_value = stats.ttest_ind(group1, group2)
                st.write(f"**独立样本t检验结果：**")
                st.write(f"统计量：{statistic:.4f}")
                st.write(f"p值：{p_value:.4f}")
                if p_value < 0.05:
                    st.success("✅ 两组间存在显著差异 (p < 0.05)")
                else:
                    st.warning("⚠️ 两组间无显著差异 (p ≥ 0.05)")
            else:
                st.error("分组列必须恰好有2个不同的值")
    
    st.info("更多统计分析功能正在开发中...")
