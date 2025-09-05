"""
智能引导系统
提供上下文相关的帮助和指导，参考Tableau、Power BI等产品的引导体验
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, List, Optional
import json


class SmartGuide:
    """智能引导系统"""
    
    def __init__(self):
        """初始化智能引导系统"""
        self.setup_guide_data()
        self.setup_session_state()
    
    def setup_guide_data(self):
        """设置引导数据"""
        self.guides = {
            "数据上传": {
                "title": "📁 数据上传指南",
                "steps": [
                    "选择数据文件（支持CSV、Excel、JSON等格式）",
                    "预览数据基本信息",
                    "确认数据类型和格式",
                    "开始数据分析"
                ],
                "tips": [
                    "💡 建议文件大小不超过100MB",
                    "💡 确保数据格式正确",
                    "💡 检查编码格式（建议UTF-8）"
                ]
            },
            "数据清洗": {
                "title": "🧹 数据清洗指南",
                "steps": [
                    "检查数据质量（缺失值、异常值）",
                    "处理缺失值（删除或填充）",
                    "处理异常值（识别和处理）",
                    "数据类型转换",
                    "删除重复数据"
                ],
                "tips": [
                    "💡 缺失值比例超过50%的列建议删除",
                    "💡 使用IQR方法识别异常值",
                    "💡 注意保持数据一致性"
                ]
            },
            "数据可视化": {
                "title": "📊 数据可视化指南",
                "steps": [
                    "选择合适的图表类型",
                    "设置图表参数",
                    "调整样式和布局",
                    "添加标题和标签",
                    "导出图表"
                ],
                "tips": [
                    "💡 数值变量适合柱状图、散点图",
                    "💡 分类变量适合饼图、条形图",
                    "💡 时间序列适合折线图",
                    "💡 多变量关系适合热力图"
                ]
            },
            "机器学习": {
                "title": "🤖 机器学习指南",
                "steps": [
                    "选择任务类型（分类/回归/聚类）",
                    "选择特征变量和目标变量",
                    "数据预处理和特征工程",
                    "选择算法和参数",
                    "训练和评估模型",
                    "结果解释和部署"
                ],
                "tips": [
                    "💡 数据量越大，模型效果越好",
                    "💡 特征工程是成功的关键",
                    "💡 使用交叉验证避免过拟合",
                    "💡 注意特征的重要性分析"
                ]
            },
            "统计分析": {
                "title": "📈 统计分析指南",
                "steps": [
                    "描述性统计分析",
                    "数据分布检验",
                    "相关性分析",
                    "假设检验",
                    "结果解释和报告"
                ],
                "tips": [
                    "💡 先进行描述性统计了解数据",
                    "💡 检查数据是否符合正态分布",
                    "💡 注意相关性和因果关系的区别",
                    "💡 选择合适的显著性水平"
                ]
            }
        }
    
    def setup_session_state(self):
        """设置会话状态"""
        if 'guide_history' not in st.session_state:
            st.session_state.guide_history = []
        
        if 'current_guide' not in st.session_state:
            st.session_state.current_guide = None
        
        if 'guide_completed' not in st.session_state:
            st.session_state.guide_completed = {}
    
    def render_contextual_help(self, current_page: str, data: Optional[pd.DataFrame] = None):
        """渲染上下文相关帮助"""
        st.sidebar.markdown("### 🎯 智能引导")
        
        # 根据当前页面和数据状态提供帮助
        if current_page == "📁 数据上传":
            self.render_upload_guide()
        elif current_page == "🧹 数据清洗":
            self.render_cleaning_guide(data)
        elif current_page == "📊 高级可视化":
            self.render_visualization_guide(data)
        elif current_page == "🤖 机器学习":
            self.render_ml_guide(data)
        elif current_page == "📊 统计分析":
            self.render_stats_guide(data)
        else:
            self.render_general_guide()
    
    def render_upload_guide(self):
        """渲染数据上传引导"""
        guide = self.guides["数据上传"]
        
        st.sidebar.markdown(f"**{guide['title']}**")
        
        for i, step in enumerate(guide['steps'], 1):
            st.sidebar.markdown(f"{i}. {step}")
        
        st.sidebar.markdown("**💡 小贴士**")
        for tip in guide['tips']:
            st.sidebar.markdown(tip)
        
        if st.sidebar.button("✅ 完成上传", key="complete_upload"):
            self.mark_guide_completed("数据上传")
            st.sidebar.success("上传指南已完成！")
    
    def render_cleaning_guide(self, data: Optional[pd.DataFrame]):
        """渲染数据清洗引导"""
        guide = self.guides["数据清洗"]
        
        st.sidebar.markdown(f"**{guide['title']}**")
        
        if data is not None:
            # 基于数据状态提供具体建议
            missing_ratio = data.isnull().sum().sum() / (len(data) * len(data.columns))
            duplicate_ratio = data.duplicated().sum() / len(data)
            
            if missing_ratio > 0.1:
                st.sidebar.warning(f"⚠️ 缺失值较多 ({missing_ratio:.1%})，建议优先处理")
            
            if duplicate_ratio > 0.05:
                st.sidebar.warning(f"⚠️ 重复数据较多 ({duplicate_ratio:.1%})，建议删除")
        
        for i, step in enumerate(guide['steps'], 1):
            st.sidebar.markdown(f"{i}. {step}")
        
        st.sidebar.markdown("**💡 小贴士**")
        for tip in guide['tips']:
            st.sidebar.markdown(tip)
    
    def render_visualization_guide(self, data: Optional[pd.DataFrame]):
        """渲染可视化引导"""
        guide = self.guides["数据可视化"]
        
        st.sidebar.markdown(f"**{guide['title']}**")
        
        if data is not None:
            # 基于数据类型推荐图表
            numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
            categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
            
            st.sidebar.markdown("**📊 推荐图表**")
            if len(numeric_cols) >= 2:
                st.sidebar.markdown("• 散点图：分析变量关系")
                st.sidebar.markdown("• 相关性热力图：多变量关系")
            
            if len(categorical_cols) > 0:
                st.sidebar.markdown("• 柱状图：分类变量频次")
                st.sidebar.markdown("• 饼图：比例分布")
        
        for i, step in enumerate(guide['steps'], 1):
            st.sidebar.markdown(f"{i}. {step}")
        
        st.sidebar.markdown("**💡 小贴士**")
        for tip in guide['tips']:
            st.sidebar.markdown(tip)
    
    def render_ml_guide(self, data: Optional[pd.DataFrame]):
        """渲染机器学习引导"""
        guide = self.guides["机器学习"]
        
        st.sidebar.markdown(f"**{guide['title']}**")
        
        if data is not None:
            # 基于数据特征提供建议
            n_samples = len(data)
            n_features = len(data.columns)
            
            st.sidebar.markdown("**📊 数据评估**")
            if n_samples < 100:
                st.sidebar.warning("⚠️ 数据量较少，建议收集更多数据")
            elif n_samples > 10000:
                st.sidebar.success("✅ 数据量充足，适合复杂模型")
            
            if n_features > 20:
                st.sidebar.info("ℹ️ 特征较多，建议进行特征选择")
        
        for i, step in enumerate(guide['steps'], 1):
            st.sidebar.markdown(f"{i}. {step}")
        
        st.sidebar.markdown("**💡 小贴士**")
        for tip in guide['tips']:
            st.sidebar.markdown(tip)
    
    def render_stats_guide(self, data: Optional[pd.DataFrame]):
        """渲染统计分析引导"""
        guide = self.guides["统计分析"]
        
        st.sidebar.markdown(f"**{guide['title']}**")
        
        if data is not None:
            # 基于数据特征提供建议
            numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
            
            st.sidebar.markdown("**📊 分析建议**")
            if len(numeric_cols) >= 2:
                st.sidebar.markdown("• 进行相关性分析")
                st.sidebar.markdown("• 检查数据分布")
            
            if len(numeric_cols) > 0:
                st.sidebar.markdown("• 描述性统计")
                st.sidebar.markdown("• 异常值检测")
        
        for i, step in enumerate(guide['steps'], 1):
            st.sidebar.markdown(f"{i}. {step}")
        
        st.sidebar.markdown("**💡 小贴士**")
        for tip in guide['tips']:
            st.sidebar.markdown(tip)
    
    def render_general_guide(self):
        """渲染通用引导"""
        st.sidebar.markdown("**🎯 快速开始**")
        
        st.sidebar.markdown("""
        1. **📁 上传数据** - 支持多种格式
        2. **🔍 数据探索** - 了解数据特征
        3. **🧹 数据清洗** - 处理质量问题
        4. **📊 可视化** - 创建图表
        5. **🤖 机器学习** - 建模分析
        6. **📈 统计分析** - 深入分析
        """)
        
        st.sidebar.markdown("**💡 使用技巧**")
        st.sidebar.markdown("• 使用AI助手获取智能建议")
        st.sidebar.markdown("• 保存常用的分析流程")
        st.sidebar.markdown("• 导出分析报告")
    
    def render_interactive_tutorial(self, topic: str):
        """渲染交互式教程"""
        st.markdown(f"## 🎓 {topic} 交互式教程")
        
        if topic == "数据上传":
            self.render_upload_tutorial()
        elif topic == "数据清洗":
            self.render_cleaning_tutorial()
        elif topic == "数据可视化":
            self.render_visualization_tutorial()
        elif topic == "机器学习":
            self.render_ml_tutorial()
    
    def render_upload_tutorial(self):
        """渲染数据上传教程"""
        st.markdown("""
        ### 📁 数据上传教程
        
        **步骤1：选择文件**
        - 点击"浏览文件"按钮
        - 选择您的数据文件
        - 支持格式：CSV、Excel、JSON、Parquet等
        
        **步骤2：预览数据**
        - 查看数据基本信息
        - 检查数据类型
        - 确认数据格式正确
        
        **步骤3：开始分析**
        - 点击"开始分析"按钮
        - 系统将自动进行初步分析
        - 获取AI智能建议
        """)
        
        # 示例数据
        if st.button("📊 查看示例数据"):
            import pandas as pd
            import numpy as np
            
            # 创建示例数据
            np.random.seed(42)
            sample_data = pd.DataFrame({
                '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
                '年龄': np.random.randint(20, 60, 5),
                '工资': np.random.randint(3000, 15000, 5),
                '部门': ['技术', '销售', '技术', '人事', '财务'],
                '评分': np.random.uniform(3.0, 5.0, 5)
            })
            
            st.dataframe(sample_data)
            st.success("✅ 这是示例数据，您可以上传自己的数据文件")
    
    def render_cleaning_tutorial(self):
        """渲染数据清洗教程"""
        st.markdown("""
        ### 🧹 数据清洗教程
        
        **常见问题及解决方案：**
        
        **1. 缺失值处理**
        - 删除：缺失比例小时直接删除
        - 填充：用均值、中位数或众数填充
        - 插值：时间序列数据使用插值
        
        **2. 异常值处理**
        - IQR方法：识别和处理异常值
        - Z-score方法：基于标准差识别
        - 可视化检查：使用箱线图识别
        
        **3. 数据类型转换**
        - 字符串转数值：处理数值型字符串
        - 日期转换：统一日期格式
        - 分类编码：将分类变量编码
        """)
    
    def render_visualization_tutorial(self):
        """渲染数据可视化教程"""
        st.markdown("""
        ### 📊 数据可视化教程
        
        **图表类型选择指南：**
        
        **1. 分布分析**
        - 直方图：查看数值变量分布
        - 箱线图：识别异常值和分布特征
        - 密度图：平滑的分布曲线
        
        **2. 关系分析**
        - 散点图：两个数值变量关系
        - 相关性热力图：多个变量相关性
        - 气泡图：三个变量关系
        
        **3. 分类数据**
        - 柱状图：分类变量频次
        - 饼图：比例分布
        - 条形图：水平展示
        """)
    
    def render_ml_tutorial(self):
        """渲染机器学习教程"""
        st.markdown("""
        ### 🤖 机器学习教程
        
        **机器学习流程：**
        
        **1. 问题定义**
        - 明确预测目标
        - 确定任务类型（分类/回归/聚类）
        - 定义成功标准
        
        **2. 数据准备**
        - 数据收集和清洗
        - 特征工程
        - 数据分割（训练/测试）
        
        **3. 模型选择**
        - 分类：随机森林、逻辑回归、SVM
        - 回归：线性回归、随机森林、SVR
        - 聚类：K-means、层次聚类
        """)
    
    def mark_guide_completed(self, guide_name: str):
        """标记引导完成"""
        st.session_state.guide_completed[guide_name] = True
        st.session_state.guide_history.append(f"完成{guide_name}引导")
    
    def get_guide_progress(self) -> Dict[str, bool]:
        """获取引导进度"""
        return st.session_state.guide_completed
    
    def render_guide_progress(self):
        """渲染引导进度"""
        progress = self.get_guide_progress()
        
        if progress:
            st.sidebar.markdown("### 📈 学习进度")
            
            for guide_name, completed in progress.items():
                status = "✅" if completed else "⏳"
                st.sidebar.markdown(f"{status} {guide_name}")
    
    def render_quick_tips(self, current_page: str):
        """渲染快速提示"""
        tips_map = {
            "📁 数据上传": [
                "💡 支持拖拽上传文件",
                "💡 大文件建议使用CSV格式",
                "💡 检查文件编码格式"
            ],
            "🧹 数据清洗": [
                "💡 先处理缺失值再处理异常值",
                "💡 保存清洗后的数据",
                "💡 记录清洗步骤"
            ],
            "📊 高级可视化": [
                "💡 选择合适的图表类型",
                "💡 注意颜色搭配",
                "💡 添加适当的标题和标签"
            ],
            "🤖 机器学习": [
                "💡 从简单模型开始",
                "💡 使用交叉验证",
                "💡 注意特征重要性"
            ]
        }
        
        if current_page in tips_map:
            st.sidebar.markdown("### 💡 快速提示")
            for tip in tips_map[current_page]:
                st.sidebar.markdown(tip)


# 全局智能引导实例
smart_guide = SmartGuide()

def get_smart_guide():
    """获取智能引导实例"""
    return smart_guide
