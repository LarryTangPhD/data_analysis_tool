"""
普通模式AI助手模块
专门为普通模式（科研导向）提供AI智能助手功能
"""

from langchain.prompts import ChatPromptTemplate
from langchain_openai.chat_models.base import BaseChatOpenAI
import os
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, List
import warnings
warnings.filterwarnings('ignore')

class IntermediateModeAI:
    """普通模式AI助手类"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"):
        """
        初始化普通模式AI助手
        
        Args:
            api_key: API密钥，如果为None则从环境变量获取
            base_url: API基础URL
        """
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY 环境变量未设置或未提供")
        
        self.base_url = base_url
        self.llm = self._get_llm()
        
        # 普通模式预设问题模板（科研导向）
        self.preset_questions = {
            "data_upload": [
                "如何导入SPSS数据文件？",
                "如何处理实验设计数据？",
                "如何检查数据质量？",
                "如何识别和处理异常值？",
                "如何转换变量类型？",
                "如何合并多个数据集？"
            ],
            "statistical_analysis": [
                "如何选择合适的统计方法？",
                "如何解释p值和效应量？",
                "什么时候使用参数检验vs非参数检验？",
                "如何处理多重比较问题？",
                "如何报告统计结果？",
                "如何计算样本量？"
            ],
            "research_design": [
                "如何设计实验研究？",
                "如何确定样本量？",
                "如何处理缺失数据？",
                "如何评估数据质量？",
                "如何确保分析的可重复性？",
                "如何选择对照组？"
            ],
            "visualization": [
                "如何选择合适的图表类型？",
                "如何制作期刊标准的图表？",
                "如何解释统计图表？",
                "如何优化图表可读性？",
                "如何导出高质量图表？",
                "如何制作APA格式的图表？"
            ],
            "academic_writing": [
                "如何撰写方法学部分？",
                "如何报告统计结果？",
                "如何解释研究发现？",
                "如何制作统计表格？",
                "如何避免常见的统计错误？",
                "如何撰写结果讨论？"
            ],
            "data_cleaning": [
                "如何处理实验数据中的缺失值？",
                "如何检测和处理异常值？",
                "如何进行数据转换？",
                "如何检查正态性假设？",
                "如何处理重复测量数据？",
                "如何标准化变量？"
            ],
            "report_generation": [
                "如何生成学术报告？",
                "如何制作统计表格？",
                "如何导出高质量图表？",
                "如何生成方法学描述？",
                "如何制作结果摘要？",
                "如何生成参考文献？"
            ]
        }
    
    def _get_llm(self, temperature: float = 0.7) -> BaseChatOpenAI:
        """创建LLM实例"""
        return BaseChatOpenAI(
            model="qwen-plus",
            temperature=temperature,
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    def answer_research_question(self, question: str, context: str = "", data_context: str = "") -> str:
        """
        回答科研相关问题
        
        Args:
            question: 用户问题
            context: 当前页面上下文
            data_context: 数据上下文信息
            
        Returns:
            AI回答
        """
        prompt_template = ChatPromptTemplate.from_template("""
        你是一位经验丰富的数据科学研究助手，专门帮助硕博研究生进行科研数据分析。
        
        当前上下文：{context}
        数据信息：{data_context}
        
        用户问题：{question}
        
        请提供专业、准确、实用的回答，包括：
        1. 直接回答用户问题
        2. 提供具体的操作建议
        3. 解释相关的统计概念
        4. 给出最佳实践建议
        5. 提醒注意事项
        
        回答要专业、简洁、实用，适合有基础统计学知识的研究生理解。
        """)
        
        try:
            chain = prompt_template | self.llm
            response = chain.invoke({
                "context": context,
                "data_context": data_context,
                "question": question
            })
            return response.content
        except Exception as e:
            return f"抱歉，AI助手暂时无法回答您的问题。错误信息：{str(e)}"
    
    def recommend_statistical_method(self, data_info: Dict[str, Any], research_question: str) -> str:
        """
        推荐统计方法
        
        Args:
            data_info: 数据信息
            research_question: 研究问题
            
        Returns:
            方法推荐
        """
        prompt_template = ChatPromptTemplate.from_template("""
        你是一位统计方法学专家，请根据以下信息推荐合适的统计方法：
        
        数据信息：
        - 样本量：{sample_size}
        - 变量类型：{variable_types}
        - 研究设计：{research_design}
        - 数据分布：{data_distribution}
        
        研究问题：{research_question}
        
        请推荐：
        1. 最适合的统计方法
        2. 方法选择的理由
        3. 使用该方法的注意事项
        4. 替代方法（如果有）
        5. 效应量计算方法
        
        回答要专业、准确，适合学术研究使用。
        """)
        
        try:
            chain = prompt_template | self.llm
            response = chain.invoke({
                "sample_size": data_info.get("sample_size", "未知"),
                "variable_types": data_info.get("variable_types", "未知"),
                "research_design": data_info.get("research_design", "未知"),
                "data_distribution": data_info.get("data_distribution", "未知"),
                "research_question": research_question
            })
            return response.content
        except Exception as e:
            return f"抱歉，无法生成方法推荐。错误信息：{str(e)}"
    
    def generate_academic_report_section(self, section_type: str, analysis_results: Dict[str, Any]) -> str:
        """
        生成学术报告部分
        
        Args:
            section_type: 报告部分类型（methodology, results, discussion）
            analysis_results: 分析结果
            
        Returns:
            报告内容
        """
        prompt_template = ChatPromptTemplate.from_template("""
        你是一位学术写作专家，请根据分析结果生成{section_type}部分：
        
        分析结果：{analysis_results}
        
        请生成符合学术标准的{section_type}部分，包括：
        1. 清晰的结构
        2. 准确的描述
        3. 适当的统计报告
        4. 专业的学术语言
        
        格式要求：使用学术写作的标准格式和语言。
        """)
        
        try:
            chain = prompt_template | self.llm
            response = chain.invoke({
                "section_type": section_type,
                "analysis_results": str(analysis_results)
            })
            return response.content
        except Exception as e:
            return f"抱歉，无法生成报告内容。错误信息：{str(e)}"
    
    def explain_statistical_concept(self, concept: str, context: str = "") -> str:
        """
        解释统计概念
        
        Args:
            concept: 统计概念
            context: 上下文
            
        Returns:
            概念解释
        """
        prompt_template = ChatPromptTemplate.from_template("""
        你是一位统计学教授，请解释以下统计概念：
        
        概念：{concept}
        上下文：{context}
        
        请提供：
        1. 概念的定义
        2. 实际应用场景
        3. 计算方法
        4. 解释要点
        5. 常见误区
        
        解释要清晰、准确，适合研究生理解。
        """)
        
        try:
            chain = prompt_template | self.llm
            response = chain.invoke({
                "concept": concept,
                "context": context
            })
            return response.content
        except Exception as e:
            return f"抱歉，无法解释该概念。错误信息：{str(e)}"
    
    def get_preset_questions(self, page: str) -> List[str]:
        """获取预设问题"""
        return self.preset_questions.get(page, [])
    
    def provide_research_guidance(self, current_page: str, user_progress: Dict[str, Any]) -> str:
        """
        提供研究指导
        
        Args:
            current_page: 当前页面
            user_progress: 用户进度
            
        Returns:
            研究指导
        """
        prompt_template = ChatPromptTemplate.from_template("""
        你是一位研究导师，请根据用户当前状态提供研究指导：
        
        当前页面：{current_page}
        用户进度：{user_progress}
        
        请提供：
        1. 当前步骤的指导
        2. 下一步建议
        3. 注意事项
        4. 最佳实践
        5. 常见问题提醒
        
        指导要具体、实用，帮助用户顺利完成研究。
        """)
        
        try:
            chain = prompt_template | self.llm
            response = chain.invoke({
                "current_page": current_page,
                "user_progress": str(user_progress)
            })
            return response.content
        except Exception as e:
            return f"抱歉，无法提供指导。错误信息：{str(e)}"

def get_intermediate_ai_assistant() -> Optional[IntermediateModeAI]:
    """获取普通模式AI助手实例"""
    try:
        return IntermediateModeAI()
    except Exception as e:
        print(f"无法初始化普通模式AI助手：{e}")
        return None
