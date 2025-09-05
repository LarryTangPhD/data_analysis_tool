"""
用户体验优化模块
提供用户引导、反馈系统、帮助文档等功能
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Optional, Any, Callable
import json
import time
from datetime import datetime, timedelta
import os

class UserGuide:
    """用户引导系统"""
    
    def __init__(self):
        self.guides = {
            "数据上传": {
                "title": "📁 数据上传指南",
                "steps": [
                    "选择支持的文件格式（CSV、Excel、JSON、Parquet）",
                    "确保数据格式整洁，编码为UTF-8",
                    "避免特殊字符在列名中",
                    "建议文件大小不超过100MB"
                ],
                "tips": [
                    "💡 首次使用建议上传小型数据集进行测试",
                    "💡 检查数据是否包含表头",
                    "💡 确保数值列格式正确"
                ]
            },
            "数据清洗": {
                "title": "🧹 数据清洗指南",
                "steps": [
                    "检查并处理缺失值",
                    "删除重复行",
                    "处理异常值",
                    "标准化数据格式"
                ],
                "tips": [
                    "💡 缺失值处理前先分析缺失模式",
                    "💡 异常值处理要结合业务背景",
                    "💡 保留原始数据备份"
                ]
            },
            "可视化": {
                "title": "📈 可视化指南",
                "steps": [
                    "选择合适的图表类型",
                    "设置合适的颜色方案",
                    "添加标题和标签",
                    "优化图表布局"
                ],
                "tips": [
                    "💡 柱状图适合分类数据比较",
                    "💡 散点图适合相关性分析",
                    "💡 时间序列图适合趋势分析"
                ]
            },
            "机器学习": {
                "title": "🤖 机器学习指南",
                "steps": [
                    "选择合适的问题类型（分类/回归/聚类）",
                    "准备特征和目标变量",
                    "选择合适的算法",
                    "评估模型性能"
                ],
                "tips": [
                    "💡 分类问题需要分类型目标变量",
                    "💡 回归问题需要数值型目标变量",
                    "💡 特征工程能显著提升模型性能"
                ]
            }
        }
    
    def show_guide(self, guide_key: str):
        """显示用户引导"""
        if guide_key not in self.guides:
            st.warning("未找到对应的引导信息")
            return
        
        guide = self.guides[guide_key]
        
        st.markdown(f"## {guide['title']}")
        
        st.markdown("### 📋 操作步骤")
        for i, step in enumerate(guide['steps'], 1):
            st.markdown(f"{i}. {step}")
        
        st.markdown("### 💡 实用技巧")
        for tip in guide['tips']:
            st.markdown(tip)
    
    def show_quick_tips(self):
        """显示快速提示"""
        st.sidebar.markdown("### 💡 快速提示")
        
        tips = [
            "🎯 使用AI助手获取专业建议",
            "📊 尝试不同的可视化类型",
            "🔍 利用数据洞察功能深入分析",
            "⚡ 大数据集可使用性能优化功能"
        ]
        
        for tip in tips:
            st.sidebar.info(tip)

class FeedbackSystem:
    """用户反馈系统"""
    
    def __init__(self, feedback_file: str = "feedback.json"):
        self.feedback_file = feedback_file
        self.feedback_data = self._load_feedback()
    
    def _load_feedback(self) -> Dict[str, Any]:
        """加载反馈数据"""
        if os.path.exists(self.feedback_file):
            try:
                with open(self.feedback_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {"feedbacks": [], "ratings": [], "suggestions": []}
        return {"feedbacks": [], "ratings": [], "suggestions": []}
    
    def _save_feedback(self):
        """保存反馈数据"""
        with open(self.feedback_file, 'w', encoding='utf-8') as f:
            json.dump(self.feedback_data, f, ensure_ascii=False, indent=2)
    
    def collect_feedback(self):
        """收集用户反馈"""
        st.markdown("## 📝 用户反馈")
        
        # 功能评分
        st.markdown("### ⭐ 功能评分")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        ratings = {}
        with col1:
            ratings["数据上传"] = st.slider("数据上传", 1, 5, 3, key="rating_upload")
        with col2:
            ratings["数据清洗"] = st.slider("数据清洗", 1, 5, 3, key="rating_cleaning")
        with col3:
            ratings["可视化"] = st.slider("可视化", 1, 5, 3, key="rating_viz")
        with col4:
            ratings["机器学习"] = st.slider("机器学习", 1, 5, 3, key="rating_ml")
        with col5:
            ratings["AI助手"] = st.slider("AI助手", 1, 5, 3, key="rating_ai")
        
        # 总体评分
        overall_rating = st.slider("总体评分", 1, 5, 3, key="rating_overall")
        
        # 反馈内容
        feedback_text = st.text_area(
            "请分享您的使用体验和建议：",
            placeholder="您的反馈对我们很重要！请告诉我们您的使用体验、遇到的问题或改进建议...",
            height=150
        )
        
        # 联系方式（可选）
        contact_info = st.text_input(
            "联系方式（可选）：",
            placeholder="邮箱或微信号，用于后续沟通"
        )
        
        if st.button("📤 提交反馈", type="primary"):
            if feedback_text.strip():
                feedback = {
                    "timestamp": datetime.now().isoformat(),
                    "ratings": ratings,
                    "overall_rating": overall_rating,
                    "feedback": feedback_text,
                    "contact": contact_info
                }
                
                self.feedback_data["feedbacks"].append(feedback)
                self._save_feedback()
                
                st.success("✅ 感谢您的反馈！我们会认真考虑您的建议。")
                
                # 显示反馈统计
                self.show_feedback_stats()
            else:
                st.warning("请填写反馈内容")
    
    def show_feedback_stats(self):
        """显示反馈统计"""
        if not self.feedback_data["feedbacks"]:
            return
        
        st.markdown("### 📊 反馈统计")
        
        # 计算平均评分
        overall_ratings = [f["overall_rating"] for f in self.feedback_data["feedbacks"]]
        avg_rating = sum(overall_ratings) / len(overall_ratings)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("总反馈数", len(self.feedback_data["feedbacks"]))
        with col2:
            st.metric("平均评分", f"{avg_rating:.1f}/5")
        with col3:
            st.metric("最新反馈", datetime.fromisoformat(
                self.feedback_data["feedbacks"][-1]["timestamp"]
            ).strftime("%m-%d"))

class HelpSystem:
    """帮助系统"""
    
    def __init__(self):
        self.help_topics = {
            "快速开始": {
                "content": """
                ## 🚀 快速开始指南
                
                ### 1. 上传数据
                - 支持CSV、Excel、JSON、Parquet格式
                - 确保数据格式整洁，编码为UTF-8
                - 建议文件大小不超过100MB
                
                ### 2. 选择分析模式
                - **新手模式**：简化的操作界面，适合初学者
                - **普通模式**：完整功能集，适合有一定经验的用户
                - **专业模式**：高级功能，适合专业数据分析师
                
                ### 3. 开始分析
                - 使用数据清洗功能处理数据质量问题
                - 利用可视化功能探索数据特征
                - 应用机器学习算法进行建模分析
                - 生成专业分析报告
                """,
                "icon": "🚀"
            },
            "功能说明": {
                "content": """
                ## 📋 功能说明
                
                ### 📁 数据上传
                - 支持多种文件格式
                - 自动数据格式检测
                - 数据质量初步评估
                
                ### 🧹 数据清洗
                - 缺失值处理
                - 重复值删除
                - 异常值检测和处理
                - 数据类型转换
                
                ### 📈 可视化分析
                - 20+种图表类型
                - 交互式图表
                - 3D可视化
                - 自定义样式
                
                ### 🤖 机器学习
                - 分类算法
                - 回归算法
                - 聚类分析
                - 特征工程
                
                ### 👁️ 数据洞察
                - 自动数据分析
                - 专业报告生成
                - AI智能建议
                """,
                "icon": "📋"
            },
            "常见问题": {
                "content": """
                ## ❓ 常见问题
                
                ### Q: 支持哪些数据格式？
                A: 支持CSV、Excel(.xlsx/.xls)、JSON、Parquet格式。
                
                ### Q: 数据文件大小有限制吗？
                A: 建议文件大小不超过100MB，过大的文件可能影响加载速度。
                
                ### Q: 如何处理缺失值？
                A: 可以使用删除、填充等方法，具体选择要根据业务背景。
                
                ### Q: AI助手如何使用？
                A: 在相应页面点击"获取AI建议"按钮，系统会自动分析并提供专业建议。
                
                ### Q: 如何导出分析结果？
                A: 在报告生成页面可以选择多种格式导出，包括PDF、HTML、Markdown等。
                """,
                "icon": "❓"
            },
            "高级技巧": {
                "content": """
                ## 🎯 高级技巧
                
                ### 数据预处理技巧
                - 使用数据洞察功能快速了解数据特征
                - 结合业务背景选择合适的清洗策略
                - 保留原始数据备份
                
                ### 可视化技巧
                - 选择合适的图表类型传达信息
                - 使用一致的配色方案
                - 添加适当的标题和标签
                
                ### 机器学习技巧
                - 特征工程是提升模型性能的关键
                - 使用交叉验证评估模型
                - 注意过拟合问题
                
                ### 性能优化
                - 大数据集可使用性能优化功能
                - 合理使用缓存功能
                - 定期清理内存
                """,
                "icon": "🎯"
            }
        }
    
    def show_help_page(self):
        """显示帮助页面"""
        st.markdown("## 📚 帮助中心")
        
        # 选择帮助主题
        topic = st.selectbox(
            "选择帮助主题：",
            list(self.help_topics.keys())
        )
        
        if topic in self.help_topics:
            help_content = self.help_topics[topic]
            st.markdown(f"### {help_content['icon']} {topic}")
            st.markdown(help_content['content'])
    
    def show_context_help(self, context: str):
        """显示上下文帮助"""
        context_help = {
            "数据上传": "💡 提示：确保数据格式整洁，检查编码格式，避免特殊字符在列名中",
            "数据清洗": "💡 提示：先分析数据质量，选择合适的清洗策略，保留原始数据备份",
            "可视化": "💡 提示：根据数据类型选择合适的图表，注意颜色搭配和标签设置",
            "机器学习": "💡 提示：选择合适的算法，注意特征工程，使用交叉验证评估模型"
        }
        
        if context in context_help:
            st.info(context_help[context])

class ProgressTracker:
    """进度跟踪器"""
    
    def __init__(self):
        self.progress_data = {}
    
    def start_progress(self, task_name: str, total_steps: int):
        """开始进度跟踪"""
        self.progress_data[task_name] = {
            "total": total_steps,
            "current": 0,
            "start_time": time.time(),
            "steps": []
        }
    
    def update_progress(self, task_name: str, step_name: str, step_description: str = ""):
        """更新进度"""
        if task_name in self.progress_data:
            self.progress_data[task_name]["current"] += 1
            self.progress_data[task_name]["steps"].append({
                "name": step_name,
                "description": step_description,
                "timestamp": time.time()
            })
    
    def show_progress(self, task_name: str):
        """显示进度"""
        if task_name not in self.progress_data:
            return
        
        progress = self.progress_data[task_name]
        current = progress["current"]
        total = progress["total"]
        
        # 进度条
        progress_percent = current / total
        st.progress(progress_percent)
        st.write(f"**进度**: {current}/{total} ({progress_percent:.1%})")
        
        # 当前步骤
        if progress["steps"]:
            current_step = progress["steps"][-1]
            st.info(f"🔄 当前步骤: {current_step['name']}")
            if current_step['description']:
                st.write(f"*{current_step['description']}*")
        
        # 预计剩余时间
        if current > 0:
            elapsed_time = time.time() - progress["start_time"]
            avg_time_per_step = elapsed_time / current
            remaining_steps = total - current
            estimated_remaining = avg_time_per_step * remaining_steps
            
            st.write(f"⏱️ 预计剩余时间: {estimated_remaining:.1f}秒")
    
    def complete_progress(self, task_name: str):
        """完成进度跟踪"""
        if task_name in self.progress_data:
            total_time = time.time() - self.progress_data[task_name]["start_time"]
            st.success(f"✅ 任务完成！总耗时: {total_time:.1f}秒")
            del self.progress_data[task_name]

class NotificationSystem:
    """通知系统"""
    
    def __init__(self):
        self.notifications = []
    
    def add_notification(self, message: str, level: str = "info", duration: int = 5):
        """添加通知"""
        notification = {
            "message": message,
            "level": level,
            "timestamp": time.time(),
            "duration": duration
        }
        self.notifications.append(notification)
    
    def show_notifications(self):
        """显示通知"""
        current_time = time.time()
        
        # 过滤过期通知
        self.notifications = [
            n for n in self.notifications 
            if current_time - n["timestamp"] < n["duration"]
        ]
        
        # 显示当前通知
        for notification in self.notifications:
            if notification["level"] == "success":
                st.success(notification["message"])
            elif notification["level"] == "warning":
                st.warning(notification["message"])
            elif notification["level"] == "error":
                st.error(notification["message"])
            else:
                st.info(notification["message"])

# 全局实例
user_guide = UserGuide()
feedback_system = FeedbackSystem()
help_system = HelpSystem()
progress_tracker = ProgressTracker()
notification_system = NotificationSystem()

def render_user_experience_components():
    """渲染用户体验组件"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎯 用户体验")
    
    # 快速帮助
    if st.sidebar.button("❓ 快速帮助"):
        help_system.show_context_help("数据上传")
    
    # 用户引导
    guide_option = st.sidebar.selectbox(
        "📚 用户引导",
        ["选择引导", "数据上传", "数据清洗", "可视化", "机器学习"]
    )
    
    if guide_option != "选择引导":
        user_guide.show_guide(guide_option)
    
    # 反馈系统
    if st.sidebar.button("📝 用户反馈"):
        feedback_system.collect_feedback()
    
    # 帮助中心
    if st.sidebar.button("📚 帮助中心"):
        help_system.show_help_page()
    
    # 显示快速提示
    user_guide.show_quick_tips()
