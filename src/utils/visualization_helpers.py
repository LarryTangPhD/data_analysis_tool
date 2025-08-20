"""
可视化工具模块
包含各种图表创建和样式设置功能
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import List, Optional, Dict, Any, Tuple
import streamlit as st


def create_bar_chart(data: pd.DataFrame, x_col: str, y_col: str, 
                    color_col: Optional[str] = None, title: str = "") -> go.Figure:
    """
    创建柱状图
    
    Args:
        data: 数据框
        x_col: X轴列名
        y_col: Y轴列名
        color_col: 颜色分组列名
        title: 图表标题
        
    Returns:
        go.Figure: Plotly图表对象
    """
    if color_col:
        fig = px.bar(data, x=x_col, y=y_col, color=color_col, title=title)
    else:
        fig = px.bar(data, x=x_col, y=y_col, title=title)
    
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        showlegend=True
    )
    return fig


def create_line_chart(data: pd.DataFrame, x_col: str, y_col: str,
                     color_col: Optional[str] = None, title: str = "") -> go.Figure:
    """
    创建折线图
    
    Args:
        data: 数据框
        x_col: X轴列名
        y_col: Y轴列名
        color_col: 颜色分组列名
        title: 图表标题
        
    Returns:
        go.Figure: Plotly图表对象
    """
    if color_col:
        fig = px.line(data, x=x_col, y=y_col, color=color_col, title=title)
    else:
        fig = px.line(data, x=x_col, y=y_col, title=title)
    
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        showlegend=True
    )
    return fig


def create_scatter_chart(data: pd.DataFrame, x_col: str, y_col: str,
                        color_col: Optional[str] = None, size_col: Optional[str] = None,
                        title: str = "") -> go.Figure:
    """
    创建散点图
    
    Args:
        data: 数据框
        x_col: X轴列名
        y_col: Y轴列名
        color_col: 颜色分组列名
        size_col: 大小列名
        title: 图表标题
        
    Returns:
        go.Figure: Plotly图表对象
    """
    if color_col and size_col:
        fig = px.scatter(data, x=x_col, y=y_col, color=color_col, size=size_col, title=title)
    elif color_col:
        fig = px.scatter(data, x=x_col, y=y_col, color=color_col, title=title)
    elif size_col:
        fig = px.scatter(data, x=x_col, y=y_col, size=size_col, title=title)
    else:
        fig = px.scatter(data, x=x_col, y=y_col, title=title)
    
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        showlegend=True
    )
    return fig


def create_pie_chart(data: pd.DataFrame, values_col: str, names_col: str, title: str = "") -> go.Figure:
    """
    创建饼图
    
    Args:
        data: 数据框
        values_col: 值列名
        names_col: 名称列名
        title: 图表标题
        
    Returns:
        go.Figure: Plotly图表对象
    """
    fig = px.pie(data, values=values_col, names=names_col, title=title)
    fig.update_layout(showlegend=True)
    return fig


def create_histogram(data: pd.DataFrame, x_col: str, bins: int = 20, title: str = "") -> go.Figure:
    """
    创建直方图
    
    Args:
        data: 数据框
        x_col: X轴列名
        bins: 直方图箱数
        title: 图表标题
        
    Returns:
        go.Figure: Plotly图表对象
    """
    fig = px.histogram(data, x=x_col, nbins=bins, title=title)
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title="频数",
        showlegend=False
    )
    return fig


def create_box_chart(data: pd.DataFrame, y_col: str, x_col: Optional[str] = None, title: str = "") -> go.Figure:
    """
    创建箱线图
    
    Args:
        data: 数据框
        y_col: Y轴列名
        x_col: X轴分组列名
        title: 图表标题
        
    Returns:
        go.Figure: Plotly图表对象
    """
    if x_col:
        fig = px.box(data, x=x_col, y=y_col, title=title)
    else:
        fig = px.box(data, y=y_col, title=title)
    
    fig.update_layout(
        xaxis_title=x_col if x_col else "",
        yaxis_title=y_col,
        showlegend=False
    )
    return fig


def create_heatmap(corr_matrix: pd.DataFrame, title: str = "相关性热力图") -> go.Figure:
    """
    创建热力图
    
    Args:
        corr_matrix: 相关性矩阵
        title: 图表标题
        
    Returns:
        go.Figure: Plotly图表对象
    """
    fig = px.imshow(
        corr_matrix,
        title=title,
        color_continuous_scale='RdBu',
        aspect='auto'
    )
    fig.update_layout(
        xaxis_title="变量",
        yaxis_title="变量"
    )
    return fig


def create_violin_chart(data: pd.DataFrame, y_col: str, x_col: Optional[str] = None, title: str = "") -> go.Figure:
    """
    创建小提琴图
    
    Args:
        data: 数据框
        y_col: Y轴列名
        x_col: X轴分组列名
        title: 图表标题
        
    Returns:
        go.Figure: Plotly图表对象
    """
    if x_col:
        fig = px.violin(data, x=x_col, y=y_col, title=title)
    else:
        fig = px.violin(data, y=y_col, title=title)
    
    fig.update_layout(
        xaxis_title=x_col if x_col else "",
        yaxis_title=y_col,
        showlegend=False
    )
    return fig


def create_3d_scatter(data: pd.DataFrame, x_col: str, y_col: str, z_col: str,
                     color_col: Optional[str] = None, title: str = "") -> go.Figure:
    """
    创建3D散点图
    
    Args:
        data: 数据框
        x_col: X轴列名
        y_col: Y轴列名
        z_col: Z轴列名
        color_col: 颜色分组列名
        title: 图表标题
        
    Returns:
        go.Figure: Plotly图表对象
    """
    if color_col:
        fig = px.scatter_3d(data, x=x_col, y=y_col, z=z_col, color=color_col, title=title)
    else:
        fig = px.scatter_3d(data, x=x_col, y=y_col, z=z_col, title=title)
    
    fig.update_layout(
        scene=dict(
            xaxis_title=x_col,
            yaxis_title=y_col,
            zaxis_title=z_col
        )
    )
    return fig


def create_radar_chart(data: pd.DataFrame, columns: List[str], title: str = "") -> go.Figure:
    """
    创建雷达图
    
    Args:
        data: 数据框
        columns: 要显示的列名列表
        title: 图表标题
        
    Returns:
        go.Figure: Plotly图表对象
    """
    # 计算平均值用于雷达图
    avg_values = data[columns].mean()
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=avg_values.values,
        theta=columns,
        fill='toself',
        name='平均值'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, avg_values.max() * 1.2]
            )),
        showlegend=True,
        title=title
    )
    return fig


def create_missing_values_chart(data: pd.DataFrame) -> go.Figure:
    """
    创建缺失值分析图表
    
    Args:
        data: 数据框
        
    Returns:
        go.Figure: Plotly图表对象
    """
    missing_data = data.isnull().sum()
    missing_percent = (missing_data / len(data)) * 100
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data.columns,
        y=missing_data,
        name='缺失值数量',
        marker_color='#ff7f0e'
    ))
    fig.add_trace(go.Scatter(
        x=data.columns,
        y=missing_percent,
        name='缺失值百分比',
        yaxis='y2'
    ))
    
    fig.update_layout(
        title='缺失值分析',
        xaxis_title='列名',
        yaxis=dict(title='缺失值数量'),
        yaxis2=dict(title='缺失值百分比 (%)', overlaying='y', side='right'),
        height=400
    )
    return fig


def create_data_type_chart(data: pd.DataFrame) -> go.Figure:
    """
    创建数据类型分布图表
    
    Args:
        data: 数据框
        
    Returns:
        go.Figure: Plotly图表对象
    """
    dtype_counts = data.dtypes.value_counts()
    dtype_labels = [str(dtype) for dtype in dtype_counts.index]
    
    fig = go.Figure(data=[go.Pie(
        labels=dtype_labels,
        values=dtype_counts.values,
        hole=0.3
    )])
    fig.update_layout(
        title='数据类型分布',
        showlegend=True
    )
    return fig


def create_correlation_heatmap(data: pd.DataFrame, numeric_cols: List[str]) -> go.Figure:
    """
    创建相关性热力图
    
    Args:
        data: 数据框
        numeric_cols: 数值型列名列表
        
    Returns:
        go.Figure: Plotly图表对象
    """
    if len(numeric_cols) > 1:
        corr_matrix = data[numeric_cols].corr()
        fig = px.imshow(
            corr_matrix,
            title='相关性热力图',
            color_continuous_scale='RdBu',
            aspect='auto'
        )
        return fig
    else:
        # 如果数值型列不足，返回空图表
        fig = go.Figure()
        fig.add_annotation(
            text="需要至少2个数值型列来创建相关性热力图",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig


def create_distribution_comparison(data: pd.DataFrame, column: str, title: str = "") -> go.Figure:
    """
    创建分布对比图表（直方图+箱线图）
    
    Args:
        data: 数据框
        column: 要分析的列名
        title: 图表标题
        
    Returns:
        go.Figure: Plotly图表对象
    """
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=(f'{column} 分布直方图', f'{column} 箱线图'),
        vertical_spacing=0.1
    )
    
    # 直方图
    fig.add_trace(
        go.Histogram(x=data[column], nbinsx=30, name='直方图'),
        row=1, col=1
    )
    
    # 箱线图
    fig.add_trace(
        go.Box(y=data[column], name='箱线图'),
        row=2, col=1
    )
    
    fig.update_layout(
        title=title,
        height=600,
        showlegend=False
    )
    
    return fig


def create_learning_curve(train_sizes: np.ndarray, train_scores: np.ndarray, 
                         val_scores: np.ndarray, title: str = "学习曲线") -> go.Figure:
    """
    创建学习曲线图表
    
    Args:
        train_sizes: 训练样本数
        train_scores: 训练分数
        val_scores: 验证分数
        title: 图表标题
        
    Returns:
        go.Figure: Plotly图表对象
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=train_sizes,
        y=train_scores,
        mode='lines+markers',
        name='训练分数',
        line=dict(color='blue')
    ))
    
    fig.add_trace(go.Scatter(
        x=train_sizes,
        y=val_scores,
        mode='lines+markers',
        name='验证分数',
        line=dict(color='red')
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="训练样本数",
        yaxis_title="R²分数",
        showlegend=True
    )
    
    return fig


def create_confusion_matrix(cm: np.ndarray, labels: List[str], title: str = "混淆矩阵") -> go.Figure:
    """
    创建混淆矩阵热力图
    
    Args:
        cm: 混淆矩阵
        labels: 标签列表
        title: 图表标题
        
    Returns:
        go.Figure: Plotly图表对象
    """
    fig = px.imshow(
        cm, 
        labels=dict(x="预测", y="实际", color="数量"),
        x=labels,
        y=labels,
        title=title,
        color_continuous_scale='Blues'
    )
    return fig


def create_feature_importance(feature_names: List[str], importance_scores: np.ndarray, 
                            title: str = "特征重要性") -> go.Figure:
    """
    创建特征重要性图表
    
    Args:
        feature_names: 特征名称列表
        importance_scores: 重要性分数
        title: 图表标题
        
    Returns:
        go.Figure: Plotly图表对象
    """
    importance_df = pd.DataFrame({
        '特征': feature_names,
        '重要性': importance_scores
    }).sort_values('重要性', ascending=False)
    
    fig = px.bar(
        importance_df, 
        x='重要性', 
        y='特征', 
        title=title, 
        orientation='h',
        color='重要性',
        color_continuous_scale='Viridis'
    )
    return fig


def apply_custom_theme(fig: go.Figure, theme: str = "default") -> go.Figure:
    """
    应用自定义主题
    
    Args:
        fig: Plotly图表对象
        theme: 主题名称
        
    Returns:
        go.Figure: 应用主题后的图表对象
    """
    if theme == "dark":
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
    elif theme == "light":
        fig.update_layout(
            template="plotly_white",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
    
    return fig


def save_chart_as_image(fig: go.Figure, filename: str, format: str = "png", 
                       width: int = 800, height: int = 600) -> None:
    """
    保存图表为图片文件
    
    Args:
        fig: Plotly图表对象
        filename: 文件名
        format: 图片格式 (png, jpg, svg, pdf)
        width: 图片宽度
        height: 图片高度
    """
    fig.write_image(f"{filename}.{format}", width=width, height=height)
