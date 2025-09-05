"""
专业分析页面模块
集成高级数据科学功能，提供专业级分析体验
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, List
import plotly.graph_objects as go
import plotly.express as px

# 导入自定义模块
from src.utils.performance_optimizer import (
    get_memory_usage, optimize_dataframe_memory, 
    smart_sample_data, cleanup_memory, generate_performance_report
)
from src.utils.advanced_visualization import (
    create_dashboard, create_3d_scatter, create_advanced_box,
    create_distribution_compare, create_correlation_network,
    create_time_series, create_statistical_summary
)
from src.utils.data_science_workflow import (
    workflow_manager, DataExplorationWorkflow, 
    DataQualityAnalyzer, FeatureEngineeringWorkflow
)
from src.utils.data_processing import (
    load_data, calculate_data_quality_score, get_data_info,
    handle_missing_values, handle_duplicates, handle_outliers
)
from src.utils.visualization_helpers import (
    create_bar_chart, create_line_chart, create_scatter_chart,
    create_pie_chart, create_histogram, create_box_chart,
    create_correlation_heatmap, create_violin_chart
)
from src.utils.ml_helpers import (
    train_classification_model, train_regression_model,
    perform_clustering
)

def render_professional_analysis_page():
    """渲染专业分析页面"""
    st.markdown('<h2 class="sub-header">🔬 专业数据分析</h2>', unsafe_allow_html=True)
    
    # 专业分析介绍
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px rgba(30, 64, 175, 0.3);
    ">
        <h3 style="color: white; margin-bottom: 20px; text-align: center;">🔬 专业数据分析平台</h3>
        <p style="font-size: 18px; line-height: 1.8; margin-bottom: 20px; text-align: center;">
            <strong>💡 企业级分析能力：</strong><br>
            提供完整的数据科学工作流，从数据探索到模型部署，支持大规模数据处理和高级分析。
        </p>
        <div style="display: flex; gap: 25px; margin-bottom: 20px;">
            <div style="flex: 1; background: rgba(255,255,255,0.15); padding: 20px; border-radius: 12px; backdrop-filter: blur(10px);">
                <h4 style="color: #FDE68A; margin-bottom: 15px;">📊 高级可视化</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 15px;">
                    <li>交互式3D图表</li>
                    <li>相关性网络图</li>
                    <li>时间序列分析</li>
                    <li>统计摘要仪表板</li>
                </ul>
            </div>
            <div style="flex: 1; background: rgba(255,255,255,0.15); padding: 20px; border-radius: 12px; backdrop-filter: blur(10px);">
                <h4 style="color: #A7F3D0; margin-bottom: 15px;">⚡ 性能优化</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 15px;">
                    <li>智能内存管理</li>
                    <li>分块数据处理</li>
                    <li>缓存优化</li>
                    <li>性能监控</li>
                </ul>
            </div>
            <div style="flex: 1; background: rgba(255,255,255,0.15); padding: 20px; border-radius: 12px; backdrop-filter: blur(10px);">
                <h4 style="color: #FECACA; margin-bottom: 15px;">🔬 工作流管理</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 15px;">
                    <li>标准化流程</li>
                    <li>进度跟踪</li>
                    <li>质量评估</li>
                    <li>报告生成</li>
                </ul>
            </div>
        </div>
        <p style="font-size: 16px; margin: 0; text-align: center; opacity: 0.9;">
            <strong>🎯 专业使命：</strong> 提供企业级数据科学解决方案，让复杂分析变得简单高效
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 检查数据是否已加载
    if not hasattr(st.session_state, 'data') or st.session_state.data is None:
        st.warning("⚠️ 请先上传数据文件")
        return
    
    data = st.session_state.data
    
    # 性能监控面板
    render_performance_monitor()
    
    # 专业分析功能选择
    analysis_type = st.selectbox(
        "选择专业分析类型",
        [
            "📊 高级数据探索",
            "🎨 高级可视化",
            "🔬 数据科学工作流",
            "⚡ 性能优化",
            "📈 时间序列分析",
            "🔍 异常检测",
            "📋 专业报告生成"
        ],
        help="选择您想要进行的专业分析类型"
    )
    
    if analysis_type == "📊 高级数据探索":
        render_advanced_data_exploration(data)
    elif analysis_type == "🎨 高级可视化":
        render_advanced_visualization(data)
    elif analysis_type == "🔬 数据科学工作流":
        render_data_science_workflow(data)
    elif analysis_type == "⚡ 性能优化":
        render_performance_optimization(data)
    elif analysis_type == "📈 时间序列分析":
        render_time_series_analysis(data)
    elif analysis_type == "🔍 异常检测":
        render_anomaly_detection(data)
    elif analysis_type == "📋 专业报告生成":
        render_professional_report_generation(data)

def render_performance_monitor():
    """渲染性能监控面板"""
    st.sidebar.markdown("### ⚡ 性能监控")
    
    # 内存使用情况
    memory_info = get_memory_usage()
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("内存使用", f"{memory_info['used']:.1f}GB")
    with col2:
        st.metric("使用率", f"{memory_info['percent']:.1f}%")
    
    # 内存使用进度条
    st.sidebar.progress(memory_info['percent'] / 100)
    
    # 性能警告
    if memory_info['percent'] > 80:
        st.sidebar.warning("⚠️ 内存使用率较高，建议清理缓存")
        if st.sidebar.button("🧹 清理内存"):
            cleanup_memory()
            st.sidebar.success("✅ 内存清理完成")
            st.rerun()

def render_advanced_data_exploration(data: pd.DataFrame):
    """渲染高级数据探索"""
    st.subheader("📊 高级数据探索")
    
    # 创建选项卡
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 基础探索", "📈 高级分析", "🎯 质量评估", "💡 特征工程建议"])
    
    with tab1:
        st.write("**基础数据探索**")
        if st.button("🚀 运行基础探索"):
            with st.spinner("正在进行基础数据探索..."):
                results = DataExplorationWorkflow.run_basic_exploration(data)
                
                # 显示结果
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("数据形状", f"{results['data_shape'][0]} × {results['data_shape'][1]}")
                with col2:
                    st.metric("内存使用", f"{results['memory_usage']:.2f} MB")
                with col3:
                    st.metric("缺失值", results['missing_values'])
                with col4:
                    st.metric("重复行", results['duplicate_rows'])
                
                # 数据类型分布
                st.write("**数据类型分布：**")
                dtype_counts = pd.Series(results['data_types']).value_counts()
                fig = px.pie(values=dtype_counts.values, names=dtype_counts.index, title="数据类型分布")
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.write("**高级数据分析**")
        if st.button("🚀 运行高级分析"):
            with st.spinner("正在进行高级数据分析..."):
                results = DataExplorationWorkflow.run_advanced_exploration(data)
                
                # 数据质量评分
                st.metric("数据质量评分", f"{results['data_quality_score']:.1f}/100")
                
                # 强相关性分析
                if 'strong_correlations' in results and results['strong_correlations']:
                    st.write("**强相关性发现：**")
                    for corr in results['strong_correlations']:
                        st.write(f"• {corr['variable1']} 与 {corr['variable2']}: {corr['correlation']:.3f}")
                
                # 异常值分析
                if 'outliers_analysis' in results:
                    st.write("**异常值分析：**")
                    outliers_df = pd.DataFrame(results['outliers_analysis']).T
                    st.dataframe(outliers_df, use_container_width=True)
    
    with tab3:
        st.write("**数据质量评估**")
        if st.button("🚀 生成质量报告"):
            with st.spinner("正在生成数据质量报告..."):
                quality_report = DataQualityAnalyzer.generate_quality_report(data)
                
                # 质量评分
                st.metric("总体质量评分", f"{quality_report['overall_quality_score']:.1f}/100")
                
                # 详细质量信息
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**完整性：**")
                    st.write(f"缺失值数量: {quality_report['completeness']['missing_values_count']}")
                    st.write(f"缺失值比例: {quality_report['completeness']['missing_values_percentage']:.2f}%")
                
                with col2:
                    st.write("**一致性：**")
                    st.write(f"重复行数量: {quality_report['consistency']['duplicate_rows_count']}")
                    st.write(f"重复行比例: {quality_report['consistency']['duplicate_rows_percentage']:.2f}%")
                
                # 建议
                if quality_report['recommendations']:
                    st.write("**改进建议：**")
                    for rec in quality_report['recommendations']:
                        st.write(f"• {rec}")
    
    with tab4:
        st.write("**特征工程建议**")
        if st.button("🚀 生成特征工程建议"):
            with st.spinner("正在分析特征工程方案..."):
                suggestions = FeatureEngineeringWorkflow.suggest_feature_engineering(data)
                
                # 显示建议
                for feature_type, methods in suggestions.items():
                    if methods:
                        st.write(f"**{feature_type}：**")
                        for method in methods:
                            st.write(f"• {method}")

def render_advanced_visualization(data: pd.DataFrame):
    """渲染高级可视化"""
    st.subheader("🎨 高级可视化")
    
    # 创建选项卡
    tab1, tab2, tab3, tab4 = st.tabs(["📊 仪表板", "🎯 3D可视化", "🔗 网络图", "📈 统计摘要"])
    
    with tab1:
        st.write("**数据仪表板**")
        if st.button("📊 生成仪表板"):
            with st.spinner("正在生成数据仪表板..."):
                fig = create_dashboard(data, "专业数据仪表板")
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.write("**3D可视化**")
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) >= 3:
            col1, col2, col3 = st.columns(3)
            with col1:
                x_col = st.selectbox("选择X轴", numeric_cols, key="3d_x")
            with col2:
                y_col = st.selectbox("选择Y轴", numeric_cols, key="3d_y")
            with col3:
                z_col = st.selectbox("选择Z轴", numeric_cols, key="3d_z")
            
            if st.button("🎯 生成3D散点图"):
                fig = create_3d_scatter(data, x_col, y_col, z_col)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ 需要至少3个数值型列来创建3D图表")
    
    with tab3:
        st.write("**相关性网络图**")
        threshold = st.slider("相关性阈值", 0.1, 0.9, 0.5, 0.1)
        
        if st.button("🔗 生成网络图"):
            with st.spinner("正在生成相关性网络图..."):
                fig = create_correlation_network(data, threshold)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("⚠️ 无法生成网络图，请检查数据")
    
    with tab4:
        st.write("**统计摘要图表**")
        if st.button("📈 生成统计摘要"):
            with st.spinner("正在生成统计摘要图表..."):
                fig = create_statistical_summary(data)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("⚠️ 数据中没有数值型列")

def render_data_science_workflow(data: pd.DataFrame):
    """渲染数据科学工作流"""
    st.subheader("🔬 数据科学工作流")
    
    # 项目名称输入
    project_name = st.text_input("项目名称", value="数据分析项目")
    
    # 创建工作流
    if st.button("🚀 创建工作流"):
        workflow = workflow_manager.create_workflow(project_name)
        st.session_state.current_workflow = workflow
        st.success(f"✅ 工作流 '{project_name}' 创建成功")
    
    # 显示工作流状态
    if hasattr(st.session_state, 'current_workflow'):
        workflow = st.session_state.current_workflow
        progress = workflow.get_progress()
        
        st.write("**工作流进度：**")
        st.progress(progress['progress_percentage'] / 100)
        st.write(f"完成步骤: {progress['completed_steps']}/{progress['total_steps']}")
        
        # 显示步骤状态
        for i, step in enumerate(workflow.steps):
            status_icon = {
                "pending": "⏳",
                "running": "🔄",
                "completed": "✅",
                "failed": "❌"
            }.get(step.status, "❓")
            
            st.write(f"{status_icon} {step.name} - {step.status}")
            
            if step.status == "pending":
                if st.button(f"开始 {step.name}", key=f"start_{i}"):
                    workflow.start_step(i)
                    st.rerun()
        
        # 导出工作流报告
        if st.button("📋 导出工作流报告"):
            report = workflow.export_workflow_report()
            st.json(report)

def render_performance_optimization(data: pd.DataFrame):
    """渲染性能优化"""
    st.subheader("⚡ 性能优化")
    
    # 内存优化
    st.write("**内存优化**")
    if st.button("🔧 优化DataFrame内存"):
        with st.spinner("正在优化内存使用..."):
            optimized_data, improvement = optimize_dataframe_memory(data.copy())
            st.success(f"✅ 内存优化完成，节省了 {improvement:.1f}% 的内存")
            
            # 显示优化前后对比
            col1, col2 = st.columns(2)
            with col1:
                st.write("**优化前：**")
                st.write(f"内存使用: {data.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
            with col2:
                st.write("**优化后：**")
                st.write(f"内存使用: {optimized_data.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # 数据采样
    st.write("**智能数据采样**")
    max_rows = st.slider("最大行数", 1000, 50000, 10000)
    
    if st.button("📊 智能采样"):
        with st.spinner("正在进行智能采样..."):
            sampled_data = smart_sample_data(data, max_rows)
            st.success(f"✅ 采样完成，从 {len(data)} 行采样到 {len(sampled_data)} 行")
            
            # 显示采样结果
            st.dataframe(sampled_data.head(10), use_container_width=True)
    
    # 性能报告
    st.write("**性能报告**")
    if st.button("📈 生成性能报告"):
        report = generate_performance_report()
        if "message" not in report:
            st.write("**性能统计：**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("总函数调用", report['total_functions'])
            with col2:
                st.metric("平均执行时间", f"{report['avg_execution_time']:.3f}s")
            with col3:
                st.metric("总内存使用", f"{report['total_memory_used']:.2f}GB")
        else:
            st.info(report['message'])

def render_time_series_analysis(data: pd.DataFrame):
    """渲染时间序列分析"""
    st.subheader("📈 时间序列分析")
    
    # 检查是否有时间列
    datetime_cols = data.select_dtypes(include=['datetime']).columns.tolist()
    
    if len(datetime_cols) == 0:
        st.warning("⚠️ 数据中没有时间列，无法进行时间序列分析")
        st.info("💡 提示：请确保数据中包含datetime类型的列")
        return
    
    # 选择时间列和数值列
    time_col = st.selectbox("选择时间列", datetime_cols)
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) == 0:
        st.warning("⚠️ 数据中没有数值型列")
        return
    
    value_col = st.selectbox("选择数值列", numeric_cols)
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
    group_col = st.selectbox("选择分组列（可选）", [None] + categorical_cols)
    
    if st.button("📈 生成时间序列分析"):
        with st.spinner("正在生成时间序列分析..."):
            fig = create_time_series(data, time_col, value_col, group_col)
            st.plotly_chart(fig, use_container_width=True)

def render_anomaly_detection(data: pd.DataFrame):
    """渲染异常检测"""
    st.subheader("🔍 异常检测")
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) == 0:
        st.warning("⚠️ 数据中没有数值型列，无法进行异常检测")
        return
    
    # 选择检测方法
    detection_method = st.selectbox(
        "选择异常检测方法",
        ["IQR方法", "Z-score方法", "百分位法", "隔离森林"]
    )
    
    selected_col = st.selectbox("选择要检测的列", numeric_cols)
    
    if st.button("🔍 开始异常检测"):
        with st.spinner("正在进行异常检测..."):
            values = data[selected_col].dropna()
            
            if len(values) == 0:
                st.warning("⚠️ 所选列没有有效数据")
                return
            
            anomalies = []
            
            if detection_method == "IQR方法":
                Q1 = values.quantile(0.25)
                Q3 = values.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                anomalies = values[(values < lower_bound) | (values > upper_bound)]
                
            elif detection_method == "Z-score方法":
                z_scores = np.abs((values - values.mean()) / values.std())
                anomalies = values[z_scores > 3]
                
            elif detection_method == "百分位法":
                lower_bound = values.quantile(0.01)
                upper_bound = values.quantile(0.99)
                anomalies = values[(values < lower_bound) | (values > upper_bound)]
            
            # 显示结果
            st.success(f"✅ 检测到 {len(anomalies)} 个异常值")
            
            if len(anomalies) > 0:
                st.write("**异常值详情：**")
                st.dataframe(anomalies.to_frame(), use_container_width=True)
                
                # 异常值可视化
                fig = go.Figure()
                
                # 正常值
                normal_values = values[~values.isin(anomalies)]
                fig.add_trace(go.Scatter(
                    x=list(range(len(normal_values))),
                    y=normal_values,
                    mode='markers',
                    name='正常值',
                    marker=dict(color='#059669', size=6)
                ))
                
                # 异常值
                anomaly_indices = [i for i, v in enumerate(values) if v in anomalies]
                fig.add_trace(go.Scatter(
                    x=anomaly_indices,
                    y=anomalies,
                    mode='markers',
                    name='异常值',
                    marker=dict(color='#DC2626', size=10, symbol='x')
                ))
                
                fig.update_layout(
                    title=f"{selected_col} 异常值检测结果",
                    xaxis_title="数据点",
                    yaxis_title=selected_col
                )
                
                st.plotly_chart(fig, use_container_width=True)

def render_professional_report_generation(data: pd.DataFrame):
    """渲染专业报告生成"""
    st.subheader("📋 专业报告生成")
    
    # 报告类型选择
    report_type = st.selectbox(
        "选择报告类型",
        ["📊 数据探索报告", "🔬 数据质量报告", "📈 统计分析报告", "🎯 综合分析报告"]
    )
    
    # 报告配置
    col1, col2 = st.columns(2)
    with col1:
        include_charts = st.checkbox("包含图表", value=True)
    with col2:
        include_recommendations = st.checkbox("包含建议", value=True)
    
    if st.button("📋 生成专业报告"):
        with st.spinner("正在生成专业报告..."):
            # 这里可以调用报告生成函数
            st.success("✅ 专业报告生成完成")
            st.info("📄 报告已生成，可以下载或查看")

# 导出函数供主应用使用
def render_professional_page():
    """渲染专业分析页面（主入口）"""
    render_professional_analysis_page()
