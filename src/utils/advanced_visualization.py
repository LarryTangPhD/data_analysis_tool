"""
高级可视化组件
提供专业级的数据可视化功能，包括交互式图表、3D可视化、仪表板等
"""

import plotly.graph_objects as go
import plotly.express as px
import plotly.subplots as sp
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
import streamlit as st
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class AdvancedVisualizer:
    """高级可视化器"""
    
    def __init__(self):
        self.color_schemes = {
            "数眸蓝": ["#1E40AF", "#3B82F6", "#60A5FA", "#93C5FD", "#DBEAFE"],
            "数眸绿": ["#059669", "#10B981", "#34D399", "#6EE7B7", "#A7F3D0"],
            "数眸橙": ["#D97706", "#F59E0B", "#FBBF24", "#FCD34D", "#FDE68A"],
            "数眸紫": ["#7C3AED", "#8B5CF6", "#A78BFA", "#C4B5FD", "#DDD6FE"],
            "专业灰": ["#374151", "#6B7280", "#9CA3AF", "#D1D5DB", "#F3F4F6"]
        }
        
        self.default_colors = self.color_schemes["数眸蓝"]
    
    def create_interactive_dashboard(self, data: pd.DataFrame, 
                                   numeric_cols: List[str],
                                   categorical_cols: List[str]) -> go.Figure:
        """创建交互式仪表板"""
        
        # 创建子图布局
        fig = sp.make_subplots(
            rows=2, cols=2,
            subplot_titles=("数据分布概览", "相关性热力图", "时间趋势分析", "分类统计"),
            specs=[[{"type": "scatter"}, {"type": "heatmap"}],
                   [{"type": "bar"}, {"type": "pie"}]]
        )
        
        # 1. 数据分布概览 - 散点图
        if len(numeric_cols) >= 2:
            fig.add_trace(
                go.Scatter(
                    x=data[numeric_cols[0]],
                    y=data[numeric_cols[1]],
                    mode='markers',
                    marker=dict(
                        size=8,
                        color=data[numeric_cols[0]] if len(numeric_cols) > 0 else None,
                        colorscale='Viridis',
                        showscale=True
                    ),
                    name=f"{numeric_cols[0]} vs {numeric_cols[1]}"
                ),
                row=1, col=1
            )
        
        # 2. 相关性热力图
        if len(numeric_cols) > 1:
            corr_matrix = data[numeric_cols].corr()
            fig.add_trace(
                go.Heatmap(
                    z=corr_matrix.values,
                    x=corr_matrix.columns,
                    y=corr_matrix.columns,
                    colorscale='RdBu_r',
                    zmid=0,
                    name="相关性"
                ),
                row=1, col=2
            )
        
        # 3. 时间趋势分析 - 柱状图
        if len(numeric_cols) > 0:
            # 选择第一个数值列进行趋势分析
            values = data[numeric_cols[0]].dropna()
            if len(values) > 0:
                # 创建时间索引（如果数据没有时间列）
                time_index = pd.date_range(start='2023-01-01', periods=len(values), freq='D')
                
                fig.add_trace(
                    go.Bar(
                        x=time_index,
                        y=values,
                        name=f"{numeric_cols[0]} 趋势",
                        marker_color=self.default_colors[0]
                    ),
                    row=2, col=1
                )
        
        # 4. 分类统计 - 饼图
        if len(categorical_cols) > 0:
            cat_counts = data[categorical_cols[0]].value_counts()
            fig.add_trace(
                go.Pie(
                    labels=cat_counts.index,
                    values=cat_counts.values,
                    name="分类分布",
                    marker_colors=self.default_colors
                ),
                row=2, col=2
            )
        
        # 更新布局
        fig.update_layout(
            title="数眸 - 交互式数据分析仪表板",
            height=800,
            showlegend=True,
            template="plotly_white"
        )
        
        return fig
    
    def create_3d_scatter_plot(self, data: pd.DataFrame, 
                              x_col: str, y_col: str, z_col: str,
                              color_col: Optional[str] = None,
                              size_col: Optional[str] = None) -> go.Figure:
        """创建3D散点图"""
        
        fig = go.Figure()
        
        # 准备数据
        plot_data = data[[x_col, y_col, z_col]].dropna()
        
        if color_col and color_col in data.columns:
            color_values = data[color_col].dropna()
            # 确保颜色数据与主数据长度一致
            common_index = plot_data.index.intersection(color_values.index)
            plot_data = plot_data.loc[common_index]
            color_values = color_values.loc[common_index]
        else:
            color_values = None
        
        if size_col and size_col in data.columns:
            size_values = data[size_col].dropna()
            # 确保大小数据与主数据长度一致
            common_index = plot_data.index.intersection(size_values.index)
            plot_data = plot_data.loc[common_index]
            size_values = size_values.loc[common_index]
        else:
            size_values = None
        
        # 创建3D散点图
        fig.add_trace(
            go.Scatter3d(
                x=plot_data[x_col],
                y=plot_data[y_col],
                z=plot_data[z_col],
                mode='markers',
                marker=dict(
                    size=size_values if size_values is not None else 8,
                    color=color_values if color_values is not None else None,
                    colorscale='Viridis' if color_values is not None else None,
                    showscale=color_values is not None,
                    opacity=0.8
                ),
                text=[f"X: {x:.2f}<br>Y: {y:.2f}<br>Z: {z:.2f}" 
                      for x, y, z in zip(plot_data[x_col], plot_data[y_col], plot_data[z_col])],
                hoverinfo='text'
            )
        )
        
        # 更新布局
        fig.update_layout(
            title=f"3D散点图: {x_col} vs {y_col} vs {z_col}",
            scene=dict(
                xaxis_title=x_col,
                yaxis_title=y_col,
                zaxis_title=z_col,
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            width=800,
            height=600,
            template="plotly_white"
        )
        
        return fig
    
    def create_advanced_heatmap(self, data: pd.DataFrame, 
                               method: str = "correlation",
                               color_scheme: str = "数眸蓝") -> go.Figure:
        """创建高级热力图"""
        
        colors = self.color_schemes.get(color_scheme, self.default_colors)
        
        if method == "correlation":
            # 相关性热力图
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) < 2:
                st.warning("需要至少2个数值型列来创建相关性热力图")
                return None
            
            corr_matrix = data[numeric_cols].corr()
            
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale=colors,
                zmid=0,
                text=np.round(corr_matrix.values, 3),
                texttemplate="%{text}",
                textfont={"size": 10},
                hoverongaps=False
            ))
            
            fig.update_layout(
                title="相关性热力图",
                xaxis_title="变量",
                yaxis_title="变量",
                template="plotly_white"
            )
            
        elif method == "missing_values":
            # 缺失值热力图
            missing_matrix = data.isnull().astype(int)
            
            fig = go.Figure(data=go.Heatmap(
                z=missing_matrix.values,
                x=missing_matrix.columns,
                y=missing_matrix.index,
                colorscale=[[0, colors[4]], [1, colors[0]]],
                showscale=True,
                hoverongaps=False
            ))
            
            fig.update_layout(
                title="缺失值分布热力图",
                xaxis_title="列",
                yaxis_title="行",
                template="plotly_white"
            )
        
        return fig
    
    def create_time_series_analysis(self, data: pd.DataFrame, 
                                   time_col: str, value_col: str,
                                   analysis_type: str = "trend") -> go.Figure:
        """创建时间序列分析图"""
        
        # 确保时间列格式正确
        if not pd.api.types.is_datetime64_any_dtype(data[time_col]):
            try:
                data[time_col] = pd.to_datetime(data[time_col])
            except:
                st.error(f"无法将 {time_col} 转换为时间格式")
                return None
        
        # 排序数据
        plot_data = data[[time_col, value_col]].dropna().sort_values(time_col)
        
        fig = go.Figure()
        
        if analysis_type == "trend":
            # 趋势分析
            fig.add_trace(
                go.Scatter(
                    x=plot_data[time_col],
                    y=plot_data[value_col],
                    mode='lines+markers',
                    name='原始数据',
                    line=dict(color=self.default_colors[0], width=2)
                )
            )
            
            # 添加趋势线
            x_numeric = np.arange(len(plot_data))
            z = np.polyfit(x_numeric, plot_data[value_col], 1)
            p = np.poly1d(z)
            trend_line = p(x_numeric)
            
            fig.add_trace(
                go.Scatter(
                    x=plot_data[time_col],
                    y=trend_line,
                    mode='lines',
                    name='趋势线',
                    line=dict(color=self.default_colors[2], width=3, dash='dash')
                )
            )
            
        elif analysis_type == "seasonal":
            # 季节性分析
            plot_data['month'] = plot_data[time_col].dt.month
            monthly_avg = plot_data.groupby('month')[value_col].mean()
            
            fig.add_trace(
                go.Bar(
                    x=monthly_avg.index,
                    y=monthly_avg.values,
                    name='月度平均值',
                    marker_color=self.default_colors[1]
                )
            )
            
        elif analysis_type == "decomposition":
            # 时间序列分解
            from statsmodels.tsa.seasonal import seasonal_decompose
            
            # 重采样到统一频率
            plot_data = plot_data.set_index(time_col).resample('D').mean().dropna()
            
            if len(plot_data) > 30:  # 需要足够的数据点
                decomposition = seasonal_decompose(plot_data[value_col], period=min(12, len(plot_data)//4))
                
                # 创建子图
                fig = sp.make_subplots(
                    rows=4, cols=1,
                    subplot_titles=('原始数据', '趋势', '季节性', '残差'),
                    vertical_spacing=0.05
                )
                
                fig.add_trace(
                    go.Scatter(x=plot_data.index, y=plot_data[value_col], name='原始数据'),
                    row=1, col=1
                )
                fig.add_trace(
                    go.Scatter(x=plot_data.index, y=decomposition.trend, name='趋势'),
                    row=2, col=1
                )
                fig.add_trace(
                    go.Scatter(x=plot_data.index, y=decomposition.seasonal, name='季节性'),
                    row=3, col=1
                )
                fig.add_trace(
                    go.Scatter(x=plot_data.index, y=decomposition.resid, name='残差'),
                    row=4, col=1
                )
                
                fig.update_layout(height=800, title_text="时间序列分解")
                return fig
        
        fig.update_layout(
            title=f"时间序列分析: {value_col}",
            xaxis_title="时间",
            yaxis_title=value_col,
            template="plotly_white"
        )
        
        return fig
    
    def create_distribution_comparison(self, data: pd.DataFrame,
                                     numeric_cols: List[str],
                                     plot_type: str = "histogram") -> go.Figure:
        """创建分布比较图"""
        
        if len(numeric_cols) < 2:
            st.warning("需要至少2个数值型列来创建分布比较图")
            return None
        
        if plot_type == "histogram":
            # 直方图比较
            fig = go.Figure()
            
            for i, col in enumerate(numeric_cols):
                fig.add_trace(
                    go.Histogram(
                        x=data[col].dropna(),
                        name=col,
                        opacity=0.7,
                        marker_color=self.default_colors[i % len(self.default_colors)]
                    )
                )
            
            fig.update_layout(
                title="分布比较 - 直方图",
                xaxis_title="值",
                yaxis_title="频数",
                barmode='overlay',
                template="plotly_white"
            )
            
        elif plot_type == "box":
            # 箱线图比较
            fig = go.Figure()
            
            for i, col in enumerate(numeric_cols):
                fig.add_trace(
                    go.Box(
                        y=data[col].dropna(),
                        name=col,
                        marker_color=self.default_colors[i % len(self.default_colors)]
                    )
                )
            
            fig.update_layout(
                title="分布比较 - 箱线图",
                yaxis_title="值",
                template="plotly_white"
            )
            
        elif plot_type == "violin":
            # 小提琴图比较
            fig = go.Figure()
            
            for i, col in enumerate(numeric_cols):
                fig.add_trace(
                    go.Violin(
                        y=data[col].dropna(),
                        name=col,
                        marker_color=self.default_colors[i % len(self.default_colors)]
                    )
                )
            
            fig.update_layout(
                title="分布比较 - 小提琴图",
                yaxis_title="值",
                template="plotly_white"
            )
        
        return fig
    
    def create_interactive_table(self, data: pd.DataFrame,
                                page_size: int = 10) -> go.Figure:
        """创建交互式表格"""
        
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=list(data.columns),
                fill_color=self.default_colors[0],
                align='left',
                font=dict(color='white', size=12)
            ),
            cells=dict(
                values=[data[col] for col in data.columns],
                fill_color='lavender',
                align='left',
                font=dict(size=11)
            )
        )])
        
        fig.update_layout(
            title="交互式数据表格",
            height=400
        )
        
        return fig

