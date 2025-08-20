"""
分析报告导出模块
支持多种格式的报告导出功能
"""

import os
import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from typing import Dict, Any, List, Optional
import streamlit as st
from io import BytesIO
import base64

class ReportExporter:
    """分析报告导出器"""
    
    def __init__(self):
        """初始化报告导出器"""
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def export_markdown_report(self, data_info: Dict[str, Any], ai_analysis: str, 
                             data_preview: pd.DataFrame, charts_data: List[Dict] = None) -> str:
        """
        导出Markdown格式的分析报告
        
        Args:
            data_info: 数据基本信息
            ai_analysis: AI分析结果
            data_preview: 数据预览
            charts_data: 图表数据
            
        Returns:
            str: Markdown格式的报告内容
        """
        report = f"""# 📊 数据分析报告

**生成时间**: {datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")}
**报告ID**: {self.timestamp}

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

## 🤖 AI智能分析

{ai_analysis}

---

## 📈 数据预览

### 前5行数据
```
{data_preview.head().to_string()}
```

### 数据统计信息
```
{data_preview.describe().to_string()}
```

---

## 📊 数据质量评估

### 缺失值分析
{self._format_missing_values_summary(data_info)}

### 数据完整性评分
**综合评分**: {self._calculate_data_quality_score(data_info):.1f}/100

---

## 🔍 关键发现

1. **数据规模**: 这是一个包含{data_info.get('rows', 'N/A')}行{data_info.get('columns', 'N/A')}列的数据集
2. **数据质量**: {self._get_quality_assessment(data_info)}
3. **主要特征**: {self._get_main_features(data_info)}

---

## 📝 建议与下一步

### 数据清洗建议
- 处理缺失值
- 检查异常值
- 数据类型转换

### 分析方向建议
- 探索性数据分析
- 可视化分析
- 统计建模

---

*报告由智能数据分析平台自动生成*
"""
        return report
    
    def export_html_report(self, data_info: Dict[str, Any], ai_analysis: str, 
                          data_preview: pd.DataFrame, charts_data: List[Dict] = None) -> str:
        """
        导出HTML格式的分析报告
        
        Args:
            data_info: 数据基本信息
            ai_analysis: AI分析结果
            data_preview: 数据预览
            charts_data: 图表数据
            
        Returns:
            str: HTML格式的报告内容
        """
        html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>数据分析报告 - {self.timestamp}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid #667eea;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #2c3e50;
            margin: 0;
            font-size: 2.5em;
        }}
        .meta-info {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        .section {{
            margin-bottom: 30px;
            padding: 20px;
            border-left: 4px solid #667eea;
            background: #f8f9fa;
        }}
        .section h2 {{
            color: #2c3e50;
            margin-top: 0;
        }}
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        .data-table th, .data-table td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        .data-table th {{
            background-color: #667eea;
            color: white;
        }}
        .data-table tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        .quality-score {{
            font-size: 1.2em;
            font-weight: bold;
            color: #27ae60;
        }}
        .ai-analysis {{
            background: #e8f4fd;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 数据分析报告</h1>
            <p>智能数据分析平台自动生成</p>
        </div>
        
        <div class="meta-info">
            <strong>生成时间:</strong> {datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")}<br>
            <strong>报告ID:</strong> {self.timestamp}
        </div>
        
        <div class="section">
            <h2>📋 数据概览</h2>
            <table class="data-table">
                <tr>
                    <th>指标</th>
                    <th>数值</th>
                </tr>
                <tr>
                    <td>数据行数</td>
                    <td>{data_info.get('rows', 'N/A')}</td>
                </tr>
                <tr>
                    <td>数据列数</td>
                    <td>{data_info.get('columns', 'N/A')}</td>
                </tr>
                <tr>
                    <td>内存使用</td>
                    <td>{data_info.get('memory_usage', 'N/A'):.2f} MB</td>
                </tr>
                <tr>
                    <td>缺失值总数</td>
                    <td>{data_info.get('missing_values', 'N/A')}</td>
                </tr>
                <tr>
                    <td>重复行数</td>
                    <td>{data_info.get('duplicate_rows', 'N/A')}</td>
                </tr>
            </table>
        </div>
        
        <div class="section">
            <h2>🤖 AI智能分析</h2>
            <div class="ai-analysis">
                {ai_analysis.replace(chr(10), '<br>')}
            </div>
        </div>
        
        <div class="section">
            <h2>📈 数据预览</h2>
            <h3>前5行数据</h3>
            {data_preview.head().to_html(classes='data-table')}
            
            <h3>数据统计信息</h3>
            {data_preview.describe().to_html(classes='data-table')}
        </div>
        
        <div class="section">
            <h2>📊 数据质量评估</h2>
            <p class="quality-score">综合评分: {self._calculate_data_quality_score(data_info):.1f}/100</p>
            <p><strong>数据质量评估:</strong> {self._get_quality_assessment(data_info)}</p>
        </div>
        
        <div class="section">
            <h2>🔍 关键发现</h2>
            <ul>
                <li><strong>数据规模:</strong> 这是一个包含{data_info.get('rows', 'N/A')}行{data_info.get('columns', 'N/A')}列的数据集</li>
                <li><strong>数据质量:</strong> {self._get_quality_assessment(data_info)}</li>
                <li><strong>主要特征:</strong> {self._get_main_features(data_info)}</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>📝 建议与下一步</h2>
            <h3>数据清洗建议</h3>
            <ul>
                <li>处理缺失值</li>
                <li>检查异常值</li>
                <li>数据类型转换</li>
            </ul>
            
            <h3>分析方向建议</h3>
            <ul>
                <li>探索性数据分析</li>
                <li>可视化分析</li>
                <li>统计建模</li>
            </ul>
        </div>
        
        <div class="footer">
            <p>报告由智能数据分析平台自动生成 | {datetime.now().strftime("%Y年%m月%d日")}</p>
        </div>
    </div>
</body>
</html>
"""
        return html_template
    
    def export_json_report(self, data_info: Dict[str, Any], ai_analysis: str, 
                          data_preview: pd.DataFrame, charts_data: List[Dict] = None) -> str:
        """
        导出JSON格式的分析报告
        
        Args:
            data_info: 数据基本信息
            ai_analysis: AI分析结果
            data_preview: 数据预览
            charts_data: 图表数据
            
        Returns:
            str: JSON格式的报告内容
        """
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
            elif hasattr(obj, 'dtype'):  # 处理pandas数据类型
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
                "platform": "智能数据分析平台"
            },
            "data_overview": {
                "rows": convert_to_serializable(data_info.get('rows')),
                "columns": convert_to_serializable(data_info.get('columns')),
                "memory_usage_mb": convert_to_serializable(data_info.get('memory_usage')),
                "missing_values": convert_to_serializable(data_info.get('missing_values')),
                "duplicate_rows": convert_to_serializable(data_info.get('duplicate_rows')),
                "data_types": convert_to_serializable(self._get_data_types_dict(data_info)),
                "quality_score": convert_to_serializable(self._calculate_data_quality_score(data_info))
            },
            "ai_analysis": ai_analysis,
            "data_preview": {
                "head": convert_to_serializable(data_preview.head().to_dict('records')),
                "describe": convert_to_serializable(data_preview.describe().to_dict()),
                "dtypes": {str(k): str(v) for k, v in data_preview.dtypes.to_dict().items()}
            },
            "quality_assessment": {
                "score": convert_to_serializable(self._calculate_data_quality_score(data_info)),
                "assessment": self._get_quality_assessment(data_info),
                "main_features": self._get_main_features(data_info)
            },
            "recommendations": {
                "data_cleaning": [
                    "处理缺失值",
                    "检查异常值", 
                    "数据类型转换"
                ],
                "analysis_directions": [
                    "探索性数据分析",
                    "可视化分析",
                    "统计建模"
                ]
            }
        }
        
        return json.dumps(report_data, ensure_ascii=False, indent=2)
    
    def export_pdf_report(self, data_info: Dict[str, Any], ai_analysis: str, 
                         data_preview: pd.DataFrame, charts_data: List[Dict] = None) -> bytes:
        """
        导出PDF格式的分析报告
        
        Args:
            data_info: 数据基本信息
            ai_analysis: AI分析结果
            data_preview: 数据预览
            charts_data: 图表数据
            
        Returns:
            bytes: PDF文件内容
        """
        try:
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib import colors
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            
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
                alignment=1  # 居中
            )
            
            # 标题
            story.append(Paragraph("📊 数据分析报告", title_style))
            story.append(Spacer(1, 20))
            
            # 基本信息
            story.append(Paragraph("📋 数据概览", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            # 创建数据概览表格
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
            
            # AI分析结果
            story.append(Paragraph("🤖 AI智能分析", styles['Heading2']))
            story.append(Spacer(1, 12))
            story.append(Paragraph(ai_analysis, styles['Normal']))
            story.append(Spacer(1, 20))
            
            # 数据质量评估
            story.append(Paragraph("📊 数据质量评估", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            quality_score = self._calculate_data_quality_score(data_info)
            story.append(Paragraph(f"综合评分: {quality_score:.1f}/100", styles['Heading3']))
            story.append(Paragraph(f"质量评估: {self._get_quality_assessment(data_info)}", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # 建议
            story.append(Paragraph("📝 建议与下一步", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            story.append(Paragraph("数据清洗建议:", styles['Heading3']))
            story.append(Paragraph("• 处理缺失值", styles['Normal']))
            story.append(Paragraph("• 检查异常值", styles['Normal']))
            story.append(Paragraph("• 数据类型转换", styles['Normal']))
            story.append(Spacer(1, 12))
            
            story.append(Paragraph("分析方向建议:", styles['Heading3']))
            story.append(Paragraph("• 探索性数据分析", styles['Normal']))
            story.append(Paragraph("• 可视化分析", styles['Normal']))
            story.append(Paragraph("• 统计建模", styles['Normal']))
            
            # 生成PDF
            doc.build(story)
            buffer.seek(0)
            return buffer.getvalue()
            
        except ImportError:
            raise ImportError("PDF导出需要安装reportlab库: pip install reportlab")
    
    def _format_data_types_summary(self, data_info: Dict[str, Any]) -> str:
        """格式化数据类型摘要"""
        data_types = data_info.get('data_types', {})
        if not data_types:
            return "数据类型信息不可用"
        
        summary = []
        for dtype, count in data_types.items():
            summary.append(f"- {dtype}: {count}列")
        return "\n".join(summary)
    
    def _format_missing_values_summary(self, data_info: Dict[str, Any]) -> str:
        """格式化缺失值摘要"""
        missing_info = data_info.get('missing_values_summary', {})
        if not missing_info:
            return "缺失值信息不可用"
        
        summary = []
        for col, count in missing_info.items():
            if count > 0:
                summary.append(f"- {col}: {count}个缺失值")
        
        if not summary:
            return "数据中没有缺失值"
        
        return "\n".join(summary)
    
    def _calculate_data_quality_score(self, data_info: Dict[str, Any]) -> float:
        """计算数据质量评分"""
        score = 100.0
        
        # 根据缺失值扣分
        total_cells = data_info.get('rows', 1) * data_info.get('columns', 1)
        missing_cells = data_info.get('missing_values', 0)
        if total_cells > 0:
            missing_ratio = missing_cells / total_cells
            score -= missing_ratio * 30  # 缺失值最多扣30分
        
        # 根据重复值扣分
        duplicate_ratio = data_info.get('duplicate_rows', 0) / max(data_info.get('rows', 1), 1)
        score -= duplicate_ratio * 20  # 重复值最多扣20分
        
        return max(score, 0.0)
    
    def _get_quality_assessment(self, data_info: Dict[str, Any]) -> str:
        """获取质量评估描述"""
        score = self._calculate_data_quality_score(data_info)
        
        if score >= 90:
            return "优秀 - 数据质量很高，适合直接进行分析"
        elif score >= 80:
            return "良好 - 数据质量较好，建议进行少量清洗"
        elif score >= 70:
            return "一般 - 数据质量中等，需要适当的数据清洗"
        elif score >= 60:
            return "较差 - 数据质量较低，需要大量清洗工作"
        else:
            return "很差 - 数据质量很差，建议重新收集数据"
    
    def _get_main_features(self, data_info: Dict[str, Any]) -> str:
        """获取主要特征描述"""
        features = []
        
        if data_info.get('rows', 0) > 10000:
            features.append("大规模数据集")
        elif data_info.get('rows', 0) > 1000:
            features.append("中等规模数据集")
        else:
            features.append("小规模数据集")
        
        if data_info.get('columns', 0) > 20:
            features.append("高维特征")
        elif data_info.get('columns', 0) > 10:
            features.append("中等维度特征")
        else:
            features.append("低维特征")
        
        if data_info.get('missing_values', 0) > 0:
            features.append("包含缺失值")
        
        if data_info.get('duplicate_rows', 0) > 0:
            features.append("包含重复数据")
        
        return "、".join(features) if features else "标准数据集"
    
    def _get_data_types_dict(self, data_info: Dict[str, Any]) -> Dict[str, int]:
        """获取数据类型字典"""
        return data_info.get('data_types', {})

def get_download_link(content: str, filename: str, file_type: str = "text/plain") -> str:
    """
    生成下载链接
    
    Args:
        content: 文件内容
        filename: 文件名
        file_type: 文件类型
        
    Returns:
        str: 下载链接HTML
    """
    b64 = base64.b64encode(content.encode()).decode()
    return f'<a href="data:{file_type};base64,{b64}" download="{filename}">📥 下载 {filename}</a>'

def get_download_link_bytes(content: bytes, filename: str, file_type: str = "application/octet-stream") -> str:
    """
    生成二进制文件下载链接
    
    Args:
        content: 文件内容（字节）
        filename: 文件名
        file_type: 文件类型
        
    Returns:
        str: 下载链接HTML
    """
    b64 = base64.b64encode(content).decode()
    return f'<a href="data:{file_type};base64,{b64}" download="{filename}">📥 下载 {filename}</a>'
