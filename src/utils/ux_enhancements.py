"""
用户体验增强模块
提供现代化的UI组件和交互体验
参考行业最佳实践：Tableau、Power BI、Jupyter等
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
import time
import json


class UXEnhancements:
    """用户体验增强类"""
    
    def __init__(self):
        """初始化用户体验增强"""
        self.setup_custom_css()
        self.setup_session_state()
    
    def setup_custom_css(self):
        """设置自定义CSS样式"""
        st.markdown("""
        <style>
        /* 现代化卡片样式 */
        .modern-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            backdrop-filter: blur(10px);
        }
        
        /* 进度指示器样式 */
        .progress-container {
            background: #f0f2f6;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
        }
        
        /* 状态指示器样式 */
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-success { background-color: #00ff88; }
        .status-warning { background-color: #ffaa00; }
        .status-error { background-color: #ff4444; }
        .status-info { background-color: #0088ff; }
        
        /* 工具提示样式 */
        .tooltip {
            position: relative;
            display: inline-block;
        }
        
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 200px;
            background-color: #555;
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 5px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -100px;
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
        
        /* 动画效果 */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .fade-in {
            animation: fadeIn 0.5s ease-in-out;
        }
        
        /* 响应式布局 */
        @media (max-width: 768px) {
            .modern-card {
                padding: 15px;
                margin: 5px 0;
            }
        }
        </style>
        """, unsafe_allow_html=True)
    
    def setup_session_state(self):
        """设置会话状态"""
        if 'user_preferences' not in st.session_state:
            st.session_state.user_preferences = {
                'theme': 'light',
                'language': 'zh',
                'auto_save': True,
                'notifications': True
            }
        
        if 'workflow_history' not in st.session_state:
            st.session_state.workflow_history = []
        
        if 'favorites' not in st.session_state:
            st.session_state.favorites = []
    
    def render_welcome_screen(self):
        """渲染欢迎屏幕"""
        st.markdown("""
        <div class="modern-card fade-in">
            <h1 style="text-align: center; color: white; margin-bottom: 20px;">
                👁️ 欢迎使用数眸数据分析平台
            </h1>
            <p style="text-align: center; color: white; font-size: 18px; margin-bottom: 30px;">
                让数据洞察如眸般清澈明亮
            </p>
            <div style="text-align: center;">
                <div style="display: inline-block; margin: 10px; padding: 15px; background: rgba(255,255,255,0.2); border-radius: 10px;">
                    <h3 style="color: white; margin: 0;">🚀 快速开始</h3>
                    <p style="color: white; margin: 5px 0;">上传数据，开始分析</p>
                </div>
                <div style="display: inline-block; margin: 10px; padding: 15px; background: rgba(255,255,255,0.2); border-radius: 10px;">
                    <h3 style="color: white; margin: 0;">📊 智能洞察</h3>
                    <p style="color: white; margin: 5px 0;">AI驱动的数据分析</p>
                </div>
                <div style="display: inline-block; margin: 10px; padding: 15px; background: rgba(255,255,255,0.2); border-radius: 10px;">
                    <h3 style="color: white; margin: 0;">🎯 专业工具</h3>
                    <p style="color: white; margin: 5px 0;">企业级分析能力</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def render_quick_actions(self):
        """渲染快速操作面板"""
        st.sidebar.markdown("### ⚡ 快速操作")
        
        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            if st.button("📁 上传数据", use_container_width=True):
                st.session_state.current_page = "📁 数据上传"
                st.rerun()
        
        with col2:
            if st.button("🔍 快速分析", use_container_width=True):
                st.session_state.current_page = "🔍 自动数据分析"
                st.rerun()
        
        st.sidebar.markdown("### 📋 最近操作")
        if st.session_state.workflow_history:
            for i, action in enumerate(st.session_state.workflow_history[-5:]):
                st.sidebar.text(f"{i+1}. {action}")
        else:
            st.sidebar.text("暂无操作记录")
    
    def render_data_status_card(self, data: Optional[pd.DataFrame] = None):
        """渲染数据状态卡片"""
        if data is None:
            st.markdown("""
            <div class="modern-card">
                <h3 style="color: white; margin-bottom: 15px;">📊 数据状态</h3>
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <span class="status-indicator status-warning"></span>
                    <span style="color: white;">未加载数据</span>
                </div>
                <p style="color: white; opacity: 0.8;">请先上传数据文件开始分析</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # 计算数据质量指标
            missing_ratio = data.isnull().sum().sum() / (len(data) * len(data.columns))
            duplicate_ratio = data.duplicated().sum() / len(data)
            
            quality_score = max(0, 100 - missing_ratio * 50 - duplicate_ratio * 30)
            
            st.markdown(f"""
            <div class="modern-card">
                <h3 style="color: white; margin-bottom: 15px;">📊 数据状态</h3>
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <span class="status-indicator status-success"></span>
                    <span style="color: white;">数据已加载</span>
                </div>
                <div style="color: white; margin-bottom: 10px;">
                    <strong>数据集:</strong> {len(data)} 行 × {len(data.columns)} 列
                </div>
                <div style="color: white; margin-bottom: 10px;">
                    <strong>质量评分:</strong> {quality_score:.0f}/100
                </div>
                <div style="color: white; margin-bottom: 10px;">
                    <strong>缺失值:</strong> {data.isnull().sum().sum()} ({missing_ratio:.1%})
                </div>
                <div style="color: white;">
                    <strong>重复行:</strong> {data.duplicated().sum()} ({duplicate_ratio:.1%})
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def render_progress_tracker(self, current_step: int, total_steps: int, step_name: str):
        """渲染进度跟踪器"""
        progress = current_step / total_steps
        
        st.markdown(f"""
        <div class="progress-container">
            <h4 style="margin-bottom: 10px;">🔄 分析进度</h4>
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>步骤 {current_step}/{total_steps}</span>
                <span>{progress:.0%}</span>
            </div>
            <div style="background: #e0e0e0; border-radius: 5px; height: 10px;">
                <div style="background: linear-gradient(90deg, #667eea, #764ba2); width: {progress:.0%}; height: 100%; border-radius: 5px; transition: width 0.3s;"></div>
            </div>
            <p style="margin-top: 10px; font-weight: bold;">{step_name}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_notification(self, message: str, notification_type: str = "info"):
        """渲染通知消息"""
        icon_map = {
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
            "info": "ℹ️"
        }
        
        color_map = {
            "success": "#00ff88",
            "warning": "#ffaa00",
            "error": "#ff4444",
            "info": "#0088ff"
        }
        
        st.markdown(f"""
        <div style="
            background: {color_map[notification_type]};
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            display: flex;
            align-items: center;
            animation: fadeIn 0.3s ease-in-out;
        ">
            <span style="font-size: 20px; margin-right: 10px;">{icon_map[notification_type]}</span>
            <span>{message}</span>
        </div>
        """, unsafe_allow_html=True)
    
    def render_tooltip(self, text: str, tooltip_text: str):
        """渲染带工具提示的文本"""
        return f"""
        <div class="tooltip">
            {text}
            <span class="tooltiptext">{tooltip_text}</span>
        </div>
        """
    
    def render_help_section(self, title: str, content: str):
        """渲染帮助部分"""
        with st.expander(f"❓ {title}"):
            st.markdown(content)
    
    def render_feedback_form(self):
        """渲染反馈表单"""
        st.sidebar.markdown("### 💬 反馈")
        
        feedback_type = st.sidebar.selectbox(
            "反馈类型",
            ["功能建议", "问题报告", "使用体验", "其他"]
        )
        
        feedback_text = st.sidebar.text_area(
            "您的反馈",
            placeholder="请详细描述您的建议或遇到的问题...",
            height=100
        )
        
        if st.sidebar.button("提交反馈"):
            if feedback_text.strip():
                # 这里可以添加反馈保存逻辑
                st.sidebar.success("感谢您的反馈！")
            else:
                st.sidebar.warning("请输入反馈内容")
    
    def render_shortcuts_panel(self):
        """渲染快捷键面板"""
        st.sidebar.markdown("### ⌨️ 快捷键")
        
        shortcuts = [
            ("Ctrl+U", "上传数据"),
            ("Ctrl+A", "自动分析"),
            ("Ctrl+V", "可视化"),
            ("Ctrl+M", "机器学习"),
            ("Ctrl+H", "帮助"),
            ("Ctrl+S", "保存"),
        ]
        
        for key, desc in shortcuts:
            st.sidebar.text(f"**{key}** - {desc}")
    
    def render_data_preview_enhanced(self, data: pd.DataFrame, max_rows: int = 10):
        """增强的数据预览"""
        st.subheader("📋 数据预览")
        
        # 数据概览
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("行数", len(data))
        with col2:
            st.metric("列数", len(data.columns))
        with col3:
            st.metric("内存使用", f"{data.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB")
        with col4:
            st.metric("数据类型", len(data.dtypes.unique()))
        
        # 数据类型分布
        st.write("**数据类型分布**")
        dtype_counts = data.dtypes.value_counts()
        col1, col2 = st.columns(2)
        
        with col1:
            st.dataframe(dtype_counts, use_container_width=True)
        
        with col2:
            # 数据类型饼图
            import plotly.express as px
            fig = px.pie(
                values=dtype_counts.values,
                names=dtype_counts.index,
                title="数据类型分布"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # 数据预览表格
        st.write("**数据预览**")
        preview_data = data.head(max_rows)
        st.dataframe(preview_data, use_container_width=True)
        
        # 列信息
        st.write("**列信息**")
        column_info = []
        for col in data.columns:
            col_info = {
                "列名": col,
                "数据类型": str(data[col].dtype),
                "非空值": data[col].count(),
                "缺失值": data[col].isnull().sum(),
                "缺失比例": f"{data[col].isnull().sum() / len(data) * 100:.1f}%"
            }
            column_info.append(col_info)
        
        st.dataframe(pd.DataFrame(column_info), use_container_width=True)
    
    def render_analysis_suggestions(self, data: pd.DataFrame):
        """渲染分析建议"""
        st.subheader("💡 智能分析建议")
        
        # 基于数据特征生成建议
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
        missing_ratio = data.isnull().sum().sum() / (len(data) * len(data.columns))
        
        suggestions = []
        
        # 数据质量建议
        if missing_ratio > 0.1:
            suggestions.append({
                "优先级": "🔥 高",
                "建议": "处理缺失值",
                "描述": f"数据中有{missing_ratio:.1%}的缺失值，建议进行数据清洗"
            })
        
        if data.duplicated().sum() > 0:
            suggestions.append({
                "优先级": "🔥 高",
                "建议": "删除重复行",
                "描述": f"发现{data.duplicated().sum()}行重复数据"
            })
        
        # 分析建议
        if len(numeric_cols) >= 2:
            suggestions.append({
                "优先级": "📊 推荐",
                "建议": "相关性分析",
                "描述": "数值型变量较多，适合进行相关性分析"
            })
        
        if len(categorical_cols) > 0:
            suggestions.append({
                "优先级": "📊 推荐",
                "建议": "分类变量分析",
                "描述": "包含分类变量，可以进行频次分析和可视化"
            })
        
        if len(data) > 1000:
            suggestions.append({
                "优先级": "🤖 推荐",
                "建议": "机器学习建模",
                "描述": "数据量充足，适合进行机器学习分析"
            })
        
        # 显示建议
        if suggestions:
            for suggestion in suggestions:
                st.markdown(f"""
                <div style="
                    background: {'#ffebee' if '高' in suggestion['优先级'] else '#e8f5e8' if '推荐' in suggestion['优先级'] else '#fff3e0'};
                    border-left: 4px solid {'#f44336' if '高' in suggestion['优先级'] else '#4caf50' if '推荐' in suggestion['优先级'] else '#ff9800'};
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 5px;
                ">
                    <div style="font-weight: bold; margin-bottom: 5px;">
                        {suggestion['优先级']} {suggestion['建议']}
                    </div>
                    <div style="color: #666;">
                        {suggestion['描述']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("✅ 数据质量良好，可以直接进行分析")
    
    def render_workflow_summary(self):
        """渲染工作流摘要"""
        if st.session_state.workflow_history:
            st.sidebar.markdown("### 📈 工作流摘要")
            
            # 统计操作类型
            operations = {}
            for action in st.session_state.workflow_history:
                op_type = action.split()[0] if action else "其他"
                operations[op_type] = operations.get(op_type, 0) + 1
            
            # 显示统计
            for op_type, count in operations.items():
                st.sidebar.text(f"{op_type}: {count}次")
    
    def add_to_history(self, action: str):
        """添加到操作历史"""
        timestamp = time.strftime("%H:%M:%S")
        st.session_state.workflow_history.append(f"[{timestamp}] {action}")
        
        # 保持历史记录在合理范围内
        if len(st.session_state.workflow_history) > 50:
            st.session_state.workflow_history = st.session_state.workflow_history[-50:]


# 全局用户体验增强实例
ux_enhancements = UXEnhancements()

def get_ux_enhancements():
    """获取用户体验增强实例"""
    return ux_enhancements
