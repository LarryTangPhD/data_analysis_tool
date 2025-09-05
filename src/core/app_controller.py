"""
应用控制器
负责页面路由和调度，是应用的核心控制中心
"""

import streamlit as st
from typing import Dict, Any, Optional
from src.config.settings import NAV_PAGES, ANALYSIS_MODES
from src.modules.page_router import PageRouter
from src.modules.mode_manager import ModeManager
from src.utils.session_manager import SessionManager
from src.utils.ux_enhancements import get_ux_enhancements
from src.utils.smart_guide import get_smart_guide


class AppController:
    """应用主控制器"""
    
    def __init__(self):
        """初始化应用控制器"""
        self.page_router = PageRouter()
        self.mode_manager = ModeManager()
        self.session_manager = SessionManager()
        self.ux_enhancements = get_ux_enhancements()
        self.smart_guide = get_smart_guide()
        
    def initialize_app(self):
        """初始化应用"""
        # 初始化session state
        self.session_manager.initialize_session_state()
        
    def render_header(self):
        """渲染应用头部"""
        st.markdown('<h1 class="main-header">👁️ 数眸 - 智能数据分析平台</h1>', unsafe_allow_html=True)
        st.markdown('<p class="brand-slogan">让数据洞察如眸般清澈明亮</p>', unsafe_allow_html=True)
        
    def render_navigation(self):
        """渲染导航栏"""
        # 获取当前模式
        current_mode = self.mode_manager.get_current_mode()
        
        # 只在专业模式下显示横向导航
        if current_mode == 'professional':
            # 创建横向导航（移除模式选择页面）
            nav_pages_without_mode = [page for page in NAV_PAGES if page != "🎯 模式选择"]
            selected_page = st.radio(
                "选择功能模块",
                nav_pages_without_mode,
                horizontal=True,
                key="page_navigation"
            )
            
            # 更新当前页面
            if selected_page != st.session_state.get('current_page'):
                st.session_state.current_page = selected_page
                st.rerun()
            
            page = st.session_state.current_page
            st.markdown("---")
            
            # 渲染侧边栏
            from src.modules.sidebar import render_sidebar
            render_sidebar()
            
            # 渲染用户体验增强组件
            self.render_ux_components(page)
        else:
            # 新手模式和普通模式使用固定页面
            page = "🏠 首页"
            
        return page
    
    def render_ux_components(self, current_page: str):
        """渲染用户体验组件"""
        # 获取当前数据
        data = self.session_manager.get_data()
        
        # 渲染智能引导
        self.smart_guide.render_contextual_help(current_page, data)
        
        # 渲染快速操作
        self.ux_enhancements.render_quick_actions()
        
        # 渲染数据状态卡片
        self.ux_enhancements.render_data_status_card(data)
        
        # 渲染快速提示
        self.smart_guide.render_quick_tips(current_page)
        
        # 渲染引导进度
        self.smart_guide.render_guide_progress()
        
        # 渲染工作流摘要
        self.ux_enhancements.render_workflow_summary()
        
        # 渲染反馈表单
        self.ux_enhancements.render_feedback_form()
        
        # 渲染快捷键面板
        self.ux_enhancements.render_shortcuts_panel()
        
    def run(self):
        """运行应用主逻辑"""
        # 初始化应用
        self.initialize_app()
        
        # 渲染头部
        self.render_header()
        
        # 渲染导航并获取当前页面
        current_page = self.render_navigation()
        
        # 路由到对应页面
        self.page_router.route_to_page(current_page)
        
        # 渲染页脚
        from src.modules.footer import render_footer
        render_footer()
        
        # 渲染用户体验组件
        from src.modules.user_experience import render_user_experience_components
        render_user_experience_components()
        
        # 渲染性能优化控制
        from src.utils.performance_optimizer import performance_optimizer
        performance_optimizer.render_optimization_controls()
