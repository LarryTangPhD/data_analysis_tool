"""
数据科学工作流管理模块
提供标准化的数据分析流程和最佳实践
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
import streamlit as st
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkflowStage(Enum):
    """工作流阶段枚举"""
    DATA_LOADING = "数据加载"
    DATA_EXPLORATION = "数据探索"
    DATA_CLEANING = "数据清洗"
    FEATURE_ENGINEERING = "特征工程"
    MODELING = "建模分析"
    EVALUATION = "模型评估"
    DEPLOYMENT = "结果部署"

@dataclass
class WorkflowStep:
    """工作流步骤数据类"""
    stage: WorkflowStage
    name: str
    description: str
    completed: bool = False
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    metrics: Dict[str, Any] = None
    artifacts: List[str] = None

class DataScienceWorkflow:
    """数据科学工作流管理器"""
    
    def __init__(self):
        self.steps: List[WorkflowStep] = []
        self.current_step_index = 0
        self.workflow_start_time = datetime.now()
        self.metadata = {}
        
        # 初始化标准工作流
        self._initialize_standard_workflow()
    
    def _initialize_standard_workflow(self):
        """初始化标准数据科学工作流"""
        standard_steps = [
            WorkflowStep(
                stage=WorkflowStage.DATA_LOADING,
                name="数据加载与验证",
                description="加载数据文件，验证数据格式和完整性"
            ),
            WorkflowStep(
                stage=WorkflowStage.DATA_EXPLORATION,
                name="探索性数据分析",
                description="分析数据分布、相关性、缺失值等基本特征"
            ),
            WorkflowStep(
                stage=WorkflowStage.DATA_CLEANING,
                name="数据清洗与预处理",
                description="处理缺失值、异常值、重复值，标准化数据格式"
            ),
            WorkflowStep(
                stage=WorkflowStage.FEATURE_ENGINEERING,
                name="特征工程",
                description="特征选择、转换、创建新特征"
            ),
            WorkflowStep(
                stage=WorkflowStage.MODELING,
                name="模型构建",
                description="选择合适的算法，训练和调优模型"
            ),
            WorkflowStep(
                stage=WorkflowStage.EVALUATION,
                name="模型评估",
                description="使用多种指标评估模型性能"
            ),
            WorkflowStep(
                stage=WorkflowStage.DEPLOYMENT,
                name="结果部署",
                description="生成报告，部署模型或结果"
            )
        ]
        
        self.steps = standard_steps
    
    def start_step(self, step_name: str) -> bool:
        """开始执行工作流步骤"""
        for i, step in enumerate(self.steps):
            if step.name == step_name:
                step.start_time = datetime.now()
                step.completed = False
                self.current_step_index = i
                logger.info(f"开始执行步骤: {step_name}")
                return True
        return False
    
    def complete_step(self, step_name: str, metrics: Dict[str, Any] = None, artifacts: List[str] = None) -> bool:
        """完成工作流步骤"""
        for step in self.steps:
            if step.name == step_name:
                step.end_time = datetime.now()
                step.completed = True
                step.metrics = metrics or {}
                step.artifacts = artifacts or []
                logger.info(f"完成步骤: {step_name}")
                return True
        return False
    
    def get_current_step(self) -> Optional[WorkflowStep]:
        """获取当前步骤"""
        if 0 <= self.current_step_index < len(self.steps):
            return self.steps[self.current_step_index]
        return None
    
    def get_progress(self) -> Dict[str, Any]:
        """获取工作流进度"""
        completed_steps = sum(1 for step in self.steps if step.completed)
        total_steps = len(self.steps)
        progress_percentage = (completed_steps / total_steps) * 100
        
        return {
            "completed_steps": completed_steps,
            "total_steps": total_steps,
            "progress_percentage": progress_percentage,
            "current_step": self.get_current_step(),
            "workflow_duration": datetime.now() - self.workflow_start_time
        }
    
    def get_workflow_summary(self) -> Dict[str, Any]:
        """获取工作流总结"""
        completed_steps = [step for step in self.steps if step.completed]
        pending_steps = [step for step in self.steps if not step.completed]
        
        return {
            "workflow_name": "标准数据科学工作流",
            "start_time": self.workflow_start_time,
            "current_time": datetime.now(),
            "completed_steps": len(completed_steps),
            "pending_steps": len(pending_steps),
            "total_steps": len(self.steps),
            "completion_rate": (len(completed_steps) / len(self.steps)) * 100,
            "completed_step_details": [
                {
                    "name": step.name,
                    "duration": step.end_time - step.start_time if step.end_time and step.start_time else None,
                    "metrics": step.metrics
                }
                for step in completed_steps
            ]
        }

def render_workflow_dashboard(workflow: DataScienceWorkflow):
    """渲染工作流仪表板"""
    st.subheader("📊 数据科学工作流仪表板")
    
    # 获取进度信息
    progress = workflow.get_progress()
    
    # 进度条
    st.progress(progress["progress_percentage"] / 100)
    st.write(f"**进度**: {progress['completed_steps']}/{progress['total_steps']} 步骤完成 ({progress['progress_percentage']:.1f}%)")
    
    # 当前步骤
    current_step = progress["current_step"]
    if current_step:
        st.info(f"**当前步骤**: {current_step.name} - {current_step.description}")
    
    # 工作流步骤列表
    st.subheader("📋 工作流步骤")
    
    for i, step in enumerate(workflow.steps):
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col1:
            if step.completed:
                st.success("✅")
            elif i == workflow.current_step_index:
                st.info("🔄")
            else:
                st.write("⏳")
        
        with col2:
            st.write(f"**{step.name}**")
            st.write(f"*{step.description}*")
            
            if step.completed and step.metrics:
                with st.expander("查看指标"):
                    for metric_name, metric_value in step.metrics.items():
                        st.write(f"• {metric_name}: {metric_value}")
        
        with col3:
            if step.completed and step.start_time and step.end_time:
                duration = step.end_time - step.start_time
                st.write(f"⏱️ {duration.total_seconds():.1f}s")

def create_custom_workflow(workflow_type: str) -> DataScienceWorkflow:
    """创建自定义工作流"""
    workflow = DataScienceWorkflow()
    
    if workflow_type == "快速分析":
        # 简化的快速分析工作流
        quick_steps = [
            WorkflowStep(
                stage=WorkflowStage.DATA_LOADING,
                name="数据加载",
                description="快速加载和验证数据"
            ),
            WorkflowStep(
                stage=WorkflowStage.DATA_EXPLORATION,
                name="快速探索",
                description="基础数据概览和可视化"
            ),
            WorkflowStep(
                stage=WorkflowStage.DEPLOYMENT,
                name="生成报告",
                description="快速生成分析报告"
            )
        ]
        workflow.steps = quick_steps
    
    elif workflow_type == "深度分析":
        # 深度分析工作流，包含更多步骤
        deep_steps = workflow.steps + [
            WorkflowStep(
                stage=WorkflowStage.FEATURE_ENGINEERING,
                name="高级特征工程",
                description="复杂的特征转换和选择"
            ),
            WorkflowStep(
                stage=WorkflowStage.MODELING,
                name="多模型比较",
                description="训练和比较多个模型"
            )
        ]
        workflow.steps = deep_steps
    
    return workflow

def validate_data_for_workflow(data: pd.DataFrame) -> Dict[str, Any]:
    """验证数据是否适合工作流分析"""
    validation_results = {
        "is_valid": True,
        "warnings": [],
        "errors": [],
        "recommendations": []
    }
    
    # 检查数据大小
    if len(data) < 10:
        validation_results["warnings"].append("数据量较少，可能影响分析可靠性")
    
    if len(data.columns) < 2:
        validation_results["errors"].append("数据列数过少，无法进行有效分析")
        validation_results["is_valid"] = False
    
    # 检查缺失值
    missing_ratio = data.isnull().sum().sum() / (len(data) * len(data.columns))
    if missing_ratio > 0.5:
        validation_results["warnings"].append(f"缺失值比例较高 ({missing_ratio:.1%})，建议进行数据清洗")
    
    # 检查数据类型
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) == 0:
        validation_results["warnings"].append("没有数值型列，某些分析功能可能受限")
    
    # 提供建议
    if len(data) > 1000:
        validation_results["recommendations"].append("数据量较大，建议使用采样进行快速探索")
    
    if len(numeric_cols) > 10:
        validation_results["recommendations"].append("特征较多，建议进行特征选择")
    
    return validation_results

def generate_workflow_report(workflow: DataScienceWorkflow, data: pd.DataFrame) -> str:
    """生成工作流报告"""
    summary = workflow.get_workflow_summary()
    
    report = f"""
# 数据科学工作流报告

## 工作流概览
- **工作流名称**: {summary['workflow_name']}
- **开始时间**: {summary['start_time'].strftime('%Y-%m-%d %H:%M:%S')}
- **完成时间**: {summary['current_time'].strftime('%Y-%m-%d %H:%M:%S')}
- **完成率**: {summary['completion_rate']:.1f}%

## 数据集信息
- **数据规模**: {len(data)} 行 × {len(data.columns)} 列
- **数据类型**: {', '.join([f'{dtype}({count})' for dtype, count in data.dtypes.value_counts().items()])}
- **缺失值**: {data.isnull().sum().sum()} 个

## 完成步骤详情
"""
    
    for step_detail in summary['completed_step_details']:
        report += f"""
### {step_detail['name']}
- **执行时长**: {step_detail['duration'].total_seconds():.1f} 秒
"""
        if step_detail['metrics']:
            report += "- **关键指标**:\n"
            for metric_name, metric_value in step_detail['metrics'].items():
                report += f"  - {metric_name}: {metric_value}\n"
    
    return report
