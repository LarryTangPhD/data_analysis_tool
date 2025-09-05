"""
会话管理器
负责管理Streamlit的session state
"""

import streamlit as st
from typing import Any, Optional


class SessionManager:
    """会话管理器"""
    
    def __init__(self):
        """初始化会话管理器"""
        self.default_values = {
            'data': None,
            'data_cleaned': None,
            'profile_report': None,
            'current_page': "🏠 首页",
            'selected_mode': "professional",
            'ai_assistant': None,
            'workflow': None,
            'analysis_results': {},
            'visualization_config': {},
            'ml_models': {},
            'reports': {}
        }
    
    def initialize_session_state(self):
        """初始化session state"""
        for key, default_value in self.default_values.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
    
    def get_data(self) -> Optional[Any]:
        """获取当前数据"""
        return st.session_state.get('data')
    
    def set_data(self, data: Any):
        """设置数据"""
        st.session_state.data = data
    
    def get_cleaned_data(self) -> Optional[Any]:
        """获取清洗后的数据"""
        return st.session_state.get('data_cleaned')
    
    def set_cleaned_data(self, data: Any):
        """设置清洗后的数据"""
        st.session_state.data_cleaned = data
    
    def get_current_page(self) -> str:
        """获取当前页面"""
        return st.session_state.get('current_page', "🏠 首页")
    
    def set_current_page(self, page: str):
        """设置当前页面"""
        st.session_state.current_page = page
    
    def get_selected_mode(self) -> str:
        """获取选中的模式"""
        return st.session_state.get('selected_mode', "professional")
    
    def set_selected_mode(self, mode: str):
        """设置选中的模式"""
        st.session_state.selected_mode = mode
    
    def get_ai_assistant(self) -> Optional[Any]:
        """获取AI助手实例"""
        return st.session_state.get('ai_assistant')
    
    def set_ai_assistant(self, assistant: Any):
        """设置AI助手实例"""
        st.session_state.ai_assistant = assistant
    
    def get_workflow(self) -> Optional[Any]:
        """获取工作流实例"""
        return st.session_state.get('workflow')
    
    def set_workflow(self, workflow: Any):
        """设置工作流实例"""
        st.session_state.workflow = workflow
    
    def get_analysis_results(self) -> dict:
        """获取分析结果"""
        return st.session_state.get('analysis_results', {})
    
    def set_analysis_results(self, results: dict):
        """设置分析结果"""
        st.session_state.analysis_results = results
    
    def add_analysis_result(self, key: str, value: Any):
        """添加分析结果"""
        if 'analysis_results' not in st.session_state:
            st.session_state.analysis_results = {}
        st.session_state.analysis_results[key] = value
    
    def get_visualization_config(self) -> dict:
        """获取可视化配置"""
        return st.session_state.get('visualization_config', {})
    
    def set_visualization_config(self, config: dict):
        """设置可视化配置"""
        st.session_state.visualization_config = config
    
    def get_ml_models(self) -> dict:
        """获取机器学习模型"""
        return st.session_state.get('ml_models', {})
    
    def set_ml_models(self, models: dict):
        """设置机器学习模型"""
        st.session_state.ml_models = models
    
    def add_ml_model(self, name: str, model: Any):
        """添加机器学习模型"""
        if 'ml_models' not in st.session_state:
            st.session_state.ml_models = {}
        st.session_state.ml_models[name] = model
    
    def get_reports(self) -> dict:
        """获取报告"""
        return st.session_state.get('reports', {})
    
    def set_reports(self, reports: dict):
        """设置报告"""
        st.session_state.reports = reports
    
    def add_report(self, name: str, report: Any):
        """添加报告"""
        if 'reports' not in st.session_state:
            st.session_state.reports = {}
        st.session_state.reports[name] = report
    
    def clear_data(self):
        """清除数据"""
        st.session_state.data = None
        st.session_state.data_cleaned = None
    
    def clear_analysis_results(self):
        """清除分析结果"""
        st.session_state.analysis_results = {}
    
    def clear_ml_models(self):
        """清除机器学习模型"""
        st.session_state.ml_models = {}
    
    def clear_all(self):
        """清除所有session state"""
        for key in self.default_values.keys():
            if key in st.session_state:
                del st.session_state[key]
        self.initialize_session_state()
    
    def has_data(self) -> bool:
        """检查是否有数据"""
        return st.session_state.get('data') is not None
    
    def has_cleaned_data(self) -> bool:
        """检查是否有清洗后的数据"""
        return st.session_state.get('data_cleaned') is not None
    
    def get_data_info(self) -> dict:
        """获取数据信息"""
        data = self.get_data()
        if data is None:
            return {}
        
        return {
            'rows': len(data),
            'columns': len(data.columns),
            'memory_usage': data.memory_usage(deep=True).sum() / 1024**2,
            'missing_values': data.isnull().sum().sum(),
            'duplicate_rows': data.duplicated().sum()
        }
