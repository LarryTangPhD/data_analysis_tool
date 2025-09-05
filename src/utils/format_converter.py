"""
文件格式转换模块
提供多种格式间的相互转换功能
"""

import pandas as pd
import numpy as np
import json
import streamlit as st
from typing import Dict, Any, List, Optional, Tuple
import io
import base64
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FormatConverter:
    """文件格式转换器"""
    
    def __init__(self):
        self.supported_formats = {
            'input': ['json', 'csv', 'xlsx', 'xls', 'parquet'],
            'output': ['csv', 'xlsx', 'parquet', 'json']
        }
    
    def detect_file_format(self, file) -> str:
        """检测文件格式"""
        filename = file.name.lower()
        if filename.endswith('.json'):
            return 'json'
        elif filename.endswith('.csv'):
            return 'csv'
        elif filename.endswith(('.xlsx', '.xls')):
            return 'excel'
        elif filename.endswith('.parquet'):
            return 'parquet'
        else:
            raise ValueError(f"不支持的文件格式: {filename}")
    
    def load_file(self, file) -> pd.DataFrame:
        """加载文件为DataFrame"""
        try:
            format_type = self.detect_file_format(file)
            
            if format_type == 'json':
                return self._load_json(file)
            elif format_type == 'csv':
                return pd.read_csv(file)
            elif format_type == 'excel':
                return pd.read_excel(file)
            elif format_type == 'parquet':
                return pd.read_parquet(file)
            else:
                raise ValueError(f"不支持的文件格式: {format_type}")
                
        except Exception as e:
            raise Exception(f"文件加载失败: {str(e)}")
    
    def _load_json(self, file) -> pd.DataFrame:
        """加载JSON文件"""
        try:
            # 尝试标准方式
            data = pd.read_json(file)
        except:
            # 如果失败，尝试读取为列表格式
            file.seek(0)
            data = pd.read_json(file, lines=True)
        
        # 处理复杂JSON结构
        return self._flatten_json_data(data)
    
    def _flatten_json_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """扁平化JSON数据 - 简化版本"""
        # 直接返回原始数据，不进行复杂转换
        return data
    
    def convert_format(self, data: pd.DataFrame, target_format: str, **kwargs) -> Tuple[bytes, str]:
        """转换数据格式"""
        try:
            if target_format == 'csv':
                return self._to_csv(data, **kwargs)
            elif target_format == 'xlsx':
                return self._to_excel(data, **kwargs)
            elif target_format == 'parquet':
                return self._to_parquet(data, **kwargs)
            elif target_format == 'json':
                return self._to_json(data, **kwargs)
            else:
                raise ValueError(f"不支持的目标格式: {target_format}")
        except Exception as e:
            raise Exception(f"格式转换失败: {str(e)}")
    
    def _to_csv(self, data: pd.DataFrame, **kwargs) -> Tuple[bytes, str]:
        """转换为CSV格式"""
        buffer = io.StringIO()
        
        # 处理编码参数，避免重复
        encoding = kwargs.pop('encoding', 'utf-8-sig')
        sep = kwargs.pop('sep', ',')
        
        data.to_csv(buffer, index=False, encoding='utf-8-sig' if encoding == 'utf-8' else encoding, sep=sep, **kwargs)
        csv_data = buffer.getvalue().encode(encoding)
        filename = f"converted_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        return csv_data, filename
    
    def _to_excel(self, data: pd.DataFrame, **kwargs) -> Tuple[bytes, str]:
        """转换为Excel格式"""
        buffer = io.BytesIO()
        
        # 处理工作表名称参数
        sheet_name = kwargs.pop('sheet_name', 'Sheet1')
        
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            data.to_excel(writer, index=False, sheet_name=sheet_name, **kwargs)
        excel_data = buffer.getvalue()
        filename = f"converted_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        return excel_data, filename
    
    def _to_parquet(self, data: pd.DataFrame, **kwargs) -> Tuple[bytes, str]:
        """转换为Parquet格式"""
        buffer = io.BytesIO()
        data.to_parquet(buffer, index=False, **kwargs)
        parquet_data = buffer.getvalue()
        filename = f"converted_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.parquet"
        return parquet_data, filename
    
    def _to_json(self, data: pd.DataFrame, **kwargs) -> Tuple[bytes, str]:
        """转换为JSON格式"""
        buffer = io.StringIO()
        data.to_json(buffer, orient='records', force_ascii=False, indent=2, **kwargs)
        json_data = buffer.getvalue().encode('utf-8')
        filename = f"converted_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        return json_data, filename
    
    def get_conversion_options(self, source_format: str) -> List[str]:
        """获取可用的转换选项"""
        if source_format == 'json':
            return ['csv', 'xlsx', 'parquet']
        elif source_format == 'csv':
            return ['xlsx', 'parquet', 'json']
        elif source_format == 'excel':
            return ['csv', 'parquet', 'json']
        elif source_format == 'parquet':
            return ['csv', 'xlsx', 'json']
        else:
            return []
    
    def analyze_data_structure(self, data: pd.DataFrame) -> Dict[str, Any]:
        """分析数据结构"""
        analysis = {
            "rows": len(data),
            "columns": len(data.columns),
            "memory_usage": data.memory_usage(deep=True).sum() / (1024**2),  # MB
            "data_types": data.dtypes.value_counts().to_dict(),
            "missing_values": data.isnull().sum().to_dict(),
            "complex_columns": []
        }
        
        # 检测复杂列
        for col in data.columns:
            if data[col].dtype == 'object':
                sample_values = data[col].dropna().head(5)
                if len(sample_values) > 0:
                    first_value = sample_values.iloc[0]
                    if isinstance(first_value, (dict, list)):
                        analysis["complex_columns"].append({
                            "column": col,
                            "type": type(first_value).__name__,
                            "sample": str(first_value)[:100] + "..." if len(str(first_value)) > 100 else str(first_value)
                        })
        
        return analysis

class DownloadManager:
    """下载管理器"""
    
    @staticmethod
    def create_download_button(data: bytes, filename: str, label: str = "下载文件"):
        """创建下载按钮"""
        b64 = base64.b64encode(data).decode()
        href = f'<a href="data:file/octet-stream;base64,{b64}" download="{filename}">{label}</a>'
        return href
    
    @staticmethod
    def get_file_size_mb(data: bytes) -> float:
        """获取文件大小（MB）"""
        return len(data) / (1024**2)

# 全局转换器实例
format_converter = FormatConverter()
download_manager = DownloadManager()
