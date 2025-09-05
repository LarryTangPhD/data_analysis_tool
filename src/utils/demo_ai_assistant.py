"""
演示用AI助手模块
提供本地AI建议功能，不依赖外部API
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, Any, List


class DemoAI:
    """演示用AI助手类"""
    
    def __init__(self):
        """初始化演示AI助手"""
        self.name = "数眸AI助手（演示版）"
    
    def analyze_uploaded_data(self, data: pd.DataFrame, data_info: Dict[str, Any]) -> str:
        """
        分析上传的数据并提供建议
        
        Args:
            data: 数据框
            data_info: 数据基本信息
            
        Returns:
            str: 分析建议
        """
        # 计算数据特征
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
        missing_ratio = data.isnull().sum().sum() / (len(data) * len(data.columns))
        
        # 生成分析建议
        analysis = f"""
# 📊 数据初步分析报告

## 📋 数据概览
- **数据集大小**: {data_info['rows']} 行 × {data_info['columns']} 列
- **内存使用**: {data_info['memory_usage']} MB
- **缺失值**: {data_info['missing_values']} 个 ({missing_ratio:.1%})
- **重复行**: {data_info['duplicate_rows']} 行

## 🔍 数据类型分析
- **数值型列**: {len(numeric_cols)} 列
- **分类型列**: {len(categorical_cols)} 列

## 📈 数据质量评估

### 完整性评分: {max(0, 100 - missing_ratio * 100):.0f}/100
"""
        
        if missing_ratio < 0.05:
            analysis += "- ✅ 数据完整性良好，缺失值较少\n"
        elif missing_ratio < 0.2:
            analysis += "- ⚠️ 数据完整性一般，需要处理缺失值\n"
        else:
            analysis += "- ❌ 数据完整性较差，缺失值较多\n"
        
        analysis += f"""
### 数据规模评估: {'大规模' if len(data) > 10000 else '中等规模' if len(data) > 1000 else '小规模'}
- 适合进行{'深度分析' if len(data) > 10000 else '常规分析' if len(data) > 1000 else '快速分析'}

## 🎯 分析建议

### 1. 数据清洗优先级
"""
        
        if missing_ratio > 0.1:
            analysis += "- 🔥 **高优先级**: 处理缺失值\n"
        if data_info['duplicate_rows'] > 0:
            analysis += "- 🔥 **高优先级**: 删除重复行\n"
        
        analysis += """
### 2. 推荐的分析流程
1. **数据探索**: 使用描述性统计了解数据分布
2. **数据清洗**: 处理缺失值和异常值
3. **特征分析**: 分析变量间的关系
4. **可视化**: 创建图表展示数据特征
"""
        
        if len(numeric_cols) >= 2:
            analysis += "5. **建模准备**: 数据适合进行机器学习分析\n"
        
        analysis += """
### 3. 可视化建议
- 📊 使用直方图查看数值变量分布
- 📈 使用散点图分析变量间关系
- 🥧 使用饼图展示分类变量分布
- 🔥 使用热力图分析相关性

### 4. 注意事项
- 确保数据类型正确
- 检查异常值
- 考虑数据标准化
- 保存清洗后的数据

---
*由数眸AI助手生成的分析报告*
"""
        
        return analysis
    
    def suggest_ml_approach(self, data: pd.DataFrame, task_type: str, 
                           target_col: str, feature_cols: List[str]) -> str:
        """
        建议机器学习方法
        
        Args:
            data: 数据框
            task_type: 任务类型
            target_col: 目标变量
            feature_cols: 特征变量
            
        Returns:
            str: 建议
        """
        n_samples = len(data)
        n_features = len(feature_cols)
        
        suggestion = f"""
# 🤖 机器学习方法建议

## 📊 任务信息
- **任务类型**: {task_type}
- **目标变量**: {target_col}
- **特征数量**: {n_features}
- **样本数量**: {n_samples}

## 🎯 推荐算法

### 对于{task_type}任务，推荐以下算法：

"""
        
        if task_type == "分类":
            suggestion += """
1. **随机森林** ⭐⭐⭐⭐⭐
   - 优点：处理高维数据，自动特征选择
   - 适用：大多数分类问题

2. **逻辑回归** ⭐⭐⭐⭐
   - 优点：可解释性强，训练快速
   - 适用：线性可分问题

3. **支持向量机** ⭐⭐⭐⭐
   - 优点：处理非线性问题
   - 适用：小到中等规模数据集
"""
        elif task_type == "回归":
            suggestion += """
1. **随机森林回归** ⭐⭐⭐⭐⭐
   - 优点：处理非线性关系，鲁棒性强
   - 适用：大多数回归问题

2. **线性回归** ⭐⭐⭐⭐
   - 优点：简单快速，可解释性强
   - 适用：线性关系明显的问题

3. **支持向量回归** ⭐⭐⭐⭐
   - 优点：处理复杂非线性关系
   - 适用：小到中等规模数据集
"""
        
        suggestion += f"""
## ⚙️ 参数建议

### 基于数据特征的建议：
- **样本数量**: {n_samples} {'(适合复杂模型)' if n_samples > 1000 else '(建议使用简单模型)'}
- **特征数量**: {n_features} {'(需要特征选择)' if n_features > 20 else '(特征数量适中)'}

