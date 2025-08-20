"""
字体配置文件
用于管理PDF导出功能的中文字体设置
支持本地环境和云平台部署
"""

import platform
import os
from typing import Optional, List

class FontConfig:
    """字体配置管理类"""
    
    @staticmethod
    def get_system_font_paths() -> List[str]:
        """获取系统字体路径列表"""
        system = platform.system()
        
        if system == "Windows":
            return [
                "C:/Windows/Fonts/simsun.ttc",      # 宋体
                "C:/Windows/Fonts/simhei.ttf",      # 黑体
                "C:/Windows/Fonts/msyh.ttc",        # 微软雅黑
                "C:/Windows/Fonts/simkai.ttf",      # 楷体
                "C:/Windows/Fonts/simfang.ttf",     # 仿宋
            ]
        elif system == "Darwin":  # macOS
            return [
                "/System/Library/Fonts/PingFang.ttc",           # 苹方
                "/System/Library/Fonts/STHeiti Light.ttc",      # 华文黑体
                "/System/Library/Fonts/Arial Unicode MS.ttf",   # Arial Unicode
                "/System/Library/Fonts/STSong.ttc",             # 华文宋体
                "/System/Library/Fonts/STKaiti.ttc",            # 华文楷体
            ]
        else:  # Linux (包括云平台)
            return [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
                "/usr/share/fonts/truetype/arphic/uming.ttc",
                "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            ]
    
    @staticmethod
    def find_available_font() -> Optional[str]:
        """查找可用的中文字体"""
        font_paths = FontConfig.get_system_font_paths()
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                return font_path
        
        return None
    
    @staticmethod
    def register_chinese_font():
        """注册中文字体 - 云平台兼容版本"""
        try:
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            from reportlab.pdfbase.cidfonts import UnicodeCIDFont
            
            # 首先尝试注册系统中文字体
            font_path = FontConfig.find_available_font()
            
            if font_path:
                try:
                    pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                    print(f"成功注册系统字体: {font_path}")
                    return 'ChineseFont'
                except Exception as e:
                    print(f"TTF字体注册失败: {e}")
            
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
                    print(f"成功注册内置字体: {font_name}")
                    return font_name
                except Exception as e:
                    print(f"内置字体 {font_name} 注册失败: {e}")
                    continue
            
            # 如果都失败，使用默认字体
            print("所有中文字体注册失败，使用默认字体")
            return 'Helvetica'
            
        except ImportError:
            print("reportlab库未安装，无法注册字体")
            return 'Helvetica'
        except Exception as e:
            print(f"字体注册失败: {e}")
            return 'Helvetica'
    
    @staticmethod
    def clean_text_for_pdf(text: str) -> str:
        """清理文本，移除或替换emoji字符"""
        if not text:
            return ""
        
        import re
        # 移除emoji字符，保留中文、英文、数字和常用符号
        # 保留的Unicode范围：
        # \u0020-\u007E: 基本拉丁字符
        # \u00A0-\u00FF: 拉丁补充字符
        # \u0100-\u017F: 拉丁扩展A
        # \u0180-\u024F: 拉丁扩展B
        # \u1E00-\u1EFF: 拉丁扩展附加
        # \u2C60-\u2C7F: 拉丁扩展C
        # \uA720-\uA7FF: 拉丁扩展D
        # \u2000-\u206F: 常用标点
        # \u3000-\u303F: 中文标点
        # \uFF00-\uFFEF: 全角字符
        # \u4E00-\u9FFF: 中文汉字
        text = re.sub(r'[^\u0020-\u007E\u00A0-\u00FF\u0100-\u017F\u0180-\u024F\u1E00-\u1EFF\u2C60-\u2C7F\uA720-\uA7FF\u2000-\u206F\u3000-\u303F\uFF00-\uFFEF\u4E00-\u9FFF]', '', text)
        return text
    
    @staticmethod
    def create_chinese_styles(chinese_font_name: str):
        """创建支持中文的样式"""
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        
        styles = getSampleStyleSheet()
        
        # 创建支持中文的样式
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1,  # 居中
            fontName=chinese_font_name,
            leading=28
        )
        
        heading2_style = ParagraphStyle(
            'CustomHeading2',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            fontName=chinese_font_name,
            leading=18
        )
        
        heading3_style = ParagraphStyle(
            'CustomHeading3',
            parent=styles['Heading3'],
            fontSize=14,
            spaceAfter=8,
            fontName=chinese_font_name,
            leading=16
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            fontName=chinese_font_name,
            leading=12
        )
        
        return {
            'title': title_style,
            'heading2': heading2_style,
            'heading3': heading3_style,
            'normal': normal_style
        }
    
    @staticmethod
    def create_fallback_styles():
        """创建备用样式（当无法使用中文字体时）"""
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        
        styles = getSampleStyleSheet()
        
        # 使用默认字体创建样式
        title_style = ParagraphStyle(
            'FallbackTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1,  # 居中
            fontName='Helvetica',
            leading=28
        )
        
        heading2_style = ParagraphStyle(
            'FallbackHeading2',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            fontName='Helvetica',
            leading=18
        )
        
        heading3_style = ParagraphStyle(
            'FallbackHeading3',
            parent=styles['Heading3'],
            fontSize=14,
            spaceAfter=8,
            fontName='Helvetica',
            leading=16
        )
        
        normal_style = ParagraphStyle(
            'FallbackNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            fontName='Helvetica',
            leading=12
        )
        
        return {
            'title': title_style,
            'heading2': heading2_style,
            'heading3': heading3_style,
            'normal': normal_style
        }
