"""
统一的报告导出组件
可在所有模式（新手、中级、专业）中使用
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from src.utils.report_exporter import ReportExporter, get_download_link, get_download_link_bytes
from src.utils.data_processing import get_data_info

def render_report_export_section(
    data: pd.DataFrame, 
    ai_analysis: str, 
    mode: str = "专业模式",
    additional_context: Dict[str, Any] = None
):
    """
    渲染报告导出部分
    
    Args:
        data: 数据框
        ai_analysis: AI分析结果
        mode: 当前模式（新手模式、中级模式、专业模式）
        additional_context: 额外的上下文信息
    """
    if data is None or ai_analysis is None or ai_analysis.strip() == "":
        return
    
    st.markdown("---")
    st.subheader("📄 导出分析报告")
    
    # 创建报告导出器
    exporter = ReportExporter()
    
    # 准备数据信息
    try:
        data_info = get_data_info(data)
        if additional_context:
            data_info.update(additional_context)
    except Exception as e:
        st.error(f"获取数据信息失败: {str(e)}")
        return
    
    # 根据模式调整报告内容
    mode_specific_analysis = _enhance_analysis_for_mode(ai_analysis, mode, data_info)
    
    # 导出格式选择
    col1, col2 = st.columns([2, 1])
    
    with col1:
        export_format = st.selectbox(
            "选择导出格式：",
            ["Markdown (.md)", "HTML (.html)", "JSON (.json)", "PDF (.pdf)"],
            key=f"export_format_{mode}",
            help="选择适合您需求的报告格式"
        )
    
    with col2:
        st.markdown("**💡 格式说明：**")
        format_info = {
            "Markdown (.md)": "适合技术文档和GitHub",
            "HTML (.html)": "美观的网页格式",
            "JSON (.json)": "结构化数据格式", 
            "PDF (.pdf)": "专业报告格式"
        }
        st.caption(format_info.get(export_format, ""))
    
    # 生成和下载按钮
    if st.button("📥 生成并下载报告", type="primary", key=f"generate_report_{mode}"):
        with st.spinner("正在生成报告..."):
            try:
                # 根据选择的格式生成报告
                success = _generate_and_download_report(
                    exporter, export_format, data_info, mode_specific_analysis, data, mode
                )
                
                if success:
                    st.success("✅ 报告生成成功！点击上方链接下载。")
                    
                    # 显示报告统计信息
                    _show_report_stats(data_info, mode)
                
            except Exception as e:
                st.error(f"❌ 报告生成失败：{str(e)}")

def _enhance_analysis_for_mode(ai_analysis: str, mode: str, data_info: Dict[str, Any]) -> str:
    """
    根据不同模式增强AI分析内容
    
    Args:
        ai_analysis: 原始AI分析
        mode: 当前模式
        data_info: 数据信息
        
    Returns:
        str: 增强后的分析内容
    """
    mode_prefix = {
        "新手模式": """
## 🎓 新手模式分析报告

**适合人群**: 数据分析初学者
**分析特点**: 循序渐进、详细解释、实用指导

""",
        "中级模式": """
## 🔬 中级模式分析报告

**适合人群**: 科研人员和数据分析从业者
**分析特点**: 科学严谨、统计分析、研究导向

""",
        "专业模式": """
## 💼 专业模式分析报告

**适合人群**: 专业数据分析师和决策者
**分析特点**: 全面深入、商业洞察、决策支持

"""
    }
    
    enhanced_analysis = mode_prefix.get(mode, "") + ai_analysis
    
    # 添加模式特定的建议
    if mode == "新手模式":
        enhanced_analysis += """

---

## 📚 新手学习建议

### 下一步学习方向
1. **基础概念**: 深入学习描述性统计概念
2. **实践练习**: 多使用不同类型的数据集练习
3. **工具掌握**: 熟悉Excel、Python或R等分析工具
4. **统计知识**: 学习基础的统计推断方法

### 推荐资源
- 在线课程: Coursera、edX上的数据分析基础课程
- 书籍推荐: 《数据分析实战》、《统计学入门》
- 实践平台: Kaggle Learn、DataCamp
"""
    
    elif mode == "中级模式":
        enhanced_analysis += """

---

## 🔬 科研分析建议

### 统计方法选择
1. **描述性分析**: 均值、标准差、分布特征
2. **推断性分析**: t检验、方差分析、卡方检验
3. **关联性分析**: 相关分析、回归分析
4. **多变量分析**: 主成分分析、聚类分析

