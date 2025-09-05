"""
优化版AI助手模块
针对性能问题进行优化，提高响应速度
"""

from langchain.prompts import ChatPromptTemplate
from langchain_openai.chat_models.base import BaseChatOpenAI
import os
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, List
import warnings
import hashlib
import json
from functools import lru_cache
warnings.filterwarnings('ignore')


class OptimizedDataAnalysisAI:
    """优化版数据分析AI助手类"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"):
        """
        初始化优化版AI助手
        
        Args:
            api_key: API密钥，如果为None则从环境变量获取
            base_url: API基础URL
        """
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY 环境变量未设置或未提供")
        
        self.base_url = base_url
        self.llm = self._get_optimized_llm()
        self.cache = {}
    
    def _get_optimized_llm(self, temperature: float = 0.3) -> BaseChatOpenAI:
        """
        创建优化版LLM实例
        
        Args:
            temperature: 创造性参数（降低以提高速度）
            
        Returns:
            BaseChatOpenAI实例
        """
        return BaseChatOpenAI(
            model="qwen-turbo",  # 使用更快的模型
            openai_api_key=self.api_key,
            openai_api_base=self.base_url,
            temperature=temperature,
            max_tokens=1000,     # 减少token数量
            timeout=30,          # 减少超时时间
            request_timeout=30   # 减少请求超时时间
        )
    
    def _generate_cache_key(self, func_name: str, *args, **kwargs) -> str:
        """生成缓存键"""
        # 创建参数摘要
        args_str = str(args) + str(sorted(kwargs.items()))
        return hashlib.md5(f"{func_name}:{args_str}".encode()).hexdigest()
    
    def _get_cached_result(self, cache_key: str) -> Optional[str]:
        """获取缓存结果"""
        return self.cache.get(cache_key)
    
    def _set_cached_result(self, cache_key: str, result: str):
        """设置缓存结果"""
        self.cache[cache_key] = result
    
    # ==================== 优化版数据上传页面AI功能 ====================
    
    def analyze_uploaded_data(self, data: pd.DataFrame, data_info: Dict[str, Any]) -> str:
        """
        分析上传的数据并提供初始建议（优化版）
        
        Args:
            data: 数据框
            data_info: 数据基本信息
            
        Returns:
            str: 分析建议
        """
        # 生成缓存键
        cache_key = self._generate_cache_key("analyze_uploaded_data", 
                                           data.shape, data.dtypes.to_dict(), data_info)
        
        # 检查缓存
        cached_result = self._get_cached_result(cache_key)
        if cached_result:
            return cached_result
        
        # 简化数据特征计算
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # 使用简化的提示词
        template = ChatPromptTemplate.from_messages([
            ("human", """
            分析数据集并提供建议：
            
            数据信息：{rows}行×{columns}列，数值型{num_numeric}列，分类型{num_categorical}列
            缺失值：{missing_values}个，重复行：{duplicate_rows}个
            
            请简要回答：
            1. 数据质量评分（0-100）
            2. 主要问题识别
            3. 清洗建议
            4. 分析方向推荐
            
            用中文回答，简洁明了。
            """)
        ])
        
        chain = template | self.llm
        result = chain.invoke({
            "rows": data_info['rows'],
            "columns": data_info['columns'],
            "num_numeric": len(numeric_cols),
            "num_categorical": len(categorical_cols),
            "missing_values": data_info['missing_values'],
            "duplicate_rows": data_info['duplicate_rows']
        })
        
        # 缓存结果
        self._set_cached_result(cache_key, result.content)
        
        return result.content
    
    # ==================== 优化版数据清洗页面AI功能 ====================
    
    def suggest_cleaning_strategy(self, data: pd.DataFrame, cleaning_issue: str) -> str:
        """
        为数据清洗提供智能建议（优化版）
        
        Args:
            data: 数据框
            cleaning_issue: 清洗问题类型
            
        Returns:
            str: 清洗建议
        """
        # 生成缓存键
        cache_key = self._generate_cache_key("suggest_cleaning_strategy", 
                                           data.shape, cleaning_issue)
        
        # 检查缓存
        cached_result = self._get_cached_result(cache_key)
        if cached_result:
            return cached_result
        
        # 简化问题详情
        if cleaning_issue == "missing_values":
            missing_count = data.isnull().sum().sum()
            problem_details = f"缺失值总数：{missing_count}"
        elif cleaning_issue == "duplicates":
            duplicate_count = data.duplicated().sum()
            problem_details = f"重复行数：{duplicate_count}"
        else:
            problem_details = "数据类型问题"
        
        # 使用简化的提示词
        template = ChatPromptTemplate.from_messages([
            ("human", """
            数据清洗建议：
            
            问题类型：{cleaning_issue}
            数据规模：{data_size}
            问题详情：{problem_details}
            
            请提供：
            1. 问题严重程度
            2. 推荐处理方法
            3. 操作步骤
            4. 注意事项
            
            简洁回答，突出重点。
            """)
        ])
        
        chain = template | self.llm
        result = chain.invoke({
            "cleaning_issue": cleaning_issue,
            "data_size": f"{len(data)}行×{len(data.columns)}列",
            "problem_details": problem_details
        })
        
        # 缓存结果
        self._set_cached_result(cache_key, result.content)
        
        return result.content
    
    # ==================== 优化版自动数据分析页面AI功能 ====================
    
    def interpret_auto_analysis(self, data: pd.DataFrame, analysis_results: Dict[str, Any]) -> str:
        """
        解释自动数据分析结果（优化版）
        
        Args:
            data: 数据框
            analysis_results: 自动分析结果
            
        Returns:
            str: 解释和建议
        """
        # 生成缓存键
        cache_key = self._generate_cache_key("interpret_auto_analysis", 
                                           data.shape, str(analysis_results))
        
        # 检查缓存
        cached_result = self._get_cached_result(cache_key)
        if cached_result:
            return cached_result
        
        # 使用简化的提示词
        template = ChatPromptTemplate.from_messages([
            ("human", """
            分析结果解释：
            
            数据规模：{data_size}
            分析结果：{analysis_results}
            
            请简要说明：
            1. 关键发现
            2. 业务意义
            3. 进一步分析建议
            4. 可视化建议
            
            简洁明了，突出重点。
            """)
        ])
        
        chain = template | self.llm
        result = chain.invoke({
            "data_size": f"{len(data)}行×{len(data.columns)}列",
            "analysis_results": str(analysis_results)[:500]  # 限制长度
        })
        
        # 缓存结果
        self._set_cached_result(cache_key, result.content)
        
        return result.content
    
    # ==================== 优化版高级可视化页面AI功能 ====================
    
    def suggest_visualization(self, data: pd.DataFrame, analysis_goal: str) -> str:
        """
        为可视化提供智能建议（优化版）
        
        Args:
            data: 数据框
            analysis_goal: 分析目标
            
        Returns:
            str: 可视化建议
        """
        # 生成缓存键
        cache_key = self._generate_cache_key("suggest_visualization", 
                                           data.shape, analysis_goal)
        
        # 检查缓存
        cached_result = self._get_cached_result(cache_key)
        if cached_result:
            return cached_result
        
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # 使用简化的提示词
        template = ChatPromptTemplate.from_messages([
            ("human", """
            可视化建议：
            
            分析目标：{analysis_goal}
            数据特征：{data_size}，数值型{num_numeric}个，分类型{num_categorical}个
            
            请推荐：
            1. 最适合的图表类型
            2. 变量选择建议
            3. 设计要点
            4. 注意事项
            
            简洁回答，实用为主。
            """)
        ])
        
        chain = template | self.llm
        result = chain.invoke({
            "analysis_goal": analysis_goal,
            "data_size": f"{len(data)}行×{len(data.columns)}列",
            "num_numeric": len(numeric_cols),
            "num_categorical": len(categorical_cols)
        })
        
        # 缓存结果
        self._set_cached_result(cache_key, result.content)
        
        return result.content
    
    # ==================== 优化版统计分析页面AI功能 ====================
    
    def suggest_statistical_tests(self, data: pd.DataFrame, analysis_question: str) -> str:
        """
        推荐统计检验方法（优化版）
        
        Args:
            data: 数据框
            analysis_question: 分析问题
            
        Returns:
            str: 统计检验建议
        """
        # 生成缓存键
        cache_key = self._generate_cache_key("suggest_statistical_tests", 
                                           data.shape, analysis_question)
        
        # 检查缓存
        cached_result = self._get_cached_result(cache_key)
        if cached_result:
            return cached_result
        
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # 使用简化的提示词
        template = ChatPromptTemplate.from_messages([
            ("human", """
            统计检验建议：
            
            分析问题：{analysis_question}
            数据特征：{data_size}，数值型{num_numeric}个，分类型{num_categorical}个
            
            请推荐：
            1. 最适合的检验方法
            2. 前提条件检查
            3. 实施步骤
            4. 结果解释要点
            
            简洁回答，专业准确。
            """)
        ])
        
        chain = template | self.llm
        result = chain.invoke({
            "analysis_question": analysis_question,
            "data_size": f"{len(data)}行×{len(data.columns)}列",
            "num_numeric": len(numeric_cols),
            "num_categorical": len(categorical_cols)
        })
        
        # 缓存结果
        self._set_cached_result(cache_key, result.content)
        
        return result.content
    
    # ==================== 优化版机器学习页面AI功能 ====================
    
    def suggest_ml_approach(self, data: pd.DataFrame, task_type: str, 
                           target_col: str, feature_cols: List[str]) -> str:
        """
        推荐机器学习方法（优化版）
        
        Args:
            data: 数据框
            task_type: 任务类型
            target_col: 目标变量
            feature_cols: 特征变量
            
        Returns:
            str: 机器学习建议
        """
        # 生成缓存键
        cache_key = self._generate_cache_key("suggest_ml_approach", 
                                           data.shape, task_type, target_col, str(feature_cols))
        
        # 检查缓存
        cached_result = self._get_cached_result(cache_key)
        if cached_result:
            return cached_result
        
        # 使用简化的提示词
        template = ChatPromptTemplate.from_messages([
            ("human", """
            机器学习建议：
            
            任务类型：{task_type}
            目标变量：{target_col}
            特征数量：{num_features}个
            数据规模：{data_size}
            
            请推荐：
            1. 最适合的算法
            2. 数据预处理要点
            3. 训练参数建议
            4. 评估方法
            5. 实施步骤
            
            简洁回答，实用为主。
            """)
        ])
        
        chain = template | self.llm
        result = chain.invoke({
            "task_type": task_type,
            "target_col": target_col,
            "num_features": len(feature_cols),
            "data_size": f"{len(data)}行×{len(data.columns)}列"
        })
        
        # 缓存结果
        self._set_cached_result(cache_key, result.content)
        
        return result.content
    
    # ==================== 优化版通用智能问答功能 ====================
    
    def answer_data_question(self, question: str, data_context: str, 
                           current_page: str = "通用") -> str:
        """
        回答数据相关问题（优化版）
        
        Args:
            question: 用户问题
            data_context: 数据上下文
            current_page: 当前页面
            
        Returns:
            str: 回答
        """
        # 生成缓存键
        cache_key = self._generate_cache_key("answer_data_question", 
                                           question, data_context, current_page)
        
        # 检查缓存
        cached_result = self._get_cached_result(cache_key)
        if cached_result:
            return cached_result
        
        # 使用简化的提示词
        template = ChatPromptTemplate.from_messages([
            ("human", """
            数据分析问题回答：
            
            问题：{question}
            数据上下文：{data_context}
            当前页面：{current_page}
            
            请提供：
            1. 直接回答
            2. 简要解释
            3. 操作建议
            4. 注意事项
            
            简洁回答，实用为主。
            """)
        ])
        
        chain = template | self.llm
        result = chain.invoke({
            "question": question,
            "data_context": data_context,
            "current_page": current_page
        })
        
        # 缓存结果
        self._set_cached_result(cache_key, result.content)
        
        return result.content
    
    def clear_cache(self):
        """清空缓存"""
        self.cache.clear()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        return {
            "cache_size": len(self.cache),
            "cache_keys": list(self.cache.keys())
        }


# 全局优化版AI助手实例
optimized_ai_assistant = None

def get_optimized_ai_assistant() -> Optional[OptimizedDataAnalysisAI]:
    """
    获取优化版AI助手实例
    
    Returns:
        OptimizedDataAnalysisAI实例或None
    """
    global optimized_ai_assistant
    if optimized_ai_assistant is None:
        try:
            optimized_ai_assistant = OptimizedDataAnalysisAI()
        except ValueError:
            return None
    return optimized_ai_assistant
