"""
模式管理器
负责管理不同的分析模式（新手、普通、专业）
"""

import streamlit as st
from typing import Dict, Any, Optional
from src.config.settings import ANALYSIS_MODES


class ModeManager:
    """模式管理器"""
    
    def __init__(self):
        """初始化模式管理器"""
        self.modes = ANALYSIS_MODES
        
    def get_current_mode(self) -> str:
        """获取当前模式"""
        return st.session_state.get('selected_mode', 'professional')
    
    def set_mode(self, mode: str):
        """设置模式"""
        if mode in self.modes:
            st.session_state.selected_mode = mode
            st.rerun()
        else:
            st.error(f"无效的模式：{mode}")
    
    def get_mode_info(self, mode: str) -> Optional[Dict[str, Any]]:
        """获取模式信息"""
        return self.modes.get(mode)
    
    def get_all_modes(self) -> Dict[str, Any]:
        """获取所有模式信息"""
        return self.modes
    
    def is_beginner_mode(self) -> bool:
        """检查是否为新手模式"""
        return self.get_current_mode() == 'beginner'
    
    def is_intermediate_mode(self) -> bool:
        """检查是否为普通模式"""
        return self.get_current_mode() == 'intermediate'
    
    def is_professional_mode(self) -> bool:
        """检查是否为专业模式"""
        return self.get_current_mode() == 'professional'
    
    def get_mode_features(self, mode: str) -> list:
        """获取模式功能列表"""
        mode_info = self.get_mode_info(mode)
        return mode_info.get('features', []) if mode_info else []
    
    def validate_mode_access(self, required_mode: str, current_page: str) -> bool:
        """验证模式访问权限"""
        current_mode = self.get_current_mode()
        
        # 专业模式可以访问所有页面
        if current_mode == 'professional':
            return True
        
        # 新手模式只能访问基础页面
        if current_mode == 'beginner':
            allowed_pages = ["🏠 首页", "📁 数据上传", "🧹 数据清洗"]
            return current_page in allowed_pages
        
        # 普通模式可以访问大部分页面
        if current_mode == 'intermediate':
            restricted_pages = ["📊 工作流管理", "🤖 机器学习"]
            return current_page not in restricted_pages
        
        return False
