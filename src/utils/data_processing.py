"""
数据处理工具模块
提供数据加载、清洗、质量评估等核心功能
"""

import pandas as pd
import numpy as np
import streamlit as st
from typing import Optional, List, Dict, Any
import warnings
warnings.filterwarnings('ignore')


@st.cache_data
def load_data(uploaded_file) -> pd.DataFrame:
    """
    缓存数据加载函数
    
    Args:
        uploaded_file: 上传的文件对象
        
    Returns:
        pd.DataFrame: 加载的数据框
    """
    if uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(('.xlsx', '.xls')):
        return pd.read_excel(uploaded_file)
    elif uploaded_file.name.endswith('.json'):
        return pd.read_json(uploaded_file)
    elif uploaded_file.name.endswith('.parquet'):
        return pd.read_parquet(uploaded_file)


@st.cache_data
def calculate_correlation_matrix(data: pd.DataFrame) -> pd.DataFrame:
    """
    缓存相关性矩阵计算
    
    Args:
        data: 数据框
        
    Returns:
        pd.DataFrame: 相关性矩阵
    """
    return data.corr()


@st.cache_data
def calculate_data_quality_score(data: pd.DataFrame) -> float:
    """
    缓存数据质量评分计算
    
    Args:
        data: 数据框
        
    Returns:
        float: 数据质量评分 (0-100)
    """
    score = 100
    total_rows, total_cols = len(data), len(data.columns)
    
    # 缺失值扣分
    missing_ratio = data.isnull().sum().sum() / (total_rows * total_cols)
    score -= missing_ratio * 30
    
    # 重复值扣分
    duplicate_ratio = data.duplicated().sum() / total_rows
    score -= duplicate_ratio * 20
    
    # 数据类型合理性检查
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns
    
    # 如果数值型列过多，可能存在问题
    if len(numeric_cols) / total_cols > 0.8:
        score -= 10
    
    # 检查异常值
    outlier_score = 0
    for col in numeric_cols:
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = data[(data[col] < Q1 - 1.5 * IQR) | (data[col] > Q3 + 1.5 * IQR)]
        outlier_ratio = len(outliers) / total_rows
        outlier_score += outlier_ratio
    
    score -= min(outlier_score * 15, 20)
    
    return max(score, 0)


def get_data_info(data: pd.DataFrame) -> Dict[str, Any]:
    """
    获取数据基本信息
    
    Args:
        data: 数据框
        
    Returns:
        Dict: 数据信息字典
    """
    return {
        'rows': len(data),
        'columns': len(data.columns),
        'memory_usage': data.memory_usage(deep=True).sum() / 1024**2,
        'missing_values': data.isnull().sum().sum(),
        'duplicate_rows': data.duplicated().sum(),
        'data_types': data.dtypes.value_counts().to_dict(),
        'unique_values': [data[col].nunique() for col in data.columns]
    }


