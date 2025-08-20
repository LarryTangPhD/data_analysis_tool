"""
机器学习工具模块
提供机器学习相关的功能，包括模型训练、评估、特征工程等
"""

import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Any, Tuple
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler, PolynomialFeatures
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.cluster import KMeans
from sklearn.metrics import (
    classification_report, confusion_matrix, mean_squared_error, r2_score,
    precision_score, recall_score, f1_score, accuracy_score
)
from scipy import stats
import warnings
warnings.filterwarnings('ignore')


def validate_data_for_ml(data: pd.DataFrame, task_type: str) -> Dict[str, Any]:
    """
    验证数据是否适合机器学习任务
    
    Args:
        data: 数据框
        task_type: 任务类型 ('classification', 'regression', 'clustering')
        
    Returns:
        Dict: 验证结果
    """
    validation_result = {
        'is_valid': True,
        'issues': [],
        'recommendations': []
    }
    
    # 检查数据大小
    if len(data) < 10:
        validation_result['is_valid'] = False
        validation_result['issues'].append("数据量太少（少于10行）")
        validation_result['recommendations'].append("建议增加数据量")
    
    # 检查缺失值
    missing_ratio = data.isnull().sum().sum() / (len(data) * len(data.columns))
    if missing_ratio > 0.5:
        validation_result['is_valid'] = False
        validation_result['issues'].append(f"缺失值比例过高（{missing_ratio:.2%}）")
        validation_result['recommendations'].append("建议处理缺失值")
    
    # 检查数值型列
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) == 0:
        validation_result['is_valid'] = False
        validation_result['issues'].append("没有数值型列")
        validation_result['recommendations'].append("需要数值型特征")
    
    # 任务特定检查
    if task_type == 'classification':
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) == 0:
            validation_result['is_valid'] = False
            validation_result['issues'].append("分类任务需要分类目标变量")
            validation_result['recommendations'].append("需要至少一个分类列作为目标变量")
    
    return validation_result


def preprocess_data_for_ml(data: pd.DataFrame, target_col: str, 
                          feature_cols: Optional[List[str]] = None) -> Tuple[np.ndarray, np.ndarray]:
    """
    为机器学习预处理数据
    
    Args:
        data: 数据框
        target_col: 目标变量列名
        feature_cols: 特征列名列表
        
    Returns:
        Tuple: (特征矩阵, 目标向量)
    """
    if feature_cols is None:
        feature_cols = [col for col in data.select_dtypes(include=[np.number]).columns if col != target_col]
    
    # 处理缺失值
    data_cleaned = data[feature_cols + [target_col]].dropna()
    
    X = data_cleaned[feature_cols].values
    y = data_cleaned[target_col].values
    
    # 标准化特征
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, y


def train_classification_model(X: np.ndarray, y: np.ndarray,
                             n_estimators: int = 100, max_depth: int = 10,
                             min_samples_split: int = 2, min_samples_leaf: int = 1,
                             random_state: int = 42) -> Tuple[RandomForestClassifier, Dict[str, Any]]:
    """
    训练分类模型
    
    Args:
        X: 特征矩阵
        y: 目标向量
        n_estimators: 决策树数量
        max_depth: 最大深度
        min_samples_split: 最小分裂样本数
        min_samples_leaf: 最小叶子样本数
        random_state: 随机种子
        
    Returns:
        Tuple: (训练好的模型, 训练信息)
    """
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        random_state=random_state
    )
    
    # 数据分割
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_state)
    
    # 训练模型
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)
    
    # 计算评估指标
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    training_info = {
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test,
        'y_pred': y_pred,
        'y_pred_proba': y_pred_proba,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': confusion_matrix(y_test, y_pred),
        'feature_importance': model.feature_importances_
    }
    
    return model, training_info


def train_regression_model(X: np.ndarray, y: np.ndarray,
                          model_type: str = 'random_forest',
                          random_state: int = 42) -> Tuple[Any, Dict[str, Any]]:
    """
    训练回归模型
    
    Args:
        X: 特征矩阵
        y: 目标向量
        model_type: 模型类型 ('linear', 'random_forest', 'svr')
        random_state: 随机种子
        
    Returns:
        Tuple: (训练好的模型, 训练信息)
    """
    # 数据分割
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_state)
    
    # 选择模型
    if model_type == 'linear':
        model = LinearRegression()
    elif model_type == 'random_forest':
        model = RandomForestRegressor(n_estimators=100, random_state=random_state)
    elif model_type == 'svr':
        model = SVR()
    else:
        raise ValueError(f"不支持的模型类型: {model_type}")
    
    # 训练模型
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    # 计算评估指标
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    training_info = {
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test,
        'y_pred': y_pred,
        'mse': mse,
        'r2_score': r2,
        'rmse': np.sqrt(mse)
    }
    
    if hasattr(model, 'feature_importances_'):
        training_info['feature_importance'] = model.feature_importances_
    
    return model, training_info


