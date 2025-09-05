"""
机器学习页面模块
提供机器学习功能
"""

import streamlit as st
import pandas as pd
import numpy as np
from src.utils.session_manager import SessionManager
from src.utils.ai_assistant_utils import get_smart_ai_assistant


def render_machine_learning_page():
    """渲染机器学习页面"""
    st.markdown('<h2 class="sub-header">🤖 机器学习</h2>', unsafe_allow_html=True)
    
    # 获取会话管理器
    session_manager = SessionManager()
    
    # 检查是否有数据
    if not session_manager.has_data():
        st.warning("⚠️ 请先上传数据文件")
        return
    
    data = session_manager.get_data()
    
    # 机器学习指南
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    ">
        <h3 style="color: white; margin-bottom: 15px;">🤖 机器学习指南</h3>
        <p style="font-size: 16px; line-height: 1.6; margin-bottom: 15px;">
            <strong>💡 智能算法：</strong><br>
            基于scikit-learn的机器学习平台，提供分类、回归、聚类等多种算法，支持模型训练、评估和预测。
        </p>
        <div style="display: flex; gap: 20px; margin-bottom: 15px;">
            <div style="flex: 1; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                <h4 style="color: #ff6b6b; margin-bottom: 10px;">🎯 任务类型</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 14px;">
                    <li>分类任务 - 预测类别标签</li>
                    <li>回归任务 - 预测连续数值</li>
                    <li>聚类任务 - 数据分组分析</li>
                    <li>特征工程 - 特征优化</li>
                    <li>模型评估 - 性能分析</li>
                </ul>
            </div>
            <div style="flex: 1; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                <h4 style="color: #51cf66; margin-bottom: 10px;">🔧 核心功能</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 14px;">
                    <li>自动数据预处理</li>
                    <li>模型参数调优</li>
                    <li>交叉验证评估</li>
                    <li>特征重要性分析</li>
                    <li>预测结果可视化</li>
                </ul>
            </div>
        </div>
        <p style="font-size: 14px; margin: 0; opacity: 0.9;">
            <strong>🎯 适用场景：</strong> 预测建模、模式识别、数据挖掘、业务智能
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.success(f"✅ 数据加载成功: {len(data)} 行 × {len(data.columns)} 列")
    
    # 机器学习任务选择
    ml_task = st.selectbox(
        "选择机器学习任务",
        ["分类", "回归", "聚类", "特征工程", "模型评估"]
    )
    
    st.info(f"🎯 当前选择的任务: {ml_task}")
    
    # 根据任务类型执行相应功能
    if ml_task == "分类":
        render_classification_task(data)
    elif ml_task == "回归":
        render_regression_task(data)
    elif ml_task == "聚类":
        render_clustering_task(data)
    elif ml_task == "特征工程":
        render_feature_engineering_task(data)
    elif ml_task == "模型评估":
        render_model_evaluation_task(data)
    
    # AI智能机器学习建议
    render_ai_ml_advice(data, ml_task)


def render_classification_task(data):
    """渲染分类任务"""
    st.subheader("🎯 分类任务")
    
    # 选择特征和目标变量
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if len(numeric_cols) == 0:
        st.warning("⚠️ 数据中没有数值型列，无法进行分类任务")
        return
    elif len(categorical_cols) == 0:
        st.warning("⚠️ 数据中没有分类列，无法进行分类任务")
        return
    
    target_col = st.selectbox("选择目标变量（分类列）", categorical_cols)
    feature_cols = st.multiselect("选择特征变量（数值列）", numeric_cols, default=numeric_cols[:3])
    
    if target_col and feature_cols:
        if st.button("训练分类模型"):
            with st.spinner("正在训练分类模型..."):
                try:
                    from src.utils.ml_helpers import train_classification_model, create_confusion_matrix, create_feature_importance
                    
                    # 数据预处理
                    X = data[feature_cols].dropna()
                    y = data[target_col].dropna()
                    
                    # 确保X和y的长度一致
                    common_index = X.index.intersection(y.index)
                    X = X.loc[common_index]
                    y = y.loc[common_index]
                    
                    if len(X) > 0:
                        # 训练模型
                        model, training_info = train_classification_model(X.values, y.values)
                        
                        # 显示结果
                        st.success("✅ 分类模型训练完成！")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("准确率", f"{training_info['accuracy']:.3f}")
                        with col2:
                            st.metric("精确率", f"{training_info['precision']:.3f}")
                        with col3:
                            st.metric("召回率", f"{training_info['recall']:.3f}")
                        with col4:
                            st.metric("F1分数", f"{training_info['f1_score']:.3f}")
                        
                        # 混淆矩阵
                        st.subheader("📊 混淆矩阵")
                        fig = create_confusion_matrix(training_info['confusion_matrix'])
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # 特征重要性
                        st.subheader("🎯 特征重要性")
                        fig = create_feature_importance(feature_cols, training_info['feature_importance'])
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.error("❌ 预处理后没有足够的数据进行训练")
                except Exception as e:
                    st.error(f"❌ 模型训练失败: {str(e)}")


