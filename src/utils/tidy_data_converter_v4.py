"""
整洁数据转换器 V4
修复转换效果问题，提供更好的Tidy Data转换
"""

import pandas as pd
import numpy as np
import json
from typing import Dict, Any, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class TidyDataConverterV4:
    """整洁数据转换器 V4"""
    
    def __init__(self):
        self.conversion_strategies = {
            'preserve_structure': self._preserve_structure_strategy,
            'normalize_only': self._normalize_only_strategy,
            'normalize_explode': self._normalize_explode_strategy,
            'flatten_all': self._flatten_all_strategy
        }
    
    def convert_to_tidy_data(self, data: pd.DataFrame, strategy: str = 'normalize_only', **kwargs) -> pd.DataFrame:
        """
        将数据转换为整洁格式
        
        Args:
            data: 原始DataFrame
            strategy: 转换策略
            **kwargs: 额外参数
            
        Returns:
            pd.DataFrame: 整洁格式的数据
        """
        if strategy not in self.conversion_strategies:
            raise ValueError(f"不支持的转换策略: {strategy}")
        
        return self.conversion_strategies[strategy](data, **kwargs)
    
    def _preserve_structure_strategy(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """
        策略1: 保持结构
        将复杂对象转换为JSON字符串，保持原始结构
        适用于：数据交换、存储
        """
        preserved_data = []
        
        for idx, row in data.iterrows():
            preserved_row = {}
            for col, value in row.items():
                if isinstance(value, (dict, list)):
                    # 将复杂对象转换为JSON字符串
                    preserved_row[col] = json.dumps(value, ensure_ascii=False)
                else:
                    preserved_row[col] = value
            preserved_data.append(preserved_row)
        
        return pd.DataFrame(preserved_data)
    
    def _normalize_only_strategy(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """
        策略2: 仅标准化（使用pd.json_normalize）
        展开嵌套字典，保持数组为列表格式
        适用于：数据分析，需要访问嵌套字段
        """
        # 将DataFrame转换为JSON格式，然后使用json_normalize
        json_data = data.to_dict('records')
        
        # 使用pd.json_normalize展开嵌套结构
        separator = kwargs.get('separator', '.')
        normalized_df = pd.json_normalize(json_data, sep=separator)
        
        return normalized_df
    
    def _normalize_explode_strategy(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """
        策略3: 标准化+展开（Tidy Data）
        展开嵌套字典，并将数组展开为多行
        适用于：统计建模、时间序列分析
        """
        # 首先标准化
        normalized_df = self._normalize_only_strategy(data, **kwargs)
        
        # 找出包含列表的列
        list_columns = []
        for col in normalized_df.columns:
            if normalized_df[col].apply(lambda x: isinstance(x, list)).any():
                list_columns.append(col)
        
        if list_columns:
            # 选择第一个列表列进行展开
            explode_col = list_columns[0]
            
            # 检查展开列的长度是否一致
            lengths = normalized_df[explode_col].apply(lambda x: len(x) if isinstance(x, list) else 1)
            max_length = lengths.max()
            
            # 如果长度不一致，填充到相同长度
            def pad_list(x, max_len):
                if isinstance(x, list):
                    return x + [None] * (max_len - len(x))
                return [x] * max_len
            
            # 临时填充列表列
            temp_df = normalized_df.copy()
            temp_df[explode_col] = temp_df[explode_col].apply(lambda x: pad_list(x, max_length))
            
            # 展开
            exploded_df = temp_df.explode(explode_col)
            exploded_df = exploded_df.reset_index(drop=True)
            
            # 如果展开的列包含字典，进一步标准化
            if exploded_df[explode_col].apply(lambda x: isinstance(x, dict)).any():
                # 将展开的字典列进一步标准化
                separator = kwargs.get('separator', '.')
                temp_df = exploded_df.drop(columns=[explode_col])
                dict_data = exploded_df[explode_col].to_dict()
                
                # 标准化字典数据
                dict_df = pd.json_normalize(dict_data, sep=separator)
                dict_df.index = temp_df.index
                
                # 合并结果
                result_df = pd.concat([temp_df, dict_df], axis=1)
                return result_df
            
            return exploded_df
        
        return normalized_df
    
    def _flatten_all_strategy(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """
        策略4: 完全扁平化
        展开所有嵌套结构，包括字典和数组
        适用于：机器学习、完全扁平化需求
        """
        # 首先标准化
        normalized_df = self._normalize_only_strategy(data, **kwargs)
        
        # 找出所有包含列表的列
        list_columns = []
        for col in normalized_df.columns:
            if normalized_df[col].apply(lambda x: isinstance(x, list)).any():
                list_columns.append(col)
        
        if list_columns:
            # 展开所有列表列
            exploded_df = normalized_df.copy()
            
            # 逐个展开列表列
            for col in list_columns:
                # 检查长度
                lengths = exploded_df[col].apply(lambda x: len(x) if isinstance(x, list) else 1)
                max_length = lengths.max()
                
                # 填充列表
                def pad_list(x, max_len):
                    if isinstance(x, list):
                        return x + [None] * (max_len - len(x))
                    return [x] * max_len
                
                exploded_df[col] = exploded_df[col].apply(lambda x: pad_list(x, max_length))
                exploded_df = exploded_df.explode(col)
                exploded_df = exploded_df.reset_index(drop=True)
            
            return exploded_df
        
        return normalized_df
    
    def analyze_data_structure(self, data: pd.DataFrame) -> Dict[str, Any]:
        """分析数据结构，推荐最佳转换策略"""
        analysis = {
            "total_rows": len(data),
            "total_columns": len(data.columns),
            "complex_columns": [],
            "array_columns": [],
            "dict_columns": [],
            "simple_columns": [],
            "recommended_strategy": "normalize_only"
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
            analysis["recommended_strategy"] = "preserve_structure"
        elif len(analysis["array_columns"]) > 0 and len(analysis["dict_columns"]) == 0:
            analysis["recommended_strategy"] = "normalize_explode"
        elif len(analysis["dict_columns"]) > 0 and len(analysis["array_columns"]) == 0:
            analysis["recommended_strategy"] = "normalize_only"
        else:
            analysis["recommended_strategy"] = "flatten_all"
        
        return analysis
    
    def get_strategy_description(self, strategy: str) -> str:
        """获取策略描述"""
        descriptions = {
            'preserve_structure': '保持结构：将复杂对象转换为JSON字符串，保持原始结构',
            'normalize_only': '仅标准化：展开嵌套字典，保持数组为列表格式',
            'normalize_explode': '标准化+展开：展开嵌套字典，并将数组展开为多行（Tidy Data）',
            'flatten_all': '完全扁平化：展开所有嵌套结构，包括字典和数组'
        }
        return descriptions.get(strategy, '未知策略')
    
    def get_strategy_use_case(self, strategy: str) -> str:
        """获取策略适用场景"""
        use_cases = {
            'preserve_structure': '数据交换、存储、保持原始语义',
            'normalize_only': '数据分析、需要访问嵌套字段',
            'normalize_explode': '统计建模、时间序列分析、Tidy Data需求',
            'flatten_all': '机器学习、完全扁平化需求'
        }
        return use_cases.get(strategy, '未知场景')

# 全局转换器实例
tidy_converter_v4 = TidyDataConverterV4()
