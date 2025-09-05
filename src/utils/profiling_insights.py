"""
数据洞察模块 - 基于ydata-profiling等成熟方案
完全使用专业的数据分析工具，不自行构建分析功能
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any
import warnings
warnings.filterwarnings('ignore')

# 尝试导入专业数据分析工具
try:
    from ydata_profiling import ProfileReport
    YDATA_AVAILABLE = True
except ImportError:
    YDATA_AVAILABLE = False
    st.warning("⚠️ ydata-profiling未安装，请运行: pip install ydata-profiling")

try:
    import sweetviz as sv
    SWEETVIZ_AVAILABLE = True
except ImportError:
    SWEETVIZ_AVAILABLE = False
    st.warning("⚠️ sweetviz未安装，请运行: pip install sweetviz")

try:
    from streamlit_pandas_profiling import st_profile_report
    STREAMLIT_PROFILING_AVAILABLE = True
except ImportError:
    STREAMLIT_PROFILING_AVAILABLE = False
    st.warning("⚠️ streamlit-pandas-profiling未安装，请运行: pip install streamlit-pandas-profiling")


def render_ydata_profiling_insights(data: pd.DataFrame) -> None:
    """
    使用ydata-profiling进行专业数据洞察分析
    
    Args:
        data: 要分析的数据框
    """
    if not YDATA_AVAILABLE:
        st.error("❌ ydata-profiling不可用，请先安装该包")
        return
    
    st.subheader("📊 YData Profiling - 专业数据洞察")
    
    # 配置选项
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("报告标题", value="数眸 - 数据洞察报告")
    with col2:
        dark_mode = st.checkbox("深色主题", value=False)
    
    # 高级配置
    with st.expander("🔧 高级配置选项"):
        col1, col2, col3 = st.columns(3)
        with col1:
            correlations = st.multiselect(
                "相关性分析",
                ["pearson", "spearman", "kendall", "phi_k", "cramers"],
                default=["pearson", "spearman"]
            )
        with col2:
            missing_diagrams = st.multiselect(
                "缺失值图表",
                ["matrix", "bar", "heatmap", "dendrogram"],
                default=["matrix", "bar"]
            )
        with col3:
            samples = st.number_input("样本数量", min_value=100, max_value=10000, value=1000)
    
    # 生成报告
    if st.button("🚀 生成YData Profiling报告", type="primary"):
        with st.spinner("数眸正在生成专业数据洞察报告..."):
            try:
                # 配置ProfileReport - 修复参数
                profile = ProfileReport(
                    data,
                    title=title,
                    dark_mode=dark_mode,
                    correlations=correlations,
                    missing_diagrams=missing_diagrams,
                    samples=samples
                )
                
                # 显示报告
                st.success("✅ 数眸YData Profiling报告生成完成！")
                st_profile_report(profile)
                
                # 下载报告
                html_report = profile.to_html()
                st.download_button(
                    label="📥 下载完整报告",
                    data=html_report,
                    file_name=f"数眸_YData_洞察报告_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.html",
                    mime="text/html"
                )
                
            except Exception as e:
                st.error(f"❌ 报告生成失败：{str(e)}")


def render_sweetviz_insights(data: pd.DataFrame) -> None:
    """
    使用Sweetviz进行数据对比分析
    
    Args:
        data: 要分析的数据框
    """
    if not SWEETVIZ_AVAILABLE:
        st.error("❌ Sweetviz不可用，请先安装该包")
        return
    
    st.subheader("🍯 Sweetviz - 数据对比分析")
    
    # 分析类型选择
    analysis_type = st.selectbox(
        "选择分析类型",
        ["单数据集分析", "训练集vs测试集对比"]
    )
    
    if analysis_type == "单数据集分析":
        if st.button("🚀 生成Sweetviz单数据集分析", type="primary"):
            with st.spinner("数眸正在生成Sweetviz分析报告..."):
                try:
                    # 生成Sweetviz报告
                    report = sv.analyze(data)
                    
                    # 显示报告
                    st.success("✅ 数眸Sweetviz分析完成！")
                    report.show_html()
                    
                    # 下载报告
                    html_report = report.get_html()
                    st.download_button(
                        label="📥 下载Sweetviz报告",
                        data=html_report,
                        file_name=f"数眸_Sweetviz_分析报告_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.html",
                        mime="text/html"
                    )
                    
                except Exception as e:
                    st.error(f"❌ Sweetviz分析失败：{str(e)}")
    
    elif analysis_type == "训练集vs测试集对比":
        # 分割数据
        split_ratio = st.slider("训练集比例", 0.5, 0.9, 0.8)
        
        if st.button("🚀 生成训练集vs测试集对比", type="primary"):
            with st.spinner("数眸正在生成数据集对比分析..."):
                try:
                    # 分割数据
                    train_size = int(len(data) * split_ratio)
                    train_data = data.iloc[:train_size]
                    test_data = data.iloc[train_size:]
                    
                    # 生成对比报告 - 修复语法错误
                    report = sv.compare(train_data, test_data, target_feat=None)
                    
                    # 显示报告
                    st.success("✅ 数眸数据集对比分析完成！")
                    report.show_html()
                    
                    # 下载报告
                    html_report = report.get_html()
                    st.download_button(
                        label="📥 下载对比分析报告",
                        data=html_report,
                        file_name=f"数眸_数据集对比报告_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.html",
                        mime="text/html"
                    )
                    
                except Exception as e:
                    st.error(f"❌ 对比分析失败：{str(e)}")


def render_comprehensive_insights(data: pd.DataFrame) -> None:
    """
    综合数据洞察 - 结合多个专业工具
    
    Args:
        data: 要分析的数据框
    """
    st.subheader("🎯 综合数据洞察")
    
    # 选择要使用的工具
    tools = st.multiselect(
        "选择分析工具",
        ["YData Profiling", "Sweetviz", "基础统计"],
        default=["YData Profiling"]
    )
    
    if st.button("🚀 生成综合洞察报告", type="primary"):
        with st.spinner("数眸正在生成综合数据洞察..."):
            try:
                # 创建综合报告
                report_sections = []
                
                # 基础统计信息
                if "基础统计" in tools:
                    report_sections.append("""
                    <h2>📊 基础统计信息</h2>
                    <div class="metric">
                        <strong>数据集规模：</strong> {} 行 × {} 列<br>
                        <strong>内存使用：</strong> {:.2f} MB<br>
                        <strong>缺失值总数：</strong> {}<br>
                        <strong>重复行数：</strong> {}
                    </div>
                    """.format(
                        len(data), len(data.columns),
                        data.memory_usage(deep=True).sum() / 1024**2,
                        data.isnull().sum().sum(),
                        data.duplicated().sum()
                    ))
                
                # 生成综合HTML报告
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>数眸 - 综合数据洞察报告</title>
                    <style>
                        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; line-height: 1.6; }}
                        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }}
                        h1 {{ color: #1E40AF; text-align: center; border-bottom: 3px solid #1E40AF; padding-bottom: 20px; }}
                        h2 {{ color: #2563EB; border-bottom: 2px solid #DBEAFE; padding-bottom: 10px; margin-top: 30px; }}
                        .metric {{ background: #f8f9fa; padding: 15px; margin: 15px 0; border-radius: 10px; border-left: 4px solid #059669; }}
                        .footer {{ text-align: center; color: #6B7280; margin-top: 50px; padding-top: 20px; border-top: 2px solid #E5E7EB; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>👁️ 数眸 - 综合数据洞察报告</h1>
                        <p style="text-align: center; color: #6B7280;">让数据洞察如眸般清澈明亮</p>
                        
                        {''.join(report_sections)}
                        
                        <div class="footer">
                            <p>👁️ 数眸 - 智能数据分析平台 | 生成时间: {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                        </div>
                    </div>
                </body>
                </html>
                """
                
                # 显示报告
                st.success("✅ 数眸综合数据洞察完成！")
                st.components.v1.html(html_content, height=600, scrolling=True)
                
                # 下载报告
                st.download_button(
                    label="📥 下载综合洞察报告",
                    data=html_content,
                    file_name=f"数眸_综合洞察报告_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.html",
                    mime="text/html"
                )
                
            except Exception as e:
                st.error(f"❌ 综合洞察生成失败：{str(e)}")


