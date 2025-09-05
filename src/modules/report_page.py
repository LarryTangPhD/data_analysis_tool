"""
报告生成页面模块
负责报告生成功能
"""

import streamlit as st
import pandas as pd
import numpy as np
from src.utils.session_manager import SessionManager


def render_report_page():
    """渲染报告生成页面"""
    st.markdown('<h2 class="sub-header">📋 报告生成</h2>', unsafe_allow_html=True)
    
    # 获取会话管理器
    session_manager = SessionManager()
    
    # 检查是否有数据
    if not session_manager.has_data():
        st.warning("⚠️ 请先上传数据文件")
        return
    
    data = session_manager.get_data()
    
    st.subheader("📄 生成分析报告")
    
    if st.button("🚀 生成完整报告"):
        with st.spinner("正在生成报告..."):
            try:
                # 创建简单的报告内容
                report_content = f"""
                # 📊 数据分析报告
                
                ## 📋 数据概览
                - 数据集大小：{len(data)} 行 × {len(data.columns)} 列
                - 内存使用：{data.memory_usage(deep=True).sum() / 1024**2:.2f} MB
                - 缺失值总数：{data.isnull().sum().sum()}
                - 数据类型分布：{', '.join([f'{str(dtype)}({count})' for dtype, count in data.dtypes.value_counts().items()])}
                
                ## 🔍 数据质量评估
                - 缺失值比例：{data.isnull().sum().sum() / (len(data) * len(data.columns)) * 100:.2f}%
                - 重复行比例：{data.duplicated().sum() / len(data) * 100:.2f}%
                
                ## 📈 描述性统计
                {data.select_dtypes(include=[np.number]).describe().to_html() if len(data.select_dtypes(include=[np.number]).columns) > 0 else '数据中没有数值型列'}
                
                ## 📅 报告信息
                - 生成时间：{pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")}
                - 分析平台：数眸智能数据分析平台 v3.0.0 (重构版)
                - 报告类型：自动生成分析报告
                """
                
                # 显示报告
                st.markdown(report_content)
                
                # 下载报告
                st.download_button(
                    label="📥 下载完整报告",
                    data=report_content,
                    file_name="data_analysis_report.md",
                    mime="text/markdown"
                )
                
                st.success("✅ 报告生成成功！")
                
            except Exception as e:
                st.error(f"❌ 报告生成失败：{str(e)}")
    
    st.info("📋 更多报告功能正在开发中，敬请期待！")