def perform_clustering(X: np.ndarray, n_clusters: int = 3,
                      random_state: int = 42) -> Dict[str, Any]:
    """
    执行聚类分析
    
    Args:
        X: 特征矩阵
        n_clusters: 聚类数量
        random_state: 随机种子
        
    Returns:
        Dict: 聚类结果
    """
    # 标准化数据
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 执行聚类
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
    labels = kmeans.fit_predict(X_scaled)
    
    # 计算聚类质量
    inertia = kmeans.inertia_
    
    clustering_results = {
        'labels': labels,
        'centroids': kmeans.cluster_centers_,
        'inertia': inertia,
        'n_clusters': n_clusters,
        'cluster_sizes': np.bincount(labels)
    }
    
    return clustering_results


def perform_cross_validation(X: np.ndarray, y: np.ndarray, 
                           model_type: str = 'classification',
                           cv_folds: int = 5) -> Dict[str, Any]:
    """
    执行交叉验证
    
    Args:
        X: 特征矩阵
        y: 目标向量
        model_type: 模型类型 ('classification', 'regression')
        cv_folds: 交叉验证折数
        
    Returns:
        Dict: 交叉验证结果
    """
    if model_type == 'classification':
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        scoring = 'accuracy'
    else:
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        scoring = 'r2'
    
    # 执行交叉验证
    cv_scores = cross_val_score(model, X, y, cv=cv_folds, scoring=scoring)
    
    cv_results = {
        'scores': cv_scores,
        'mean_score': cv_scores.mean(),
        'std_score': cv_scores.std(),
        'cv_folds': cv_folds,
        'model_type': model_type
    }
    
    return cv_results


def generate_learning_curve(X: np.ndarray, y: np.ndarray,
                           model_type: str = 'classification',
                           train_sizes: Optional[List[float]] = None) -> Dict[str, Any]:
    """
    生成学习曲线
    
    Args:
        X: 特征矩阵
        y: 目标向量
        model_type: 模型类型 ('classification', 'regression')
        train_sizes: 训练集大小比例
        
    Returns:
        Dict: 学习曲线数据
    """
    from sklearn.model_selection import learning_curve
    
    if train_sizes is None:
        train_sizes = np.linspace(0.1, 1.0, 10)
    
    if model_type == 'classification':
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        scoring = 'accuracy'
    else:
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        scoring = 'r2'
    
    # 计算学习曲线
    train_sizes, train_scores, val_scores = learning_curve(
        model, X, y, train_sizes=train_sizes, cv=5, scoring=scoring, n_jobs=-1
    )
    
    learning_curve_data = {
        'train_sizes': train_sizes,
        'train_scores': train_scores,
        'val_scores': val_scores,
        'train_scores_mean': train_scores.mean(axis=1),
        'train_scores_std': train_scores.std(axis=1),
        'val_scores_mean': val_scores.mean(axis=1),
        'val_scores_std': val_scores.std(axis=1)
    }
    
    return learning_curve_data


def perform_feature_engineering(X: np.ndarray, feature_names: List[str],
                              engineering_type: str = 'polynomial') -> Tuple[np.ndarray, List[str]]:
    """
    执行特征工程
    
    Args:
        X: 特征矩阵
        feature_names: 特征名称列表
        engineering_type: 特征工程类型 ('polynomial', 'interaction', 'ratio')
        
    Returns:
        Tuple: (工程化后的特征矩阵, 新的特征名称列表)
    """
    if engineering_type == 'polynomial':
        poly = PolynomialFeatures(degree=2, include_bias=False)
        X_engineered = poly.fit_transform(X)
        new_feature_names = poly.get_feature_names_out(feature_names)
    
    elif engineering_type == 'interaction':
        # 创建交互特征
        n_features = X.shape[1]
        interaction_features = []
        interaction_names = []
        
        for i in range(n_features):
            for j in range(i+1, n_features):
                interaction = X[:, i] * X[:, j]
                interaction_features.append(interaction)
                interaction_names.append(f"{feature_names[i]}_{feature_names[j]}_interaction")
        
        X_engineered = np.column_stack([X] + interaction_features)
        new_feature_names = feature_names + interaction_names
    
    elif engineering_type == 'ratio':
        # 创建比率特征
        ratio_features = []
        ratio_names = []
        
        for i in range(X.shape[1]):
            for j in range(i+1, X.shape[1]):
                # 避免除零
                denominator = X[:, j]
                denominator[denominator == 0] = 1e-8
                ratio = X[:, i] / denominator
                ratio_features.append(ratio)
                ratio_names.append(f"{feature_names[i]}_{feature_names[j]}_ratio")
        
        X_engineered = np.column_stack([X] + ratio_features)
        new_feature_names = feature_names + ratio_names
    
    else:
        raise ValueError(f"不支持的特征工程类型: {engineering_type}")
    
    return X_engineered, new_feature_names


