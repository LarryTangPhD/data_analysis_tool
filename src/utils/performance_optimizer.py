"""
性能优化模块
提供数据缓存、懒加载、内存优化等功能
参考行业最佳实践优化用户体验
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Callable
import time
import functools
import gc


class PerformanceOptimizer:
    """性能优化器"""
    
    def __init__(self):
        """初始化性能优化器"""
        self.setup_cache_config()
        self.setup_session_state()
    
    def setup_cache_config(self):
        """设置缓存配置"""
        self.cache_config = {
            'max_entries': 100,
            'ttl': 3600,  # 1小时
            'show_spinner': True
        }
    
    def setup_session_state(self):
        """设置会话状态"""
        if 'performance_metrics' not in st.session_state:
            st.session_state.performance_metrics = {
                'load_times': {},
                'memory_usage': {},
                'cache_hits': 0,
                'cache_misses': 0
            }
        
        if 'optimization_settings' not in st.session_state:
            st.session_state.optimization_settings = {
                'enable_cache': True,
                'enable_lazy_loading': True,
                'enable_memory_optimization': True,
                'max_data_size': 1000000  # 100万行
            }
    
    @st.cache_data(ttl=3600, max_entries=50)
    def cached_data_processing(_data: pd.DataFrame, operation: str, **kwargs) -> Any:
        """
        缓存数据处理结果
        
        Args:
            _data: 数据框
            operation: 操作类型
            **kwargs: 其他参数
            
        Returns:
            处理结果
        """
        start_time = time.time()
        
        if operation == "describe":
            result = _data.describe()
        elif operation == "correlation":
            numeric_data = _data.select_dtypes(include=[np.number])
            result = numeric_data.corr() if len(numeric_data.columns) > 1 else pd.DataFrame()
        elif operation == "missing_summary":
            result = _data.isnull().sum().to_frame('missing_count')
            result['missing_ratio'] = result['missing_count'] / len(_data)
        elif operation == "dtype_summary":
            result = _data.dtypes.value_counts().to_frame('count')
        else:
            result = None
        
        # 记录性能指标
        if 'performance_metrics' in st.session_state:
            st.session_state.performance_metrics['load_times'][operation] = time.time() - start_time
            st.session_state.performance_metrics['cache_hits'] += 1
        
        return result
    
    def optimize_dataframe(_df: pd.DataFrame) -> pd.DataFrame:
        """
        优化DataFrame内存使用
        
        Args:
            _df: 原始DataFrame
            
        Returns:
            优化后的DataFrame
        """
        start_memory = _df.memory_usage(deep=True).sum()
        
        # 优化数值列
        for col in _df.select_dtypes(include=['int64']).columns:
            col_min = _df[col].min()
            col_max = _df[col].max()
            
            if col_min >= np.iinfo(np.int8).min and col_max <= np.iinfo(np.int8).max:
                _df[col] = _df[col].astype(np.int8)
            elif col_min >= np.iinfo(np.int16).min and col_max <= np.iinfo(np.int16).max:
                _df[col] = _df[col].astype(np.int16)
            elif col_min >= np.iinfo(np.int32).min and col_max <= np.iinfo(np.int32).max:
                _df[col] = _df[col].astype(np.int32)
        
        # 优化浮点列
        for col in _df.select_dtypes(include=['float64']).columns:
            _df[col] = pd.to_numeric(_df[col], downcast='float')
        
        # 优化字符串列
        for col in _df.select_dtypes(include=['object']).columns:
            if _df[col].nunique() / len(_df) < 0.5:  # 如果唯一值比例小于50%
                _df[col] = _df[col].astype('category')
        
        end_memory = _df.memory_usage(deep=True).sum()
        memory_reduction = (start_memory - end_memory) / start_memory * 100
        
        # 记录内存优化指标
        if 'performance_metrics' in st.session_state:
            st.session_state.performance_metrics['memory_usage']['optimization'] = {
                'before': start_memory,
                'after': end_memory,
                'reduction_percent': memory_reduction
            }
        
        return _df
    
    def lazy_load_data(data: pd.DataFrame, chunk_size: int = 10000) -> pd.DataFrame:
        """
        懒加载数据，分批处理大数据集
        
        Args:
            data: 完整数据集
            chunk_size: 分块大小
            
        Returns:
            处理后的数据
        """
        if len(data) <= chunk_size:
            return data
        
        # 显示进度条
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        processed_chunks = []
        total_chunks = (len(data) + chunk_size - 1) // chunk_size
        
        for i in range(0, len(data), chunk_size):
            chunk = data.iloc[i:i+chunk_size]
            processed_chunk = PerformanceOptimizer.optimize_dataframe(chunk)
            processed_chunks.append(processed_chunk)
            
            # 更新进度
            progress = (i + chunk_size) / len(data)
            progress_bar.progress(min(progress, 1.0))
            status_text.text(f"处理数据中... {i+chunk_size}/{len(data)} 行")
        
        progress_bar.empty()
        status_text.empty()
        
        return pd.concat(processed_chunks, ignore_index=True)
    
    def render_optimization_controls(self):
        """渲染性能优化控制面板"""
        st.sidebar.markdown("### ⚡ 性能设置")
        
        # 缓存设置
        enable_cache = st.sidebar.checkbox(
            "启用缓存",
            value=st.session_state.optimization_settings['enable_cache'],
            help="缓存计算结果以提高性能"
        )
        st.session_state.optimization_settings['enable_cache'] = enable_cache
        
        # 懒加载设置
        enable_lazy_loading = st.sidebar.checkbox(
            "启用懒加载",
            value=st.session_state.optimization_settings['enable_lazy_loading'],
            help="分批处理大数据集"
        )
        st.session_state.optimization_settings['enable_lazy_loading'] = enable_lazy_loading
        
        # 内存优化设置
        enable_memory_optimization = st.sidebar.checkbox(
            "启用内存优化",
            value=st.session_state.optimization_settings['enable_memory_optimization'],
            help="优化数据类型以减少内存使用"
        )
        st.session_state.optimization_settings['enable_memory_optimization'] = enable_memory_optimization
        
        # 性能指标
        if st.sidebar.button("📊 查看性能指标"):
            self.render_performance_metrics()
    
    def render_performance_metrics(self):
        """渲染性能指标"""
        metrics = st.session_state.performance_metrics
        
        st.markdown("### 📊 性能指标")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("缓存命中", metrics.get('cache_hits', 0))
        
        with col2:
            st.metric("缓存未命中", metrics.get('cache_misses', 0))
        
        with col3:
            if metrics.get('load_times'):
                avg_load_time = np.mean(list(metrics['load_times'].values()))
                st.metric("平均加载时间", f"{avg_load_time:.3f}s")
        
        with col4:
            if metrics.get('memory_usage', {}).get('optimization'):
                reduction = metrics['memory_usage']['optimization']['reduction_percent']
                st.metric("内存优化", f"{reduction:.1f}%")
        
        # 详细指标
        if metrics.get('load_times'):
            st.markdown("**加载时间详情：**")
            for operation, load_time in metrics['load_times'].items():
                st.text(f"• {operation}: {load_time:.3f}s")
        
        if metrics.get('memory_usage', {}).get('optimization'):
            opt = metrics['memory_usage']['optimization']
            st.markdown("**内存优化详情：**")
            st.text(f"• 优化前: {opt['before'] / 1024 / 1024:.2f} MB")
            st.text(f"• 优化后: {opt['after'] / 1024 / 1024:.2f} MB")
            st.text(f"• 减少: {opt['reduction_percent']:.1f}%")
    
    def clear_cache(self):
        """清除缓存"""
        st.cache_data.clear()
        st.cache_resource.clear()
        st.success("✅ 缓存已清除")
    
    def optimize_for_large_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        针对大数据集的优化
        
        Args:
            data: 原始数据
            
        Returns:
            优化后的数据
        """
        settings = st.session_state.optimization_settings
        
        if len(data) > settings['max_data_size']:
            st.warning(f"⚠️ 数据集较大 ({len(data):,} 行)，建议启用优化选项")
        
        if settings['enable_memory_optimization']:
            data = self.optimize_dataframe(data)
        
        if settings['enable_lazy_loading'] and len(data) > 50000:
            data = self.lazy_load_data(data)
        
        return data
    
    def monitor_performance(func: Callable) -> Callable:
        """
        性能监控装饰器
        
        Args:
            func: 要监控的函数
            
        Returns:
            包装后的函数
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            start_memory = gc.get_count()
            
            try:
                result = func(*args, **kwargs)
                
                # 记录性能指标
                execution_time = time.time() - start_time
                end_memory = gc.get_count()
                memory_used = sum(end_memory) - sum(start_memory)
                
                if 'performance_metrics' in st.session_state:
                    st.session_state.performance_metrics['load_times'][func.__name__] = execution_time
                    st.session_state.performance_metrics['memory_usage'][func.__name__] = memory_used
                
                return result
                
            except Exception as e:
                st.error(f"函数 {func.__name__} 执行失败: {str(e)}")
                raise
        
        return wrapper
    
    def get_data_sample(self, data: pd.DataFrame, sample_size: int = 1000) -> pd.DataFrame:
        """
        获取数据样本用于快速预览
        
        Args:
            data: 完整数据集
            sample_size: 样本大小
            
        Returns:
            数据样本
        """
        if len(data) <= sample_size:
            return data
        
        # 分层采样以保持数据分布
        if len(data.columns) > 0:
            # 选择数值列进行分层
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                # 基于第一个数值列进行分层采样
                sample_data = data.groupby(pd.qcut(data[numeric_cols[0]], 10, duplicates='drop')).apply(
                    lambda x: x.sample(min(len(x), sample_size // 10))
                ).reset_index(drop=True)
                return sample_data
        
        # 简单随机采样
        return data.sample(n=sample_size, random_state=42)
    
    def render_data_size_warning(self, data: pd.DataFrame):
        """渲染数据大小警告"""
        if len(data) > 100000:
            st.warning("""
            ⚠️ **大数据集警告**
            
            当前数据集较大，可能影响性能。建议：
            - 启用内存优化
            - 使用数据采样进行快速预览
            - 考虑数据预处理
            """)
            
            if st.button("🔧 应用优化设置"):
                st.session_state.optimization_settings.update({
                    'enable_cache': True,
                    'enable_lazy_loading': True,
                    'enable_memory_optimization': True
                })
                st.success("✅ 优化设置已应用")
    
    def cleanup_memory(self):
        """清理内存"""
        gc.collect()
        st.success("✅ 内存清理完成")


# 全局性能优化器实例
performance_optimizer = PerformanceOptimizer()

def get_performance_optimizer():
    """获取性能优化器实例"""
    return performance_optimizer
