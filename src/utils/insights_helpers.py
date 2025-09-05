"""
数据洞察辅助工具模块
提供各种数据洞察功能的辅助函数
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt


def check_tool_availability():
    """检查各种数据洞察工具的可用性"""
    tool_status = {
        "ydata_profiling": False,
        "sweetviz": False,
        "streamlit_profiling": False
    }
    
    try:
        import ydata_profiling
        tool_status["ydata_profiling"] = True
    except ImportError:
        pass
    
    try:
        import sweetviz
        tool_status["sweetviz"] = True
    except ImportError:
        pass
    
    try:
        import streamlit_pandas_profiling
        tool_status["streamlit_profiling"] = True
    except ImportError:
        pass
    
    return tool_status


def render_ydata_profiling_insights(data):
    """渲染YData Profiling洞察"""
    st.subheader("📊 YData Profiling 全面分析")
    
    try:
        import ydata_profiling
        from ydata_profiling import ProfileReport
        
        if st.button("🚀 生成YData Profiling报告"):
            with st.spinner("正在生成YData Profiling报告..."):
                try:
                    # 创建配置文件
                    profile = ProfileReport(data, title="数眸数据洞察报告", explorative=True)
                    
                    # 显示报告
                    st_profile_report(profile)
                    
                    st.success("✅ YData Profiling报告生成完成！")
                    
                except Exception as e:
                    st.error(f"❌ YData Profiling报告生成失败: {str(e)}")
    except ImportError:
        st.warning("⚠️ YData Profiling未安装，请运行: pip install ydata-profiling")
        st.info("💡 YData Profiling提供全面的数据质量评估和统计分析")


def render_sweetviz_insights(data):
    """渲染Sweetviz洞察"""
    st.subheader("🍯 Sweetviz 对比分析")
    
    try:
        import sweetviz as sv
        
        if st.button("🚀 生成Sweetviz报告"):
            with st.spinner("正在生成Sweetviz报告..."):
                try:
                    # 创建Sweetviz报告
                    report = sv.analyze(data)
                    
                    # 显示报告
                    st_sweetviz_report(report)
                    
                    st.success("✅ Sweetviz报告生成完成！")
                    
                except Exception as e:
                    st.error(f"❌ Sweetviz报告生成失败: {str(e)}")
    except ImportError:
        st.warning("⚠️ Sweetviz未安装，请运行: pip install sweetviz")
        st.info("💡 Sweetviz提供数据集对比分析和可视化")


def render_quick_insights(data):
    """渲染快速数据洞察"""
    st.subheader("⚡ 快速数据洞察")
    
    # 数据概览
    st.write("**📋 数据概览**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("行数", len(data))
    with col2:
        st.metric("列数", len(data.columns))
    with col3:
        st.metric("缺失值", data.isnull().sum().sum())
    with col4:
        st.metric("重复行", data.duplicated().sum())
    
    # 数据类型分布
    st.write("**📊 数据类型分布**")
    dtype_counts = data.dtypes.value_counts()
    fig = px.pie(values=dtype_counts.values, names=dtype_counts.index, title="数据类型分布")
    st.plotly_chart(fig, use_container_width=True)
    
    # 数值型列统计
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        st.write("**📈 数值型列统计**")
        st.dataframe(data[numeric_cols].describe(), use_container_width=True)
    
    # 缺失值分析
    missing_data = data.isnull().sum()
    if missing_data.sum() > 0:
        st.write("**🔍 缺失值分析**")
        missing_df = pd.DataFrame({
            '列名': missing_data.index,
            '缺失值数量': missing_data.values,
            '缺失比例': (missing_data.values / len(data)) * 100
        }).sort_values('缺失值数量', ascending=False)
        
        fig = px.bar(missing_df.head(10), x='列名', y='缺失值数量', 
                    title="缺失值分布（前10列）")
        st.plotly_chart(fig, use_container_width=True)


def render_data_quality_assessment(data):
    """渲染数据质量评估"""
    st.subheader("🔍 数据质量评估")
    
    # 计算数据质量评分
    quality_score = calculate_data_quality_score(data)
    
    # 显示质量评分
    col1, col2, col3 = st.columns(3)
    with col1:
        if quality_score >= 80:
            st.success(f"数据质量评分: {quality_score:.1f}/100")
        elif quality_score >= 60:
            st.warning(f"数据质量评分: {quality_score:.1f}/100")
        else:
            st.error(f"数据质量评分: {quality_score:.1f}/100")
    
    with col2:
        st.metric("缺失值比例", f"{data.isnull().sum().sum() / (len(data) * len(data.columns)) * 100:.2f}%")
    
    with col3:
        st.metric("重复值比例", f"{data.duplicated().sum() / len(data) * 100:.2f}%")
    
    # 数据质量详细分析
    st.write("**📊 数据质量详细分析**")
    
    # 完整性分析
    completeness = (1 - data.isnull().sum() / len(data)) * 100
    fig = px.bar(x=completeness.index, y=completeness.values, 
                title="数据完整性分析", labels={'x': '列名', 'y': '完整性(%)'})
    st.plotly_chart(fig, use_container_width=True)
    
    # 一致性分析
    st.write("**🔄 数据一致性分析**")
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 1:
        # 计算相关性
        corr_matrix = data[numeric_cols].corr()
        fig = px.imshow(corr_matrix, title="数值型列相关性矩阵")
        st.plotly_chart(fig, use_container_width=True)


def render_comprehensive_insights(data):
    """渲染综合数据洞察"""
    st.subheader("🎯 综合数据洞察")
    
    # 模式发现
    render_pattern_discovery(data)
    
    # 趋势分析
    render_trend_analysis(data)
    
    # 异常检测
    render_anomaly_detection(data)
    
    # 商业洞察
    render_business_insights(data)


def render_pattern_discovery(data):
    """数据模式发现"""
    st.write("**🔍 数据模式发现**")
    
    # 相关性模式发现
    st.write("**1. 相关性模式分析**")
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) >= 2:
        # 计算相关性矩阵
        corr_matrix = data[numeric_cols].corr()
        
        # 找出强相关性
        strong_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:
                    strong_corr.append({
                        'var1': corr_matrix.columns[i],
                        'var2': corr_matrix.columns[j],
                        'correlation': corr_value
                    })
        
        if strong_corr:
            st.success(f"✅ 数眸发现 {len(strong_corr)} 个强相关性模式")
            for corr in strong_corr:
                st.write(f"• {corr['var1']} 与 {corr['var2']} 的相关系数为 {corr['correlation']:.3f}")
        else:
            st.info("ℹ️ 数眸未发现强相关性模式")
        
        # 相关性热力图
        fig = px.imshow(corr_matrix, 
                       title="相关性模式热力图",
                       color_continuous_scale='RdBu_r',
                       aspect='auto')
        st.plotly_chart(fig, use_container_width=True)
    
    # 聚类模式发现
    st.write("**2. 聚类模式分析**")
    if len(numeric_cols) >= 2:
        selected_cols = st.multiselect("选择用于聚类的特征", numeric_cols, default=numeric_cols[:3])
        
        if selected_cols and len(selected_cols) >= 2:
            if st.button("🔍 数眸发现聚类模式"):
                with st.spinner("数眸正在分析聚类模式..."):
                    # 数据预处理
                    X = data[selected_cols].dropna()
                    
                    if len(X) > 0:
                        # 标准化
                        scaler = StandardScaler()
                        X_scaled = scaler.fit_transform(X)
                        
                        # 使用肘部法则确定最佳聚类数
                        inertias = []
                        K_range = range(2, min(11, len(X)//10 + 1))
                        
                        for k in K_range:
                            kmeans = KMeans(n_clusters=k, random_state=42)
                            kmeans.fit(X_scaled)
                            inertias.append(kmeans.inertia_)
                        
                        # 绘制肘部图
                        fig_elbow = px.line(x=list(K_range), y=inertias, 
                                          title="肘部法则 - 确定最佳聚类数",
                                          labels={'x': '聚类数', 'y': '惯性'})
                        st.plotly_chart(fig_elbow, use_container_width=True)
                        
                        # 执行聚类
                        optimal_k = 3  # 可以根据肘部图自动确定
                        kmeans = KMeans(n_clusters=optimal_k, random_state=42)
                        clusters = kmeans.fit_predict(X_scaled)
                        
                        # 可视化聚类结果
                        if len(selected_cols) >= 2:
                            fig_cluster = px.scatter(
                                x=X.iloc[:, 0], y=X.iloc[:, 1],
                                color=clusters,
                                title=f"聚类模式发现 ({selected_cols[0]} vs {selected_cols[1]})",
                                labels={'x': selected_cols[0], 'y': selected_cols[1], 'color': '聚类'}
                            )
                            st.plotly_chart(fig_cluster, use_container_width=True)
                        
                        st.success(f"✅ 数眸发现 {optimal_k} 个聚类模式")


def render_trend_analysis(data):
    """趋势分析"""
    st.write("**📈 趋势分析**")
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) == 0:
        st.warning("⚠️ 数据中没有数值型列，无法进行趋势分析")
        return
    
    # 选择分析列
    selected_col = st.selectbox("选择要分析的列", numeric_cols, key="trend_analysis")
    
    if selected_col:
        # 基础趋势分析
        values = data[selected_col].dropna()
        
        if len(values) > 0:
            # 计算趋势
            x = np.arange(len(values))
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, values)
            
            # 趋势判断
            if slope > 0:
                trend_direction = "上升趋势"
                trend_icon = "📈"
            elif slope < 0:
                trend_direction = "下降趋势"
                trend_icon = "📉"
            else:
                trend_direction = "无明显趋势"
                trend_icon = "➡️"
            
            # 显示趋势信息
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("趋势方向", f"{trend_icon} {trend_direction}")
            with col2:
                st.metric("趋势强度", f"{abs(slope):.4f}")
            with col3:
                st.metric("相关系数", f"{r_value:.3f}")
            with col4:
                st.metric("显著性", f"{p_value:.4f}")
            
            # 趋势可视化
            fig = go.Figure()
            
            # 原始数据
            fig.add_trace(go.Scatter(
                x=list(range(len(values))),
                y=values,
                mode='lines+markers',
                name='原始数据',
                line=dict(color='#1E40AF', width=2)
            ))
            
            # 趋势线
            trend_line = slope * np.arange(len(values)) + intercept
            fig.add_trace(go.Scatter(
                x=list(range(len(values))),
                y=trend_line,
                mode='lines',
                name='趋势线',
                line=dict(color='#DC2626', width=3, dash='dash')
            ))
            
            fig.update_layout(
                title=f"{selected_col} 趋势分析",
                xaxis_title="数据点",
                yaxis_title=selected_col,
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)


def render_anomaly_detection(data):
    """异常检测"""
    st.write("**🎯 异常检测**")
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) == 0:
        st.warning("⚠️ 数据中没有数值型列，无法进行异常检测")
        return
    
    selected_col = st.selectbox("选择要检测异常的列", numeric_cols, key="anomaly_detection")
    
    if selected_col:
        values = data[selected_col].dropna()
        
        if len(values) > 0:
            # IQR方法检测异常值
            Q1 = values.quantile(0.25)
            Q3 = values.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = values[(values < lower_bound) | (values > upper_bound)]
            
            # 显示异常值信息
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("异常值数量", len(outliers))
            with col2:
                st.metric("异常值比例", f"{len(outliers) / len(values) * 100:.2f}%")
            with col3:
                st.metric("正常值范围", f"[{lower_bound:.2f}, {upper_bound:.2f}]")
            
            # 异常值可视化
            fig = go.Figure()
            
            # 正常值
            normal_values = values[(values >= lower_bound) & (values <= upper_bound)]
            fig.add_trace(go.Scatter(
                x=list(range(len(normal_values))),
                y=normal_values,
                mode='markers',
                name='正常值',
                marker=dict(color='#1E40AF', size=6)
            ))
            
            # 异常值
            if len(outliers) > 0:
                outlier_indices = values[(values < lower_bound) | (values > upper_bound)].index
                fig.add_trace(go.Scatter(
                    x=outlier_indices,
                    y=outliers,
                    mode='markers',
                    name='异常值',
                    marker=dict(color='#DC2626', size=8, symbol='x')
                ))
            
            fig.update_layout(
                title=f"{selected_col} 异常值检测",
                xaxis_title="数据点",
                yaxis_title=selected_col,
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)


def render_business_insights(data):
    """商业洞察"""
    st.write("**💡 商业洞察**")
    
    # 数据概览洞察
    st.write("**📊 数据概览洞察**")
    
    # 数据规模洞察
    data_size = len(data)
    if data_size > 10000:
        size_insight = "大规模数据集，适合深度分析"
    elif data_size > 1000:
        size_insight = "中等规模数据集，适合常规分析"
    else:
        size_insight = "小规模数据集，适合快速分析"
    
    st.info(f"💡 数据规模洞察: {size_insight}")
    
    # 数据质量洞察
    missing_ratio = data.isnull().sum().sum() / (len(data) * len(data.columns))
    if missing_ratio < 0.05:
        quality_insight = "数据质量良好，缺失值较少"
    elif missing_ratio < 0.2:
        quality_insight = "数据质量一般，需要处理缺失值"
    else:
        quality_insight = "数据质量较差，缺失值较多，需要重点关注"
    
    st.info(f"💡 数据质量洞察: {quality_insight}")
    
    # 数据类型洞察
    numeric_count = len(data.select_dtypes(include=[np.number]).columns)
    categorical_count = len(data.select_dtypes(include=['object', 'category']).columns)
    
    if numeric_count > categorical_count:
        type_insight = "数值型数据为主，适合统计分析"
    elif categorical_count > numeric_count:
        type_insight = "分类型数据为主，适合分类分析"
    else:
        type_insight = "数据类型均衡，适合综合分析"
    
    st.info(f"💡 数据类型洞察: {type_insight}")


def calculate_data_quality_score(data):
    """计算数据质量评分"""
    score = 100
    
    # 缺失值扣分
    missing_ratio = data.isnull().sum().sum() / (len(data) * len(data.columns))
    score -= missing_ratio * 50
    
    # 重复值扣分
    duplicate_ratio = data.duplicated().sum() / len(data)
    score -= duplicate_ratio * 30
    
    # 数据类型一致性扣分
    # 这里可以添加更多质量评估标准
    
    return max(0, score)


# 兼容性函数
def st_profile_report(profile):
    """显示YData Profiling报告"""
    try:
        from streamlit_pandas_profiling import st_profile_report
        st_profile_report(profile)
    except ImportError:
        st.warning("streamlit-pandas-profiling未安装，无法显示报告")
        st.info("请运行: pip install streamlit-pandas-profiling")


def st_sweetviz_report(report):
    """显示Sweetviz报告"""
    try:
        from streamlit_sweetviz import st_sweetviz
        st_sweetviz(report)
    except ImportError:
        st.warning("streamlit-sweetviz未安装，无法显示报告")
        st.info("请运行: pip install streamlit-sweetviz")