### 科研报告撰写
- 遵循APA或其他学科规范
- 包含详细的方法学描述
- 提供统计显著性检验结果
- 讨论研究局限性和后续研究方向
"""
    
    elif mode == "专业模式":
        enhanced_analysis += """

---

## 💼 商业价值分析

### 关键业务指标
1. **数据价值**: 评估数据资产的商业价值
2. **决策支持**: 基于数据的战略决策建议
3. **风险评估**: 识别潜在的业务风险
4. **机会识别**: 发现新的商业机会

### 行动计划建议
- 建立数据驱动的决策流程
- 投资数据基础设施建设
- 培养团队的数据分析能力
- 建立持续的数据监控机制
"""
    
    return enhanced_analysis

def _generate_and_download_report(
    exporter: ReportExporter, 
    export_format: str, 
    data_info: Dict[str, Any], 
    ai_analysis: str, 
    data: pd.DataFrame,
    mode: str
) -> bool:
    """
    生成并提供下载链接
    
    Returns:
        bool: 是否成功生成
    """
    try:
        if export_format == "Markdown (.md)":
            report_content = exporter.export_markdown_report(data_info, ai_analysis, data)
            filename = f"{mode}_数据分析报告_{exporter.timestamp}.md"
            st.markdown(
                get_download_link(report_content, filename, "text/markdown"), 
                unsafe_allow_html=True
            )
            
        elif export_format == "HTML (.html)":
            report_content = exporter.export_html_report(data_info, ai_analysis, data)
            filename = f"{mode}_数据分析报告_{exporter.timestamp}.html"
            st.markdown(
                get_download_link(report_content, filename, "text/html"), 
                unsafe_allow_html=True
            )
            
        elif export_format == "JSON (.json)":
            report_content = exporter.export_json_report(data_info, ai_analysis, data)
            filename = f"{mode}_数据分析报告_{exporter.timestamp}.json"
            st.markdown(
                get_download_link(report_content, filename, "application/json"), 
                unsafe_allow_html=True
            )
            
        elif export_format == "PDF (.pdf)":
            report_content = exporter.export_pdf_report(data_info, ai_analysis, data)
            filename = f"{mode}_数据分析报告_{exporter.timestamp}.pdf"
            st.markdown(
                get_download_link_bytes(report_content, filename, "application/pdf"), 
                unsafe_allow_html=True
            )
        
        return True
        
    except Exception as e:
        st.error(f"生成 {export_format} 格式报告失败: {str(e)}")
        return False

def _show_report_stats(data_info: Dict[str, Any], mode: str):
    """显示报告统计信息"""
    st.markdown("### 📊 报告统计信息")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("数据行数", f"{data_info.get('rows', 0):,}")
    
    with col2:
        st.metric("数据列数", data_info.get('columns', 0))
    
    with col3:
        st.metric("缺失值", data_info.get('missing_values', 0))
    
    with col4:
        quality_score = _calculate_simple_quality_score(data_info)
        st.metric("质量评分", f"{quality_score:.1f}/100")
    
    # 模式特定信息
    mode_info = {
        "新手模式": "🎓 适合学习和教育场景",
        "中级模式": "🔬 适合科研和专业分析",
        "专业模式": "💼 适合商业决策和深度分析"
    }
    
    st.info(f"**{mode}**: {mode_info.get(mode, '专业数据分析模式')}")

def _calculate_simple_quality_score(data_info: Dict[str, Any]) -> float:
    """计算简单的数据质量评分"""
    score = 100.0
    
    # 根据缺失值扣分
    total_cells = data_info.get('rows', 1) * data_info.get('columns', 1)
    missing_cells = data_info.get('missing_values', 0)
    if total_cells > 0:
        missing_ratio = missing_cells / total_cells
        score -= missing_ratio * 30
    
    # 根据重复值扣分
    duplicate_ratio = data_info.get('duplicate_rows', 0) / max(data_info.get('rows', 1), 1)
    score -= duplicate_ratio * 20
    
    return max(score, 0.0)

def show_export_success_message(mode: str):
    """显示导出成功信息"""
    st.balloons()
    st.success(f"🎉 {mode}分析报告导出成功！")
    
    st.markdown("""
    ### 📋 报告使用建议
    
    - **Markdown**: 适合上传到GitHub或技术文档
    - **HTML**: 适合在浏览器中查看或邮件分享
    - **JSON**: 适合程序读取或进一步数据处理
    - **PDF**: 适合打印或正式汇报使用
    """)