### 推荐参数设置：
```python
# 随机森林参数
n_estimators = {min(100, n_samples // 10)}
max_depth = {min(10, n_features * 2)}
min_samples_split = {max(2, n_samples // 1000)}
```

## 📈 评估指标

### 推荐使用的评估指标：
"""
        
        if task_type == "分类":
            suggestion += """
- **准确率 (Accuracy)**: 整体预测正确率
- **精确率 (Precision)**: 预测为正例中实际为正例的比例
- **召回率 (Recall)**: 实际正例中被正确预测的比例
- **F1分数**: 精确率和召回率的调和平均
"""
        else:
            suggestion += """
- **R²分数**: 模型解释方差的比例
- **均方误差 (MSE)**: 预测误差的平方平均
- **平均绝对误差 (MAE)**: 预测误差的绝对平均
"""
        
        suggestion += """
## 🔄 下一步建议

1. **数据预处理**:
   - 标准化数值特征
   - 编码分类变量
   - 处理缺失值

2. **模型训练**:
   - 使用交叉验证
   - 尝试多种算法
   - 调整超参数

3. **模型评估**:
   - 比较不同模型性能
   - 分析特征重要性
   - 检查过拟合情况

---
*由数眸AI助手生成的机器学习建议*
"""
        
        return suggestion
    
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
        # 简单的关键词匹配回答
        question_lower = question.lower()
        
        if "可视化" in question_lower or "图表" in question_lower:
            return """
# 📊 数据可视化建议

## 🎨 常用图表类型

### 1. 分布分析
- **直方图**: 查看数值变量分布
- **箱线图**: 识别异常值和分布特征
- **密度图**: 平滑的分布曲线

### 2. 关系分析
- **散点图**: 两个数值变量关系
- **相关性热力图**: 多个变量相关性
- **气泡图**: 三个变量关系

### 3. 分类数据
- **柱状图**: 分类变量频次
- **饼图**: 比例分布
- **条形图**: 水平展示

### 4. 时间序列
- **折线图**: 时间趋势
- **面积图**: 累积变化

## 💡 选择建议

根据您的数据特征选择合适的图表：
- 数值变量 → 直方图、箱线图
- 两个变量关系 → 散点图
- 分类数据 → 柱状图、饼图
- 时间数据 → 折线图

---
*由数眸AI助手提供的可视化建议*
"""
        
        elif "清洗" in question_lower or "预处理" in question_lower:
            return """
# 🧹 数据清洗指南

## 🔍 常见问题处理

### 1. 缺失值处理
- **删除**: 缺失比例小时直接删除
- **填充**: 用均值、中位数或众数填充
- **插值**: 时间序列数据使用插值

### 2. 异常值处理
- **IQR方法**: 识别和处理异常值
- **Z-score方法**: 基于标准差识别
- **可视化检查**: 使用箱线图识别

### 3. 数据类型转换
- **字符串转数值**: 处理数值型字符串
- **日期转换**: 统一日期格式
- **分类编码**: 将分类变量编码

### 4. 重复数据处理
- **删除重复行**: 完全重复的数据
- **合并相似记录**: 部分重复数据

## ⚡ 快速清洗步骤

1. 检查数据类型
2. 处理缺失值
3. 识别异常值
4. 删除重复数据
5. 标准化数值变量

---
*由数眸AI助手提供的数据清洗建议*
"""
        
        elif "机器学习" in question_lower or "建模" in question_lower:
            return """
# 🤖 机器学习入门指南

## 🎯 机器学习流程

### 1. 问题定义
- 明确预测目标
- 确定任务类型（分类/回归/聚类）
- 定义成功标准

### 2. 数据准备
- 数据收集和清洗
- 特征工程
- 数据分割（训练/测试）

### 3. 模型选择
- **分类**: 随机森林、逻辑回归、SVM
- **回归**: 线性回归、随机森林、SVR
- **聚类**: K-means、层次聚类

### 4. 模型训练
- 使用训练数据训练模型
- 调整超参数
- 交叉验证

### 5. 模型评估
- 使用测试数据评估
- 分析性能指标
- 检查过拟合

## 💡 实用建议

- 从简单模型开始
- 使用交叉验证
- 注意特征重要性
- 定期重新训练模型

---
*由数眸AI助手提供的机器学习指导*
"""
        
        else:
            return f"""
# 💡 通用数据分析建议

## 📊 当前数据情况
{data_context}

## 🎯 分析建议

### 1. 探索性数据分析
- 查看数据基本统计信息
- 分析数据分布特征
- 检查变量间关系

### 2. 数据质量检查
- 识别缺失值和异常值
- 检查数据类型是否正确
- 评估数据完整性

### 3. 可视化分析
- 创建合适的图表
- 发现数据模式
- 识别潜在问题

### 4. 统计分析
- 进行描述性统计
- 执行假设检验
- 分析相关性

## 🔄 下一步操作

1. 使用"数据概览"功能了解数据
2. 使用"数据清洗"功能处理问题
3. 使用"可视化"功能创建图表
4. 使用"统计分析"功能深入分析

---
*由数眸AI助手提供的通用建议*
"""


# 全局演示AI助手实例
demo_ai = DemoAI()

def get_demo_ai_assistant():
    """
    获取演示AI助手实例
    
    Returns:
        DemoAI: 演示AI助手实例
    """
    return demo_ai
