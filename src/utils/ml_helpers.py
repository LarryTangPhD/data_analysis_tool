"""
机器学习辅助工具模块
提供各种机器学习功能的辅助函数
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 安全导入sklearn相关模块
try:
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
    from sklearn.linear_model import LogisticRegression, LinearRegression
    from sklearn.svm import SVC, SVR
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score, f1_score, confusion_matrix,
        r2_score, mean_squared_error, classification_report
    )
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    SKLEARN_AVAILABLE = True
except ImportError as e:
    st.warning(f"⚠️ sklearn导入失败: {e}")
    SKLEARN_AVAILABLE = False
except RuntimeError as e:
    st.warning(f"⚠️ sklearn运行时错误: {e}")
    SKLEARN_AVAILABLE = False

import seaborn as sns
import matplotlib.pyplot as plt


def train_classification_model(X, y):
    """
    训练分类模型
    
    Args:
        X: 特征数据
        y: 目标变量
        
    Returns:
        tuple: (模型, 训练信息)
    """
    if not SKLEARN_AVAILABLE:
        st.error("❌ sklearn不可用，无法训练模型")
        return None, None
    
    # 数据预处理
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 标签编码
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    # 分割数据
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded, test_size=0.2, random_state=42
    )
    
    # 训练多个模型
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'SVM': SVC(random_state=42, probability=True)
    }
    
    best_model = None
    best_score = 0
    best_model_name = None
    
    for name, model in models.items():
        # 交叉验证
        cv_scores = cross_val_score(model, X_train, y_train, cv=5)
        avg_score = cv_scores.mean()
        
        if avg_score > best_score:
            best_score = avg_score
            best_model = model
            best_model_name = name
    
    # 训练最佳模型
    best_model.fit(X_train, y_train)
    y_pred = best_model.predict(X_test)
    
    # 计算评估指标
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    conf_matrix = confusion_matrix(y_test, y_pred)
    
    # 特征重要性（仅适用于树模型）
    feature_importance = None
    if hasattr(best_model, 'feature_importances_'):
        feature_importance = best_model.feature_importances_
    elif hasattr(best_model, 'coef_'):
        feature_importance = np.abs(best_model.coef_[0])
    
    training_info = {
        'model_name': best_model_name,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': conf_matrix,
        'feature_importance': feature_importance,
        'cv_score': best_score
    }
    
    return best_model, training_info


def train_regression_model(X, y):
    """
    训练回归模型
    
    Args:
        X: 特征数据
        y: 目标变量
        
    Returns:
        tuple: (模型, 训练信息)
    """
    if not SKLEARN_AVAILABLE:
        st.error("❌ sklearn不可用，无法训练模型")
        return None, None
    
    # 数据预处理
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 分割数据
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )
    
    # 训练多个模型
    models = {
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'Linear Regression': LinearRegression(),
        'SVR': SVR()
    }
    
    best_model = None
    best_score = 0
    best_model_name = None
    
    for name, model in models.items():
        # 交叉验证
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
        avg_score = cv_scores.mean()
        
        if avg_score > best_score:
            best_score = avg_score
            best_model = model
            best_model_name = name
    
    # 训练最佳模型
    best_model.fit(X_train, y_train)
    y_pred = best_model.predict(X_test)
    
    # 计算评估指标
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    
    # 特征重要性（仅适用于树模型）
    feature_importance = None
    if hasattr(best_model, 'feature_importances_'):
        feature_importance = best_model.feature_importances_
    elif hasattr(best_model, 'coef_'):
        feature_importance = np.abs(best_model.coef_)
    
    training_info = {
        'model_name': best_model_name,
        'r2_score': r2,
        'mse': mse,
        'feature_importance': feature_importance,
        'cv_score': best_score
    }
    
    return best_model, training_info


def perform_clustering(X, n_clusters):
    """
    执行聚类分析
    
    Args:
        X: 特征数据
        n_clusters: 聚类数量
        
    Returns:
        dict: 聚类结果
    """
    if not SKLEARN_AVAILABLE:
        st.error("❌ sklearn不可用，无法执行聚类")
        return None
    
    # 数据预处理
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 执行K-means聚类
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X_scaled)
    
    # 计算聚类质量
    inertia = kmeans.inertia_
    
    # 计算轮廓系数（如果可能）
    try:
        from sklearn.metrics import silhouette_score
        silhouette_avg = silhouette_score(X_scaled, labels)
    except:
        silhouette_avg = None
    
    cluster_results = {
        'labels': labels,
        'centroids': kmeans.cluster_centers_,
        'inertia': inertia,
        'silhouette_score': silhouette_avg,
        'n_clusters': n_clusters
    }
    
    return cluster_results


def create_confusion_matrix(conf_matrix):
    """
    创建混淆矩阵可视化
    
    Args:
        conf_matrix: 混淆矩阵
        
    Returns:
        plotly figure: 混淆矩阵图
    """
    fig = px.imshow(
        conf_matrix,
        text_auto=True,
        aspect="auto",
        title="混淆矩阵",
        labels=dict(x="预测值", y="真实值", color="数量"),
        color_continuous_scale="Blues"
    )
    
    fig.update_layout(
        xaxis_title="预测值",
        yaxis_title="真实值"
    )
    
    return fig


def create_feature_importance(feature_names, importance_scores):
    """
    创建特征重要性可视化
    
    Args:
        feature_names: 特征名称列表
        importance_scores: 重要性分数
        
    Returns:
        plotly figure: 特征重要性图
    """
    if importance_scores is None:
        return None
    
    # 创建特征重要性DataFrame
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importance_scores
    }).sort_values('Importance', ascending=True)
    
    # 创建水平条形图
    fig = px.bar(
        importance_df,
        x='Importance',
        y='Feature',
        orientation='h',
        title="特征重要性分析",
        labels={'Importance': '重要性', 'Feature': '特征'}
    )
    
    fig.update_layout(
        xaxis_title="重要性",
        yaxis_title="特征"
    )
    
    return fig


def create_scatter_chart(data, x_col, y_col, color_col=None, title="散点图"):
    """
    创建散点图
    
    Args:
        data: 数据DataFrame
        x_col: X轴列名
        y_col: Y轴列名
        color_col: 颜色列名（可选）
        title: 图表标题
        
    Returns:
        plotly figure: 散点图
    """
    if color_col:
        fig = px.scatter(
            data,
            x=x_col,
            y=y_col,
            color=color_col,
            title=title,
            labels={x_col: x_col, y_col: y_col, color_col: color_col}
        )
    else:
        fig = px.scatter(
            data,
            x=x_col,
            y=y_col,
            title=title,
            labels={x_col: x_col, y_col: y_col}
        )
    
    return fig


def create_regression_plot(y_true, y_pred, title="回归预测结果"):
    """
    创建回归预测结果图
    
    Args:
        y_true: 真实值
        y_pred: 预测值
        title: 图表标题
        
    Returns:
        plotly figure: 回归图
    """
    # 创建散点图
    fig = px.scatter(
        x=y_true,
        y=y_pred,
        title=title,
        labels={'x': '真实值', 'y': '预测值'}
    )
    
    # 添加对角线
    min_val = min(min(y_true), min(y_pred))
    max_val = max(max(y_true), max(y_pred))
    
    fig.add_trace(
        go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode='lines',
            name='理想线',
            line=dict(color='red', dash='dash')
        )
    )
    
    fig.update_layout(
        xaxis_title="真实值",
        yaxis_title="预测值"
    )
    
    return fig


def create_cluster_visualization(X, labels, centroids=None, title="聚类结果"):
    """
    创建聚类结果可视化
    
    Args:
        X: 特征数据
        labels: 聚类标签
        centroids: 聚类中心（可选）
        title: 图表标题
        
    Returns:
        plotly figure: 聚类图
    """
    # 创建散点图
    fig = px.scatter(
        x=X[:, 0],
        y=X[:, 1],
        color=labels,
        title=title,
        labels={'x': '特征1', 'y': '特征2', 'color': '聚类'}
    )
    
    # 添加聚类中心
    if centroids is not None:
        fig.add_trace(
            go.Scatter(
                x=centroids[:, 0],
                y=centroids[:, 1],
                mode='markers',
                marker=dict(
                    symbol='x',
                    size=15,
                    color='red',
                    line=dict(width=2, color='black')
                ),
                name='聚类中心'
            )
        )
    
    return fig


def get_model_performance_summary(training_info, task_type):
    """
    获取模型性能摘要
    
    Args:
        training_info: 训练信息字典
        task_type: 任务类型（'classification' 或 'regression'）
        
    Returns:
        str: 性能摘要文本
    """
    if task_type == 'classification':
        summary = f"""
        **模型性能摘要：**
        - 模型类型：{training_info['model_name']}
        - 准确率：{training_info['accuracy']:.3f}
        - 精确率：{training_info['precision']:.3f}
        - 召回率：{training_info['recall']:.3f}
        - F1分数：{training_info['f1_score']:.3f}
        - 交叉验证分数：{training_info['cv_score']:.3f}
        """
    else:  # regression
        summary = f"""
        **模型性能摘要：**
        - 模型类型：{training_info['model_name']}
        - R²分数：{training_info['r2_score']:.3f}
        - 均方误差：{training_info['mse']:.3f}
        - 交叉验证分数：{training_info['cv_score']:.3f}
        """
    
    return summary


def suggest_hyperparameters(task_type, data_size, n_features):
    """
    根据数据特征建议超参数
    
    Args:
        task_type: 任务类型
        data_size: 数据大小
        n_features: 特征数量
        
    Returns:
        dict: 建议的超参数
    """
    suggestions = {}
    
    if task_type == 'classification':
        if data_size < 1000:
            suggestions['Random Forest'] = {
                'n_estimators': 50,
                'max_depth': 5,
                'min_samples_split': 5
            }
        else:
            suggestions['Random Forest'] = {
                'n_estimators': 100,
                'max_depth': 10,
                'min_samples_split': 2
            }
    
    elif task_type == 'regression':
        if data_size < 1000:
            suggestions['Random Forest'] = {
                'n_estimators': 50,
                'max_depth': 5,
                'min_samples_split': 5
            }
        else:
            suggestions['Random Forest'] = {
                'n_estimators': 100,
                'max_depth': 10,
                'min_samples_split': 2
            }
    
    return suggestions
