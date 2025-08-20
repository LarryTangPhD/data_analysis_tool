"""
综合报告导出模块
收集所有分析结果并生成完整的分析报告
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any, List, Optional
from src.utils.report_exporter import ReportExporter, get_download_link, get_download_link_bytes
from src.utils.data_processing import get_data_info

class ComprehensiveReportExporter:
    """综合报告导出器"""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.exporter = ReportExporter()
    
    def collect_analysis_data(self, mode: str) -> Dict[str, Any]:
        """
        收集当前模式的所有分析数据
        
        Args:
            mode: 当前模式（新手模式、中级模式、专业模式）
            
        Returns:
            Dict: 包含所有分析数据的字典
        """
        analysis_data = {
            'mode': mode,
            'timestamp': self.timestamp,
            'data_info': {},
            'cleaning_results': {},
            'visualization_results': {},
            'statistical_results': {},
            'ai_analysis': {},
            'learning_progress': {}
        }
        
        # 获取数据信息
        if 'data' in st.session_state and st.session_state.data is not None:
            analysis_data['data_info'] = get_data_info(st.session_state.data)
        
        # 获取清洗结果
        if 'cleaning_results' in st.session_state:
            analysis_data['cleaning_results'] = st.session_state.cleaning_results
        
        # 获取可视化结果
        if 'visualization_results' in st.session_state:
            analysis_data['visualization_results'] = st.session_state.visualization_results
        
        # 获取统计分析结果
        if 'analysis_results' in st.session_state:
            analysis_data['statistical_results'] = st.session_state.analysis_results
        
        # 获取学习进度（新手模式）
        if 'learning_progress' in st.session_state:
            analysis_data['learning_progress'] = st.session_state.learning_progress
        
        # 获取研究数据（中级模式）
        if 'research_data' in st.session_state and st.session_state.research_data is not None:
            analysis_data['research_data_info'] = get_data_info(st.session_state.research_data)
        
        return analysis_data
    
    def generate_comprehensive_report(self, analysis_data: Dict[str, Any], format_type: str) -> str:
        """
        生成综合报告
        
        Args:
            analysis_data: 分析数据
            format_type: 报告格式
            
        Returns:
            str: 报告内容
        """
        if format_type == "Markdown (.md)":
            return self._generate_markdown_report(analysis_data)
        elif format_type == "HTML (.html)":
            return self._generate_html_report(analysis_data)
        elif format_type == "JSON (.json)":
            return self._generate_json_report(analysis_data)
        elif format_type == "PDF (.pdf)":
            return self._generate_pdf_report(analysis_data)
        else:
            raise ValueError(f"不支持的格式: {format_type}")
    
    def _generate_markdown_report(self, analysis_data: Dict[str, Any]) -> str:
        """生成Markdown格式的综合报告"""
        mode = analysis_data['mode']
        data_info = analysis_data.get('data_info', {})
        
        report = f"""# 📊 数据分析综合报告

