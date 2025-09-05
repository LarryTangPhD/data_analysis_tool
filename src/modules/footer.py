"""
页脚模块
负责渲染应用的页脚信息
"""

import streamlit as st


def render_footer():
    """渲染页脚"""
    st.markdown("---")
    
    # 页脚内容
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown("""
        <div style="text-align: center;">
            <p style="font-size: 14px; color: #666;">
                👁️ 数眸
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <p style="font-size: 12px; color: #888;">
                让数据洞察如眸般清澈明亮<br>
                智能数据分析平台 v3.0.0 (重构版)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center;">
            <p style="font-size: 12px; color: #666;">
                © 2024 数眸团队
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # 底部链接
    st.markdown("""
    <div style="text-align: center; margin-top: 10px;">
        <a href="#" style="color: #1E40AF; text-decoration: none; margin: 0 10px; font-size: 12px;">使用条款</a>
        <a href="#" style="color: #1E40AF; text-decoration: none; margin: 0 10px; font-size: 12px;">隐私政策</a>
        <a href="#" style="color: #1E40AF; text-decoration: none; margin: 0 10px; font-size: 12px;">帮助中心</a>
        <a href="#" style="color: #1E40AF; text-decoration: none; margin: 0 10px; font-size: 12px;">联系我们</a>
    </div>
    """, unsafe_allow_html=True)
