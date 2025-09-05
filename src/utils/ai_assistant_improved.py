"""
改进的AI助手模块
添加更好的错误处理和调试信息
"""

from langchain.prompts import ChatPromptTemplate
from langchain_openai.chat_models.base import BaseChatOpenAI
import os
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, List
import warnings
import logging
warnings.filterwarnings('ignore')

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataAnalysisAI:
    """数据分析AI助手类"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"):
        """
        初始化AI助手
        
        Args:
            api_key: API密钥，如果为None则从环境变量获取
            base_url: API基础URL
        """
        logger.info("开始初始化AI助手...")
        
        # 获取API密钥
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        logger.info(f"API密钥状态: {'已设置' if self.api_key else '未设置'}")
        
        if not self.api_key:
            logger.error("DASHSCOPE_API_KEY 环境变量未设置或未提供")
            raise ValueError("DASHSCOPE_API_KEY 环境变量未设置或未提供")
        
        self.base_url = base_url
        logger.info(f"使用API基础URL: {self.base_url}")
        
        # 创建LLM实例
        try:
            self.llm = self._get_llm()
            logger.info("LLM实例创建成功")
        except Exception as e:
            logger.error(f"LLM实例创建失败: {e}")
            raise
    
    def _get_llm(self, temperature: float = 0.7) -> BaseChatOpenAI:
        """
        创建LLM实例
        
        Args:
            temperature: 创造性参数
            
        Returns:
            BaseChatOpenAI实例
        """
        logger.info("正在创建LLM实例...")
        
        try:
            llm = BaseChatOpenAI(
                model="qwen-plus",
                openai_api_key=self.api_key,
                openai_api_base=self.base_url,
                temperature=temperature,
                max_tokens=2000,
                timeout=60,
                request_timeout=60
            )
            logger.info("LLM实例创建成功")
            return llm
        except Exception as e:
            logger.error(f"LLM实例创建失败: {e}")
            raise
    
    def test_connection(self) -> bool:
        """
        测试API连接
        
        Returns:
            bool: 连接是否成功
        """
        logger.info("测试API连接...")
        
        try:
            # 创建一个简单的测试提示
            test_template = ChatPromptTemplate.from_messages([
                ("human", "请回答：你好")
            ])
            
            chain = test_template | self.llm
            result = chain.invoke({})
            
            logger.info("API连接测试成功")
            return True
            
        except Exception as e:
            logger.error(f"API连接测试失败: {e}")
            return False
    
    def analyze_uploaded_data(self, data: pd.DataFrame, data_info: Dict[str, Any]) -> str:
        """
        分析上传的数据并提供初始建议
        
        Args:
            data: 数据框
            data_info: 数据基本信息
            
        Returns:
            str: 分析建议
        """
        logger.info("开始分析上传的数据...")
        
        try:
            # 计算更多数据特征
            numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
            missing_summary = data.isnull().sum().to_dict()
            
            logger.info(f"数据特征: 数值型列{len(numeric_cols)}个, 分类型列{len(categorical_cols)}个")
            
            template = ChatPromptTemplate.from_messages([
                ("human", """
                你是一位专业的数据分析师，正在帮助用户分析刚上传的数据集。请根据以下信息提供专业的初始分析建议：
                
                📊 数据基本信息：
                - 数据集大小：{rows} 行 × {columns} 列
                - 内存使用：{memory_usage} MB
                - 缺失值总数：{missing_values}
                - 重复行数：{duplicate_rows}
                
                📈 数据类型分布：
                - 数值型列：{numeric_cols} (共{num_numeric}列)
                - 分类型列：{categorical_cols} (共{num_categorical}列)
                
                🔍 缺失值详情：
                {missing_summary}
                
                请从以下角度提供专业建议：
                
                1. **数据质量评估** (0-100分)
                   - 数据完整性评分
                   - 数据一致性评估
                   - 潜在问题识别
                
                2. **数据特征分析**
                   - 数据集类型判断（时间序列/横截面/面板数据等）
                   - 主要变量类型分析
                   - 数据规模评估
                
                3. **清洗建议**
                   - 缺失值处理策略
                   - 数据类型转换建议
                   - 异常值检测方法
                
                4. **分析方向推荐**
                   - 适合的探索性分析方法
                   - 可视化建议
                   - 建模可能性评估
                
                5. **下一步行动建议**
                   - 优先处理的问题
                   - 推荐的分析流程
                   - 注意事项提醒
                
                请用中文回答，内容要专业、实用、易懂。格式要清晰，使用markdown格式。
                """)
            ])
            
            chain = template | self.llm
            result = chain.invoke({
                "rows": data_info['rows'],
                "columns": data_info['columns'],
                "memory_usage": data_info['memory_usage'],
                "missing_values": data_info['missing_values'],
                "duplicate_rows": data_info['duplicate_rows'],
                "numeric_cols": str(numeric_cols),
                "num_numeric": len(numeric_cols),
                "categorical_cols": str(categorical_cols),
                "num_categorical": len(categorical_cols),
                "missing_summary": str(missing_summary)
            })
            
            logger.info("数据分析完成")
            return result.content
            
        except Exception as e:
            logger.error(f"数据分析失败: {e}")
            raise
    
    def answer_data_question(self, question: str, data_context: str, 
                           current_page: str = "通用") -> str:
        """
        回答数据相关问题
        
        Args:
            question: 用户问题
            data_context: 数据上下文
            current_page: 当前页面
            
        Returns:
            str: 回答
        """
        logger.info(f"回答用户问题: {question[:50]}...")
        
        try:
            template = ChatPromptTemplate.from_messages([
                ("human", """
                你是一位专业的数据分析师，正在{current_page}页面帮助用户解答问题。请根据以下信息提供专业回答：
                
                ❓ 用户问题：{question}
                
                📊 数据上下文：{data_context}
                
                请提供以下方面的专业回答：
                
                1. **直接回答**
                   - 针对问题的具体答案
                   - 核心要点总结
                   - 关键信息提取
                
                2. **详细解释**
                   - 相关概念说明
                   - 方法原理介绍
                   - 背景知识补充
                
                3. **操作指导**
                   - 具体操作步骤
                   - 工具使用建议
                   - 参数设置指导
                
                4. **注意事项**
                   - 常见错误提醒
                   - 风险点说明
                   - 最佳实践建议
                
                5. **扩展建议**
                   - 相关分析方向
                   - 深入学习资源
                   - 进阶方法推荐
                
                请用中文回答，内容要准确、专业、易懂。使用markdown格式，确保回答结构清晰。
                """)
            ])
            
            chain = template | self.llm
            result = chain.invoke({
                "current_page": current_page,
                "question": question,
                "data_context": data_context
            })
            
            logger.info("问题回答完成")
            return result.content
            
        except Exception as e:
            logger.error(f"问题回答失败: {e}")
            raise

# 全局AI助手实例
ai_assistant = None

def get_ai_assistant() -> Optional[DataAnalysisAI]:
    """
    获取AI助手实例
    
    Returns:
        DataAnalysisAI实例或None
    """
    global ai_assistant
    
    logger.info("获取AI助手实例...")
    
    if ai_assistant is None:
        try:
            logger.info("创建新的AI助手实例...")
            ai_assistant = DataAnalysisAI()
            logger.info("AI助手实例创建成功")
        except ValueError as e:
            logger.error(f"AI助手创建失败 - 配置错误: {e}")
            return None
        except Exception as e:
            logger.error(f"AI助手创建失败 - 其他错误: {e}")
            return None
    
    return ai_assistant

def test_ai_assistant_connection() -> Dict[str, Any]:
    """
    测试AI助手连接
    
    Returns:
        Dict: 测试结果
    """
    logger.info("开始测试AI助手连接...")
    
    result = {
        "success": False,
        "error": None,
        "details": {}
    }
    
    try:
        # 获取AI助手实例
        ai_assistant = get_ai_assistant()
        if ai_assistant is None:
            result["error"] = "AI助手实例创建失败"
            return result
        
        # 测试连接
        if ai_assistant.test_connection():
            result["success"] = True
            result["details"]["message"] = "AI助手连接正常"
        else:
            result["error"] = "API连接测试失败"
            
    except Exception as e:
        result["error"] = str(e)
        logger.error(f"AI助手连接测试失败: {e}")
    
    return result
