"""
新手模式AI助手模块
专门为新手模式提供教育导向的AI智能助手功能
"""

from langchain.prompts import ChatPromptTemplate
from langchain_openai.chat_models.base import BaseChatOpenAI
import os
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, List
import warnings
warnings.filterwarnings('ignore')

class BeginnerModeAI:
    """新手模式AI助手类"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"):
        """
        初始化新手模式AI助手
        
        Args:
            api_key: API密钥，如果为None则从环境变量获取
            base_url: API基础URL
        """
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY 环境变量未设置或未提供")
        
        self.base_url = base_url
        self.llm = self._get_llm()
        
        # 新手模式预设问题模板
        self.preset_questions = {
            "welcome": [
                "什么是数据分析？",
                "我需要学习哪些基础知识？",
                "整个学习流程大概需要多长时间？",
                "我应该从哪里开始？",
                "数据分析在哪些领域应用？",
                "学习数据分析有什么好处？"
            ],
            "data_upload": [
                "什么是CSV文件？",
                "如何选择合适的数据文件？",
                "数据上传失败怎么办？",
                "为什么需要了解数据结构？",
                "Excel文件和CSV文件有什么区别？",
                "数据文件太大怎么办？"
            ],
            "data_structure": [
                "什么是数值型数据？",
                "什么是分类型数据？",
                "缺失值是什么意思？",
                "为什么要检查数据类型？",
                "如何识别数据类型？",
                "数据类型错误会有什么影响？"
            ],
            "data_cleaning": [
                "什么是数据清洗？",
                "为什么要处理缺失值？",
                "重复数据有什么问题？",
                "异常值是什么？",
                "如何处理缺失值？",
                "数据清洗的标准是什么？",
                "清洗后的数据质量如何评估？"
            ],
            "visualization": [
                "什么时候用柱状图？",
                "散点图能看出什么？",
                "如何选择合适的图表？",
                "什么是数据分布？",
                "箱线图能告诉我们什么？",
                "热力图有什么用？",
                "如何解读图表结果？"
            ],
            "statistical_analysis": [
                "什么是描述性统计？",
                "相关系数是什么意思？",
                "为什么要做统计分析？",
                "如何解释统计结果？",
                "均值和中位数有什么区别？",
                "标准差代表什么？",
                "如何判断相关性是否显著？"
            ],
            "report": [
                "如何写数据分析报告？",
                "报告应该包含哪些内容？",
                "如何展示分析结果？",
                "有什么注意事项？",
                "如何让报告更有说服力？",
                "报告的结构应该如何安排？",
                "如何总结分析结论？"
            ]
        }
    
    def _get_llm(self, temperature: float = 0.7) -> BaseChatOpenAI:
        """创建LLM实例"""
        return BaseChatOpenAI(
            model="qwen-plus",
            openai_api_key=self.api_key,
            openai_api_base=self.base_url,
            temperature=temperature,
            max_tokens=2000,
            timeout=60,
            request_timeout=60
        )
    
    # ==================== 新手模式专用AI功能 ====================
    
    def answer_beginner_question(self, question: str, current_step: str, data_context: str = "") -> str:
        """
        回答新手问题（教育导向）
        
        Args:
            question: 用户问题
            current_step: 当前学习步骤
            data_context: 数据上下文（可选）
            
        Returns:
            str: 教育导向的回答
        """
        template = ChatPromptTemplate.from_messages([
            ("human", """
            你是一位专业的数据分析导师，正在指导一位初学者学习数据分析。
            
            📚 当前学习阶段：{current_step}
            ❓ 学生问题：{question}
            📊 数据上下文：{data_context}
            
            请以导师的身份回答，要求：
            
            1. **通俗易懂**：用简单明了的语言解释概念
            2. **循序渐进**：从基础概念开始，逐步深入
            3. **实例说明**：用具体例子帮助理解
            4. **鼓励学习**：给予积极的学习建议
            5. **联系实际**：说明在实际工作中的应用
            
            回答结构：
            - 🎯 直接回答
            - 📖 概念解释
            - 💡 实例说明
            - 🚀 学习建议
            - ⚠️ 注意事项
            
            请用中文回答，语气友好、鼓励性强。
            """)
        ])
        
        chain = template | self.llm
        result = chain.invoke({
            "current_step": current_step,
            "question": question,
            "data_context": data_context or "暂无数据"
        })
        
        return result.content
    
    def provide_learning_guidance(self, current_step: str, user_progress: Dict[str, Any]) -> str:
        """
        提供学习指导
        
        Args:
            current_step: 当前学习步骤
            user_progress: 用户学习进度
            
        Returns:
            str: 学习指导
        """
        template = ChatPromptTemplate.from_messages([
            ("human", """
            你是一位数据分析学习导师，正在为一位初学者提供学习指导。
            
            📚 当前学习阶段：{current_step}
            📊 学习进度：{user_progress}
            
            请提供：
            
            1. **学习重点**：当前阶段需要掌握的核心概念
            2. **学习方法**：推荐的学习方法和技巧
            3. **常见误区**：提醒可能遇到的常见问题
            4. **下一步建议**：为下一阶段学习做准备
            5. **鼓励话语**：给予学习动力和信心
            
            请用中文回答，语气温暖、鼓励性强。
            """)
        ])
        
        chain = template | self.llm
        result = chain.invoke({
            "current_step": current_step,
            "user_progress": str(user_progress)
        })
        
        return result.content
    
    def explain_concept(self, concept: str, current_step: str) -> str:
        """
        解释概念（新手友好）
        
        Args:
            concept: 要解释的概念
            current_step: 当前学习步骤
            
        Returns:
            str: 概念解释
        """
        template = ChatPromptTemplate.from_messages([
            ("human", """
            你是一位数据分析导师，正在向初学者解释概念。
            
            📖 要解释的概念：{concept}
            📚 当前学习阶段：{current_step}
            
            请提供：
            
            1. **简单定义**：用最通俗的语言定义概念
            2. **生活类比**：用生活中的例子类比
            3. **重要性说明**：为什么需要了解这个概念
            4. **实际应用**：在数据分析中如何使用
            5. **学习建议**：如何更好地理解这个概念
            
            请用中文回答，语言简单易懂，避免专业术语。
            """)
        ])
        
        chain = template | self.llm
        result = chain.invoke({
            "concept": concept,
            "current_step": current_step
        })
        
        return result.content
    
    def analyze_learning_progress(self, user_actions: List[str], current_step: str) -> str:
        """
        分析学习进度
        
        Args:
            user_actions: 用户操作记录
            current_step: 当前学习步骤
            
        Returns:
            str: 学习进度分析
        """
        template = ChatPromptTemplate.from_messages([
            ("human", """
            你是一位数据分析学习导师，正在分析学生的学习进度。
            
            📊 用户操作记录：{user_actions}
            📚 当前学习阶段：{current_step}
            
            请分析：
            
            1. **学习表现**：评估当前学习效果
            2. **学习习惯**：分析学习方法和习惯
            3. **薄弱环节**：识别需要加强的地方
            4. **学习建议**：提供改进建议
            5. **鼓励话语**：给予积极反馈
            
            请用中文回答，语气积极、建设性强。
            """)
        ])
        
        chain = template | self.llm
        result = chain.invoke({
            "user_actions": str(user_actions),
            "current_step": current_step
        })
        
        return result.content
    
    def get_preset_questions(self, step: str) -> List[str]:
        """获取预设问题"""
        return self.preset_questions.get(step, [])
    
    def suggest_next_steps(self, current_step: str, user_performance: Dict[str, Any]) -> str:
        """
        建议下一步学习
        
        Args:
            current_step: 当前学习步骤
            user_performance: 用户表现
            
        Returns:
            str: 下一步建议
        """
        template = ChatPromptTemplate.from_messages([
            ("human", """
            你是一位数据分析学习导师，正在为学生规划下一步学习。
            
            📚 当前学习阶段：{current_step}
            📊 学习表现：{user_performance}
            
            请提供：
            
            1. **学习建议**：下一步应该学习什么
            2. **学习方法**：推荐的学习方法
            3. **时间安排**：建议的学习时间
            4. **重点提醒**：需要注意的重点
            5. **学习目标**：设定明确的学习目标
            
            请用中文回答，建议具体、可操作。
            """)
        ])
        
        chain = template | self.llm
        result = chain.invoke({
            "current_step": current_step,
            "user_performance": str(user_performance)
        })
        
        return result.content

# 全局新手模式AI助手实例
beginner_ai_assistant = None

def get_beginner_ai_assistant() -> BeginnerModeAI:
    """获取新手模式AI助手实例"""
    global beginner_ai_assistant
    if beginner_ai_assistant is None:
        try:
            beginner_ai_assistant = BeginnerModeAI()
        except Exception as e:
            print(f"AI助手初始化失败：{e}")
            return None
    return beginner_ai_assistant
