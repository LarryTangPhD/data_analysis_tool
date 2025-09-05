"""
页面路由器
负责将页面请求路由到对应的处理函数
"""

import streamlit as st
from typing import Dict, Any, Callable
from src.modules.pages import (
    render_home_page, render_mode_selection_page
)
from src.modules.beginner_mode import render_beginner_mode
from src.modules.intermediate_mode import render_intermediate_mode
from src.modules.data_upload_page import render_data_upload_page
from src.modules.data_cleaning_page import render_data_cleaning_page
from src.modules.data_analysis_page import render_data_analysis_page
from src.modules.visualization_page import render_visualization_page
from src.modules.statistics_page import render_statistics_page
from src.modules.machine_learning_page import render_machine_learning_page
from src.modules.workflow_page import render_workflow_page
from src.modules.report_page import render_report_page
from src.modules.insights_page import render_insights_page
from src.modules.format_conversion_page import render_format_conversion_page


class PageRouter:
    """页面路由器"""
    
    def __init__(self):
        """初始化路由器"""
        self.page_handlers = self._initialize_page_handlers()
        
    def _initialize_page_handlers(self) -> Dict[str, Callable]:
        """初始化页面处理器映射"""
        return {
            "🎯 模式选择": render_mode_selection_page,
            "🏠 首页": self._handle_home_page,
            "📁 数据上传": render_data_upload_page,
            "🔄 数据格式转换": render_format_conversion_page,
            "🧹 数据清洗": render_data_cleaning_page,
            "🔍 自动数据分析": render_data_analysis_page,
            "👁️ 数据洞察": render_insights_page,
            "📈 高级可视化": render_visualization_page,
            "📊 统计分析": render_statistics_page,
            "🤖 机器学习": render_machine_learning_page,
            "📊 工作流管理": render_workflow_page,
            "📋 报告生成": render_report_page
        }
    
    def _handle_home_page(self):
        """处理首页路由，根据模式选择不同的页面"""
        current_mode = st.session_state.get('selected_mode', 'professional')
        
        if current_mode == 'beginner':
            render_beginner_mode()
        elif current_mode == 'intermediate':
            render_intermediate_mode()
        else:
            render_home_page()
    
    def route_to_page(self, page_name: str):
        """路由到指定页面"""
        if page_name in self.page_handlers:
            try:
                self.page_handlers[page_name]()
            except Exception as e:
                st.error(f"页面加载失败：{str(e)}")
                st.error("请检查数据是否正确加载")
        else:
            st.error(f"未知页面：{page_name}")
            st.info("请选择有效的页面")