def render_quick_insights(data: pd.DataFrame) -> None:
    """
    快速数据洞察 - 使用ydata-profiling的快速模式
    
    Args:
        data: 要分析的数据框
    """
    if not YDATA_AVAILABLE:
        st.error("❌ ydata-profiling不可用，请先安装该包")
        return
    
    st.subheader("⚡ 快速数据洞察")
    
    if st.button("🚀 生成快速洞察", type="primary"):
        with st.spinner("数眸正在生成快速数据洞察..."):
            try:
                # 使用ydata-profiling的快速模式
                profile = ProfileReport(
                    data,
                    title="数眸 - 快速数据洞察",
                    minimal=True  # 快速模式
                )
                
                # 显示报告
                st.success("✅ 数眸快速数据洞察完成！")
                st_profile_report(profile)
                
            except Exception as e:
                st.error(f"❌ 快速洞察生成失败：{str(e)}")


def render_data_quality_assessment(data: pd.DataFrame) -> None:
    """
    数据质量评估 - 使用ydata-profiling的质量评估功能
    
    Args:
        data: 要分析的数据框
    """
    if not YDATA_AVAILABLE:
        st.error("❌ ydata-profiling不可用，请先安装该包")
        return
    
    st.subheader("🔍 数据质量评估")
    
    if st.button("🚀 生成质量评估报告", type="primary"):
        with st.spinner("数眸正在评估数据质量..."):
            try:
                # 生成质量评估报告
                profile = ProfileReport(
                    data,
                    title="数眸 - 数据质量评估",
                    correlations=None,  # 关闭相关性分析以加快速度
                    samples=None  # 使用全部数据
                )
                
                # 显示报告
                st.success("✅ 数眸数据质量评估完成！")
                st_profile_report(profile)
                
                # 显示质量评分
                quality_score = profile.get_description()["analysis"]["data_quality"]
                st.info(f"📊 数据质量评分：{quality_score:.1f}/100")
                
            except Exception as e:
                st.error(f"❌ 质量评估失败：{str(e)}")


def check_tool_availability() -> Dict[str, bool]:
    """
    检查各种分析工具的可用性
    
    Returns:
        Dict[str, bool]: 工具可用性字典
    """
    return {
        "ydata_profiling": YDATA_AVAILABLE,
        "sweetviz": SWEETVIZ_AVAILABLE,
        "streamlit_profiling": STREAMLIT_PROFILING_AVAILABLE
    }
