"""
响应式UI组件模块
提供现代化的用户界面组件
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any, Optional, Tuple, Union
import time
from datetime import datetime

class ModernUIComponents:
    """现代化UI组件类"""
    
    @staticmethod
    def create_hero_section(title: str, subtitle: str, background_color: str = "#1E40AF"):
        """创建英雄区域"""
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {background_color} 0%, #3B82F6 100%);
            padding: 40px 20px;
            border-radius: 20px;
            color: white;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(30, 64, 175, 0.3);
        ">
            <h1 style="
                font-size: 3rem;
                font-weight: bold;
                margin-bottom: 15px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            ">{title}</h1>
            <p style="
                font-size: 1.2rem;
                opacity: 0.9;
                line-height: 1.6;
                max-width: 600px;
                margin: 0 auto;
            ">{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_feature_card(title: str, description: str, icon: str, 
                          color: str = "#3B82F6", action_button: str = None):
        """创建功能卡片"""
        card_html = f"""
        <div style="
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin: 15px 0;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            border-left: 5px solid {color};
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;
        " onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 8px 30px rgba(0,0,0,0.15)'"
           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 20px rgba(0,0,0,0.1)'">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <span style="font-size: 2rem; margin-right: 15px;">{icon}</span>
                <h3 style="margin: 0; color: #1F2937; font-size: 1.3rem;">{title}</h3>
            </div>
            <p style="color: #6B7280; line-height: 1.6; margin: 0;">{description}</p>
        </div>
        """
        
        if action_button:
            card_html += f"""
            <div style="text-align: center; margin-top: 15px;">
                <button style="
                    background: {color};
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 8px;
                    cursor: pointer;
                    font-weight: 500;
                    transition: background 0.3s ease;
                " onmouseover="this.style.background='{color}dd'" onmouseout="this.style.background='{color}'">
                    {action_button}
                </button>
            </div>
            """
        
        st.markdown(card_html, unsafe_allow_html=True)
    
    @staticmethod
    def create_progress_card(title: str, current: int, total: int, 
                           color: str = "#10B981", show_percentage: bool = True):
        """创建进度卡片"""
        percentage = (current / total) * 100 if total > 0 else 0
        
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <h4 style="margin: 0; color: #374151;">{title}</h4>
                <span style="color: #6B7280; font-size: 0.9rem;">
                    {current}/{total} {f"({percentage:.1f}%)" if show_percentage else ""}
                </span>
            </div>
            <div style="
                background: #E5E7EB;
                border-radius: 10px;
                height: 8px;
                overflow: hidden;
            ">
                <div style="
                    background: {color};
                    height: 100%;
                    width: {percentage}%;
                    border-radius: 10px;
                    transition: width 0.5s ease;
                "></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_metric_card(title: str, value: str, change: str = None, 
                          change_type: str = "positive", icon: str = "📊"):
        """创建指标卡片"""
        change_color = "#10B981" if change_type == "positive" else "#EF4444"
        change_icon = "↗️" if change_type == "positive" else "↘️"
        
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        ">
            <div style="font-size: 2rem; margin-bottom: 10px;">{icon}</div>
            <h3 style="margin: 0; color: #1F2937; font-size: 1.8rem; font-weight: bold;">{value}</h3>
            <p style="margin: 5px 0; color: #6B7280; font-size: 0.9rem;">{title}</p>
            {f'<p style="margin: 0; color: {change_color}; font-size: 0.8rem;">{change_icon} {change}</p>' if change else ''}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_alert_box(message: str, alert_type: str = "info", 
                        title: str = None, dismissible: bool = True):
        """创建警告框"""
        colors = {
            "info": {"bg": "#DBEAFE", "border": "#3B82F6", "text": "#1E40AF"},
            "success": {"bg": "#D1FAE5", "border": "#10B981", "text": "#065F46"},
            "warning": {"bg": "#FEF3C7", "border": "#F59E0B", "text": "#92400E"},
            "error": {"bg": "#FEE2E2", "border": "#EF4444", "text": "#991B1B"}
        }
        
        color = colors.get(alert_type, colors["info"])
        
        st.markdown(f"""
        <div style="
            background: {color['bg']};
            border: 1px solid {color['border']};
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            color: {color['text']};
        ">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    {f'<h4 style="margin: 0 0 5px 0; font-size: 1rem;">{title}</h4>' if title else ''}
                    <p style="margin: 0; line-height: 1.5;">{message}</p>
                </div>
                {f'<button style="background: none; border: none; color: {color["text"]}; cursor: pointer; font-size: 1.2rem;">×</button>' if dismissible else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_tab_navigation(tabs: List[Dict[str, str]], active_tab: str = None):
        """创建标签导航"""
        tab_html = '<div style="display: flex; background: #F3F4F6; border-radius: 8px; padding: 4px; margin: 20px 0;">'
        
        for tab in tabs:
            is_active = tab["id"] == active_tab
            tab_html += f"""
            <div style="
                flex: 1;
                text-align: center;
                padding: 10px;
                border-radius: 6px;
                cursor: pointer;
                transition: all 0.3s ease;
                background: {'white' if is_active else 'transparent'};
                color: {'#1F2937' if is_active else '#6B7280'};
                font-weight: {'600' if is_active else '400'};
                box-shadow: {'0 2px 4px rgba(0,0,0,0.1)' if is_active else 'none'};
            ">
                {tab["icon"]} {tab["label"]}
            </div>
            """
        
        tab_html += '</div>'
        st.markdown(tab_html, unsafe_allow_html=True)

class InteractiveComponents:
    """交互式组件类"""
    
    @staticmethod
    def create_draggable_dataframe(df: pd.DataFrame, key: str = "dataframe"):
        """创建可拖拽的数据表格"""
        st.markdown("""
        <style>
        .dataframe-container {
            border: 2px dashed #E5E7EB;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            margin: 20px 0;
            transition: border-color 0.3s ease;
        }
        .dataframe-container:hover {
            border-color: #3B82F6;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="dataframe-container" id="{key}">
            <p style="color: #6B7280; margin: 0;">拖拽数据文件到这里或点击上传</p>
        </div>
        """, unsafe_allow_html=True)
        
        return st.file_uploader("选择文件", type=['csv', 'xlsx', 'xls'], key=key)
    
    @staticmethod
    def create_animated_chart(fig, animation_duration: int = 1000):
        """创建动画图表"""
        # 为图表添加动画效果
        fig.update_layout(
            transition={
                'duration': animation_duration,
                'easing': 'cubic-in-out'
            }
        )
        return fig
    
    @staticmethod
    def create_floating_action_button(icon: str, tooltip: str, key: str):
        """创建浮动操作按钮"""
        st.markdown(f"""
        <style>
        .fab {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 56px;
            height: 56px;
            background: #3B82F6;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 24px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
            transition: all 0.3s ease;
            z-index: 1000;
        }}
        .fab:hover {{
            transform: scale(1.1);
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6);
        }}
        </style>
        <div class="fab" title="{tooltip}">
            {icon}
        </div>
        """, unsafe_allow_html=True)
        
        return st.button(icon, key=key)

class ResponsiveLayout:
    """响应式布局类"""
    
    @staticmethod
    def create_sidebar_navigation():
        """创建侧边栏导航"""
        st.sidebar.markdown("""
        <div style="
            background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
            padding: 20px;
            border-radius: 12px;
            color: white;
            margin-bottom: 20px;
        ">
            <h3 style="margin: 0; text-align: center;">👁️ 数眸</h3>
            <p style="margin: 5px 0 0 0; text-align: center; opacity: 0.9; font-size: 0.9rem;">
                智能数据分析平台
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_main_content_area():
        """创建主内容区域"""
        st.markdown("""
        <style>
        .main-content {
            padding: 20px;
            background: #F9FAFB;
            min-height: 100vh;
        }
        .content-card {
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_grid_layout(columns: int = 2):
        """创建网格布局"""
        return st.columns(columns)
    
    @staticmethod
    def create_flexible_container():
        """创建灵活容器"""
        st.markdown("""
        <div style="
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin: 20px 0;
        ">
        """, unsafe_allow_html=True)

class LoadingStates:
    """加载状态类"""
    
    @staticmethod
    def show_skeleton_loading():
        """显示骨架屏加载"""
        st.markdown("""
        <div style="
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
        ">
            <div style="
                background: #E5E7EB;
                height: 20px;
                border-radius: 4px;
                margin-bottom: 15px;
                animation: pulse 1.5s infinite;
            "></div>
            <div style="
                background: #E5E7EB;
                height: 15px;
                border-radius: 4px;
                margin-bottom: 10px;
                width: 80%;
                animation: pulse 1.5s infinite;
            "></div>
            <div style="
                background: #E5E7EB;
                height: 15px;
                border-radius: 4px;
                width: 60%;
                animation: pulse 1.5s infinite;
            "></div>
        </div>
        <style>
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def show_progress_with_message(message: str, progress: float):
        """显示带消息的进度条"""
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
            text-align: center;
        ">
            <p style="margin: 0 0 15px 0; color: #374151;">{message}</p>
            <div style="
                background: #E5E7EB;
                border-radius: 10px;
                height: 8px;
                overflow: hidden;
            ">
                <div style="
                    background: #3B82F6;
                    height: 100%;
                    width: {progress}%;
                    border-radius: 10px;
                    transition: width 0.3s ease;
                "></div>
            </div>
            <p style="margin: 10px 0 0 0; color: #6B7280; font-size: 0.9rem;">
                {progress:.1f}% 完成
            </p>
        </div>
        """, unsafe_allow_html=True)

class ThemeManager:
    """主题管理器"""
    
    @staticmethod
    def apply_light_theme():
        """应用浅色主题"""
        st.markdown("""
        <style>
        .stApp {
            background-color: #F9FAFB;
        }
        .stButton > button {
            background-color: #3B82F6;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 20px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #2563EB;
            transform: translateY(-1px);
        }
        .stSelectbox > div > div {
            border-radius: 8px;
            border: 1px solid #D1D5DB;
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def apply_dark_theme():
        """应用深色主题"""
        st.markdown("""
        <style>
        .stApp {
            background-color: #111827;
            color: #F9FAFB;
        }
        .stButton > button {
            background-color: #3B82F6;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 20px;
            font-weight: 500;
        }
        .stSelectbox > div > div {
            background-color: #374151;
            border-radius: 8px;
            border: 1px solid #4B5563;
            color: #F9FAFB;
        }
        </style>
        """, unsafe_allow_html=True)

# 便捷函数
def create_modern_ui():
    """创建现代化UI"""
    ui = ModernUIComponents()
    return ui

def create_interactive_ui():
    """创建交互式UI"""
    interactive = InteractiveComponents()
    return interactive

def create_responsive_layout():
    """创建响应式布局"""
    layout = ResponsiveLayout()
    return layout

def show_loading_state():
    """显示加载状态"""
    loading = LoadingStates()
    loading.show_skeleton_loading()

def apply_theme(theme: str = "light"):
    """应用主题"""
    theme_manager = ThemeManager()
    if theme == "dark":
        theme_manager.apply_dark_theme()
    else:
        theme_manager.apply_light_theme()