def handle_missing_values(data: pd.DataFrame, strategy: str, columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    处理缺失值
    
    Args:
        data: 数据框
        strategy: 处理策略
        columns: 要处理的列名列表
        
    Returns:
        pd.DataFrame: 处理后的数据框
    """
    data_cleaned = data.copy()
    
    if columns is None:
        columns = data.columns
    
    if strategy == "删除行":
        data_cleaned = data_cleaned.dropna(subset=columns)
    elif strategy == "删除列":
        data_cleaned = data_cleaned.dropna(axis=1)
    elif strategy == "均值填充":
        numeric_cols = data_cleaned[columns].select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if data_cleaned[col].isnull().any():
                data_cleaned[col] = data_cleaned[col].fillna(data_cleaned[col].mean())
    elif strategy == "中位数填充":
        numeric_cols = data_cleaned[columns].select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if data_cleaned[col].isnull().any():
                data_cleaned[col] = data_cleaned[col].fillna(data_cleaned[col].median())
    elif strategy == "众数填充":
        for col in columns:
            if data_cleaned[col].isnull().any():
                mode_value = data_cleaned[col].mode()
                if len(mode_value) > 0:
                    data_cleaned[col] = data_cleaned[col].fillna(mode_value[0])
    elif strategy == "前向填充":
        data_cleaned = data_cleaned.fillna(method='ffill')
    elif strategy == "后向填充":
        data_cleaned = data_cleaned.fillna(method='bfill')
    
    return data_cleaned


def handle_duplicates(data: pd.DataFrame) -> pd.DataFrame:
    """
    处理重复值
    
    Args:
        data: 数据框
        
    Returns:
        pd.DataFrame: 处理后的数据框
    """
    return data.drop_duplicates()


def handle_outliers(data: pd.DataFrame, strategy: str, columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    处理异常值
    
    Args:
        data: 数据框
        strategy: 处理策略
        columns: 要处理的列名列表
        
    Returns:
        pd.DataFrame: 处理后的数据框
    """
    data_cleaned = data.copy()
    
    if columns is None:
        columns = data.select_dtypes(include=[np.number]).columns.tolist()
    
    for col in columns:
        if col in data_cleaned.columns and data_cleaned[col].dtype in ['int64', 'float64']:
            if strategy == "IQR方法":
                Q1 = data_cleaned[col].quantile(0.25)
                Q3 = data_cleaned[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                data_cleaned[col] = data_cleaned[col].clip(lower=lower_bound, upper=upper_bound)
            elif strategy == "Z-score方法":
                z_scores = np.abs((data_cleaned[col] - data_cleaned[col].mean()) / data_cleaned[col].std())
                data_cleaned[col] = data_cleaned[col].mask(z_scores > 3, data_cleaned[col].median())
            elif strategy == "百分位法":
                lower_percentile = data_cleaned[col].quantile(0.01)
                upper_percentile = data_cleaned[col].quantile(0.99)
                data_cleaned[col] = data_cleaned[col].clip(lower=lower_percentile, upper=upper_percentile)
    
    return data_cleaned


def clean_string_data(data: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    清洗字符串数据
    
    Args:
        data: 数据框
        columns: 要处理的列名列表
        
    Returns:
        pd.DataFrame: 处理后的数据框
    """
    data_cleaned = data.copy()
    
    if columns is None:
        columns = data.select_dtypes(include=['object']).columns.tolist()
    
    for col in columns:
        if col in data_cleaned.columns:
            # 去除首尾空格
            data_cleaned[col] = data_cleaned[col].astype(str).str.strip()
            # 统一大小写
            data_cleaned[col] = data_cleaned[col].str.lower()
            # 替换空字符串为NaN
            data_cleaned[col] = data_cleaned[col].replace('', np.nan)
    
    return data_cleaned


def get_outlier_statistics(data: pd.DataFrame, columns: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    获取异常值统计信息
    
    Args:
        data: 数据框
        columns: 要分析的列名列表
        
    Returns:
        Dict: 异常值统计信息
    """
    if columns is None:
        columns = data.select_dtypes(include=[np.number]).columns.tolist()
    
    outlier_stats = {}
    for col in columns:
        if col in data.columns and data[col].dtype in ['int64', 'float64']:
            Q1 = data[col].quantile(0.25)
            Q3 = data[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = data[(data[col] < lower_bound) | (data[col] > upper_bound)]
            outlier_stats[col] = {
                'count': len(outliers),
                'percentage': len(outliers) / len(data) * 100,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound
            }
    
    return outlier_stats


def convert_data_format(data: pd.DataFrame, format_type: str, id_vars: Optional[List[str]] = None, 
                       value_vars: Optional[List[str]] = None) -> pd.DataFrame:
    """
    转换数据格式（宽格式与长格式互转）
    
    Args:
        data: 数据框
        format_type: 转换类型 ('wide_to_long' 或 'long_to_wide')
        id_vars: 标识变量
        value_vars: 值变量
        
    Returns:
        pd.DataFrame: 转换后的数据框
    """
    if format_type == 'wide_to_long':
        if id_vars is None or value_vars is None:
            return data
        return pd.melt(data, id_vars=id_vars, value_vars=value_vars, 
                      var_name='variable', value_name='value')
    elif format_type == 'long_to_wide':
        if id_vars is None or value_vars is None:
            return data
        return data.pivot(index=id_vars, columns=value_vars, values='value').reset_index()
    else:
        return data


def get_missing_value_summary(data: pd.DataFrame) -> pd.DataFrame:
    """
    获取缺失值摘要
    
    Args:
        data: 数据框
        
    Returns:
        pd.DataFrame: 缺失值摘要
    """
    missing_data = data.isnull().sum()
    missing_df = pd.DataFrame({
        '列名': missing_data.index,
        '缺失值数量': missing_data.values,
        '缺失比例': (missing_data.values / len(data) * 100).round(2)
    }).sort_values('缺失值数量', ascending=False)
    
    return missing_df


def get_data_type_summary(data: pd.DataFrame) -> pd.DataFrame:
    """
    获取数据类型摘要
    
    Args:
        data: 数据框
        
    Returns:
        pd.DataFrame: 数据类型摘要
    """
    dtype_info = pd.DataFrame({
        '列名': data.columns,
        '数据类型': [str(dtype) for dtype in data.dtypes],
        '非空值数量': data.count(),
        '空值数量': data.isnull().sum(),
        '唯一值数量': [data[col].nunique() for col in data.columns]
    })
    
    return dtype_info