def analyze_feature_importance(model, feature_names: List[str]) -> pd.DataFrame:
    """
    分析特征重要性
    
    Args:
        model: 训练好的模型
        feature_names: 特征名称列表
        
    Returns:
        pd.DataFrame: 特征重要性数据框
    """
    if hasattr(model, 'feature_importances_'):
        importance = model.feature_importances_
    else:
        # 对于线性模型，使用系数的绝对值
        if hasattr(model, 'coef_'):
            importance = np.abs(model.coef_)
        else:
            raise ValueError("模型不支持特征重要性分析")
    
    feature_importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importance
    }).sort_values('importance', ascending=False)
    
    return feature_importance_df


def detect_outliers_iqr(data: pd.DataFrame, columns: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    使用IQR方法检测异常值
    
    Args:
        data: 数据框
        columns: 要检测的列名列表
        
    Returns:
        Dict: 异常值检测结果
    """
    if columns is None:
        columns = data.select_dtypes(include=[np.number]).columns.tolist()
    
    outlier_results = {}
    
    for col in columns:
        if col in data.columns and data[col].dtype in ['int64', 'float64']:
            Q1 = data[col].quantile(0.25)
            Q3 = data[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = data[(data[col] < lower_bound) | (data[col] > upper_bound)]
            
            outlier_results[col] = {
                'outliers_count': len(outliers),
                'outliers_percentage': len(outliers) / len(data) * 100,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'outlier_indices': outliers.index.tolist()
            }
    
    return outlier_results


def perform_statistical_tests(data: pd.DataFrame, test_type: str, 
                            columns: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    执行统计检验
    
    Args:
        data: 数据框
        test_type: 检验类型 ('normality', 'ttest', 'anova', 'correlation', 'chi2')
        columns: 要检验的列名列表
        
    Returns:
        Dict: 统计检验结果
    """
    if columns is None:
        columns = data.select_dtypes(include=[np.number]).columns.tolist()
    
    test_results = {}
    
    if test_type == 'normality':
        # 正态性检验
        for col in columns:
            if col in data.columns:
                statistic, p_value = stats.shapiro(data[col].dropna())
                test_results[col] = {
                    'statistic': statistic,
                    'p_value': p_value,
                    'is_normal': p_value > 0.05
                }
    
    elif test_type == 'ttest':
        # t检验（需要分组变量）
        if len(columns) >= 2:
            col1, col2 = columns[0], columns[1]
            statistic, p_value = stats.ttest_ind(data[col1].dropna(), data[col2].dropna())
            test_results = {
                'statistic': statistic,
                'p_value': p_value,
                'significant': p_value < 0.05
            }
    
    elif test_type == 'correlation':
        # 相关性检验
        if len(columns) >= 2:
            col1, col2 = columns[0], columns[1]
            correlation, p_value = stats.pearsonr(data[col1].dropna(), data[col2].dropna())
            test_results = {
                'correlation': correlation,
                'p_value': p_value,
                'significant': p_value < 0.05
            }
    
    return test_results


def calculate_elbow_curve(X: np.ndarray, max_k: int = 10) -> Dict[str, Any]:
    """
    计算肘部曲线（用于确定最佳聚类数）
    
    Args:
        X: 特征矩阵
        max_k: 最大聚类数
        
    Returns:
        Dict: 肘部曲线数据
    """
    # 标准化数据
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    inertias = []
    k_values = range(1, max_k + 1)
    
    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)
    
    elbow_data = {
        'k_values': list(k_values),
        'inertias': np.array(inertias)
    }
    
    return elbow_data