def render_advanced_visualization_page(data: pd.DataFrame):
    """渲染高级可视化页面"""
    
    st.subheader("📈 高级可视化分析")
    
    if data is None or len(data) == 0:
        st.warning("请先上传数据")
        return
    
    # 初始化可视化器
    visualizer = AdvancedVisualizer()
    
    # 获取数据类型
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime_cols = data.select_dtypes(include=['datetime']).columns.tolist()
    
    # 可视化类型选择
    viz_type = st.selectbox(
        "选择可视化类型",
        [
            "📊 交互式仪表板",
            "🎯 3D散点图",
            "🔥 高级热力图",
            "📈 时间序列分析",
            "📊 分布比较",
            "📋 交互式表格"
        ]
    )
    
    if viz_type == "📊 交互式仪表板":
        st.write("**创建交互式数据分析仪表板**")
        
        if len(numeric_cols) >= 2:
            fig = visualizer.create_interactive_dashboard(data, numeric_cols, categorical_cols)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("需要至少2个数值型列来创建仪表板")
    
    elif viz_type == "🎯 3D散点图":
        st.write("**创建3D散点图**")
        
        if len(numeric_cols) >= 3:
            col1, col2, col3 = st.columns(3)
            with col1:
                x_col = st.selectbox("选择X轴", numeric_cols)
            with col2:
                y_col = st.selectbox("选择Y轴", [col for col in numeric_cols if col != x_col])
            with col3:
                z_col = st.selectbox("选择Z轴", [col for col in numeric_cols if col not in [x_col, y_col]])
            
            color_col = st.selectbox("选择颜色列（可选）", [None] + categorical_cols)
            size_col = st.selectbox("选择大小列（可选）", [None] + numeric_cols)
            
            if st.button("生成3D散点图"):
                fig = visualizer.create_3d_scatter_plot(
                    data, x_col, y_col, z_col, color_col, size_col
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("需要至少3个数值型列来创建3D散点图")
    
    elif viz_type == "🔥 高级热力图":
        st.write("**创建高级热力图**")
        
        heatmap_type = st.selectbox("选择热力图类型", ["correlation", "missing_values"])
        color_scheme = st.selectbox("选择配色方案", list(visualizer.color_schemes.keys()))
        
        if st.button("生成热力图"):
            fig = visualizer.create_advanced_heatmap(data, heatmap_type, color_scheme)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "📈 时间序列分析":
        st.write("**时间序列分析**")
        
        if len(datetime_cols) > 0:
            time_col = st.selectbox("选择时间列", datetime_cols)
        else:
            st.warning("数据中没有时间列，无法进行时间序列分析")
            return
        
        if len(numeric_cols) > 0:
            value_col = st.selectbox("选择数值列", numeric_cols)
            analysis_type = st.selectbox("选择分析类型", ["trend", "seasonal", "decomposition"])
            
            if st.button("生成时间序列分析"):
                fig = visualizer.create_time_series_analysis(
                    data, time_col, value_col, analysis_type
                )
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "📊 分布比较":
        st.write("**分布比较分析**")
        
        if len(numeric_cols) >= 2:
            selected_cols = st.multiselect("选择要比较的列", numeric_cols, default=numeric_cols[:3])
            plot_type = st.selectbox("选择图表类型", ["histogram", "box", "violin"])
            
            if st.button("生成分布比较图"):
                fig = visualizer.create_distribution_comparison(
                    data, selected_cols, plot_type
                )
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("需要至少2个数值型列来创建分布比较图")
    
    elif viz_type == "📋 交互式表格":
        st.write("**交互式数据表格**")
        
        page_size = st.slider("每页显示行数", 5, 50, 10)
        
        fig = visualizer.create_interactive_table(data, page_size)
        st.plotly_chart(fig, use_container_width=True)
