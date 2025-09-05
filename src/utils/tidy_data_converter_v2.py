"""
整洁数据转换器 V2
提供真正有区别的转换策略
"""

import pandas as pd
import numpy as np
import json
from typing import Dict, Any, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class TidyDataConverterV2:
    """整洁数据转换器 V2"""
    
    def __init__(self):
        self.conversion_strategies = {
            'minimal': self._minimal_strategy,
            'flatten_dicts': self._flatten_dicts_strategy,
            'normalize_arrays': self._normalize_arrays_strategy,
            'full_flatten': self._full_flatten_strategy
        }
    
    def convert_to_tidy_data(self, data: pd.DataFrame, strategy: str = 'minimal') -> pd.DataFrame:
        """
        将数据转换为整洁格式
        
        Args:
            data: 原始DataFrame
            strategy: 转换策略
            
        Returns:
            pd.DataFrame: 整洁格式的数据
        """
        if strategy not in self.conversion_strategies:
            raise ValueError(f"不支持的转换策略: {strategy}")
        
        return self.conversion_strategies[strategy](data)
    
    def _minimal_strategy(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        策略1: 最小化转换
        只将复杂对象转换为JSON字符串，保持原始结构
        适用于：数据交换、存储
        """
        minimal_data = []
        
        for idx, row in data.iterrows():
            minimal_row = {}
            for col, value in row.items():
                if isinstance(value, (dict, list)):
                    # 将复杂对象转换为JSON字符串
                    minimal_row[col] = json.dumps(value, ensure_ascii=False)
                else:
                    minimal_row[col] = value
            minimal_data.append(minimal_row)
        
        return pd.DataFrame(minimal_data)
    
    def _flatten_dicts_strategy(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        策略2: 扁平化字典
        展开字典为独立列，保持数组为字符串
        适用于：数据分析，需要字典字段独立访问
        """
        flattened_data = []
        
        for idx, row in data.iterrows():
            flat_row = {}
            for col, value in row.items():
                if isinstance(value, dict):
                    # 展开字典
                    for key, val in value.items():
                        flat_row[f"{col}_{key}"] = val
                elif isinstance(value, list):
                    # 保持数组为字符串格式
                    flat_row[col] = json.dumps(value, ensure_ascii=False)
                else:
                    flat_row[col] = value
            flattened_data.append(flat_row)
        
        return pd.DataFrame(flattened_data)
    
    def _normalize_arrays_strategy(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        策略3: 标准化数组
        将数组展开为多行，创建长格式数据
        适用于：统计建模、时间序列分析
        """
        normalized_rows = []
        
        for idx, row in data.iterrows():
            # 找出所有数组列
            array_columns = []
            for col, value in row.items():
                if isinstance(value, list):
                    array_columns.append(col)
            
            if not array_columns:
                # 没有数组，直接添加行
                normalized_rows.append(row.to_dict())
            else:
                # 有数组，需要展开
                max_length = max(len(row[col]) for col in array_columns)
                
                for i in range(max_length):
                    new_row = {}
                    for col, value in row.items():
                        if isinstance(value, list):
                            new_row[col] = value[i] if i < len(value) else None
                        else:
                            new_row[col] = value
                    normalized_rows.append(new_row)
        
        return pd.DataFrame(normalized_rows)
    
    def _full_flatten_strategy(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        策略4: 完全扁平化
        展开所有复杂结构（字典和数组）
        适用于：机器学习、完全扁平化需求
        """
        fully_flattened_data = []
        
        for idx, row in data.iterrows():
            flat_row = {}
            for col, value in row.items():
                if isinstance(value, dict):
                    # 展开字典
                    for key, val in value.items():
                        flat_row[f"{col}_{key}"] = val
                elif isinstance(value, list):
                    # 展开数组
                    for i, item in enumerate(value):
                        flat_row[f"{col}_{i}"] = item
                else:
                    flat_row[col] = value
            fully_flattened_data.append(flat_row)
        
        return pd.DataFrame(fully_flattened_data)
    
    def analyze_data_structure(self, data: pd.DataFrame) -> Dict[str, Any]:
        """分析数据结构，推荐最佳转换策略"""
        analysis = {
            "total_rows": len(data),
            "total_columns": len(data.columns),
            "complex_columns": [],
            "array_columns": [],
            "dict_columns": [],
            "simple_columns": [],
            "recommended_strategy": "minimal"
        }
        
        for col in data.columns:
            sample_values = data[col].dropna().head(5)
            if len(sample_values) > 0:
                first_value = sample_values.iloc[0]
                
                if isinstance(first_value, dict):
                    analysis["dict_columns"].append(col)
                    analysis["complex_columns"].append(col)
                elif isinstance(first_value, list):
                    analysis["array_columns"].append(col)
                    analysis["complex_columns"].append(col)
                else:
                    analysis["simple_columns"].append(col)
        
        # 推荐策略
        if len(analysis["complex_columns"]) == 0:
            analysis["recommended_strategy"] = "minimal"
        elif len(analysis["array_columns"]) > 0 and len(analysis["dict_columns"]) == 0:
            analysis["recommended_strategy"] = "normalize_arrays"
        elif len(analysis["dict_columns"]) > 0 and len(analysis["array_columns"]) == 0:
            analysis["recommended_strategy"] = "flatten_dicts"
        else:
            analysis["recommended_strategy"] = "full_flatten"
        
        return analysis
    
    def get_strategy_description(self, strategy: str) -> str:
        """获取策略描述"""
        descriptions = {
            'minimal': '最小化转换：保持原始结构，只将复杂对象转为JSON字符串',
            'flatten_dicts': '扁平化字典：展开字典为独立列，保持数组为字符串',
            'normalize_arrays': '标准化数组：将数组展开为多行，创建长格式数据',
            'full_flatten': '完全扁平化：展开所有复杂结构（字典和数组）'
        }
        return descriptions.get(strategy, '未知策略')
    
    def get_strategy_use_case(self, strategy: str) -> str:
        """获取策略适用场景"""
        use_cases = {
            'minimal': '数据交换、存储、保持原始语义',
            'flatten_dicts': '数据分析、需要字典字段独立访问',
            'normalize_arrays': '统计建模、时间序列分析',
            'full_flatten': '机器学习、完全扁平化需求'
        }
        return use_cases.get(strategy, '未知场景')

# 全局转换器实例
tidy_converter_v2 = TidyDataConverterV2()
