"""
AI助手模块
为数据分析应用提供智能建议、解释和辅助功能
重构版本：将AI功能分散到各个页面中
"""

from langchain.prompts import ChatPromptTemplate
from langchain_openai.chat_models.base import BaseChatOpenAI
import os
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, List
import warnings
warnings.filterwarnings('ignore')


class DataAnalysisAI:
    """数据分析AI助手类"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"):
        """
        初始化AI助手
        
        Args:
            api_key: API密钥，如果为None则从环境变量获取
            base_url: API基础URL
        """
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY 环境变量未设置或未提供")
        
        self.base_url = base_url
        self.llm = self._get_llm()
    
    def _get_llm(self, temperature: float = 0.7) -> BaseChatOpenAI:
        """
        创建LLM实例
        
        Args:
            temperature: 创造性参数
            
        Returns:
            BaseChatOpenAI实例
        """
        return BaseChatOpenAI(
            model="qwen-plus",
            openai_api_key=self.api_key,
            openai_api_base=self.base_url,
            temperature=temperature,
            max_tokens=2000,
            timeout=60,
            request_timeout=60
        )
    
    # ==================== 数据上传页面AI功能 ====================
    
    def analyze_uploaded_data(self, data: pd.DataFrame, data_info: Dict[str, Any]) -> str:
        """
        分析上传的数据并提供初始建议（数据上传页面）
        
        Args:
            data: 数据框
            data_info: 数据基本信息
            
        Returns:
            str: 分析建议
        """
        # 计算更多数据特征
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
        missing_summary = data.isnull().sum().to_dict()
        
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
        
        return result.content
    
    # ==================== 数据清洗页面AI功能 ====================
    
    def suggest_cleaning_strategy(self, data: pd.DataFrame, cleaning_issue: str) -> str:
        """
        为数据清洗提供智能建议（数据清洗页面）
        
        Args:
            data: 数据框
            cleaning_issue: 清洗问题类型（missing_values/duplicates/outliers/data_types）
            
        Returns:
            str: 清洗建议
        """
        # 获取具体的问题信息
        if cleaning_issue == "missing_values":
            missing_info = data.isnull().sum()
            missing_ratio = missing_info / len(data)
            problem_details = f"缺失值详情：\n{missing_info.to_dict()}\n缺失比例：\n{missing_ratio.to_dict()}"
        elif cleaning_issue == "duplicates":
            duplicate_count = data.duplicated().sum()
            problem_details = f"重复行数：{duplicate_count}，重复比例：{duplicate_count/len(data)*100:.2f}%"
        elif cleaning_issue == "outliers":
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            outlier_info = {}
            for col in numeric_cols:
                Q1 = data[col].quantile(0.25)
                Q3 = data[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = data[(data[col] < Q1 - 1.5 * IQR) | (data[col] > Q3 + 1.5 * IQR)]
                outlier_info[col] = len(outliers)
            problem_details = f"异常值详情：{outlier_info}"
        else:
            problem_details = "数据类型问题"
        
        template = ChatPromptTemplate.from_messages([
            ("human", """
            你是一位数据清洗专家，正在帮助用户解决数据质量问题。请根据以下信息提供专业的清洗建议：
            
            🔍 清洗问题类型：{cleaning_issue}
            
            📊 数据基本信息：
            - 数据集大小：{data_size}
            - 数据类型分布：{data_types}
            
            ⚠️ 问题详情：
            {problem_details}
            
            请提供以下方面的专业建议：
            
            1. **问题严重程度评估**
               - 问题对分析的影响程度
               - 是否需要立即处理
               - 优先级排序
            
            2. **清洗策略推荐**
               - 具体处理方法
               - 不同方法的优缺点
               - 推荐的处理顺序
            
            3. **操作步骤指导**
               - 详细的清洗步骤
               - 参数设置建议
               - 注意事项提醒
            
            4. **质量验证方法**
               - 清洗效果评估指标
               - 验证方法
               - 成功标准
            
            5. **最佳实践建议**
               - 行业标准做法
               - 常见错误避免
               - 效率优化建议
            
            请用中文回答，内容要具体、可操作、专业。使用markdown格式，突出重点。
            """)
        ])
        
        chain = template | self.llm
        result = chain.invoke({
            "cleaning_issue": cleaning_issue,
            "data_size": f"{len(data)}行 × {len(data.columns)}列",
            "data_types": str(data.dtypes.value_counts().to_dict()),
            "problem_details": problem_details
        })
        
        return result.content
    
    # ==================== 自动数据分析页面AI功能 ====================
    
    def interpret_auto_analysis(self, data: pd.DataFrame, analysis_results: Dict[str, Any]) -> str:
        """
        解释自动数据分析结果（自动数据分析页面）
        
        Args:
            data: 数据框
            analysis_results: 自动分析结果
            
        Returns:
            str: 解释和建议
        """
        template = ChatPromptTemplate.from_messages([
            ("human", """
            你是一位数据分析专家，正在帮助用户理解自动数据分析的结果。请根据以下信息提供专业的解释和建议：
            
            📊 数据集信息：
            - 数据规模：{data_size}
            - 数据类型：{data_types}
            
            📈 自动分析结果：
            {analysis_results}
            
            请从以下角度提供专业解释：
            
            1. **结果解读**
               - 关键发现总结
               - 数据模式识别
               - 异常情况说明
            
            2. **业务意义**
               - 发现的实际意义
               - 潜在的业务洞察
               - 决策支持建议
            
            3. **深入分析建议**
               - 需要进一步探索的方向
               - 推荐的分析方法
               - 重点关注的数据特征
            
            4. **可视化建议**
               - 适合的图表类型
               - 展示重点
               - 视觉效果优化
            
            5. **下一步行动**
               - 优先分析方向
               - 建模可能性
               - 报告重点
            
            请用中文回答，内容要专业、易懂、有实用价值。使用markdown格式，结构清晰。
            """)
        ])
        
        chain = template | self.llm
        result = chain.invoke({
            "data_size": f"{len(data)}行 × {len(data.columns)}列",
            "data_types": str(data.dtypes.value_counts().to_dict()),
            "analysis_results": str(analysis_results)
        })
        
        return result.content
    
    # ==================== 高级可视化页面AI功能 ====================
    
    def suggest_visualization(self, data: pd.DataFrame, analysis_goal: str) -> str:
        """
        为可视化提供智能建议（高级可视化页面）
        
        Args:
            data: 数据框
            analysis_goal: 分析目标（trend_analysis/distribution_comparison/correlation_analysis/pattern_detection）
            
        Returns:
            str: 可视化建议
        """
        # 分析数据特征
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
        
        template = ChatPromptTemplate.from_messages([
            ("human", """
            你是一位数据可视化专家，正在帮助用户选择合适的可视化方法。请根据以下信息提供专业的可视化建议：
            
            🎯 分析目标：{analysis_goal}
            
            📊 数据特征：
            - 数据规模：{data_size}
            - 数值型变量：{numeric_cols} (共{num_numeric}个)
            - 分类型变量：{categorical_cols} (共{num_categorical}个)
            
            请从以下角度提供专业建议：
            
            1. **图表类型推荐**
               - 最适合的图表类型
               - 不同图表的优缺点
               - 组合使用建议
            
            2. **变量选择指导**
               - 主要变量推荐
               - 辅助变量建议
               - 分组变量选择
            
            3. **可视化设计建议**
               - 颜色搭配建议
               - 布局优化
               - 交互功能推荐
            
            4. **洞察挖掘指导**
               - 重点关注的数据特征
               - 异常模式识别
               - 趋势分析要点
            
            5. **最佳实践提醒**
               - 可视化原则
               - 常见错误避免
               - 效果优化技巧
            
            请用中文回答，内容要具体、实用、专业。使用markdown格式，提供可操作的建议。
            """)
        ])
        
        chain = template | self.llm
        result = chain.invoke({
            "analysis_goal": analysis_goal,
            "data_size": f"{len(data)}行 × {len(data.columns)}列",
            "numeric_cols": str(numeric_cols),
            "num_numeric": len(numeric_cols),
            "categorical_cols": str(categorical_cols),
            "num_categorical": len(categorical_cols)
        })
        
        return result.content
    
    def explain_chart_insights(self, chart_type: str, data: pd.DataFrame, 
                             chart_config: Dict[str, Any], chart_stats: Dict[str, Any]) -> str:
        """
        解释图表洞察（高级可视化页面）
        
        Args:
            chart_type: 图表类型
            data: 数据框
            chart_config: 图表配置
            chart_stats: 图表统计信息
            
        Returns:
            str: 洞察解释
        """
        template = ChatPromptTemplate.from_messages([
            ("human", """
            你是一位数据可视化专家，正在帮助用户理解图表中的洞察。请根据以下信息提供专业的解释：
            
            📊 图表信息：
            - 图表类型：{chart_type}
            - 数据规模：{data_size}
            - 图表配置：{chart_config}
            
            📈 统计信息：
            {chart_stats}
            
            请从以下角度提供专业解释：
            
            1. **图表含义解读**
               - 图表展示的核心信息
               - 数据关系说明
               - 关键特征识别
            
            2. **数据模式分析**
               - 发现的模式或趋势
               - 异常情况说明
               - 分布特征描述
            
            3. **业务洞察**
               - 实际业务意义
               - 决策支持信息
               - 潜在机会或风险
            
            4. **进一步分析建议**
               - 需要深入探索的方向
               - 相关分析推荐
               - 验证方法建议
            
            5. **可视化优化建议**
               - 图表改进方向
               - 展示效果优化
               - 交互功能建议
            
            请用中文回答，内容要专业、易懂、有实用价值。使用markdown格式，突出重点。
            """)
        ])
        
        chain = template | self.llm
        result = chain.invoke({
            "chart_type": chart_type,
            "data_size": f"{len(data)}行 × {len(data.columns)}列",
            "chart_config": str(chart_config),
            "chart_stats": str(chart_stats)
        })
        
        return result.content
    
    # ==================== 统计分析页面AI功能 ====================
    
    def suggest_statistical_tests(self, data: pd.DataFrame, analysis_question: str) -> str:
        """
        推荐统计检验方法（统计分析页面）
        
        Args:
            data: 数据框
            analysis_question: 分析问题
            
        Returns:
            str: 统计检验建议
        """
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
        
        template = ChatPromptTemplate.from_messages([
            ("human", """
            你是一位统计学专家，正在帮助用户选择合适的统计检验方法。请根据以下信息提供专业的建议：
            
            ❓ 分析问题：{analysis_question}
            
            📊 数据特征：
            - 数据规模：{data_size}
            - 数值型变量：{numeric_cols} (共{num_numeric}个)
            - 分类型变量：{categorical_cols} (共{num_categorical}个)
            
            请从以下角度提供专业建议：
            
            1. **检验方法推荐**
               - 最适合的统计检验
               - 检验方法选择理由
               - 替代方案说明
            
            2. **前提条件检查**
               - 数据分布要求
               - 样本量要求
               - 独立性假设
            
            3. **实施步骤指导**
               - 详细的操作步骤
               - 参数设置建议
               - 注意事项提醒
            
            4. **结果解释指导**
               - 如何解读检验结果
               - 显著性水平说明
               - 效应量计算建议
            
            5. **报告撰写建议**
               - 结果报告格式
               - 关键信息展示
               - 结论表述方式
            
            请用中文回答，内容要专业、准确、可操作。使用markdown格式，提供具体的统计建议。
            """)
        ])
        
        chain = template | self.llm
        result = chain.invoke({
            "analysis_question": analysis_question,
            "data_size": f"{len(data)}行 × {len(data.columns)}列",
            "numeric_cols": str(numeric_cols),
            "num_numeric": len(numeric_cols),
            "categorical_cols": str(categorical_cols),
            "num_categorical": len(categorical_cols)
        })
        
        return result.content
    
    def interpret_statistical_results(self, test_type: str, test_results: Dict[str, Any], 
                                    data_context: str) -> str:
        """
        解释统计检验结果（统计分析页面）
        
        Args:
            test_type: 检验类型
            test_results: 检验结果
            data_context: 数据上下文
            
        Returns:
            str: 结果解释
        """
        template = ChatPromptTemplate.from_messages([
            ("human", """
            你是一位统计学专家，正在帮助用户理解统计检验结果。请根据以下信息提供专业的解释：
            
            🔬 检验信息：
            - 检验类型：{test_type}
            - 数据上下文：{data_context}
            
            📊 检验结果：
            {test_results}
            
            请从以下角度提供专业解释：
            
            1. **结果含义解读**
               - 统计量的含义
               - p值的解释
               - 置信区间说明
            
            2. **统计显著性判断**
               - 显著性水平说明
               - 拒绝或接受原假设
               - 统计意义解释
            
            3. **实际意义分析**
               - 结果的业务含义
               - 实际影响程度
               - 决策支持信息
            
            4. **局限性说明**
               - 检验的假设条件
               - 可能的偏差来源
               - 结果适用范围
            
            5. **进一步分析建议**
               - 补充检验推荐
               - 深入分析方向
               - 验证方法建议
            
            请用中文回答，内容要专业、准确、易懂。使用markdown格式，确保解释清晰。
            """)
        ])
        
        chain = template | self.llm
        result = chain.invoke({
            "test_type": test_type,
            "data_context": data_context,
            "test_results": str(test_results)
        })
        
        return result.content
    
    # ==================== 机器学习页面AI功能 ====================
    
    def suggest_ml_approach(self, data: pd.DataFrame, task_type: str, 
                           target_col: str, feature_cols: List[str]) -> str:
        """
        推荐机器学习方法（机器学习页面）
        
        Args:
            data: 数据框
            task_type: 任务类型（分类/回归/聚类）
            target_col: 目标变量
            feature_cols: 特征变量
            
        Returns:
            str: 机器学习建议
        """
        # 获取数据统计信息
        numeric_stats = data[feature_cols].describe() if feature_cols else {}
        target_distribution = data[target_col].value_counts() if task_type == "分类" else data[target_col].describe()
        
        template = ChatPromptTemplate.from_messages([
            ("human", """
            你是一位机器学习专家，正在帮助用户选择合适的机器学习方法。请根据以下信息提供专业的建议：
            
            🤖 任务信息：
            - 任务类型：{task_type}
            - 目标变量：{target_col}
            - 特征变量：{feature_cols} (共{num_features}个)
            
            📊 数据特征：
            - 数据规模：{data_size}
            - 特征统计：{numeric_stats}
            - 目标分布：{target_distribution}
            
            请从以下角度提供专业建议：
            
            1. **算法推荐**
               - 最适合的算法
               - 算法选择理由
               - 备选方案说明
            
            2. **数据预处理建议**
               - 特征工程方法
               - 数据清洗策略
               - 特征选择建议
            
            3. **模型训练指导**
               - 训练参数设置
               - 验证方法选择
               - 超参数调优策略
            
            4. **评估方法推荐**
               - 评估指标选择
               - 交叉验证设置
               - 模型比较方法
            
            5. **实施步骤规划**
               - 详细的操作流程
               - 关键节点检查
               - 风险控制建议
            
            请用中文回答，内容要专业、具体、可操作。使用markdown格式，提供实用的建议。
            """)
        ])
        
        chain = template | self.llm
        result = chain.invoke({
            "task_type": task_type,
            "target_col": target_col,
            "feature_cols": str(feature_cols),
            "num_features": len(feature_cols),
            "data_size": f"{len(data)}行 × {len(data.columns)}列",
            "numeric_stats": str(numeric_stats),
            "target_distribution": str(target_distribution)
        })
        
        return result.content
    
    def interpret_ml_results(self, task_type: str, model_results: Dict[str, Any], 
                           feature_importance: Optional[Dict[str, float]] = None) -> str:
        """
        解释机器学习结果（机器学习页面）
        
        Args:
            task_type: 任务类型
            model_results: 模型结果
            feature_importance: 特征重要性
            
        Returns:
            str: 结果解释
        """
        template = ChatPromptTemplate.from_messages([
            ("human", """
            你是一位机器学习专家，正在帮助用户理解机器学习模型的结果。请根据以下信息提供专业的解释：
            
            🤖 模型信息：
            - 任务类型：{task_type}
            - 模型结果：{model_results}
            - 特征重要性：{feature_importance}
            
            请从以下角度提供专业解释：
            
            1. **模型性能评估**
               - 性能指标解读
               - 模型表现评价
               - 与基准比较
            
            2. **结果可靠性分析**
               - 过拟合/欠拟合检查
               - 泛化能力评估
               - 稳定性分析
            
            3. **特征重要性解释**
               - 关键特征识别
               - 特征影响程度
               - 业务意义分析
            
            4. **模型局限性**
               - 假设条件说明
               - 适用范围限制
               - 潜在偏差分析
            
            5. **应用建议**
               - 实际应用指导
               - 部署注意事项
               - 持续优化建议
            
            请用中文回答，内容要专业、准确、实用。使用markdown格式，确保解释清晰易懂。
            """)
        ])
        
        chain = template | self.llm
        result = chain.invoke({
            "task_type": task_type,
            "model_results": str(model_results),
            "feature_importance": str(feature_importance) if feature_importance else "无特征重要性信息"
        })
        
        return result.content
    
    # ==================== 报告生成页面AI功能 ====================
    
    def suggest_report_structure(self, data: pd.DataFrame, analysis_summary: Dict[str, Any]) -> str:
        """
        建议报告结构（报告生成页面）
        
        Args:
            data: 数据框
            analysis_summary: 分析总结
            
        Returns:
            str: 报告结构建议
        """
        template = ChatPromptTemplate.from_messages([
            ("human", """
            你是一位数据分析报告专家，正在帮助用户设计专业的分析报告。请根据以下信息提供报告结构建议：
            
            📊 数据信息：
            - 数据规模：{data_size}
            - 数据类型：{data_types}
            
            📈 分析总结：
            {analysis_summary}
            
            请从以下角度提供专业建议：
            
            1. **报告结构设计**
               - 章节组织建议
               - 内容逻辑顺序
               - 重点突出策略
            
            2. **关键内容规划**
               - 核心发现展示
               - 数据支撑要求
               - 结论建议框架
            
            3. **可视化设计**
               - 图表类型选择
               - 展示顺序安排
               - 视觉效果优化
            
            4. **受众适配建议**
               - 技术深度调整
               - 语言风格建议
               - 重点内容突出
            
            5. **报告质量提升**
               - 专业术语使用
               - 逻辑清晰度
               - 可读性优化
            
            请用中文回答，内容要专业、全面、实用。使用markdown格式，提供具体的报告建议。
            """)
        ])
        
        chain = template | self.llm
        result = chain.invoke({
            "data_size": f"{len(data)}行 × {len(data.columns)}列",
            "data_types": str(data.dtypes.value_counts().to_dict()),
            "analysis_summary": str(analysis_summary)
        })
        
        return result.content
    
    # ==================== 通用智能问答功能 ====================
    
    def answer_data_question(self, question: str, data_context: str, 
                           current_page: str = "通用") -> str:
        """
        回答数据相关问题（通用功能）
        
        Args:
            question: 用户问题
            data_context: 数据上下文
            current_page: 当前页面
            
        Returns:
            str: 回答
        """
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
        
        return result.content


# 全局AI助手实例
ai_assistant = None

def get_ai_assistant() -> Optional[DataAnalysisAI]:
    """
    获取AI助手实例
    
    Returns:
        DataAnalysisAI实例或None
    """
    global ai_assistant
    if ai_assistant is None:
        try:
            ai_assistant = DataAnalysisAI()
        except ValueError as e:
            print(f"AI助手创建失败 - 配置错误: {e}")
            return None
        except Exception as e:
            print(f"AI助手创建失败 - 其他错误: {e}")
            return None
    return ai_assistant
