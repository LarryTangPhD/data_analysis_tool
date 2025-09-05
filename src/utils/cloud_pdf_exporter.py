"""
云平台PDF导出器
专门处理Streamlit云平台等环境的PDF导出功能
"""

import os
import json
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any, List, Optional
from io import BytesIO
import base64

class CloudPDFExporter:
    """云平台PDF导出器"""
    
    def __init__(self):
        """初始化云平台PDF导出器"""
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def export_pdf_report(self, data_info: Dict[str, Any], ai_analysis: str, 
                         data_preview: pd.DataFrame, charts_data: List[Dict] = None) -> bytes:
        """
        导出PDF格式的分析报告 - 云平台兼容版本
        
        Args:
            data_info: 数据基本信息
            ai_analysis: AI分析结果
            data_preview: 数据预览
            charts_data: 图表数据
            
        Returns:
            bytes: PDF文件内容
        """
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib import colors
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            from reportlab.pdfbase.cidfonts import UnicodeCIDFont
            
            # 创建PDF文档
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            story = []
            
            # 尝试注册字体
            font_name = self._register_font_for_cloud()
            
            # 获取样式
            styles = self._create_styles_for_cloud(font_name)
            
            # 标题
            story.append(Paragraph(self._clean_text("数据分析报告"), styles['title']))
            story.append(Spacer(1, 20))
            
            # 基本信息
            story.append(Paragraph(self._clean_text("数据概览"), styles['heading2']))
            story.append(Spacer(1, 12))
            
            # 创建数据概览表格
            overview_data = [
                [self._clean_text('指标'), self._clean_text('数值')],
                [self._clean_text('数据行数'), str(data_info.get('rows', 'N/A'))],
                [self._clean_text('数据列数'), str(data_info.get('columns', 'N/A'))],
                [self._clean_text('内存使用'), f"{data_info.get('memory_usage', 0):.2f} MB"],
                [self._clean_text('缺失值总数'), str(data_info.get('missing_values', 'N/A'))],
                [self._clean_text('重复行数'), str(data_info.get('duplicate_rows', 'N/A'))]
            ]
            
            overview_table = Table(overview_data)
            overview_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), font_name),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(overview_table)
            story.append(Spacer(1, 20))
            
            # AI分析结果
            story.append(Paragraph(self._clean_text("AI智能分析"), styles['heading2']))
            story.append(Spacer(1, 12))
            
            # 处理AI分析文本，分段显示
            ai_analysis_clean = self._clean_text(ai_analysis)
            if ai_analysis_clean:
                # 按段落分割
                paragraphs = ai_analysis_clean.split('\n\n')
                for para in paragraphs:
                    if para.strip():
                        story.append(Paragraph(para.strip(), styles['normal']))
                        story.append(Spacer(1, 6))
            else:
                story.append(Paragraph("无AI分析结果", styles['normal']))
            story.append(Spacer(1, 20))
            
            # 数据质量评估
            story.append(Paragraph(self._clean_text("数据质量评估"), styles['heading2']))
            story.append(Spacer(1, 12))
            
            quality_score = self._calculate_data_quality_score(data_info)
            story.append(Paragraph(self._clean_text(f"综合评分: {quality_score:.1f}/100"), styles['heading3']))
            story.append(Paragraph(self._clean_text(f"质量评估: {self._get_quality_assessment(data_info)}"), styles['normal']))
            story.append(Spacer(1, 20))
            
            # 建议
            story.append(Paragraph(self._clean_text("建议与下一步"), styles['heading2']))
            story.append(Spacer(1, 12))
            
            story.append(Paragraph(self._clean_text("数据清洗建议:"), styles['heading3']))
            story.append(Paragraph(self._clean_text("• 处理缺失值"), styles['normal']))
            story.append(Paragraph(self._clean_text("• 检查异常值"), styles['normal']))
            story.append(Paragraph(self._clean_text("• 数据类型转换"), styles['normal']))
            story.append(Spacer(1, 12))
            
            story.append(Paragraph(self._clean_text("分析方向建议:"), styles['heading3']))
            story.append(Paragraph(self._clean_text("• 探索性数据分析"), styles['normal']))
            story.append(Paragraph(self._clean_text("• 可视化分析"), styles['normal']))
            story.append(Paragraph(self._clean_text("• 统计建模"), styles['normal']))
            
            # 生成PDF
            doc.build(story)
            buffer.seek(0)
            return buffer.getvalue()
            
        except ImportError:
            raise ImportError("PDF导出需要安装reportlab库: pip install reportlab")
        except Exception as e:
            raise Exception(f"PDF生成失败: {str(e)}")
    
    def _register_font_for_cloud(self) -> str:
        """为云平台注册字体"""
        try:
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.cidfonts import UnicodeCIDFont
            
            # 尝试注册reportlab内置的中文字体
            builtin_fonts = [
                'STSong-Light',      # 华文宋体
                'STSongStd-Light',   # 华文宋体标准版
                'HeiseiMin-W3',      # 平成明朝
                'HeiseiKakuGo-W5',   # 平成角ゴシック
                'HYSong',            # 华文宋体
                'HYGothic-Medium',   # 华文黑体
            ]
            
            for font_name in builtin_fonts:
                try:
                    pdfmetrics.registerFont(UnicodeCIDFont(font_name))
                    print(f"云平台成功注册字体: {font_name}")
                    return font_name
                except Exception as e:
                    print(f"字体 {font_name} 注册失败: {e}")
                    continue
            
            # 如果都失败，使用默认字体
            print("云平台字体注册失败，使用默认字体")
            return 'Helvetica'
            
        except Exception as e:
            print(f"云平台字体注册失败: {e}")
            return 'Helvetica'
    
    def _create_styles_for_cloud(self, font_name: str):
        """为云平台创建样式"""
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        
        styles = getSampleStyleSheet()
        
        # 创建样式
        title_style = ParagraphStyle(
            'CloudTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1,  # 居中
            fontName=font_name,
            leading=28
        )
        
        heading2_style = ParagraphStyle(
            'CloudHeading2',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            fontName=font_name,
            leading=18
        )
        
        heading3_style = ParagraphStyle(
            'CloudHeading3',
            parent=styles['Heading3'],
            fontSize=14,
            spaceAfter=8,
            fontName=font_name,
            leading=16
        )
        
        normal_style = ParagraphStyle(
            'CloudNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            fontName=font_name,
            leading=12
        )
        
        return {
            'title': title_style,
            'heading2': heading2_style,
            'heading3': heading3_style,
            'normal': normal_style
        }
    
    def _clean_text(self, text: str) -> str:
        """清理文本，移除或替换emoji字符"""
        if not text:
            return ""
        
        import re
        # 移除emoji字符，保留中文、英文、数字和常用符号
        text = re.sub(r'[^\u0020-\u007E\u00A0-\u00FF\u0100-\u017F\u0180-\u024F\u1E00-\u1EFF\u2C60-\u2C7F\uA720-\uA7FF\u2000-\u206F\u3000-\u303F\uFF00-\uFFEF\u4E00-\u9FFF]', '', text)
        return text
    
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
