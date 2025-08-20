"""
页面模块
包含各个页面的绘制功能，将UI与业务逻辑分离
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import warnings
import io
warnings.filterwarnings('ignore')

from src.utils.data_processing import (
    load_data, calculate_correlation_matrix, calculate_data_quality_score,
    get_data_info, handle_missing_values, handle_outliers, handle_duplicates,
    clean_string_data, get_outlier_statistics, convert_data_format,
    get_missing_value_summary, get_data_type_summary
)
from src.utils.visualization_helpers import (
    create_bar_chart, create_line_chart, create_scatter_chart, create_pie_chart,
    create_histogram, create_box_chart, create_heatmap, create_violin_chart,
    create_3d_scatter, create_radar_chart, create_missing_values_chart,
    create_data_type_chart, create_correlation_heatmap, create_distribution_comparison,
    create_learning_curve, create_confusion_matrix, create_feature_importance
)
from src.utils.ml_helpers import (
    validate_data_for_ml, preprocess_data_for_ml, train_classification_model,
    train_regression_model, perform_clustering, perform_cross_validation,
    generate_learning_curve, perform_feature_engineering, analyze_feature_importance,
    detect_outliers_iqr, perform_statistical_tests, calculate_elbow_curve
)
from src.config.settings import (
    NAV_PAGES, CUSTOM_CSS, SUPPORTED_FILE_TYPES, COMPONENT_AVAILABILITY,
    ML_CONFIG, VISUALIZATION_CONFIG, STATISTICAL_CONFIG, DATA_CLEANING_CONFIG,
    ANALYSIS_MODES, AUTHOR_INFO
)


def render_mode_selection_page():
    """渲染模式选择页面 - Material Design 3风格"""
    st.markdown('<h1 class="md-headline" style="text-align: center; margin-bottom: 2rem;">🎯 选择您的分析模式</h1>', unsafe_allow_html=True)
    
    # Material Design 3 欢迎卡片
    st.markdown("""
    <div class="md-card elevated md-animate-fade-in" style="text-align: center; margin-bottom: 3rem;">
        <h2 class="md-title" style="margin-bottom: 1rem;">🚀 欢迎使用智能数据分析平台</h2>
        <p class="md-body" style="margin: 0; opacity: 0.8;">
            请根据您的数据分析经验和需求选择合适的模式，我们将为您提供最适合的分析体验。
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 创建三列布局
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mode = ANALYSIS_MODES["beginner"]
        st.markdown(f"""
        <div class="md-card md-animate-scale-in" style="
            text-align: center;
            border: 2px solid transparent;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
        " onmouseover="this.style.transform='translateY(-8px)'; this.style.boxShadow='0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22)';" 
           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)';">
            <div style="margin-bottom: 1.5rem;">
                <span style="font-size: 4rem; display: block; margin-bottom: 0.5rem;">{mode['icon']}</span>
            </div>
            <h3 class="md-title" style="margin-bottom: 1rem; color: var(--md-primary);">{mode['name']}</h3>
            <p class="md-body" style="margin-bottom: 1.5rem; opacity: 0.8; line-height: 1.6;">
                {mode['description']}
            </p>
            <div class="md-chip" style="
                background: var(--md-primary-container);
                color: var(--md-on-primary-container);
                margin: 0.5rem;
                display: inline-block;
            ">
                ✨ 主要功能
            </div>
            <div style="margin-top: 1rem;">
                {''.join([f'<div class="md-chip" style="margin: 0.25rem; font-size: 0.8rem;">{feature}</div>' for feature in mode['features']])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🌱 选择新手模式", key="beginner_mode", use_container_width=True):
            st.session_state.selected_mode = "beginner"
            st.session_state.current_page = "🏠 首页"
            st.rerun()
    
    with col2:
        mode = ANALYSIS_MODES["intermediate"]
        st.markdown(f"""
        <div class="md-card md-animate-scale-in" style="
            text-align: center;
            border: 2px solid transparent;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
        " onmouseover="this.style.transform='translateY(-8px)'; this.style.boxShadow='0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22)';" 
           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)';">
            <div style="margin-bottom: 1.5rem;">
                <span style="font-size: 4rem; display: block; margin-bottom: 0.5rem;">{mode['icon']}</span>
            </div>
            <h3 class="md-title" style="margin-bottom: 1rem; color: var(--md-secondary);">{mode['name']}</h3>
            <p class="md-body" style="margin-bottom: 1.5rem; opacity: 0.8; line-height: 1.6;">
                {mode['description']}
            </p>
            <div class="md-chip" style="
                background: var(--md-secondary-container);
                color: var(--md-on-secondary-container);
                margin: 0.5rem;
                display: inline-block;
            ">
                ✨ 主要功能
            </div>
            <div style="margin-top: 1rem;">
                {''.join([f'<div class="md-chip" style="margin: 0.25rem; font-size: 0.8rem;">{feature}</div>' for feature in mode['features']])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 选择普通模式", key="intermediate_mode", use_container_width=True):
            st.session_state.selected_mode = "intermediate"
            st.session_state.current_page = "🏠 首页"
            st.rerun()
    
    with col3:
        mode = ANALYSIS_MODES["professional"]
        st.markdown(f"""
        <div class="md-card md-animate-scale-in" style="
            text-align: center;
            border: 2px solid var(--md-tertiary);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            position: relative;
        " onmouseover="this.style.transform='translateY(-8px)'; this.style.boxShadow='0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22)';" 
           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)';">
            <div style="
                position: absolute;
                top: 1rem;
                right: 1rem;
                background: var(--md-tertiary-container);
                color: var(--md-on-tertiary-container);
                padding: 0.5rem 1rem;
                border-radius: var(--md-radius-extra-large);
                font-size: 0.75rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.1em;
            ">
                推荐
            </div>
            <div style="margin-bottom: 1.5rem;">
                <span style="font-size: 4rem; display: block; margin-bottom: 0.5rem;">{mode['icon']}</span>
            </div>
            <h3 class="md-title" style="margin-bottom: 1rem; color: var(--md-tertiary);">{mode['name']}</h3>
            <p class="md-body" style="margin-bottom: 1.5rem; opacity: 0.8; line-height: 1.6;">
                {mode['description']}
            </p>
            <div class="md-chip" style="
                background: var(--md-tertiary-container);
                color: var(--md-on-tertiary-container);
                margin: 0.5rem;
                display: inline-block;
            ">
                ✨ 主要功能
            </div>
            <div style="margin-top: 1rem;">
                {''.join([f'<div class="md-chip" style="margin: 0.25rem; font-size: 0.8rem;">{feature}</div>' for feature in mode['features']])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("⚡ 选择专业模式", key="professional_mode", use_container_width=True):
            st.session_state.selected_mode = "professional"
            st.session_state.current_page = "🏠 首页"
            st.rerun()
    
    # 显示当前选择的模式
    if 'selected_mode' in st.session_state and st.session_state.selected_mode in ANALYSIS_MODES:
        current_mode = ANALYSIS_MODES[st.session_state.selected_mode]
        st.markdown(f"""
        <div class="md-alert success md-animate-fade-in" style="margin-top: 2rem;">
            <span style="font-size: 1.5rem; margin-right: 0.5rem;">✅</span>
            <span class="md-body" style="font-weight: 500;">当前已选择：{current_mode['icon']} {current_mode['name']}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Material Design 3 使用提示卡片
    st.markdown("""
    <div class="md-card filled md-animate-fade-in" style="margin-top: 3rem;">
        <h4 class="md-title" style="color: var(--md-primary); margin-bottom: 1rem;">💡 使用提示</h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
            <div style="padding: 1rem; background: var(--md-surface); border-radius: var(--md-radius-medium);">
                <h5 class="md-body" style="font-weight: 600; margin-bottom: 0.5rem; color: var(--md-primary);">🌱 新手模式</h5>
                <p class="md-body" style="font-size: 0.9rem; opacity: 0.8; margin: 0;">适合数据分析初学者，界面简洁，操作简单</p>
            </div>
            <div style="padding: 1rem; background: var(--md-surface); border-radius: var(--md-radius-medium);">
                <h5 class="md-body" style="font-weight: 600; margin-bottom: 0.5rem; color: var(--md-secondary);">🚀 普通模式</h5>
                <p class="md-body" style="font-size: 0.9rem; opacity: 0.8; margin: 0;">适合有一定经验的用户，功能完整，操作便捷</p>
            </div>
            <div style="padding: 1rem; background: var(--md-surface); border-radius: var(--md-radius-medium);">
                <h5 class="md-body" style="font-weight: 600; margin-bottom: 0.5rem; color: var(--md-tertiary);">⚡ 专业模式</h5>
                <p class="md-body" style="font-size: 0.9rem; opacity: 0.8; margin: 0;">适合专业分析师，功能强大，工具齐全</p>
            </div>
        </div>
        <p class="md-body" style="margin-top: 1rem; opacity: 0.7; font-style: italic;">
            您可以随时在侧边栏切换不同的分析模式。
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_home_page():
    """渲染首页 - Material Design 3风格"""
    # 获取当前选择的模式
    current_mode = st.session_state.get('selected_mode', 'professional')
    
    # 安全检查：确保current_mode是有效的键
    if current_mode not in ANALYSIS_MODES:
        st.error("❌ 无效的模式选择，请重新选择模式")
        st.session_state.selected_mode = 'professional'
        st.session_state.current_page = "🎯 模式选择"
        st.rerun()
        return
    
    mode_info = ANALYSIS_MODES[current_mode]
    
    st.markdown('<h1 class="md-headline" style="text-align: center; margin-bottom: 2rem;">欢迎使用智能数据分析平台</h1>', unsafe_allow_html=True)
    
    # Material Design 3 模式提示卡片
    st.markdown(f"""
    <div class="md-card elevated md-animate-fade-in" style="
        text-align: center;
        margin-bottom: 3rem;
        background: linear-gradient(135deg, var(--md-primary-container) 0%, var(--md-secondary-container) 100%);
        border: 2px solid var(--md-primary);
    ">
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
            <span style="font-size: 2.5rem; margin-right: 1rem;">{mode_info['icon']}</span>
            <div>
                <h2 class="md-title" style="margin: 0; color: var(--md-on-primary-container);">当前模式：{mode_info['name']}</h2>
                <p class="md-body" style="margin: 0.5rem 0 0 0; opacity: 0.8; color: var(--md-on-primary-container);">{mode_info['description']}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 根据模式显示不同的功能卡片
    if current_mode == "beginner":
        # 新手模式 - 简化的功能展示
        st.markdown('<h2 class="md-title" style="text-align: center; margin-bottom: 2rem;">🌱 新手模式功能</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="md-card md-animate-scale-in" style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📁</div>
                <h3 class="md-title" style="color: var(--md-primary);">简单数据上传</h3>
                <p class="md-body" style="opacity: 0.8;">支持常见数据格式，操作简单直观</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="md-card md-animate-scale-in" style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
                <h3 class="md-title" style="color: var(--md-primary);">基础数据预览</h3>
                <p class="md-body" style="opacity: 0.8;">快速查看数据基本信息和统计</p>
            </div>
            """, unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown("""
            <div class="md-card md-animate-scale-in" style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📈</div>
                <h3 class="md-title" style="color: var(--md-primary);">简单图表</h3>
                <p class="md-body" style="opacity: 0.8;">生成基础的可视化图表</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="md-card md-animate-scale-in" style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
                <h3 class="md-title" style="color: var(--md-primary);">AI智能指导</h3>
                <p class="md-body" style="opacity: 0.8;">AI助手提供操作指导和建议</p>
            </div>
            """, unsafe_allow_html=True)
    
    elif current_mode == "intermediate":
        # 普通模式 - 完整功能展示
        st.markdown('<h2 class="md-title" style="text-align: center; margin-bottom: 2rem;">🚀 普通模式功能</h2>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="md-card md-animate-scale-in" style="text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">📁</div>
                <h3 class="md-title" style="color: var(--md-secondary);">数据上传</h3>
                <p class="md-body" style="opacity: 0.8;">支持CSV、Excel、JSON等多种格式</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="md-card md-animate-scale-in" style="text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">🧹</div>
                <h3 class="md-title" style="color: var(--md-secondary);">数据清洗</h3>
                <p class="md-body" style="opacity: 0.8;">智能处理缺失值、异常值和重复值</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="md-card md-animate-scale-in" style="text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">🔍</div>
                <h3 class="md-title" style="color: var(--md-secondary);">自动分析</h3>
                <p class="md-body" style="opacity: 0.8;">快速了解数据特征和分布</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="md-card md-animate-scale-in" style="text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">📊</div>
                <h3 class="md-title" style="color: var(--md-secondary);">统计分析</h3>
                <p class="md-body" style="opacity: 0.8;">基础统计分析和假设检验</p>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # 专业模式 - 完整功能展示
        st.markdown('<h2 class="md-title" style="text-align: center; margin-bottom: 2rem;">⚡ 专业模式功能</h2>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="md-card md-animate-scale-in" style="text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">📁</div>
                <h3 class="md-title" style="color: var(--md-tertiary);">数据上传</h3>
                <p class="md-body" style="opacity: 0.8;">支持CSV、Excel、JSON等多种格式</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="md-card md-animate-scale-in" style="text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">🧹</div>
                <h3 class="md-title" style="color: var(--md-tertiary);">数据清洗</h3>
                <p class="md-body" style="opacity: 0.8;">智能处理缺失值、异常值和重复值</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="md-card md-animate-scale-in" style="text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">🔍</div>
                <h3 class="md-title" style="color: var(--md-tertiary);">自动分析</h3>
                <p class="md-body" style="opacity: 0.8;">使用ydata-profiling等专业工具</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="md-card md-animate-scale-in" style="text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">🤖</div>
                <h3 class="md-title" style="color: var(--md-tertiary);">机器学习</h3>
                <p class="md-body" style="opacity: 0.8;">分类、回归、聚类等算法</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Material Design 3 快速开始指南
    st.markdown('<hr class="md-divider" style="margin: 3rem 0;">', unsafe_allow_html=True)
    st.markdown('<h2 class="md-title" style="text-align: center; margin-bottom: 2rem;">🚀 快速开始</h2>', unsafe_allow_html=True)
    
    if current_mode == "beginner":
        st.markdown("""
        <div class="md-card filled md-animate-fade-in">
            <h3 class="md-title" style="color: var(--md-primary); margin-bottom: 1.5rem;">🌱 新手模式指南</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                <div style="padding: 1rem; background: var(--md-surface); border-radius: var(--md-radius-medium); border-left: 4px solid var(--md-primary);">
                    <h4 class="md-body" style="font-weight: 600; margin-bottom: 0.5rem; color: var(--md-primary);">1. 上传数据</h4>
                    <p class="md-body" style="font-size: 0.9rem; opacity: 0.8; margin: 0;">点击"数据上传"页面，选择您的数据文件</p>
                </div>
                <div style="padding: 1rem; background: var(--md-surface); border-radius: var(--md-radius-medium); border-left: 4px solid var(--md-primary);">
                    <h4 class="md-body" style="font-weight: 600; margin-bottom: 0.5rem; color: var(--md-primary);">2. 查看数据</h4>
                    <p class="md-body" style="font-size: 0.9rem; opacity: 0.8; margin: 0;">系统会自动显示数据的基本信息</p>
                </div>
                <div style="padding: 1rem; background: var(--md-surface); border-radius: var(--md-radius-medium); border-left: 4px solid var(--md-primary);">
                    <h4 class="md-body" style="font-weight: 600; margin-bottom: 0.5rem; color: var(--md-primary);">3. 生成图表</h4>
                    <p class="md-body" style="font-size: 0.9rem; opacity: 0.8; margin: 0;">在"高级可视化"页面创建简单图表</p>
                </div>
                <div style="padding: 1rem; background: var(--md-surface); border-radius: var(--md-radius-medium); border-left: 4px solid var(--md-primary);">
                    <h4 class="md-body" style="font-weight: 600; margin-bottom: 0.5rem; color: var(--md-primary);">4. 获取建议</h4>
                    <p class="md-body" style="font-size: 0.9rem; opacity: 0.8; margin: 0;">AI助手会为您提供分析建议</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    elif current_mode == "intermediate":
        st.markdown("""
        <div class="md-card filled md-animate-fade-in">
            <h3 class="md-title" style="color: var(--md-secondary); margin-bottom: 1.5rem;">🚀 普通模式指南</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                <div style="padding: 1rem; background: var(--md-surface); border-radius: var(--md-radius-medium); border-left: 4px solid var(--md-secondary);">
                    <h4 class="md-body" style="font-weight: 600; margin-bottom: 0.5rem; color: var(--md-secondary);">1. 数据准备</h4>
                    <p class="md-body" style="font-size: 0.9rem; opacity: 0.8; margin: 0;">上传并清洗您的数据</p>
                </div>
                <div style="padding: 1rem; background: var(--md-surface); border-radius: var(--md-radius-medium); border-left: 4px solid var(--md-secondary);">
                    <h4 class="md-body" style="font-weight: 600; margin-bottom: 0.5rem; color: var(--md-secondary);">2. 探索分析</h4>
                    <p class="md-body" style="font-size: 0.9rem; opacity: 0.8; margin: 0;">使用自动分析工具了解数据特征</p>
                </div>
                <div style="padding: 1rem; background: var(--md-surface); border-radius: var(--md-radius-medium); border-left: 4px solid var(--md-secondary);">
                    <h4 class="md-body" style="font-weight: 600; margin-bottom: 0.5rem; color: var(--md-secondary);">3. 可视化</h4>
                    <p class="md-body" style="font-size: 0.9rem; opacity: 0.8; margin: 0;">创建多种类型的图表</p>
                </div>
                <div style="padding: 1rem; background: var(--md-surface); border-radius: var(--md-radius-medium); border-left: 4px solid var(--md-secondary);">
                    <h4 class="md-body" style="font-weight: 600; margin-bottom: 0.5rem; color: var(--md-secondary);">4. 统计分析</h4>
                    <p class="md-body" style="font-size: 0.9rem; opacity: 0.8; margin: 0;">进行基础的统计检验</p>
                </div>
                <div style="padding: 1rem; background: var(--md-surface); border-radius: var(--md-radius-medium); border-left: 4px solid var(--md-secondary);">
                    <h4 class="md-body" style="font-weight: 600; margin-bottom: 0.5rem; color: var(--md-secondary);">5. 生成报告</h4>
                    <p class="md-body" style="font-size: 0.9rem; opacity: 0.8; margin: 0;">导出分析结果</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        st.markdown("""
        <div class="md-card filled md-animate-fade-in">
            <h3 class="md-title" style="color: var(--md-tertiary); margin-bottom: 1.5rem;">⚡ 专业模式指南</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                <div style="padding: 1rem; background: var(--md-surface); border-radius: var(--md-radius-medium); border-left: 4px solid var(--md-tertiary);">
                    <h4 class="md-body" style="font-weight: 600; margin-bottom: 0.5rem; color: var(--md-tertiary);">1. 数据预处理</h4>
                    <p class="md-body" style="font-size: 0.9rem; opacity: 0.8; margin: 0;">使用高级工具清洗和转换数据</p>
                </div>
                <div style="padding: 1rem; background: var(--md-surface); border-radius: var(--md-radius-medium); border-left: 4px solid var(--md-tertiary);">
                    <h4 class="md-body" style="font-weight: 600; margin-bottom: 0.5rem; color: var(--md-tertiary);">2. 深度分析</h4>
                    <p class="md-body" style="font-size: 0.9rem; opacity: 0.8; margin: 0;">进行全面的探索性数据分析</p>
                </div>
                <div style="padding: 1rem; background: var(--md-surface); border-radius: var(--md-radius-medium); border-left: 4px solid var(--md-tertiary);">
                    <h4 class="md-body" style="font-weight: 600; margin-bottom: 0.5rem; color: var(--md-tertiary);">3. 高级可视化</h4>
                    <p class="md-body" style="font-size: 0.9rem; opacity: 0.8; margin: 0;">创建专业的交互式图表</p>
                </div>
                <div style="padding: 1rem; background: var(--md-surface); border-radius: var(--md-radius-medium); border-left: 4px solid var(--md-tertiary);">
                    <h4 class="md-body" style="font-weight: 600; margin-bottom: 0.5rem; color: var(--md-tertiary);">4. 统计建模</h4>
                    <p class="md-body" style="font-size: 0.9rem; opacity: 0.8; margin: 0;">进行复杂的统计检验和建模</p>
                </div>
                <div style="padding: 1rem; background: var(--md-surface); border-radius: var(--md-radius-medium); border-left: 4px solid var(--md-tertiary);">
                    <h4 class="md-body" style="font-weight: 600; margin-bottom: 0.5rem; color: var(--md-tertiary);">5. 机器学习</h4>
                    <p class="md-body" style="font-size: 0.9rem; opacity: 0.8; margin: 0;">应用各种ML算法进行预测和分类</p>
                </div>
                <div style="padding: 1rem; background: var(--md-surface); border-radius: var(--md-radius-medium); border-left: 4px solid var(--md-tertiary);">
                    <h4 class="md-body" style="font-weight: 600; margin-bottom: 0.5rem; color: var(--md-tertiary);">6. AI分析</h4>
                    <p class="md-body" style="font-size: 0.9rem; opacity: 0.8; margin: 0;">利用AI助手进行深度洞察</p>
                </div>
                <div style="padding: 1rem; background: var(--md-surface); border-radius: var(--md-radius-medium); border-left: 4px solid var(--md-tertiary);">
                    <h4 class="md-body" style="font-weight: 600; margin-bottom: 0.5rem; color: var(--md-tertiary);">7. 专业报告</h4>
                    <p class="md-body" style="font-size: 0.9rem; opacity: 0.8; margin: 0;">生成详细的分析报告</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_sidebar():
    """渲染高级侧边栏 - Material Design 3风格"""
    with st.sidebar:
        # Material Design 3 侧边栏样式
        st.markdown("""
        <style>
        /* Material Design 3 侧边栏样式 */
        [data-testid="stSidebar"] {
            background: var(--md-surface) !important;
            border-right: 1px solid var(--md-outline-variant) !important;
            padding: var(--md-spacing-lg) !important;
        }
        
        /* Material Design 3 侧边栏卡片 */
        .md-sidebar-card {
            background: var(--md-surface);
            border-radius: var(--md-radius-large);
            padding: var(--md-spacing-lg);
            margin: var(--md-spacing-md) 0;
            box-shadow: var(--md-shadow-1);
            border: 1px solid var(--md-outline-variant);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .md-sidebar-card:hover {
            box-shadow: var(--md-shadow-2);
            transform: translateY(-2px);
        }
        
        /* Material Design 3 侧边栏按钮 */
        .md-sidebar-button {
            background: var(--md-primary);
            color: var(--md-on-primary);
            border: none;
            border-radius: var(--md-radius-extra-large);
            padding: var(--md-spacing-sm) var(--md-spacing-md);
            font-family: var(--md-font-family);
            font-size: var(--md-font-size-body);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            width: 100%;
            margin: var(--md-spacing-xs) 0;
            min-height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .md-sidebar-button:hover {
            box-shadow: var(--md-shadow-2);
            transform: translateY(-1px);
        }
        
        .md-sidebar-button.secondary {
            background: var(--md-secondary);
            color: var(--md-on-secondary);
        }
        
        .md-sidebar-button.outlined {
            background: transparent;
            color: var(--md-primary);
            border: 1px solid var(--md-primary);
        }
        
        /* Material Design 3 状态指示器 */
        .md-status-item {
            display: flex;
            align-items: center;
            padding: var(--md-spacing-sm) var(--md-spacing-md);
            background: var(--md-surface-variant);
            border-radius: var(--md-radius-medium);
            margin: var(--md-spacing-xs) 0;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .md-status-item:hover {
            background: var(--md-primary-container);
            color: var(--md-on-primary-container);
        }
        
        .md-status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: var(--md-spacing-sm);
            flex-shrink: 0;
        }
        
        .md-status-dot.success {
            background: var(--md-success);
            box-shadow: 0 0 8px rgba(76, 175, 80, 0.4);
        }
        
        .md-status-dot.warning {
            background: var(--md-warning);
            box-shadow: 0 0 8px rgba(255, 152, 0, 0.4);
        }
        
        .md-status-dot.error {
            background: var(--md-error);
            box-shadow: 0 0 8px rgba(244, 67, 54, 0.4);
        }
        
        .md-status-dot.info {
            background: var(--md-info);
            box-shadow: 0 0 8px rgba(33, 150, 243, 0.4);
        }
        
        /* Material Design 3 进度条 */
        .md-progress-container {
            background: var(--md-outline-variant);
            border-radius: var(--md-radius-small);
            height: 8px;
            overflow: hidden;
            margin: var(--md-spacing-sm) 0;
        }
        
        .md-progress-bar {
            height: 100%;
            background: var(--md-primary);
            border-radius: var(--md-radius-small);
            transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
        }
        
        .md-progress-bar::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
            animation: shimmer 2s infinite;
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        /* Material Design 3 分割线 */
        .md-divider {
            height: 1px;
            background: var(--md-outline-variant);
            margin: var(--md-spacing-md) 0;
            border: none;
        }
        
        /* Material Design 3 标签 */
        .md-chip {
            display: inline-flex;
            align-items: center;
            background: var(--md-surface-variant);
            color: var(--md-on-surface-variant);
            border-radius: var(--md-radius-extra-large);
            padding: var(--md-spacing-xs) var(--md-spacing-sm);
            font-size: var(--md-font-size-small);
            font-weight: 500;
            margin: var(--md-spacing-xs);
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .md-chip:hover {
            background: var(--md-primary-container);
            color: var(--md-on-primary-container);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Material Design 3 标题区域
        st.markdown("""
        <div class="md-sidebar-card" style="text-align: center; margin-bottom: 2rem;">
            <h2 class="md-title" style="color: var(--md-primary); margin: 0; font-size: 1.5rem;">🚀 专业导航</h2>
            <p class="md-body" style="margin: 0.5rem 0 0 0; opacity: 0.8; font-size: 0.9rem;">
                智能数据分析平台
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Material Design 3 模式切换区域
        st.markdown("""
        <div class="md-sidebar-card">
            <h4 class="md-title" style="margin: 0 0 1rem 0; color: var(--md-on-surface);">🔄 模式切换</h4>
        </div>
        """, unsafe_allow_html=True)
        
        current_mode = st.session_state.get('selected_mode', 'professional')
        # 安全检查：确保current_mode是有效的键
        if current_mode not in ANALYSIS_MODES:
            st.error("❌ 无效的模式选择，请重新选择模式")
            st.session_state.selected_mode = 'professional'
            st.session_state.current_page = "🎯 模式选择"
            st.rerun()
            return
        
        mode_info = ANALYSIS_MODES[current_mode]
        
        # 使用selectbox进行模式选择
        mode_options = {
            f"{ANALYSIS_MODES['beginner']['icon']} {ANALYSIS_MODES['beginner']['name']}": "beginner",
            f"{ANALYSIS_MODES['intermediate']['icon']} {ANALYSIS_MODES['intermediate']['name']}": "intermediate", 
            f"{ANALYSIS_MODES['professional']['icon']} {ANALYSIS_MODES['professional']['name']}": "professional"
        }
        
        current_mode_display = f"{mode_info['icon']} {mode_info['name']}"
        
        selected_mode_display = st.selectbox(
            "选择分析模式",
            list(mode_options.keys()),
            index=list(mode_options.keys()).index(current_mode_display),
            key="mode_selector"
        )
        
        if mode_options[selected_mode_display] != current_mode:
            st.session_state.selected_mode = mode_options[selected_mode_display]
            st.success(f"✅ 已切换到 {selected_mode_display}")
            st.rerun()
        
        # 当前模式提示
        st.markdown(f"""
        <div class="md-status-item" style="background: var(--md-primary-container); color: var(--md-on-primary-container);">
            <div class="md-status-dot success"></div>
            <span class="md-body" style="font-weight: 500;">{mode_info['icon']} 当前：{mode_info['name']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Material Design 3 快捷操作面板
        st.markdown("""
        <div class="md-sidebar-card">
            <h4 class="md-title" style="margin: 0 0 1rem 0; color: var(--md-on-surface);">🚀 快捷操作</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # 快捷操作按钮
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🏠 首页", key="quick_home_pro", use_container_width=True):
                st.session_state.current_page = "🏠 首页"
                st.rerun()
            
            if st.button("📁 数据", key="quick_data_pro", use_container_width=True):
                st.session_state.current_page = "📁 数据上传"
                st.rerun()
        
        with col2:
            if st.button("📊 可视化", key="quick_viz_pro", use_container_width=True):
                st.session_state.current_page = "📊 数据可视化"
                st.rerun()
            
            if st.button("🤖 机器学习", key="quick_ml_pro", use_container_width=True):
                st.session_state.current_page = "🤖 机器学习"
                st.rerun()
        
        # Material Design 3 页面导航选择器
        st.markdown("""
        <div class="md-sidebar-card">
            <h4 class="md-title" style="margin: 0 0 1rem 0; color: var(--md-on-surface);">🎯 页面导航</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # 创建导航选项
        nav_options = {
            "🏠 首页": "🏠 首页",
            "📁 数据上传": "📁 数据上传",
            "🧹 数据清洗": "🧹 数据清洗",
            "📊 数据可视化": "📊 数据可视化",
            "📈 统计分析": "📈 统计分析",
            "🤖 机器学习": "🤖 机器学习",
            "📄 分析报告": "📄 分析报告"
        }
        
        # 过滤可用的导航选项
        available_options = {}
        for name, page in nav_options.items():
            if page == "🏠 首页":  # 首页总是可用
                available_options[name] = page
            elif page == "📁 数据上传":  # 数据上传总是可用
                available_options[name] = page
            elif page == "🧹 数据清洗" and hasattr(st.session_state, 'data') and st.session_state.data is not None:  # 数据清洗需要数据
                available_options[name] = page
            elif page == "📊 数据可视化" and hasattr(st.session_state, 'data') and st.session_state.data is not None:  # 可视化需要数据
                available_options[name] = page
            elif page == "📈 统计分析" and hasattr(st.session_state, 'data') and st.session_state.data is not None:  # 统计分析需要数据
                available_options[name] = page
            elif page == "🤖 机器学习" and hasattr(st.session_state, 'data') and st.session_state.data is not None:  # 机器学习需要数据
                available_options[name] = page
            elif page == "📄 分析报告" and hasattr(st.session_state, 'data') and st.session_state.data is not None:  # 报告需要数据
                available_options[name] = page
        
        # 当前页面对应的选项名称
        current_option = None
        for name, page in nav_options.items():
            if page == st.session_state.current_page:
                current_option = name
                break
        
        # 导航选择器
        selected_nav = st.selectbox(
            "选择要跳转的页面：",
            options=list(available_options.keys()),
            index=list(available_options.keys()).index(current_option) if current_option in available_options else 0,
            key="nav_selector_pro",
            help="选择要跳转的页面，系统会自动检查前置条件"
        )
        
        # 处理导航跳转
        if selected_nav in available_options and available_options[selected_nav] != st.session_state.current_page:
            if st.button("🚀 跳转", key="nav_jump_pro", use_container_width=True):
                st.session_state.current_page = available_options[selected_nav]
                st.rerun()
        
        # 显示导航状态
        if len(available_options) < len(nav_options):
            st.markdown("""
            <div class="md-status-item" style="background: var(--md-warning-container); color: var(--md-warning);">
                <div class="md-status-dot warning"></div>
                <span class="md-body" style="font-size: 0.8rem;">部分页面需要先上传数据才能访问</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Material Design 3 状态指示器面板
        st.markdown("""
        <div class="md-sidebar-card">
            <h4 class="md-title" style="margin: 0 0 1rem 0; color: var(--md-on-surface);">📊 系统状态</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # 系统状态指示
        st.markdown("""
        <div class="md-status-item">
            <div class="md-status-dot success"></div>
            <span class="md-body">系统就绪</span>
        </div>
        """, unsafe_allow_html=True)
        
        # 数据状态指示
        if hasattr(st.session_state, 'data') and st.session_state.data is not None:
            st.markdown("""
            <div class="md-status-item">
                <div class="md-status-dot success"></div>
                <span class="md-body">数据已加载</span>
            </div>
            """, unsafe_allow_html=True)
        
        if hasattr(st.session_state, 'data_cleaned') and st.session_state.data_cleaned is not None:
            st.markdown("""
            <div class="md-status-item">
                <div class="md-status-dot success"></div>
                <span class="md-body">数据已清洗</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Material Design 3 组件状态
        st.markdown("""
        <div class="md-sidebar-card">
            <h4 class="md-title" style="margin: 0 0 1rem 0; color: var(--md-on-surface);">🔧 组件状态</h4>
        </div>
        """, unsafe_allow_html=True)
        
        components_ok = 0
        total_components = 2
        
        if COMPONENT_AVAILABILITY['YDATA_AVAILABLE']:
            components_ok += 1
            st.markdown("""
            <div class="md-status-item">
                <div class="md-status-dot success"></div>
                <span class="md-body">YData组件</span>
            </div>
            """, unsafe_allow_html=True)
        
        try:
            import sklearn
            components_ok += 1
            st.markdown("""
            <div class="md-status-item">
                <div class="md-status-dot success"></div>
                <span class="md-body">Scikit-learn</span>
            </div>
            """, unsafe_allow_html=True)
        except ImportError:
            st.markdown("""
            <div class="md-status-item">
                <div class="md-status-dot warning"></div>
                <span class="md-body">Scikit-learn</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Material Design 3 智能建议面板
        if st.session_state.current_page != "🏠 首页":
            st.markdown("""
            <div class="md-sidebar-card">
                <h4 class="md-title" style="margin: 0 0 1rem 0; color: var(--md-on-surface);">💡 智能建议</h4>
                <div style="font-size: 0.9rem; color: var(--md-on-surface-variant); line-height: 1.4;">
            """, unsafe_allow_html=True)
            
            if st.session_state.current_page == "📁 数据上传":
                st.markdown("• 支持多种数据格式<br>• 建议文件大小 < 100MB<br>• 检查数据编码格式", unsafe_allow_html=True)
            elif st.session_state.current_page == "🧹 数据清洗":
                st.markdown("• 选择合适的清洗策略<br>• 注意数据质量评分<br>• 保留原始数据备份", unsafe_allow_html=True)
            elif st.session_state.current_page == "📊 数据可视化":
                st.markdown("• 尝试不同类型的图表<br>• 关注数据分布特征<br>• 使用交互式图表", unsafe_allow_html=True)
            elif st.session_state.current_page == "📈 统计分析":
                st.markdown("• 深入理解统计指标<br>• 注意相关性分析<br>• 进行假设检验", unsafe_allow_html=True)
            elif st.session_state.current_page == "🤖 机器学习":
                st.markdown("• 选择合适的算法<br>• 进行交叉验证<br>• 评估模型性能", unsafe_allow_html=True)
            elif st.session_state.current_page == "📄 分析报告":
                st.markdown("• 下载完整分析报告<br>• 保存重要发现<br>• 分享分析结果", unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Material Design 3 开发信息
        st.markdown(f"""
        <div class="md-sidebar-card">
            <h4 class="md-title" style="margin: 0 0 1rem 0; color: var(--md-on-surface);">👨‍💻 开发信息</h4>
            <div style="font-size: 0.9rem; color: var(--md-on-surface-variant); line-height: 1.4;">
                <strong>{AUTHOR_INFO['name']}</strong><br>
                📧 {AUTHOR_INFO['email']}<br>
                🚀 智能数据分析平台 v3.0
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_footer():
    """渲染页脚"""
    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align: center; color: #666; font-size: 0.8rem;">
            🚀 智能数据分析平台 | {AUTHOR_INFO['name']} | {AUTHOR_INFO['email']} | 版本 3.0
        </div>
        """,
        unsafe_allow_html=True
    )
