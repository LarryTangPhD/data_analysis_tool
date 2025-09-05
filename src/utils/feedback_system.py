"""
智能反馈系统模块
提供用户反馈收集和分析功能
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import time
from enum import Enum
import plotly.express as px

class FeedbackType(Enum):
    """反馈类型枚举"""
    BUG_REPORT = "bug_report"
    FEATURE_REQUEST = "feature_request"
    USABILITY_ISSUE = "usability_issue"
    PERFORMANCE_ISSUE = "performance_issue"
    GENERAL_FEEDBACK = "general_feedback"

@dataclass
class UserFeedback:
    """用户反馈数据类"""
    timestamp: datetime
    feedback_type: FeedbackType
    title: str
    description: str
    user_level: str
    feature_category: str
    severity: str  # low, medium, high, critical
    user_satisfaction: int  # 1-5
    session_id: str
    browser_info: str
    screen_resolution: str

class FeedbackCollector:
    """反馈收集器"""
    
    def __init__(self):
        self.feedbacks: List[UserFeedback] = []
        self.session_id = self._generate_session_id()
        
    def _generate_session_id(self) -> str:
        """生成会话ID"""
        return f"session_{int(time.time())}"
    
    def collect_feedback(self, feedback_type: FeedbackType, title: str, description: str,
                        user_level: str, feature_category: str, severity: str = "medium",
                        user_satisfaction: int = 3):
        """收集用户反馈"""
        feedback = UserFeedback(
            timestamp=datetime.now(),
            feedback_type=feedback_type,
            title=title,
            description=description,
            user_level=user_level,
            feature_category=feature_category,
            severity=severity,
            user_satisfaction=user_satisfaction,
            session_id=self.session_id,
            browser_info="Unknown",
            screen_resolution="Unknown"
        )
        
        self.feedbacks.append(feedback)
        return feedback
    
    def get_feedback_summary(self) -> Dict[str, Any]:
        """获取反馈摘要"""
        if not self.feedbacks:
            return {"message": "暂无反馈数据"}
        
        total_feedbacks = len(self.feedbacks)
        feedback_types = [f.feedback_type.value for f in self.feedbacks]
        severity_counts = {}
        satisfaction_scores = []
        
        for feedback in self.feedbacks:
            severity_counts[feedback.severity] = severity_counts.get(feedback.severity, 0) + 1
            satisfaction_scores.append(feedback.user_satisfaction)
        
        return {
            "total_feedbacks": total_feedbacks,
            "feedback_types": list(set(feedback_types)),
            "severity_distribution": severity_counts,
            "avg_satisfaction": np.mean(satisfaction_scores) if satisfaction_scores else 0,
            "recent_feedbacks": len([f for f in self.feedbacks 
                                   if f.timestamp > datetime.now() - timedelta(days=7)])
        }

class FeedbackAnalyzer:
    """反馈分析器"""
    
    def __init__(self, feedbacks: List[UserFeedback]):
        self.feedbacks = feedbacks
    
    def analyze_sentiment(self) -> Dict[str, Any]:
        """分析反馈情感"""
        if not self.feedbacks:
            return {"message": "暂无反馈数据"}
        
        # 基于满意度评分分析情感
        satisfaction_scores = [f.user_satisfaction for f in self.feedbacks]
        avg_satisfaction = np.mean(satisfaction_scores)
        
        if avg_satisfaction >= 4:
            sentiment = "positive"
        elif avg_satisfaction >= 3:
            sentiment = "neutral"
        else:
            sentiment = "negative"
        
        return {
            "sentiment": sentiment,
            "avg_satisfaction": avg_satisfaction,
            "satisfaction_distribution": {
                "very_satisfied": len([s for s in satisfaction_scores if s == 5]),
                "satisfied": len([s for s in satisfaction_scores if s == 4]),
                "neutral": len([s for s in satisfaction_scores if s == 3]),
                "dissatisfied": len([s for s in satisfaction_scores if s == 2]),
                "very_dissatisfied": len([s for s in satisfaction_scores if s == 1])
            }
        }
    
    def identify_common_issues(self) -> List[Dict[str, Any]]:
        """识别常见问题"""
        if not self.feedbacks:
            return []
        
        # 按反馈类型分组
        feedback_groups = {}
        for feedback in self.feedbacks:
            feedback_type = feedback.feedback_type.value
            if feedback_type not in feedback_groups:
                feedback_groups[feedback_type] = []
            feedback_groups[feedback_type].append(feedback)
        
        common_issues = []
        for feedback_type, group in feedback_groups.items():
            if len(group) >= 2:  # 至少2个相同类型的反馈
                common_issues.append({
                    "type": feedback_type,
                    "count": len(group),
                    "avg_severity": np.mean([self._severity_to_score(f.severity) for f in group]),
                    "avg_satisfaction": np.mean([f.user_satisfaction for f in group]),
                    "sample_titles": [f.title for f in group[:3]]  # 前3个标题作为示例
                })
        
        # 按严重程度排序
        common_issues.sort(key=lambda x: x["avg_severity"], reverse=True)
        return common_issues
    
    def _severity_to_score(self, severity: str) -> int:
        """将严重程度转换为分数"""
        severity_scores = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4
        }
        return severity_scores.get(severity, 2)
    
    def analyze_user_journey(self) -> Dict[str, Any]:
        """分析用户旅程"""
        if not self.feedbacks:
            return {"message": "暂无反馈数据"}
        
        # 按时间排序
        sorted_feedbacks = sorted(self.feedbacks, key=lambda x: x.timestamp)
        
        # 分析用户级别分布
        user_levels = [f.user_level for f in self.feedbacks]
        level_distribution = {}
        for level in user_levels:
            level_distribution[level] = level_distribution.get(level, 0) + 1
        
        # 分析功能类别使用情况
        feature_categories = [f.feature_category for f in self.feedbacks]
        category_distribution = {}
        for category in feature_categories:
            category_distribution[category] = category_distribution.get(category, 0) + 1
        
        return {
            "total_sessions": len(set(f.session_id for f in self.feedbacks)),
            "user_level_distribution": level_distribution,
            "feature_category_distribution": category_distribution,
            "feedback_timeline": [
                {
                    "timestamp": f.timestamp.isoformat(),
                    "type": f.feedback_type.value,
                    "satisfaction": f.user_satisfaction
                }
                for f in sorted_feedbacks
            ]
        }

class FeedbackUI:
    """反馈UI组件"""
    
    @staticmethod
    def render_feedback_form():
        """渲染反馈表单"""
        st.markdown("### 📝 用户反馈")
        
        # 反馈类型选择
        feedback_type = st.selectbox(
            "反馈类型",
            ["bug_report", "feature_request", "usability_issue", "performance_issue", "general_feedback"],
            format_func=lambda x: {
                "bug_report": "🐛 错误报告",
                "feature_request": "💡 功能建议",
                "usability_issue": "🎯 易用性问题",
                "performance_issue": "⚡ 性能问题",
                "general_feedback": "💬 一般反馈"
            }[x]
        )
        
        # 标题输入
        title = st.text_input("标题", placeholder="请简要描述您的反馈")
        
        # 详细描述
        description = st.text_area("详细描述", placeholder="请详细描述您遇到的问题或建议")
        
        # 严重程度
        severity = st.select_slider(
            "严重程度",
            options=["low", "medium", "high", "critical"],
            value="medium",
            format_func=lambda x: {
                "low": "低",
                "medium": "中",
                "high": "高",
                "critical": "严重"
            }[x]
        )
        
        # 用户满意度
        satisfaction = st.slider("满意度评分", 1, 5, 3, help="1=非常不满意，5=非常满意")
        
        # 提交按钮
        if st.button("提交反馈", type="primary"):
            if title and description:
                # 这里可以调用反馈收集器
                st.success("✅ 反馈提交成功！感谢您的宝贵意见。")
                return {
                    "type": feedback_type,
                    "title": title,
                    "description": description,
                    "severity": severity,
                    "satisfaction": satisfaction
                }
            else:
                st.error("请填写标题和详细描述")
        
        return None
    
    @staticmethod
    def render_feedback_dashboard(feedback_analyzer: FeedbackAnalyzer):
        """渲染反馈仪表板"""
        st.markdown("### 📊 反馈分析仪表板")
        
        # 情感分析
        sentiment_analysis = feedback_analyzer.analyze_sentiment()
        if "message" not in sentiment_analysis:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("平均满意度", f"{sentiment_analysis['avg_satisfaction']:.1f}/5")
            with col2:
                sentiment_emoji = {
                    "positive": "😊",
                    "neutral": "😐",
                    "negative": "😞"
                }
                st.metric("整体情感", f"{sentiment_emoji[sentiment_analysis['sentiment']]} {sentiment_analysis['sentiment']}")
            with col3:
                st.metric("反馈总数", len(feedback_analyzer.feedbacks))
        
        # 满意度分布
        if "satisfaction_distribution" in sentiment_analysis:
            st.markdown("#### 满意度分布")
            satisfaction_data = sentiment_analysis["satisfaction_distribution"]
            satisfaction_df = pd.DataFrame([
                {"满意度": "非常满意", "数量": satisfaction_data["very_satisfied"]},
                {"满意度": "满意", "数量": satisfaction_data["satisfied"]},
                {"满意度": "一般", "数量": satisfaction_data["neutral"]},
                {"满意度": "不满意", "数量": satisfaction_data["dissatisfied"]},
                {"满意度": "非常不满意", "数量": satisfaction_data["very_dissatisfied"]}
            ])
            
            fig = px.bar(satisfaction_df, x="满意度", y="数量", 
                        title="用户满意度分布",
                        color="数量", color_continuous_scale="Blues")
            st.plotly_chart(fig, use_container_width=True)
        
        # 常见问题
        common_issues = feedback_analyzer.identify_common_issues()
        if common_issues:
            st.markdown("#### 🔍 常见问题")
            for issue in common_issues[:5]:  # 显示前5个问题
                with st.expander(f"{issue['type']} ({issue['count']} 次反馈)"):
                    st.write(f"**平均严重程度:** {issue['avg_severity']:.1f}")
                    st.write(f"**平均满意度:** {issue['avg_satisfaction']:.1f}/5")
                    st.write("**示例反馈:**")
                    for title in issue['sample_titles']:
                        st.write(f"• {title}")
        
        # 用户旅程分析
        user_journey = feedback_analyzer.analyze_user_journey()
        if "message" not in user_journey:
            st.markdown("#### 👥 用户分析")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**用户级别分布**")
                level_data = user_journey["user_level_distribution"]
                if level_data:
                    level_df = pd.DataFrame([
                        {"级别": k, "数量": v} for k, v in level_data.items()
                    ])
                    fig = px.pie(level_df, values="数量", names="级别", title="用户级别分布")
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("**功能使用分布**")
                category_data = user_journey["feature_category_distribution"]
                if category_data:
                    category_df = pd.DataFrame([
                        {"功能": k, "数量": v} for k, v in category_data.items()
                    ])
                    fig = px.bar(category_df, x="功能", y="数量", title="功能使用分布")
                    st.plotly_chart(fig, use_container_width=True)

class FeedbackExporter:
    """反馈导出器"""
    
    @staticmethod
    def export_to_csv(feedbacks: List[UserFeedback], filename: str = "user_feedback.csv"):
        """导出为CSV文件"""
        if not feedbacks:
            return None
        
        data = []
        for feedback in feedbacks:
            data.append({
                "timestamp": feedback.timestamp.isoformat(),
                "feedback_type": feedback.feedback_type.value,
                "title": feedback.title,
                "description": feedback.description,
                "user_level": feedback.user_level,
                "feature_category": feedback.feature_category,
                "severity": feedback.severity,
                "user_satisfaction": feedback.user_satisfaction,
                "session_id": feedback.session_id
            })
        
        df = pd.DataFrame(data)
        return df.to_csv(index=False)
    
    @staticmethod
    def export_to_json(feedbacks: List[UserFeedback]):
        """导出为JSON文件"""
        if not feedbacks:
            return None
        
        data = []
        for feedback in feedbacks:
            data.append({
                "timestamp": feedback.timestamp.isoformat(),
                "feedback_type": feedback.feedback_type.value,
                "title": feedback.title,
                "description": feedback.description,
                "user_level": feedback.user_level,
                "feature_category": feedback.feature_category,
                "severity": feedback.severity,
                "user_satisfaction": feedback.user_satisfaction,
                "session_id": feedback.session_id
            })
        
        return json.dumps(data, ensure_ascii=False, indent=2)

# 全局反馈收集器实例
feedback_collector = FeedbackCollector()

# 便捷函数
def collect_user_feedback(feedback_type: str, title: str, description: str,
                         user_level: str, feature_category: str, **kwargs):
    """收集用户反馈"""
    return feedback_collector.collect_feedback(
        FeedbackType(feedback_type), title, description, user_level, feature_category, **kwargs
    )

def get_feedback_summary():
    """获取反馈摘要"""
    return feedback_collector.get_feedback_summary()

def analyze_feedbacks(feedbacks: List[UserFeedback]):
    """分析反馈"""
    analyzer = FeedbackAnalyzer(feedbacks)
    return analyzer

def show_feedback_form():
    """显示反馈表单"""
    return FeedbackUI.render_feedback_form()

def show_feedback_dashboard(feedbacks: List[UserFeedback]):
    """显示反馈仪表板"""
    analyzer = FeedbackAnalyzer(feedbacks)
    FeedbackUI.render_feedback_dashboard(analyzer)

def export_feedbacks(feedbacks: List[UserFeedback], format: str = "csv"):
    """导出反馈"""
    exporter = FeedbackExporter()
    if format == "csv":
        return exporter.export_to_csv(feedbacks)
    elif format == "json":
        return exporter.export_to_json(feedbacks)
    return None