**生成时间**: {datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")}
**报告ID**: {self.timestamp}
**分析模式**: {mode}

---

## 📋 数据概览

### 基本信息
- **数据行数**: {data_info.get('rows', 'N/A')}
- **数据列数**: {data_info.get('columns', 'N/A')}
- **内存使用**: {data_info.get('memory_usage', 'N/A'):.2f} MB
- **缺失值总数**: {data_info.get('missing_values', 'N/A')}
- **重复行数**: {data_info.get('duplicate_rows', 'N/A')}

### 数据类型分布
{self._format_data_types_summary(data_info)}

---

## 🧹 数据清洗结果

{self._format_cleaning_results(analysis_data.get('cleaning_results', {}))}

---

## 📊 可视化分析结果

{self._format_visualization_results(analysis_data.get('visualization_results', {}))}

---

## 📈 统计分析结果

{self._format_statistical_results(analysis_data.get('statistical_results', {}))}

---

## 🤖 AI分析建议

{self._format_ai_analysis(analysis_data.get('ai_analysis', {}))}

---

## 📚 学习进度（新手模式）

{self._format_learning_progress(analysis_data.get('learning_progress', {}))}

---

## 📝 分析总结

### 主要发现
{self._generate_key_findings(analysis_data)}

### 建议与下一步
{self._generate_recommendations(analysis_data)}

---

*报告由智能数据分析平台自动生成*
"""
        return report
    
    def _format_data_types_summary(self, data_info: Dict[str, Any]) -> str:
        """格式化数据类型摘要"""
        data_types = data_info.get('data_types', {})
        if not data_types:
            return "数据类型信息不可用"
        
        summary = []
        for dtype, count in data_types.items():
            summary.append(f"- {dtype}: {count}列")
        return "\n".join(summary)
    
    def _format_cleaning_results(self, cleaning_results: Dict[str, Any]) -> str:
        """格式化清洗结果"""
        if not cleaning_results:
            return "无清洗结果"
        
        summary = []
        for key, value in cleaning_results.items():
            summary.append(f"- **{key}**: {value}")
        return "\n".join(summary)
    
    def _format_visualization_results(self, viz_results: Dict[str, Any]) -> str:
        """格式化可视化结果"""
        if not viz_results:
            return "无可视化结果"
        
        summary = []
        if 'chart_types' in viz_results and viz_results['chart_types']:
            summary.append("**创建的图表类型：**")
            for chart_type in viz_results['chart_types']:
                summary.append(f"- {chart_type}")
        
        if 'insights' in viz_results and viz_results['insights']:
            summary.append("\n**数据洞察：**")
            for insight in viz_results['insights']:
                summary.append(f"- {insight}")
        
        return "\n".join(summary) if summary else "无可视化结果"
    
    def _format_statistical_results(self, stat_results: Dict[str, Any]) -> str:
        """格式化统计分析结果"""
        if not stat_results:
            return "无统计分析结果"
        
        summary = []
        for analysis_type, results in stat_results.items():
            summary.append(f"### {analysis_type.upper()} 分析")
            if isinstance(results, dict):
                for key, value in results.items():
                    summary.append(f"- **{key}**: {value}")
            else:
                summary.append(f"- {results}")
            summary.append("")
        
        return "\n".join(summary)
    
    def _format_ai_analysis(self, ai_analysis: Dict[str, Any]) -> str:
        """格式化AI分析结果"""
        if not ai_analysis:
            return "无AI分析结果"
        
        summary = []
        for key, value in ai_analysis.items():
            summary.append(f"### {key}")
            summary.append(f"{value}")
            summary.append("")
        
        return "\n".join(summary)
    
    def _format_learning_progress(self, learning_progress: Dict[str, Any]) -> str:
        """格式化学习进度"""
        if not learning_progress:
            return "无学习进度信息"
        
        summary = []
        summary.append(f"**当前步骤**: {learning_progress.get('current_step', 'N/A')}")
        summary.append(f"**已完成步骤**: {', '.join(map(str, learning_progress.get('completed_steps', [])))}")
        summary.append(f"**AI交互次数**: {learning_progress.get('ai_interactions', 0)}")
        
        return "\n".join(summary)
    
    def _generate_key_findings(self, analysis_data: Dict[str, Any]) -> str:
        """生成主要发现"""
        findings = []
        
        # 数据质量发现
        data_info = analysis_data.get('data_info', {})
        if data_info:
            missing_ratio = data_info.get('missing_values', 0) / max(data_info.get('rows', 1) * data_info.get('columns', 1), 1)
            if missing_ratio > 0.1:
                findings.append("数据存在较多缺失值，需要重点关注数据质量")
            elif missing_ratio > 0:
                findings.append("数据基本完整，只有少量缺失值")
            else:
                findings.append("数据完整性良好，无缺失值")
        
        # 统计分析发现
        stat_results = analysis_data.get('statistical_results', {})
        if stat_results:
            findings.append(f"完成了{len(stat_results)}项统计分析")
        
        # 可视化发现
        viz_results = analysis_data.get('visualization_results', {})
        if viz_results and viz_results.get('chart_types'):
            findings.append(f"创建了{len(viz_results['chart_types'])}种类型的可视化图表")
        
        return "\n".join([f"- {finding}" for finding in findings]) if findings else "暂无主要发现"
    
    def _generate_recommendations(self, analysis_data: Dict[str, Any]) -> str:
        """生成建议与下一步"""
        recommendations = []
        
        mode = analysis_data.get('mode', '')
        
        if mode == "新手模式":
            recommendations.extend([
                "继续深入学习数据分析基础概念",
                "多练习不同类型的数据集",
                "尝试使用不同的可视化方法",
                "学习基础的统计推断方法"
            ])
        elif mode == "中级模式":
            recommendations.extend([
                "进行更深入的统计建模",
                "考虑使用机器学习方法",
                "撰写学术报告或论文",
                "探索更多高级分析方法"
            ])
        elif mode == "专业模式":
            recommendations.extend([
                "基于分析结果制定商业策略",
                "建立数据驱动的决策流程",
                "考虑进行预测建模",
                "定期监控关键业务指标"
            ])
        
        return "\n".join([f"- {rec}" for rec in recommendations])
    
    def _generate_html_report(self, analysis_data: Dict[str, Any]) -> str:
        """生成HTML格式的综合报告"""
        # 简化的HTML报告
        mode = analysis_data['mode']
        data_info = analysis_data.get('data_info', {})
        
        html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>数据分析综合报告 - {self.timestamp}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; }}
        .section {{ margin: 20px 0; padding: 15px; border-left: 4px solid #007bff; background: #f8f9fa; }}
        .metric {{ display: inline-block; margin: 10px; padding: 10px; background: white; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 数据分析综合报告</h1>
        <p>生成时间: {datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")}</p>
        <p>分析模式: {mode}</p>
    </div>
    
    <div class="section">
        <h2>📋 数据概览</h2>
        <div class="metric">数据行数: {data_info.get('rows', 'N/A')}</div>
        <div class="metric">数据列数: {data_info.get('columns', 'N/A')}</div>
        <div class="metric">缺失值: {data_info.get('missing_values', 'N/A')}</div>
    </div>
    
    <div class="section">
        <h2>🧹 数据清洗结果</h2>
        {self._format_cleaning_results(analysis_data.get('cleaning_results', {}))}
    </div>
    
    <div class="section">
        <h2>📊 可视化分析结果</h2>
        {self._format_visualization_results(analysis_data.get('visualization_results', {}))}
    </div>
    
    <div class="section">
        <h2>📈 统计分析结果</h2>
        {self._format_statistical_results(analysis_data.get('statistical_results', {}))}
    </div>
    
    <div class="section">
        <h2>📝 分析总结</h2>
        <h3>主要发现</h3>
        {self._generate_key_findings(analysis_data)}
        <h3>建议与下一步</h3>
        {self._generate_recommendations(analysis_data)}
    </div>
</body>
</html>
"""
        return html_template
    
    def _generate_json_report(self, analysis_data: Dict[str, Any]) -> str:
        """生成JSON格式的综合报告"""
        import json
        
        # 处理数据类型，确保JSON可序列化
        def convert_to_serializable(obj):
            if isinstance(obj, (np.integer, np.int64)):
                return int(obj)
            elif isinstance(obj, (np.floating, np.float64)):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, pd.Series):
                return obj.tolist()
            elif hasattr(obj, 'dtype'):
                return str(obj)
            elif isinstance(obj, dict):
                return {str(k): convert_to_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_serializable(item) for item in obj]
            else:
                return obj
        
        report_data = {
            "report_info": {
                "timestamp": self.timestamp,
                "generated_at": datetime.now().isoformat(),
                "mode": analysis_data['mode'],
                "platform": "智能数据分析平台"
            },
            "data_overview": convert_to_serializable(analysis_data.get('data_info', {})),
            "cleaning_results": convert_to_serializable(analysis_data.get('cleaning_results', {})),
            "visualization_results": convert_to_serializable(analysis_data.get('visualization_results', {})),
            "statistical_results": convert_to_serializable(analysis_data.get('statistical_results', {})),
            "ai_analysis": convert_to_serializable(analysis_data.get('ai_analysis', {})),
            "learning_progress": convert_to_serializable(analysis_data.get('learning_progress', {})),
            "summary": {
                "key_findings": self._generate_key_findings(analysis_data),
                "recommendations": self._generate_recommendations(analysis_data)
            }
        }
        
        return json.dumps(report_data, ensure_ascii=False, indent=2)
    
    def _generate_pdf_report(self, analysis_data: Dict[str, Any]) -> bytes:
        """生成PDF格式的综合报告"""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib import colors
            from io import BytesIO
            
            # 创建PDF文档
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            story = []
            
            # 获取样式
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=1
            )
            
            # 标题
            story.append(Paragraph("📊 数据分析综合报告", title_style))
            story.append(Spacer(1, 20))
            
            # 基本信息
            story.append(Paragraph("📋 数据概览", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            data_info = analysis_data.get('data_info', {})
            overview_data = [
                ['指标', '数值'],
                ['数据行数', str(data_info.get('rows', 'N/A'))],
                ['数据列数', str(data_info.get('columns', 'N/A'))],
                ['内存使用', f"{data_info.get('memory_usage', 0):.2f} MB"],
                ['缺失值总数', str(data_info.get('missing_values', 'N/A'))],
                ['重复行数', str(data_info.get('duplicate_rows', 'N/A'))]
            ]
            
            overview_table = Table(overview_data)
            overview_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(overview_table)
            story.append(Spacer(1, 20))
            
            # 数据清洗结果
            story.append(Paragraph("🧹 数据清洗结果", styles['Heading2']))
            story.append(Spacer(1, 12))
            cleaning_results = analysis_data.get('cleaning_results', {})
            if cleaning_results:
                for key, value in cleaning_results.items():
                    story.append(Paragraph(f"• {key}: {value}", styles['Normal']))
            else:
                story.append(Paragraph("无清洗结果", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # 统计分析结果
            story.append(Paragraph("📈 统计分析结果", styles['Heading2']))
            story.append(Spacer(1, 12))
            statistical_results = analysis_data.get('statistical_results', {})
            if statistical_results:
                for analysis_type, results in statistical_results.items():
                    story.append(Paragraph(f"**{analysis_type}分析**:", styles['Heading3']))
                    if isinstance(results, dict):
                        for key, value in results.items():
                            story.append(Paragraph(f"  - {key}: {value}", styles['Normal']))
                    else:
                        story.append(Paragraph(f"  {results}", styles['Normal']))
            else:
                story.append(Paragraph("无统计分析结果", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # 分析总结
            story.append(Paragraph("📝 分析总结", styles['Heading2']))
            story.append(Spacer(1, 12))
            story.append(Paragraph("主要发现:", styles['Heading3']))
            story.append(Paragraph(self._generate_key_findings(analysis_data), styles['Normal']))
            story.append(Spacer(1, 12))
            story.append(Paragraph("建议与下一步:", styles['Heading3']))
            story.append(Paragraph(self._generate_recommendations(analysis_data), styles['Normal']))
            
            # 生成PDF
            doc.build(story)
            buffer.seek(0)
            return buffer.getvalue()
            
        except ImportError:
            raise ImportError("PDF导出需要安装reportlab库: pip install reportlab")

def render_comprehensive_report_export(mode: str):
    """
    渲染综合报告导出界面
    
    Args:
        mode: 当前模式
    """
    st.markdown("---")
    st.subheader("📄 导出完整分析报告")
    
    # 创建综合报告导出器
    exporter = ComprehensiveReportExporter()
    
    # 收集分析数据
    try:
        analysis_data = exporter.collect_analysis_data(mode)
        st.success("✅ 分析数据收集完成")
    except Exception as e:
        st.error(f"❌ 数据收集失败: {str(e)}")
        return
    
    # 导出格式选择
    col1, col2 = st.columns([2, 1])
    
    with col1:
        export_format = st.selectbox(
            "选择导出格式：",
            ["Markdown (.md)", "HTML (.html)", "JSON (.json)", "PDF (.pdf)"],
            key=f"comprehensive_export_format_{mode}",
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
    
    # 显示报告预览
    with st.expander("👀 预览报告内容"):
        st.markdown("### 📋 报告将包含以下内容：")
        
        # 数据概览
        if analysis_data.get('data_info'):
            st.markdown("✅ **数据概览** - 数据基本信息、质量评估")
        
        # 清洗结果
        if analysis_data.get('cleaning_results'):
            st.markdown("✅ **数据清洗结果** - 清洗操作和处理效果")
        
        # 可视化结果
        if analysis_data.get('visualization_results'):
            st.markdown("✅ **可视化分析** - 图表类型和数据洞察")
        
        # 统计分析
        if analysis_data.get('statistical_results'):
            st.markdown("✅ **统计分析** - 描述性统计、相关性分析等")
        
        # AI分析
        if analysis_data.get('ai_analysis'):
            st.markdown("✅ **AI分析建议** - 智能分析结果")
        
        # 学习进度
        if analysis_data.get('learning_progress'):
            st.markdown("✅ **学习进度** - 学习步骤和进度跟踪")
    
    # 生成和下载按钮
    if st.button("📥 生成并下载完整报告", type="primary", key=f"generate_comprehensive_report_{mode}"):
        with st.spinner("正在生成完整分析报告..."):
            try:
                # 生成报告
                report_content = exporter.generate_comprehensive_report(analysis_data, export_format)
                
                # 提供下载链接
                if export_format == "Markdown (.md)":
                    filename = f"{mode}_完整分析报告_{exporter.timestamp}.md"
                    st.markdown(
                        get_download_link(report_content, filename, "text/markdown"), 
                        unsafe_allow_html=True
                    )
                elif export_format == "HTML (.html)":
                    filename = f"{mode}_完整分析报告_{exporter.timestamp}.html"
                    st.markdown(
                        get_download_link(report_content, filename, "text/html"), 
                        unsafe_allow_html=True
                    )
                elif export_format == "JSON (.json)":
                    filename = f"{mode}_完整分析报告_{exporter.timestamp}.json"
                    st.markdown(
                        get_download_link(report_content, filename, "application/json"), 
                        unsafe_allow_html=True
                    )
                elif export_format == "PDF (.pdf)":
                    filename = f"{mode}_完整分析报告_{exporter.timestamp}.pdf"
                    st.markdown(
                        get_download_link_bytes(report_content, filename, "application/pdf"), 
                        unsafe_allow_html=True
                    )
                
                st.success("✅ 完整分析报告生成成功！点击上方链接下载。")
                
                # 显示报告统计信息
                st.markdown("### 📊 报告统计信息")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("数据行数", f"{analysis_data.get('data_info', {}).get('rows', 0):,}")
                
                with col2:
                    st.metric("数据列数", analysis_data.get('data_info', {}).get('columns', 0))
                
                with col3:
                    st.metric("分析项目", len(analysis_data.get('statistical_results', {})))
                
                with col4:
                    st.metric("图表数量", len(analysis_data.get('visualization_results', {}).get('chart_types', [])))
                
            except Exception as e:
                st.error(f"❌ 报告生成失败：{str(e)}")
                if "reportlab" in str(e).lower():
                    st.info("💡 PDF导出需要安装reportlab库: pip install reportlab")