def render_regression_task(data):
    """渲染回归任务"""
    st.subheader("📈 回归任务")
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) < 2:
        st.warning("⚠️ 需要至少2个数值型列进行回归任务")
        return
    
    target_col = st.selectbox("选择目标变量", numeric_cols)
    feature_cols = st.multiselect("选择特征变量", [col for col in numeric_cols if col != target_col], default=[col for col in numeric_cols[:3] if col != target_col])
    
    if target_col and feature_cols:
        if st.button("训练回归模型"):
            with st.spinner("正在训练回归模型..."):
                try:
                    from src.utils.ml_helpers import train_regression_model
                    
                    X = data[feature_cols].dropna()
                    y = data[target_col].dropna()
                    
                    common_index = X.index.intersection(y.index)
                    X = X.loc[common_index]
                    y = y.loc[common_index]
                    
                    if len(X) > 0:
                        model, training_info = train_regression_model(X.values, y.values)
                        
                        st.success("✅ 回归模型训练完成！")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("R²分数", f"{training_info['r2_score']:.3f}")
                        with col2:
                            st.metric("均方误差", f"{training_info['mse']:.3f}")
                    else:
                        st.error("❌ 预处理后没有足够的数据进行训练")
                except Exception as e:
                    st.error(f"❌ 模型训练失败: {str(e)}")


def render_clustering_task(data):
    """渲染聚类任务"""
    st.subheader("🔍 聚类分析")
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) < 2:
        st.warning("⚠️ 需要至少2个数值型列进行聚类分析")
        return
    
    feature_cols = st.multiselect("选择特征变量", numeric_cols, default=numeric_cols[:3])
    n_clusters = st.slider("选择聚类数量", 2, 10, 3)
    
    if feature_cols:
        if st.button("执行聚类分析"):
            with st.spinner("正在执行聚类分析..."):
                try:
                    from src.utils.ml_helpers import perform_clustering, create_scatter_chart
                    
                    X = data[feature_cols].dropna()
                    
                    if len(X) > 0:
                        cluster_results = perform_clustering(X.values, n_clusters)
                        
                        st.success("✅ 聚类分析完成！")
                        
                        # 显示聚类结果
                        data_with_clusters = data[feature_cols].copy()
                        data_with_clusters['Cluster'] = cluster_results['labels']
                        
                        st.write("**聚类结果：**")
                        st.dataframe(data_with_clusters.head(10), use_container_width=True)
                        
                        # 聚类可视化
                        if len(feature_cols) >= 2:
                            fig = create_scatter_chart(
                                data_with_clusters, 
                                feature_cols[0], 
                                feature_cols[1], 
                                'Cluster',
                                title=f"聚类结果 ({feature_cols[0]} vs {feature_cols[1]})"
                            )
                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.error("❌ 预处理后没有足够的数据进行聚类")
                except Exception as e:
                    st.error(f"❌ 聚类分析失败: {str(e)}")


def render_feature_engineering_task(data):
    """渲染特征工程任务"""
    st.subheader("🔧 特征工程")
    st.info("特征工程功能正在开发中，敬请期待！")


def render_model_evaluation_task(data):
    """渲染模型评估任务"""
    st.subheader("📊 模型评估")
    st.info("模型评估功能正在开发中，敬请期待！")


def render_ai_ml_advice(data, ml_task):
    """渲染AI机器学习建议"""
    st.subheader("🤖 AI智能机器学习建议")
    
    # 检查AI助手是否可用
    ai_assistant = get_smart_ai_assistant()
    
    if ai_assistant is None:
        st.warning("⚠️ AI助手不可用，请检查API配置")
        return
    
    # 机器学习方法建议
    st.write("**💡 需要AI推荐机器学习方法？**")
    
    if ml_task in ["分类", "回归"]:
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if ml_task == "分类":
            target_col = st.selectbox("选择目标变量（分类列）", categorical_cols, key="ai_target_col")
        else:
            target_col = st.selectbox("选择目标变量（数值列）", numeric_cols, key="ai_target_col")
        
        feature_cols = st.multiselect("选择特征变量", [col for col in numeric_cols if col != target_col], key="ai_feature_cols")
        
        if target_col and feature_cols:
            if st.button("🤖 获取AI机器学习建议", type="primary"):
                with st.spinner("AI正在分析机器学习方案..."):
                    try:
                        ml_advice = ai_assistant.suggest_ml_approach(data, ml_task, target_col, feature_cols)
                        
                        st.success("✅ AI机器学习建议完成！")
                        st.markdown("### 🤖 AI机器学习建议")
                        st.markdown(ml_advice)
                        
                    except Exception as e:
                        st.error(f"❌ AI建议失败：{str(e)}")
    
    # AI智能问答
    st.write("**💡 有机器学习问题？问问AI助手：**")
    user_question = st.text_area(
        "请输入您的问题：",
        placeholder="例如：如何选择合适的算法？如何评估模型性能？",
        height=80,
        key="ml_ai_question"
    )
    
    if st.button("🤖 获取AI回答", key="ml_ai_answer") and user_question.strip():
        with st.spinner("AI正在思考..."):
            try:
                data_context = f"数据集包含{len(data)}行{len(data.columns)}列，当前任务类型：{ml_task}"
                answer = ai_assistant.answer_data_question(user_question, data_context, "机器学习")
                
                st.success("✅ AI回答完成！")
                st.markdown("### 🤖 AI回答")
                st.markdown(answer)
                
            except Exception as e:
                st.error(f"❌ AI回答失败：{str(e)}")

