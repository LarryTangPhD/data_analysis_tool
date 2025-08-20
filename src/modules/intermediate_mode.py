"""
普通模式模块 - 科研数据分析工作台
提供成熟的数据分析工具，适合有经验的研究人员快速完成科研数据分析
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from scipy.stats import pearsonr, spearmanr
import warnings
warnings.filterwarnings('ignore')

# 导入普通模式AI助手
from src.utils.ai_assistant_intermediate import get_intermediate_ai_assistant
from src.config.settings import ANALYSIS_MODES
# 导入报告导出组件
from src.modules.report_export_component import render_report_export_section
# 导入综合报告导出组件
from src.modules.comprehensive_report_export import render_comprehensive_report_export

def create_research_sample_data():
    """创建科研示例数据集"""
    np.random.seed(42)
    n = 120
    
    # 创建实验研究数据集
    data = {
        'participant_id': range(1, n+1),
        'group': np.random.choice(['实验组', '对照组'], n),
        'pre_test': np.random.normal(70, 15, n),
        'post_test': np.random.normal(75, 15, n),
        'age': np.random.normal(25, 5, n),
        'gender': np.random.choice(['男', '女'], n),
        'education_level': np.random.choice(['本科', '硕士', '博士'], n),
        'study_time': np.random.normal(3, 1, n),
        'motivation': np.random.normal(7, 2, n)
    }
    
    # 添加实验效应
    for i in range(n):
        if data['group'][i] == '实验组':
            data['post_test'][i] += np.random.normal(8, 3)  # 实验组后测成绩提高
    
    # 添加一些缺失值
    data['pre_test'][np.random.choice(n, 3, replace=False)] = np.nan
    data['post_test'][np.random.choice(n, 2, replace=False)] = np.nan
    
    return pd.DataFrame(data)

def display_research_workbench():
    """显示科研数据分析工作台主界面"""
    st.markdown('<h1 class="main-header">🔬 科研数据分析工作台 - 普通模式</h1>', unsafe_allow_html=True)
    
    # 工作台导航
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📊 数据管理", use_container_width=True, key="workbench_data_management"):
            st.session_state.current_step = 2
            st.rerun()
    with col2:
        if st.button("📈 统计分析", use_container_width=True, key="workbench_statistical_analysis"):
            st.session_state.current_step = 3
            st.rerun()
    with col3:
        if st.button("📊 数据可视化", use_container_width=True, key="workbench_data_visualization"):
            st.session_state.current_step = 4
            st.rerun()
    with col4:
        if st.button("📄 报告生成", use_container_width=True, key="workbench_report_generation"):
            st.session_state.current_step = 5
            st.rerun()
    
    st.markdown("---")
    
    # 快速分析面板
    st.markdown("### 🚀 快速分析面板")
    
    if st.session_state.research_data is not None:
        data = st.session_state.research_data
        
        # 数据概览
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("样本量", len(data))
        with col2:
            st.metric("变量数", len(data.columns))
        with col3:
            st.metric("缺失值", data.isnull().sum().sum())
        with col4:
            st.metric("数据类型", f"{len(data.select_dtypes(include=[np.number]).columns)}数值/{len(data.select_dtypes(include=['object']).columns)}分类")
        
        # 智能分析模板
        st.markdown("#### 🎯 智能分析模板")
        
        # 根据数据特征推荐合适的分析
        data = st.session_state.research_data
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        categorical_cols = data.select_dtypes(include=['object']).columns
        
        st.markdown("**根据您的数据特征，我们推荐以下分析：**")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if len(numeric_cols) > 0:
                if st.button("📊 描述性统计", key="quick_desc", help="适合所有数据类型，了解基本特征"):
                    st.session_state.quick_analysis = "descriptive"
                    st.rerun()
            else:
                st.button("📊 描述性统计", key="quick_desc_disabled", disabled=True, help="需要数值变量")
        
        with col2:
            if len(categorical_cols) >= 1 and len(numeric_cols) >= 1:
                group_options = [col for col in categorical_cols if data[col].nunique() <= 10]
                if group_options:
                    if st.button("🔬 组间比较", key="quick_ttest", help=f"推荐分组变量：{', '.join(group_options[:2])}"):
                        st.session_state.quick_analysis = "ttest"
                        st.rerun()
                else:
                    st.button("🔬 组间比较", key="quick_ttest_disabled", disabled=True, help="需要合适的分组变量")
            else:
                st.button("🔬 组间比较", key="quick_ttest_disabled", disabled=True, help="需要分组变量和数值变量")
        
        with col3:
            if len(numeric_cols) >= 2:
                if st.button("🔗 相关性分析", key="quick_corr", help=f"将分析{len(numeric_cols)}个数值变量的相关性"):
                    st.session_state.quick_analysis = "correlation"
                    st.rerun()
            else:
                st.button("🔗 相关性分析", key="quick_corr_disabled", disabled=True, help="需要至少2个数值变量")
        
        with col4:
            if len(data) >= 100 and len(numeric_cols) >= 3:
                if st.button("🤖 机器学习", key="quick_ml", help="样本量和变量数适合机器学习"):
                    st.session_state.quick_analysis = "machine_learning"
                    st.rerun()
            else:
                reason = "样本量不足" if len(data) < 100 else "变量数不足"
                st.button("🤖 机器学习", key="quick_ml_disabled", disabled=True, help=f"{reason}，推荐先进行基础分析")
        
        # 高级分析模板
        st.markdown("#### 🚀 高级分析模板")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📊 回归分析", key="quick_regression", help="探索变量间的预测关系"):
                st.session_state.quick_analysis = "regression"
                st.rerun()
        
        with col2:
            if st.button("📈 方差分析", key="quick_anova", help="多组比较分析"):
                st.session_state.quick_analysis = "anova"
                st.rerun()
        
        with col3:
            if st.button("🔍 因子分析", key="quick_factor", help="探索潜在结构"):
                st.session_state.quick_analysis = "factor"
                st.rerun()
        
        with col4:
            if st.button("🎯 聚类分析", key="quick_cluster", help="发现数据模式"):
                st.session_state.quick_analysis = "cluster"
                st.rerun()

        
        # 执行快速分析
        if 'quick_analysis' in st.session_state:
            display_quick_analysis(data, st.session_state.quick_analysis)
    
    else:
        st.info("📁 请先上传或加载数据以开始分析")
        if st.button("📁 上传数据", use_container_width=True, key="workbench_upload_data"):
            st.session_state.current_step = 2
            st.rerun()
    
    # AI助手功能
    st.markdown("---")
    st.markdown("### 🤖 AI科研助手")
    
    ai_assistant = get_intermediate_ai_assistant()
    if ai_assistant:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🧠 智能分析建议", key="ai_method"):
                if st.session_state.research_data is not None:
                    data = st.session_state.research_data
                    with st.spinner("🔍 AI正在深度分析您的数据..."):
                        try:
                            # 构建详细的数据特征
                            numeric_cols = data.select_dtypes(include=[np.number]).columns
                            categorical_cols = data.select_dtypes(include=['object']).columns
                            missing_ratio = data.isnull().sum().sum() / (len(data) * len(data.columns))
                            
                            data_context = {
                                "sample_size": len(data),
                                "numeric_variables": len(numeric_cols),
                                "categorical_variables": len(categorical_cols),
                                "missing_data_ratio": round(missing_ratio * 100, 2),
                                "data_shape": f"{len(data)}行 × {len(data.columns)}列",
                                "column_names": list(data.columns[:5])  # 前5列
                            }
                            
                            # 智能分析建议
                            if len(numeric_cols) >= 2:
                                analysis_suggestion = "建议先进行相关性分析，然后根据研究目标选择回归分析"
                            elif len(categorical_cols) >= 1 and len(numeric_cols) >= 1:
                                analysis_suggestion = "建议进行分组比较分析（t检验或方差分析）"
                            else:
                                analysis_suggestion = "建议从描述性统计开始，了解数据基本特征"
                            
                            recommendation = ai_assistant.recommend_statistical_method(
                                data_context,
                                analysis_suggestion
                            )
                            
                            st.success("✅ AI智能分析完成")
                            
                            # 结构化显示推荐结果
                            with st.expander("📊 数据特征分析", expanded=True):
                                col_a, col_b, col_c = st.columns(3)
                                with col_a:
                                    st.metric("样本量", len(data))
                                    st.metric("数值变量", len(numeric_cols))
                                with col_b:
                                    st.metric("分类变量", len(categorical_cols))
                                    st.metric("缺失比例", f"{missing_ratio*100:.1f}%")
                                with col_c:
                                    if len(data) < 30:
                                        st.warning("⚠️ 样本量较小")
                                    elif len(data) > 1000:
                                        st.info("ℹ️ 大样本数据")
                                    else:
                                        st.success("✅ 样本量适中")
                            
                            with st.expander("🎯 分析方法推荐", expanded=True):
                                st.markdown(recommendation)
                            
                            # 添加报告导出功能
                            try:
                                render_report_export_section(
                                    data=data,
                                    ai_analysis=recommendation,
                                    mode="中级模式",
                                    additional_context={
                                        "analysis_step": "分析方法推荐",
                                        "data_context": data_context,
                                        "analysis_suggestion": analysis_suggestion
                                    }
                                )
                            except Exception as export_error:
                                st.error(f"报告导出功能初始化失败: {str(export_error)}")
                                
                        except Exception as e:
                            st.error(f"❌ AI分析失败：{str(e)}")
                            st.info("💡 请检查网络连接或稍后重试")
                else:
                    st.info("请先上传数据后再使用AI分析功能")
        
        with col2:
            if st.button("📝 结果解释", key="ai_interpret"):
                if 'analysis_results' in st.session_state and st.session_state.analysis_results:
                    with st.spinner("AI正在解释结果..."):
                        try:
                            interpretation = ai_assistant.answer_research_question(
                                "请解释这些统计结果的含义和意义",
                                "结果解释",
                                str(st.session_state.analysis_results)
                            )
                            st.success("✅ AI结果解释")
                            st.markdown(interpretation)
                            
                            # 添加报告导出功能
                            try:
                                render_report_export_section(
                                    data=st.session_state.research_data,
                                    ai_analysis=interpretation,
                                    mode="中级模式",
                                    additional_context={
                                        "analysis_step": "结果解释",
                                        "analysis_results": st.session_state.analysis_results
                                    }
                                )
                            except Exception as export_error:
                                st.error(f"报告导出功能初始化失败: {str(export_error)}")
                            
                        except Exception as e:
                            st.error(f"❌ AI解释失败：{str(e)}")
        
        with col3:
            if st.button("📄 报告优化", key="ai_report"):
                if st.session_state.research_data is not None:
                    with st.spinner("AI正在优化报告..."):
                        try:
                            optimization = ai_assistant.generate_academic_report_section(
                                "results",
                                {"data_info": f"样本量{len(st.session_state.research_data)}", "analysis_results": st.session_state.get('analysis_results', {})}
                            )
                            st.success("✅ AI报告优化")
                            st.markdown(optimization)
                            
                            # 添加报告导出功能
                            try:
                                render_report_export_section(
                                    data=st.session_state.research_data,
                                    ai_analysis=optimization,
                                    mode="中级模式",
                                    additional_context={
                                        "analysis_step": "报告优化",
                                        "data_info": f"样本量{len(st.session_state.research_data)}",
                                        "analysis_results": st.session_state.get('analysis_results', {})
                                    }
                                )
                            except Exception as export_error:
                                st.error(f"报告导出功能初始化失败: {str(export_error)}")
                            
                        except Exception as e:
                            st.error(f"❌ AI优化失败：{str(e)}")
    else:
        st.warning("⚠️ AI助手暂时不可用，请检查网络连接或API配置")

def display_quick_analysis(data, analysis_type):
    """显示快速分析结果"""
    st.markdown(f"### 📊 {analysis_type.replace('_', ' ').title()} 结果")
    
    if analysis_type == "descriptive":
        display_descriptive_analysis(data)
    elif analysis_type == "ttest":
        display_ttest_analysis(data)
    elif analysis_type == "anova":
        display_anova_analysis(data)
    elif analysis_type == "correlation":
        display_correlation_analysis(data)
    elif analysis_type == "regression":
        display_regression_analysis(data)
    elif analysis_type == "factor":
        display_factor_analysis(data)
    elif analysis_type == "cluster":
        display_cluster_analysis(data)
    elif analysis_type == "machine_learning":
        display_machine_learning_analysis(data)

def display_descriptive_analysis(data):
    """显示描述性统计分析"""
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) > 0:
        # 添加进度指示器
        with st.spinner("正在计算描述性统计..."):
            # 描述性统计表格
            desc_stats = data[numeric_cols].describe()
            
            # 添加更多统计量
            progress_bar = st.progress(0)
            progress_bar.progress(25)
            desc_stats.loc['skewness'] = data[numeric_cols].skew()
            progress_bar.progress(50)
            desc_stats.loc['kurtosis'] = data[numeric_cols].kurtosis()
            progress_bar.progress(75)
            desc_stats.loc['cv'] = data[numeric_cols].std() / data[numeric_cols].mean() * 100
            progress_bar.progress(100)
            progress_bar.empty()
        
        st.markdown("#### 📊 描述性统计表")
        st.dataframe(desc_stats.round(3), use_container_width=True)
        
        # 可视化
        col1, col2 = st.columns(2)
        
        with col1:
            # 直方图
            selected_var = st.selectbox("选择变量查看分布", numeric_cols, key="desc_hist")
            fig = px.histogram(data, x=selected_var, title=f"{selected_var}的分布")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # 箱线图
            fig2 = px.box(data, y=selected_var, title=f"{selected_var}的箱线图")
            st.plotly_chart(fig2, use_container_width=True)
        
        # 保存结果
        st.session_state.analysis_results['descriptive'] = desc_stats.to_dict()
        
        st.success("✅ 描述性统计分析完成")
    else:
        st.warning("⚠️ 没有数值变量可供分析")

def display_ttest_analysis(data):
    """显示t检验分析"""
    st.markdown("#### t检验分析")
    
    # 选择变量
    col1, col2 = st.columns(2)
    with col1:
        group_var = st.selectbox("选择分组变量", data.columns, key="ttest_group")
    with col2:
        outcome_var = st.selectbox("选择结果变量", data.select_dtypes(include=[np.number]).columns, key="ttest_outcome")
    
    if group_var and outcome_var:
        # 检查分组数量
        groups = data[group_var].unique()
        if len(groups) == 2:
            # 独立样本t检验
            group1_data = data[data[group_var] == groups[0]][outcome_var].dropna()
            group2_data = data[data[group_var] == groups[1]][outcome_var].dropna()
            
            t_stat, p_value = stats.ttest_ind(group1_data, group2_data)
            
            # 计算效应量
            pooled_std = np.sqrt(((len(group1_data) - 1) * group1_data.var() + 
                                (len(group2_data) - 1) * group2_data.var()) / 
                               (len(group1_data) + len(group2_data) - 2))
            cohens_d = (group1_data.mean() - group2_data.mean()) / pooled_std
            
            # 显示结果
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("t统计量", f"{t_stat:.4f}")
            with col2:
                st.metric("p值", f"{p_value:.4f}")
            with col3:
                st.metric("Cohen's d", f"{cohens_d:.4f}")
            with col4:
                significance = "显著" if p_value < 0.05 else "不显著"
                st.metric("显著性", significance)
            
            # 描述性统计
            desc_stats = data.groupby(group_var)[outcome_var].describe()
            st.markdown("#### 分组描述性统计")
            st.dataframe(desc_stats, use_container_width=True)
            
            # 可视化
            fig = px.box(data, x=group_var, y=outcome_var, title=f"{outcome_var}在各{group_var}的分布")
            st.plotly_chart(fig, use_container_width=True)
            
            # 保存结果
            st.session_state.analysis_results['ttest'] = {
                't_stat': t_stat,
                'p_value': p_value,
                'cohens_d': cohens_d,
                'group1_mean': group1_data.mean(),
                'group2_mean': group2_data.mean(),
                'group1_std': group1_data.std(),
                'group2_std': group2_data.std()
            }
            
            st.success("✅ t检验分析完成")
        else:
            st.warning("⚠️ 分组变量必须恰好有2个水平")

def display_anova_analysis(data):
    """显示方差分析"""
    st.markdown("#### 方差分析")
    
    # 选择变量
    col1, col2 = st.columns(2)
    with col1:
        group_var = st.selectbox("选择分组变量", data.columns, key="anova_group")
    with col2:
        outcome_var = st.selectbox("选择结果变量", data.select_dtypes(include=[np.number]).columns, key="anova_outcome")
    
    if group_var and outcome_var:
        # 单因素方差分析
        groups = data[group_var].unique()
        if len(groups) > 2:
            group_data = [data[data[group_var] == group][outcome_var].dropna() for group in groups]
            
            f_stat, p_value = stats.f_oneway(*group_data)
            
            # 计算效应量
            ss_between = sum(len(g) * (g.mean() - data[outcome_var].mean())**2 for g in group_data)
            ss_total = sum((x - data[outcome_var].mean())**2 for x in data[outcome_var].dropna())
            eta_squared = ss_between / ss_total
            
            # 显示结果
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("F统计量", f"{f_stat:.4f}")
            with col2:
                st.metric("p值", f"{p_value:.4f}")
            with col3:
                st.metric("η²", f"{eta_squared:.4f}")
            with col4:
                significance = "显著" if p_value < 0.05 else "不显著"
                st.metric("显著性", significance)
            
            # 描述性统计
            desc_stats = data.groupby(group_var)[outcome_var].describe()
            st.markdown("#### 分组描述性统计")
            st.dataframe(desc_stats, use_container_width=True)
            
            # 可视化
            fig = px.box(data, x=group_var, y=outcome_var, title=f"{outcome_var}在各{group_var}的分布")
            st.plotly_chart(fig, use_container_width=True)
            
            # 保存结果
            st.session_state.analysis_results['anova'] = {
                'f_stat': f_stat,
                'p_value': p_value,
                'eta_squared': eta_squared
            }
            
            st.success("✅ 方差分析完成")
        else:
            st.warning("⚠️ 分组变量需要超过2个水平")

def display_correlation_analysis(data):
    """显示相关性分析"""
    st.markdown("#### 相关性分析")
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) > 1:
        # 计算相关性矩阵
        corr_matrix = data[numeric_cols].corr()
        
        # 显示相关性矩阵
        st.markdown("#### 相关性矩阵")
        st.dataframe(corr_matrix.round(3), use_container_width=True)
        
        # 相关性热力图
        fig = px.imshow(
            corr_matrix,
            title="变量相关性热力图",
            color_continuous_scale='RdBu',
            aspect='auto'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 散点图矩阵
        fig2 = px.scatter_matrix(data[numeric_cols], title="变量散点图矩阵")
        st.plotly_chart(fig2, use_container_width=True)
        
        # 保存结果
        st.session_state.analysis_results['correlation'] = corr_matrix.to_dict()
        
        st.success("✅ 相关性分析完成")
    else:
        st.warning("⚠️ 需要至少2个数值变量进行相关性分析")

def display_regression_analysis(data):
    """显示回归分析"""
    st.markdown("#### 📊 回归分析")
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) < 2:
        st.warning("⚠️ 需要至少2个数值变量进行回归分析")
        return
    
    # 变量选择
    st.markdown("**选择变量：**")
    col1, col2 = st.columns(2)
    with col1:
        target_var = st.selectbox("选择因变量 (Y)", numeric_cols, key="reg_target")
    with col2:
        feature_vars = st.multiselect("选择自变量 (X)", [col for col in numeric_cols if col != target_var], key="reg_features")
    
    if target_var and feature_vars:
        with st.spinner("正在执行回归分析..."):
            try:
                # 执行回归分析
                from sklearn.linear_model import LinearRegression
                from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
                from sklearn.preprocessing import StandardScaler
                
                X = data[feature_vars]
                y = data[target_var]
                
                # 处理缺失值
                valid_indices = X.notna().all(axis=1) & y.notna()
                X_clean = X[valid_indices]
                y_clean = y[valid_indices]
                
                if len(X_clean) < 10:
                    st.error("❌ 有效数据点不足，无法进行可靠的回归分析")
                    return
                
                # 标准化特征
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X_clean)
                
                # 训练模型
                model = LinearRegression()
                model.fit(X_scaled, y_clean)
                y_pred = model.predict(X_scaled)
                
                # 计算指标
                r2 = r2_score(y_clean, y_pred)
                rmse = mean_squared_error(y_clean, y_pred, squared=False)
                mae = mean_absolute_error(y_clean, y_pred)
                
                # 显示结果
                st.success("✅ 回归分析完成！")
                
                # 模型性能指标
                st.markdown("**📈 模型性能指标：**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("R² (决定系数)", f"{r2:.4f}", delta=None)
                with col2:
                    st.metric("RMSE (均方根误差)", f"{rmse:.4f}", delta=None)
                with col3:
                    st.metric("MAE (平均绝对误差)", f"{mae:.4f}", delta=None)
                
                # 系数表
                st.markdown("**🔢 回归系数：**")
                coef_df = pd.DataFrame({
                    '变量': ['截距'] + feature_vars,
                    '标准化系数': [model.intercept_] + list(model.coef_),
                    '原始系数': [model.intercept_] + list(model.coef_)
                })
                st.dataframe(coef_df.round(4), use_container_width=True)
                
                # 回归方程
                equation = f"Y = {model.intercept_:.4f}"
                for i, var in enumerate(feature_vars):
                    if model.coef_[i] >= 0:
                        equation += f" + {model.coef_[i]:.4f} × {var}"
                    else:
                        equation += f" - {abs(model.coef_[i]):.4f} × {var}"
                
                st.markdown(f"**📝 回归方程：** {equation}")
                
                # 可视化
                st.markdown("**📊 回归结果可视化：**")
                col1, col2 = st.columns(2)
                
                with col1:
                    # 实际值 vs 预测值
                    fig1 = px.scatter(x=y_clean, y=y_pred, 
                                    title="实际值 vs 预测值",
                                    labels={'x': '实际值', 'y': '预测值'})
                    fig1.add_trace(px.line(x=[y_clean.min(), y_clean.max()], 
                                          y=[y_clean.min(), y_clean.max()]).data[0])
                    st.plotly_chart(fig1, use_container_width=True)
                
                with col2:
                    # 残差图
                    residuals = y_clean - y_pred
                    fig2 = px.scatter(x=y_pred, y=residuals,
                                    title="残差图",
                                    labels={'x': '预测值', 'y': '残差'})
                    fig2.add_hline(y=0, line_dash="dash", line_color="red")
                    st.plotly_chart(fig2, use_container_width=True)
                
                # 保存结果
                if 'analysis_results' not in st.session_state:
                    st.session_state.analysis_results = {}
                
                st.session_state.analysis_results['regression'] = {
                    'target': target_var,
                    'features': feature_vars,
                    'r2': r2,
                    'rmse': rmse,
                    'mae': mae,
                    'equation': equation,
                    'coefficients': dict(zip(['截距'] + feature_vars, [model.intercept_] + list(model.coef_)))
                }
                
                st.success("✅ 回归分析结果已保存！")
                
            except Exception as e:
                st.error(f"❌ 回归分析失败：{str(e)}")
                st.info("💡 请检查数据质量和变量选择")
    else:
        st.info("ℹ️ 请选择因变量和自变量")

def display_factor_analysis(data):
    """显示因子分析"""
    st.markdown("#### 因子分析")
    st.info("因子分析功能正在开发中...")

def display_cluster_analysis(data):
    """显示聚类分析"""
    st.markdown("#### 🎯 聚类分析")
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) < 2:
        st.warning("⚠️ 需要至少2个数值变量进行聚类分析")
        return
    
    # 变量选择
    st.markdown("**选择聚类变量：**")
    selected_vars = st.multiselect("选择用于聚类的变量", numeric_cols, key="cluster_vars")
    
    if len(selected_vars) >= 2:
        # 参数设置
        st.markdown("**设置聚类参数：**")
        col1, col2 = st.columns(2)
        with col1:
            n_clusters = st.slider("聚类数量", 2, min(10, len(data)), 3, key="n_clusters")
        with col2:
            algorithm = st.selectbox("聚类算法", ["K-means", "层次聚类"], key="cluster_algorithm")
        
        if st.button("🚀 开始聚类分析", key="start_clustering"):
            with st.spinner("正在执行聚类分析..."):
                try:
                    # 执行聚类
                    from sklearn.cluster import KMeans, AgglomerativeClustering
                    from sklearn.preprocessing import StandardScaler
                    from sklearn.metrics import silhouette_score
                    
                    X = data[selected_vars].dropna()
                    
                    if len(X) < n_clusters:
                        st.error("❌ 数据点数量少于聚类数量")
                        return
                    
                    # 标准化
                    scaler = StandardScaler()
                    X_scaled = scaler.fit_transform(X)
                    
                    # 聚类
                    if algorithm == "K-means":
                        model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
                    else:
                        model = AgglomerativeClustering(n_clusters=n_clusters)
                    
                    clusters = model.fit_predict(X_scaled)
                    
                    # 计算轮廓系数
                    silhouette_avg = silhouette_score(X_scaled, clusters)
                    
                    # 显示结果
                    st.success("✅ 聚类分析完成！")
                    
                    # 聚类质量指标
                    st.markdown("**📊 聚类质量指标：**")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("聚类数量", n_clusters)
                    with col2:
                        st.metric("轮廓系数", f"{silhouette_avg:.4f}")
                    with col3:
                        st.metric("数据点数量", len(X))
                    
                    # 聚类结果
                    X_with_clusters = X.copy()
                    X_with_clusters['聚类'] = clusters
                    
                    st.markdown("**📈 各聚类统计信息：**")
                    cluster_stats = X_with_clusters.groupby('聚类').describe()
                    st.dataframe(cluster_stats.round(3), use_container_width=True)
                    
                    # 聚类大小分布
                    cluster_sizes = X_with_clusters['聚类'].value_counts().sort_index()
                    st.markdown("**📊 聚类大小分布：**")
                    fig_size = px.bar(x=cluster_sizes.index, y=cluster_sizes.values,
                                    title="各聚类包含的数据点数量",
                                    labels={'x': '聚类编号', 'y': '数据点数量'})
                    st.plotly_chart(fig_size, use_container_width=True)
                    
                    # 可视化
                    st.markdown("**🎨 聚类结果可视化：**")
                    
                    if len(selected_vars) >= 2:
                        # 散点图
                        fig_scatter = px.scatter(X_with_clusters, x=selected_vars[0], y=selected_vars[1], 
                                               color='聚类', title=f"聚类结果散点图 ({selected_vars[0]} vs {selected_vars[1]})")
                        st.plotly_chart(fig_scatter, use_container_width=True)
                        
                        # 如果变量数量>=3，显示3D图
                        if len(selected_vars) >= 3:
                            fig_3d = px.scatter_3d(X_with_clusters, x=selected_vars[0], y=selected_vars[1], z=selected_vars[2],
                                                 color='聚类', title=f"3D聚类结果 ({selected_vars[0]}, {selected_vars[1]}, {selected_vars[2]})")
                            st.plotly_chart(fig_3d, use_container_width=True)
                    
                    # 聚类特征分析
                    st.markdown("**🔍 聚类特征分析：**")
                    cluster_means = X_with_clusters.groupby('聚类')[selected_vars].mean()
                    
                    # 热力图显示各聚类的特征均值
                    fig_heatmap = px.imshow(cluster_means.T, 
                                          title="各聚类在不同变量上的均值热力图",
                                          labels=dict(x="聚类编号", y="变量", color="均值"))
                    st.plotly_chart(fig_heatmap, use_container_width=True)
                    
                    # 保存结果
                    if 'analysis_results' not in st.session_state:
                        st.session_state.analysis_results = {}
                    
                    st.session_state.analysis_results['clustering'] = {
                        'algorithm': algorithm,
                        'n_clusters': n_clusters,
                        'variables': selected_vars,
                        'silhouette_score': silhouette_avg,
                        'cluster_sizes': cluster_sizes.to_dict(),
                        'cluster_means': cluster_means.to_dict()
                    }
                    
                    st.success("✅ 聚类分析结果已保存！")
                    
                except Exception as e:
                    st.error(f"❌ 聚类分析失败：{str(e)}")
                    st.info("💡 请检查数据质量和参数设置")
    else:
        st.info("ℹ️ 请选择至少2个变量进行聚类分析")

def display_machine_learning_analysis(data):
    """显示机器学习分析"""
    st.markdown("#### 🤖 机器学习分析")
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) < 2:
        st.warning("⚠️ 需要至少2个数值变量进行机器学习分析")
        return
    
    # 选择机器学习任务类型
    ml_task = st.selectbox(
        "选择机器学习任务：",
        ["回归分析", "分类分析", "聚类分析", "降维分析"],
        key="ml_task_type"
    )
    
    if ml_task == "回归分析":
        display_ml_regression(data, numeric_cols)
    elif ml_task == "分类分析":
        display_ml_classification(data, numeric_cols)
    elif ml_task == "聚类分析":
        display_ml_clustering(data, numeric_cols)
    elif ml_task == "降维分析":
        display_ml_dimension_reduction(data, numeric_cols)

def display_ml_regression(data, numeric_cols):
    """显示机器学习回归分析"""
    st.markdown("**🤖 机器学习回归分析**")
    
    # 变量选择
    col1, col2 = st.columns(2)
    with col1:
        target_var = st.selectbox("选择因变量 (Y)", numeric_cols, key="ml_reg_target")
    with col2:
        feature_vars = st.multiselect("选择自变量 (X)", [col for col in numeric_cols if col != target_var], key="ml_reg_features")
    
    if target_var and feature_vars:
        # 选择算法
        algorithm = st.selectbox("选择回归算法", ["线性回归", "随机森林回归", "支持向量回归"], key="ml_reg_algorithm")
        
        if st.button("🚀 开始机器学习回归", key="start_ml_regression"):
            with st.spinner("正在执行机器学习回归分析..."):
                try:
                    from sklearn.model_selection import train_test_split
                    from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
                    from sklearn.preprocessing import StandardScaler
                    
                    # 准备数据
                    X = data[feature_vars]
                    y = data[target_var]
                    
                    # 处理缺失值
                    valid_indices = X.notna().all(axis=1) & y.notna()
                    X_clean = X[valid_indices]
                    y_clean = y[valid_indices]
                    
                    if len(X_clean) < 20:
                        st.error("❌ 有效数据点不足，无法进行可靠的机器学习分析")
                        return
                    
                    # 数据分割
                    X_train, X_test, y_train, y_test = train_test_split(X_clean, y_clean, test_size=0.2, random_state=42)
                    
                    # 标准化
                    scaler = StandardScaler()
                    X_train_scaled = scaler.fit_transform(X_train)
                    X_test_scaled = scaler.transform(X_test)
                    
                    # 选择模型
                    if algorithm == "线性回归":
                        from sklearn.linear_model import LinearRegression
                        model = LinearRegression()
                    elif algorithm == "随机森林回归":
                        from sklearn.ensemble import RandomForestRegressor
                        model = RandomForestRegressor(n_estimators=100, random_state=42)
                    elif algorithm == "支持向量回归":
                        from sklearn.svm import SVR
                        model = SVR(kernel='rbf')
                    
                    # 训练模型
                    model.fit(X_train_scaled, y_train)
                    y_pred = model.predict(X_test_scaled)
                    
                    # 计算指标
                    r2 = r2_score(y_test, y_pred)
                    rmse = mean_squared_error(y_test, y_pred, squared=False)
                    mae = mean_absolute_error(y_test, y_pred)
                    
                    # 显示结果
                    st.success("✅ 机器学习回归分析完成！")
                    
                    # 模型性能指标
                    st.markdown("**📈 模型性能指标：**")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("R² (决定系数)", f"{r2:.4f}", delta=None)
                    with col2:
                        st.metric("RMSE (均方根误差)", f"{rmse:.4f}", delta=None)
                    with col3:
                        st.metric("MAE (平均绝对误差)", f"{mae:.4f}", delta=None)
                    
                    # 特征重要性（如果适用）
                    if hasattr(model, 'feature_importances_'):
                        st.markdown("**🔢 特征重要性：**")
                        importance_df = pd.DataFrame({
                            '特征': feature_vars,
                            '重要性': model.feature_importances_
                        }).sort_values('重要性', ascending=False)
                        st.dataframe(importance_df, use_container_width=True)
                        
                        # 特征重要性图
                        fig = px.bar(importance_df, x='特征', y='重要性', title="特征重要性")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # 保存结果
                    if 'analysis_results' not in st.session_state:
                        st.session_state.analysis_results = {}
                    
                    st.session_state.analysis_results['ml_regression'] = {
                        'algorithm': algorithm,
                        'target': target_var,
                        'features': feature_vars,
                        'r2': r2,
                        'rmse': rmse,
                        'mae': mae
                    }
                    
                    st.success("✅ 机器学习回归结果已保存！")
                    
                except Exception as e:
                    st.error(f"❌ 机器学习回归分析失败：{str(e)}")

def display_ml_classification(data, numeric_cols):
    """显示机器学习分类分析"""
    st.markdown("**🤖 机器学习分类分析**")
    st.info("分类分析需要目标变量为分类变量，当前数据集中没有合适的分类变量")
    st.info("💡 建议：将数值变量转换为分类变量，或使用聚类分析")

def display_ml_clustering(data, numeric_cols):
    """显示机器学习聚类分析"""
    st.markdown("**🤖 机器学习聚类分析**")
    
    # 变量选择
    selected_vars = st.multiselect("选择聚类变量", numeric_cols, key="ml_cluster_vars")
    
    if len(selected_vars) >= 2:
        # 选择算法
        algorithm = st.selectbox("选择聚类算法", ["K-means", "DBSCAN", "层次聚类"], key="ml_cluster_algorithm")
        
        if algorithm == "K-means":
            n_clusters = st.slider("聚类数量", 2, min(10, len(data)), 3, key="ml_n_clusters")
        
        if st.button("🚀 开始机器学习聚类", key="start_ml_clustering"):
            with st.spinner("正在执行机器学习聚类分析..."):
                try:
                    from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
                    from sklearn.preprocessing import StandardScaler
                    from sklearn.metrics import silhouette_score
                    
                    X = data[selected_vars].dropna()
                    
                    if len(X) < 10:
                        st.error("❌ 有效数据点不足")
                        return
                    
                    # 标准化
                    scaler = StandardScaler()
                    X_scaled = scaler.fit_transform(X)
                    
                    # 选择模型
                    if algorithm == "K-means":
                        model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
                    elif algorithm == "DBSCAN":
                        model = DBSCAN(eps=0.5, min_samples=5)
                    elif algorithm == "层次聚类":
                        model = AgglomerativeClustering(n_clusters=n_clusters)
                    
                    # 执行聚类
                    clusters = model.fit_predict(X_scaled)
                    
                    # 计算轮廓系数
                    if len(set(clusters)) > 1:
                        silhouette_avg = silhouette_score(X_scaled, clusters)
                    else:
                        silhouette_avg = 0
                    
                    # 显示结果
                    st.success("✅ 机器学习聚类分析完成！")
                    
                    # 聚类质量指标
                    st.markdown("**📊 聚类质量指标：**")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("聚类数量", len(set(clusters)))
                    with col2:
                        st.metric("轮廓系数", f"{silhouette_avg:.4f}")
                    with col3:
                        st.metric("数据点数量", len(X))
                    
                    # 保存结果
                    if 'analysis_results' not in st.session_state:
                        st.session_state.analysis_results = {}
                    
                    st.session_state.analysis_results['ml_clustering'] = {
                        'algorithm': algorithm,
                        'variables': selected_vars,
                        'n_clusters': len(set(clusters)),
                        'silhouette_score': silhouette_avg
                    }
                    
                    st.success("✅ 机器学习聚类结果已保存！")
                    
                except Exception as e:
                    st.error(f"❌ 机器学习聚类分析失败：{str(e)}")

def display_ml_dimension_reduction(data, numeric_cols):
    """显示机器学习降维分析"""
    st.markdown("**🤖 机器学习降维分析**")
    
    if len(numeric_cols) < 3:
        st.warning("⚠️ 需要至少3个数值变量进行降维分析")
        return
    
    # 选择算法
    algorithm = st.selectbox("选择降维算法", ["PCA", "t-SNE"], key="ml_dim_algorithm")
    
    if st.button("🚀 开始降维分析", key="start_dim_reduction"):
        with st.spinner("正在执行降维分析..."):
            try:
                from sklearn.decomposition import PCA
                from sklearn.manifold import TSNE
                from sklearn.preprocessing import StandardScaler
                
                X = data[numeric_cols].dropna()
                
                if len(X) < 10:
                    st.error("❌ 有效数据点不足")
                    return
                
                # 标准化
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X)
                
                # 选择模型
                if algorithm == "PCA":
                    model = PCA(n_components=2)
                    result = model.fit_transform(X_scaled)
                    
                    # 解释方差比例
                    explained_variance_ratio = model.explained_variance_ratio_
                    
                    st.markdown("**📊 PCA结果：**")
                    st.write(f"解释方差比例: {explained_variance_ratio[0]:.4f}, {explained_variance_ratio[1]:.4f}")
                    st.write(f"累计解释方差: {sum(explained_variance_ratio):.4f}")
                    
                elif algorithm == "t-SNE":
                    model = TSNE(n_components=2, random_state=42)
                    result = model.fit_transform(X_scaled)
                    
                    st.markdown("**📊 t-SNE结果：**")
                    st.write("t-SNE降维完成")
                
                # 可视化结果
                fig = px.scatter(x=result[:, 0], y=result[:, 1],
                               title=f"{algorithm}降维结果",
                               labels={'x': f'{algorithm}1', 'y': f'{algorithm}2'})
                st.plotly_chart(fig, use_container_width=True)
                
                # 保存结果
                if 'analysis_results' not in st.session_state:
                    st.session_state.analysis_results = {}
                
                st.session_state.analysis_results['ml_dimension_reduction'] = {
                    'algorithm': algorithm,
                    'variables': list(numeric_cols),
                    'explained_variance_ratio': explained_variance_ratio.tolist() if algorithm == "PCA" else None
                }
                
                st.success("✅ 降维分析结果已保存！")
                
            except Exception as e:
                st.error(f"❌ 降维分析失败：{str(e)}")

def render_intermediate_sidebar():
    """渲染中间模式侧边栏 - Material Design 3风格"""
    with st.sidebar:
        # Material Design 3 侧边栏样式
        st.markdown("""
        <style>
        /* Material Design 3 侧边栏样式 */
        [data-testid="stSidebar"] {
            background: var(--md-surface) !important;
            border-right: 1px solid var(--md-outline-variant) !important;
            padding: var(--md-spacing-lg) !important;
        }
        
        /* Material Design 3 侧边栏卡片 */
        .md-sidebar-card {
            background: var(--md-surface);
            border-radius: var(--md-radius-large);
            padding: var(--md-spacing-lg);
            margin: var(--md-spacing-md) 0;
            box-shadow: var(--md-shadow-1);
            border: 1px solid var(--md-outline-variant);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .md-sidebar-card:hover {
            box-shadow: var(--md-shadow-2);
            transform: translateY(-2px);
        }
        
        /* Material Design 3 侧边栏按钮 */
        .md-sidebar-button {
            background: var(--md-primary);
            color: var(--md-on-primary);
            border: none;
            border-radius: var(--md-radius-extra-large);
            padding: var(--md-spacing-sm) var(--md-spacing-md);
            font-family: var(--md-font-family);
            font-size: var(--md-font-size-body);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            width: 100%;
            margin: var(--md-spacing-xs) 0;
            min-height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .md-sidebar-button:hover {
            box-shadow: var(--md-shadow-2);
            transform: translateY(-1px);
        }
        
        .md-sidebar-button.secondary {
            background: var(--md-secondary);
            color: var(--md-on-secondary);
        }
        
        .md-sidebar-button.outlined {
            background: transparent;
            color: var(--md-primary);
            border: 1px solid var(--md-primary);
        }
        
        /* Material Design 3 状态指示器 */
        .md-status-item {
            display: flex;
            align-items: center;
            padding: var(--md-spacing-sm) var(--md-spacing-md);
            background: var(--md-surface-variant);
            border-radius: var(--md-radius-medium);
            margin: var(--md-spacing-xs) 0;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .md-status-item:hover {
            background: var(--md-primary-container);
            color: var(--md-on-primary-container);
        }
        
        .md-status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: var(--md-spacing-sm);
            flex-shrink: 0;
        }
        
        .md-status-dot.success {
            background: var(--md-success);
            box-shadow: 0 0 8px rgba(76, 175, 80, 0.4);
        }
        
        .md-status-dot.warning {
            background: var(--md-warning);
            box-shadow: 0 0 8px rgba(255, 152, 0, 0.4);
        }
        
        .md-status-dot.error {
            background: var(--md-error);
            box-shadow: 0 0 8px rgba(244, 67, 54, 0.4);
        }
        
        .md-status-dot.info {
            background: var(--md-info);
            box-shadow: 0 0 8px rgba(33, 150, 243, 0.4);
        }
        
        /* Material Design 3 进度条 */
        .md-progress-container {
            background: var(--md-outline-variant);
            border-radius: var(--md-radius-small);
            height: 8px;
            overflow: hidden;
            margin: var(--md-spacing-sm) 0;
        }
        
        .md-progress-bar {
            height: 100%;
            background: var(--md-primary);
            border-radius: var(--md-radius-small);
            transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
        }
        
        .md-progress-bar::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
            animation: shimmer 2s infinite;
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        /* Material Design 3 分割线 */
        .md-divider {
            height: 1px;
            background: var(--md-outline-variant);
            margin: var(--md-spacing-md) 0;
            border: none;
        }
        
        /* Material Design 3 标签 */
        .md-chip {
            display: inline-flex;
            align-items: center;
            background: var(--md-surface-variant);
            color: var(--md-on-surface-variant);
            border-radius: var(--md-radius-extra-large);
            padding: var(--md-spacing-xs) var(--md-spacing-sm);
            font-size: var(--md-font-size-small);
            font-weight: 500;
            margin: var(--md-spacing-xs);
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .md-chip:hover {
            background: var(--md-primary-container);
            color: var(--md-on-primary-container);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Material Design 3 标题区域
        st.markdown("""
        <div class="md-sidebar-card" style="text-align: center; margin-bottom: 2rem;">
            <h2 class="md-title" style="color: var(--md-secondary); margin: 0; font-size: 1.5rem;">🚀 普通导航</h2>
            <p class="md-body" style="margin: 0.5rem 0 0 0; opacity: 0.8; font-size: 0.9rem;">
                智能数据分析平台
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Material Design 3 模式切换区域
        st.markdown("""
        <div class="md-sidebar-card">
            <h4 class="md-title" style="margin: 0 0 1rem 0; color: var(--md-on-surface);">🔄 模式切换</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # 使用selectbox进行模式选择，与专业模式保持一致
        current_mode = st.session_state.get('selected_mode', 'intermediate')
        # 安全检查：确保current_mode是有效的键
        if current_mode not in ANALYSIS_MODES:
            st.error("❌ 无效的模式选择，请重新选择模式")
            st.session_state.selected_mode = 'intermediate'
            st.session_state.current_page = "🎯 模式选择"
            st.rerun()
            return
        
        mode_info = ANALYSIS_MODES[current_mode]
        
        # 使用selectbox进行模式选择
        mode_options = {
            f"{ANALYSIS_MODES['beginner']['icon']} {ANALYSIS_MODES['beginner']['name']}": "beginner",
            f"{ANALYSIS_MODES['intermediate']['icon']} {ANALYSIS_MODES['intermediate']['name']}": "intermediate", 
            f"{ANALYSIS_MODES['professional']['icon']} {ANALYSIS_MODES['professional']['name']}": "professional"
        }
        
        current_mode_display = f"{mode_info['icon']} {mode_info['name']}"
        
        selected_mode_display = st.selectbox(
            "选择分析模式",
            list(mode_options.keys()),
            index=list(mode_options.keys()).index(current_mode_display),
            key="mode_selector_intermediate"
        )
        
        if mode_options[selected_mode_display] != current_mode:
            st.session_state.selected_mode = mode_options[selected_mode_display]
            st.success(f"✅ 已切换到 {selected_mode_display}")
            st.rerun()
        
        # 当前模式提示
        st.markdown(f"""
        <div class="md-status-item" style="background: var(--md-secondary-container); color: var(--md-on-secondary-container);">
            <div class="md-status-dot success"></div>
            <span class="md-body" style="font-weight: 500;">{mode_info['icon']} 当前：{mode_info['name']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Material Design 3 研究进度概览
        st.markdown("""
        <div class="md-sidebar-card">
            <h4 class="md-title" style="margin: 0 0 1rem 0; color: var(--md-on-surface);">📚 研究进度概览</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # 计算研究进度
        total_steps = 5
        current_step = st.session_state.get('current_step', 1)
        progress_percentage = (current_step / total_steps) * 100
        
        st.markdown(f"""
        <div style="margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span class="md-body" style="font-weight: 500;">研究进度</span>
                <span class="md-body" style="opacity: 0.8;">{current_step}/{total_steps}</span>
            </div>
            <div class="md-progress-container">
                <div class="md-progress-bar" style="width: {progress_percentage}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Material Design 3 研究步骤导航
        st.markdown("""
        <div class="md-sidebar-card">
            <h4 class="md-title" style="margin: 0 0 1rem 0; color: var(--md-on-surface);">🎯 研究步骤导航</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # 研究步骤按钮
        steps = [
            (1, "📁 数据管理", "上传和管理研究数据"),
            (2, "🔍 探索分析", "进行探索性数据分析"),
            (3, "📊 可视化", "创建研究图表"),
            (4, "📈 统计分析", "进行统计检验"),
            (5, "📄 研究报告", "生成研究报告")
        ]
        
        for step_num, step_title, step_desc in steps:
            is_current = step_num == current_step
            is_completed = step_num < current_step
            
            if is_current:
                st.markdown(f"""
                <div class="md-status-item" style="background: var(--md-secondary-container); color: var(--md-on-secondary-container); border: 2px solid var(--md-secondary);">
                    <div class="md-status-dot success"></div>
                    <div style="flex: 1;">
                        <div class="md-body" style="font-weight: 600;">{step_title}</div>
                        <div class="md-body" style="font-size: 0.8rem; opacity: 0.8;">{step_desc}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            elif is_completed:
                st.markdown(f"""
                <div class="md-status-item" style="background: var(--md-success-container); color: var(--md-success);">
                    <div class="md-status-dot success"></div>
                    <div style="flex: 1;">
                        <div class="md-body" style="font-weight: 600;">{step_title}</div>
                        <div class="md-body" style="font-size: 0.8rem; opacity: 0.8;">{step_desc}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="md-status-item" style="opacity: 0.6;">
                    <div class="md-status-dot info"></div>
                    <div style="flex: 1;">
                        <div class="md-body" style="font-weight: 600;">{step_title}</div>
                        <div class="md-body" style="font-size: 0.8rem; opacity: 0.8;">{step_desc}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # 添加步骤跳转按钮
            if step_num != current_step and step_num <= current_step + 1:
                if st.button(f"跳转到步骤 {step_num}", key=f"step_{step_num}_intermediate", use_container_width=True):
                    st.session_state.current_step = step_num
                    st.rerun()
        
        # Material Design 3 快捷操作面板
        st.markdown("""
        <div class="md-sidebar-card">
            <h4 class="md-title" style="margin: 0 0 1rem 0; color: var(--md-on-surface);">⚡ 快捷操作</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # 快捷操作按钮
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🏠 工作台", key="quick_workspace_intermediate", use_container_width=True):
                st.session_state.current_step = 1
                st.rerun()
            
            if st.button("📁 数据", key="quick_data_intermediate", use_container_width=True):
                st.session_state.current_step = 1
                st.rerun()
        
        with col2:
            if st.button("📊 分析", key="quick_analysis_intermediate", use_container_width=True):
                st.session_state.current_step = 2
                st.rerun()
            
            if st.button("📄 报告", key="quick_report_intermediate", use_container_width=True):
                st.session_state.current_step = 5
                st.rerun()
        
        # Material Design 3 页面导航选择器
        st.markdown("""
        <div class="md-sidebar-card">
            <h4 class="md-title" style="margin: 0 0 1rem 0; color: var(--md-on-surface);">🎯 页面导航</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # 创建导航选项
        nav_options = {
            "📁 数据管理": 1,
            "🔍 探索分析": 2,
            "📊 可视化": 3,
            "📈 统计分析": 4,
            "📄 研究报告": 5
        }
        
        # 过滤可用的导航选项
        available_options = {}
        for name, step in nav_options.items():
            if step == 1:  # 数据管理总是可用
                available_options[name] = step
            elif step == 2 and hasattr(st.session_state, 'data') and st.session_state.data is not None:  # 探索分析需要数据
                available_options[name] = step
            elif step == 3 and hasattr(st.session_state, 'data') and st.session_state.data is not None:  # 可视化需要数据
                available_options[name] = step
            elif step == 4 and hasattr(st.session_state, 'data') and st.session_state.data is not None:  # 统计分析需要数据
                available_options[name] = step
            elif step == 5 and hasattr(st.session_state, 'data') and st.session_state.data is not None:  # 研究报告需要数据
                available_options[name] = step
        
        # 当前步骤对应的选项名称
        current_option = None
        for name, step in nav_options.items():
            if step == st.session_state.current_step:
                current_option = name
                break
        
        # 导航选择器
        selected_nav = st.selectbox(
            "选择要跳转的页面：",
            options=list(available_options.keys()),
            index=list(available_options.keys()).index(current_option) if current_option in available_options else 0,
            key="nav_selector_intermediate",
            help="选择要跳转的页面，系统会自动检查前置条件"
        )
        
        if selected_nav in available_options and available_options[selected_nav] != st.session_state.current_step:
            if st.button("🚀 跳转", key="nav_jump_intermediate", use_container_width=True):
                st.session_state.current_step = available_options[selected_nav]
                st.rerun()
        
        # Material Design 3 状态指示器面板
        st.markdown("""
        <div class="md-sidebar-card">
            <h4 class="md-title" style="margin: 0 0 1rem 0; color: var(--md-on-surface);">📊 状态指示器</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # 系统状态指示
        st.markdown("""
        <div class="md-status-item">
            <div class="md-status-dot success"></div>
            <span class="md-body">系统就绪</span>
        </div>
        """, unsafe_allow_html=True)
        
        # 数据状态指示
        if hasattr(st.session_state, 'data') and st.session_state.data is not None:
            st.markdown("""
            <div class="md-status-item">
                <div class="md-status-dot success"></div>
                <span class="md-body">数据已加载</span>
            </div>
            """, unsafe_allow_html=True)
        
        if hasattr(st.session_state, 'cleaned_data') and st.session_state.cleaned_data is not None:
            st.markdown("""
            <div class="md-status-item">
                <div class="md-status-dot success"></div>
                <span class="md-body">数据已清洗</span>
            </div>
            """, unsafe_allow_html=True)
        
        if hasattr(st.session_state, 'analysis_complete') and st.session_state.analysis_complete:
            st.markdown("""
            <div class="md-status-item">
                <div class="md-status-dot success"></div>
                <span class="md-body">分析已完成</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Material Design 3 智能建议面板
        st.markdown("""
        <div class="md-sidebar-card">
            <h4 class="md-title" style="margin: 0 0 1rem 0; color: var(--md-on-surface);">💡 智能建议面板</h4>
            <div style="font-size: 0.9rem; color: var(--md-on-surface-variant); line-height: 1.4;">
        """, unsafe_allow_html=True)
        
        if st.session_state.current_step == 1:
            st.markdown("• 准备您的研究数据<br>• 支持多种数据格式<br>• 注意数据质量", unsafe_allow_html=True)
        elif st.session_state.current_step == 2:
            st.markdown("• 进行探索性数据分析<br>• 了解数据特征<br>• 识别数据模式", unsafe_allow_html=True)
        elif st.session_state.current_step == 3:
            st.markdown("• 创建合适的图表<br>• 选择合适的可视化类型<br>• 注意图表美观性", unsafe_allow_html=True)
        elif st.session_state.current_step == 4:
            st.markdown("• 选择合适的统计方法<br>• 进行假设检验<br>• 解释统计结果", unsafe_allow_html=True)
        elif st.session_state.current_step == 5:
            st.markdown("• 生成完整研究报告<br>• 包含所有分析结果<br>• 导出多种格式", unsafe_allow_html=True)
        else:
            st.markdown("• 按照研究流程进行<br>• 每个步骤都要仔细完成<br>• 注意研究质量", unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Material Design 3 研究统计
        st.markdown("""
        <div class="md-sidebar-card">
            <h4 class="md-title" style="margin: 0 0 1rem 0; color: var(--md-on-surface);">📈 研究统计</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # 研究统计信息
        completed_steps = current_step - 1
        remaining_steps = total_steps - current_step
        
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
            <div style="text-align: center; padding: 1rem; background: var(--md-success-container); border-radius: var(--md-radius-medium);">
                <div class="md-body" style="font-size: 1.5rem; font-weight: 600; color: var(--md-success);">{completed_steps}</div>
                <div class="md-body" style="font-size: 0.8rem; color: var(--md-success);">已完成</div>
            </div>
            <div style="text-align: center; padding: 1rem; background: var(--md-info-container); border-radius: var(--md-radius-medium);">
                <div class="md-body" style="font-size: 1.5rem; font-weight: 600; color: var(--md-info);">{remaining_steps}</div>
                <div class="md-body" style="font-size: 0.8rem; color: var(--md-info);">待完成</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 研究时间估算
        estimated_time = remaining_steps * 10  # 假设每个步骤10分钟
        st.markdown(f"""
        <div class="md-status-item" style="background: var(--md-warning-container); color: var(--md-warning);">
            <div class="md-status-dot warning"></div>
            <span class="md-body">预计还需 {estimated_time} 分钟完成研究</span>
        </div>
        """, unsafe_allow_html=True)

def render_intermediate_mode():
    """渲染普通模式主界面"""
    # 初始化session state
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
    if 'research_data' not in st.session_state:
        st.session_state.research_data = None
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = {}
    
    # 渲染侧边栏
    render_intermediate_sidebar()
    
    # 根据当前步骤显示不同页面
    if st.session_state.current_step == 1:
        display_research_workbench()
    elif st.session_state.current_step == 2:
        display_data_management()
    elif st.session_state.current_step == 3:
        display_statistical_analysis()
    elif st.session_state.current_step == 4:
        display_data_visualization()
    elif st.session_state.current_step == 5:
        display_report_generation()

# 继续添加其他函数...

def display_data_management():
    """显示数据管理页面"""
    st.markdown('<h2 class="sub-header">📊 数据管理</h2>', unsafe_allow_html=True)
    
    # 数据上传选项
    upload_option = st.radio(
        "选择数据来源：",
        ["📊 使用示例数据", "📁 上传数据文件"],
        horizontal=True,
        key="data_upload_option"
    )
    
    if upload_option == "📊 使用示例数据":
        st.markdown("### 📊 示例科研数据")
        st.markdown("""
        **数据集说明：**
        - 实验研究数据（实验组 vs 对照组）
        - 前后测设计
        - 包含120名参与者
        - 变量：组别、前测成绩、后测成绩、年龄、性别等
        """)
        
        if st.button("📊 加载示例数据", use_container_width=True, key="load_sample_data"):
            data = create_research_sample_data()
            st.session_state.research_data = data
            st.success("✅ 示例数据加载成功！")
            st.rerun()
    
    else:
        st.markdown("### 📁 上传数据文件")
        uploaded_file = st.file_uploader(
            "选择数据文件",
            type=['csv', 'xlsx', 'xls', 'json', 'parquet'],
            help="支持CSV、Excel、JSON、Parquet格式",
            key="data_file_uploader"
        )
        
        if uploaded_file is not None:
            try:
                # 显示文件信息
                file_size = uploaded_file.size / 1024 / 1024  # MB
                st.info(f"📁 文件信息：{uploaded_file.name} ({file_size:.2f} MB)")
                
                with st.spinner("正在读取数据文件..."):
                    # 根据文件类型读取数据
                    if uploaded_file.name.endswith('.csv'):
                        data = pd.read_csv(uploaded_file)
                    elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                        data = pd.read_excel(uploaded_file)
                    elif uploaded_file.name.endswith('.json'):
                        data = pd.read_json(uploaded_file)
                    elif uploaded_file.name.endswith('.parquet'):
                        data = pd.read_parquet(uploaded_file)
                    else:
                        st.error("❌ 不支持的文件格式")
                        return
                
                # 数据质量初步检查
                with st.spinner("正在检查数据质量..."):
                    missing_count = data.isnull().sum().sum()
                    duplicate_count = data.duplicated().sum()
                    
                st.session_state.research_data = data
                
                # 详细的成功信息
                st.success(f"✅ 数据上传成功！")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("数据行数", len(data))
                with col2:
                    st.metric("数据列数", len(data.columns))
                with col3:
                    st.metric("缺失值", missing_count)
                with col4:
                    st.metric("重复行", duplicate_count)
                
                # 数据质量提示
                if missing_count > 0:
                    st.warning(f"⚠️ 检测到 {missing_count} 个缺失值，建议在分析前进行处理")
                if duplicate_count > 0:
                    st.warning(f"⚠️ 检测到 {duplicate_count} 行重复数据，建议检查数据质量")
                
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ 数据上传失败：{str(e)}")
                st.info("💡 请检查文件格式是否正确，或尝试其他格式的文件")
    
    # 数据概览
    if st.session_state.research_data is not None:
        data = st.session_state.research_data
        
        st.markdown("### 📋 数据概览")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("样本量", len(data))
        with col2:
            st.metric("变量数", len(data.columns))
        with col3:
            st.metric("缺失值", data.isnull().sum().sum())
        with col4:
            st.metric("内存使用", f"{data.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
        
        # 数据预览
        st.markdown("### 👀 数据预览")
        st.dataframe(data.head(10), use_container_width=True)
        
        # 数据类型分析
        st.markdown("### 🔍 数据类型分析")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**数据类型分布：**")
            dtype_counts = data.dtypes.value_counts()
            fig = px.pie(
                values=dtype_counts.values,
                names=dtype_counts.index.astype(str),
                title="数据类型分布"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**变量列表：**")
            for col in data.columns:
                dtype = str(data[col].dtype)
                missing = data[col].isnull().sum()
                st.write(f"• **{col}** ({dtype}) - 缺失值: {missing}")
        
        # 智能数据质量分析
        st.markdown("### 🔍 智能数据质量分析")
        
        with st.spinner("正在分析数据质量..."):
            # 缺失值分析
            missing_data = data.isnull().sum()
            missing_percent = (missing_data / len(data) * 100)
            
            # 重复值分析
            duplicate_count = data.duplicated().sum()
            
            # 数据类型一致性检查
            inconsistent_types = []
            for col in data.columns:
                if data[col].dtype == 'object':
                    # 检查是否应该是数值类型
                    try:
                        pd.to_numeric(data[col].dropna())
                        inconsistent_types.append(col)
                    except:
                        pass
        
        # 数据质量概览
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("缺失值总数", missing_data.sum(), delta=None)
        with col2:
            st.metric("重复行数", duplicate_count, delta=None)
        with col3:
            st.metric("完整度", f"{(1-missing_data.sum()/(len(data)*len(data.columns)))*100:.1f}%")
        with col4:
            st.metric("类型异常列", len(inconsistent_types))
        
        # 缺失值详细分析
        if missing_data.sum() > 0:
            st.markdown("#### 📊 缺失值分布")
            missing_df = pd.DataFrame({
                '变量': missing_data.index,
                '缺失数量': missing_data.values,
                '缺失比例(%)': missing_percent.values
            }).sort_values('缺失数量', ascending=False)
            
            # 只显示有缺失值的变量
            missing_df_filtered = missing_df[missing_df['缺失数量'] > 0]
            
            if len(missing_df_filtered) > 0:
                fig = px.bar(
                    missing_df_filtered,
                    x='变量',
                    y='缺失数量',
                    title="各变量缺失值数量",
                    color='缺失比例(%)',
                    color_continuous_scale='Reds'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # 智能处理建议
                with st.expander("💡 数据质量改进建议", expanded=True):
                    for _, row in missing_df_filtered.iterrows():
                        if row['缺失比例(%)'] > 50:
                            st.error(f"❌ **{row['变量']}**: 缺失比例过高({row['缺失比例(%)']:.1f}%)，建议考虑删除该变量")
                        elif row['缺失比例(%)'] > 20:
                            st.warning(f"⚠️ **{row['变量']}**: 缺失比例较高({row['缺失比例(%)']:.1f}%)，建议使用插值法或均值填充")
                        elif row['缺失比例(%)'] > 5:
                            st.info(f"ℹ️ **{row['变量']}**: 少量缺失({row['缺失比例(%)']:.1f}%)，可考虑删除缺失行或简单填充")
                        else:
                            st.success(f"✅ **{row['变量']}**: 缺失比例很低({row['缺失比例(%)']:.1f}%)，数据质量良好")
        else:
            st.success("✅ 恭喜！数据中没有缺失值")
        
        # 重复值提醒
        if duplicate_count > 0:
            st.warning(f"⚠️ 检测到 {duplicate_count} 行重复数据，建议检查后决定是否删除")
        
        # 数据类型异常提醒
        if inconsistent_types:
            st.info(f"💡 检测到可能的数据类型异常列：{', '.join(inconsistent_types)}，建议检查数据格式")
    
    # 返回工作台
    if st.button("🏠 返回工作台", use_container_width=True, key="data_management_return_workbench"):
        st.session_state.current_step = 1
        st.rerun()

def display_statistical_analysis():
    """显示统计分析页面"""
    st.markdown('<h2 class="sub-header">📈 统计分析</h2>', unsafe_allow_html=True)
    
    if st.session_state.research_data is None:
        st.warning("⚠️ 请先上传或加载数据")
        if st.button("📊 数据管理", use_container_width=True, key="statistical_analysis_data_management"):
            st.session_state.current_step = 2
            st.rerun()
        return
    
    data = st.session_state.research_data
    
    # 分析类型选择
    st.markdown("### 🎯 选择分析类型")
    analysis_type = st.selectbox(
        "选择分析类型：",
        [
            "描述性统计分析",
            "推断性统计分析",
            "相关性分析",
            "回归分析",
            "多变量分析",
            "非参数检验"
        ],
        key="statistical_analysis_type"
    )
    
    if analysis_type == "描述性统计分析":
        display_descriptive_analysis(data)
    elif analysis_type == "推断性统计分析":
        display_inferential_analysis(data)
    elif analysis_type == "相关性分析":
        display_correlation_analysis(data)
    elif analysis_type == "回归分析":
        display_regression_analysis(data)
    elif analysis_type == "多变量分析":
        display_multivariate_analysis(data)
    elif analysis_type == "非参数检验":
        display_nonparametric_analysis(data)
    
    # 返回工作台
    if st.button("🏠 返回工作台", use_container_width=True, key="statistical_analysis_return_workbench"):
        st.session_state.current_step = 1
        st.rerun()

def display_inferential_analysis(data):
    """显示推断性统计分析"""
    st.markdown("#### 推断性统计分析")
    
    # 选择分析类型
    inferential_type = st.selectbox(
        "选择推断性分析方法：",
        ["t检验", "方差分析", "卡方检验"],
        key="inferential_analysis_type"
    )
    
    if inferential_type == "t检验":
        display_ttest_analysis(data)
    elif inferential_type == "方差分析":
        display_anova_analysis(data)
    elif inferential_type == "卡方检验":
        display_chi_square_analysis(data)

def display_chi_square_analysis(data):
    """显示卡方检验分析"""
    st.markdown("#### 卡方检验分析")
    
    # 选择变量
    col1, col2 = st.columns(2)
    with col1:
        var1 = st.selectbox("选择第一个变量", data.columns, key="chi_var1")
    with col2:
        var2 = st.selectbox("选择第二个变量", data.columns, key="chi_var2")
    
    if var1 and var2:
        # 创建列联表
        contingency_table = pd.crosstab(data[var1], data[var2])
        
        st.markdown("#### 列联表")
        st.dataframe(contingency_table, use_container_width=True)
        
        # 卡方检验
        from scipy.stats import chi2_contingency
        chi2, p_value, dof, expected = chi2_contingency(contingency_table)
        
        # 显示结果
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("χ²统计量", f"{chi2:.4f}")
        with col2:
            st.metric("p值", f"{p_value:.4f}")
        with col3:
            significance = "显著" if p_value < 0.05 else "不显著"
            st.metric("显著性", significance)
        
        # 可视化
        fig = px.imshow(
            contingency_table,
            title=f"{var1}与{var2}的列联表热力图",
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 保存结果
        st.session_state.analysis_results['chi_square'] = {
            'chi2': chi2,
            'p_value': p_value,
            'dof': dof
        }
        
        st.success("✅ 卡方检验分析完成")

def display_multivariate_analysis(data):
    """显示多变量分析"""
    st.markdown("#### 多变量分析")
    st.info("多变量分析功能正在开发中...")

def display_nonparametric_analysis(data):
    """显示非参数检验"""
    st.markdown("#### 非参数检验")
    st.info("非参数检验功能正在开发中...")

def display_data_visualization():
    """显示数据可视化页面"""
    st.markdown('<h2 class="sub-header">📊 数据可视化</h2>', unsafe_allow_html=True)
    
    if st.session_state.research_data is None:
        st.warning("⚠️ 请先上传或加载数据")
        if st.button("📊 数据管理", use_container_width=True, key="visualization_data_management"):
            st.session_state.current_step = 2
            st.rerun()
        return
    
    data = st.session_state.research_data
    
    # 可视化类型选择
    st.markdown("### 📈 选择可视化类型")
    viz_type = st.selectbox(
        "选择图表类型：",
        [
            "分布图",
            "关系图",
            "比较图",
            "统计图",
            "高级图表"
        ],
        key="visualization_type"
    )
    
    if viz_type == "分布图":
        display_distribution_charts(data)
    elif viz_type == "关系图":
        display_relationship_charts(data)
    elif viz_type == "比较图":
        display_comparison_charts(data)
    elif viz_type == "统计图":
        display_statistical_charts(data)
    elif viz_type == "高级图表":
        display_advanced_charts(data)
    
    # 返回工作台
    if st.button("🏠 返回工作台", use_container_width=True, key="visualization_return_workbench"):
        st.session_state.current_step = 1
        st.rerun()

def display_distribution_charts(data):
    """显示分布图"""
    st.markdown("#### 分布图")
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        selected_var = st.selectbox("选择变量", numeric_cols, key="dist_var")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 直方图
            fig1 = px.histogram(data, x=selected_var, title=f"{selected_var}的分布直方图")
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # 密度图
            fig2 = px.histogram(data, x=selected_var, nbins=30, title=f"{selected_var}的密度图")
            fig2.update_traces(opacity=0.7)
            st.plotly_chart(fig2, use_container_width=True)
        
        # 箱线图
        fig3 = px.box(data, y=selected_var, title=f"{selected_var}的箱线图")
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("⚠️ 没有数值变量可供分析")

def display_relationship_charts(data):
    """显示关系图"""
    st.markdown("#### 关系图")
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 1:
        col1, col2 = st.columns(2)
        
        with col1:
            x_var = st.selectbox("选择X变量", numeric_cols, key="rel_x")
        with col2:
            y_var = st.selectbox("选择Y变量", numeric_cols, key="rel_y")
        
        if x_var != y_var:
            # 散点图
            fig = px.scatter(data, x=x_var, y=y_var, title=f"{x_var}与{y_var}的散点图")
            st.plotly_chart(fig, use_container_width=True)
            
            # 相关性热力图
            corr_matrix = data[[x_var, y_var]].corr()
            fig2 = px.imshow(
                corr_matrix,
                title="相关性热力图",
                color_continuous_scale='RdBu'
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("⚠️ 请选择不同的变量")
    else:
        st.warning("⚠️ 需要至少2个数值变量")

def display_comparison_charts(data):
    """显示比较图"""
    st.markdown("#### 比较图")
    
    # 选择变量
    col1, col2 = st.columns(2)
    with col1:
        group_var = st.selectbox("选择分组变量", data.columns, key="comp_group")
    with col2:
        value_var = st.selectbox("选择数值变量", data.select_dtypes(include=[np.number]).columns, key="comp_value")
    
    if group_var and value_var:
        # 分组箱线图
        fig1 = px.box(data, x=group_var, y=value_var, title=f"{value_var}在各{group_var}的分布")
        st.plotly_chart(fig1, use_container_width=True)
        
        # 分组条形图
        mean_data = data.groupby(group_var)[value_var].mean().reset_index()
        fig2 = px.bar(mean_data, x=group_var, y=value_var, title=f"{value_var}在各{group_var}的平均值")
        st.plotly_chart(fig2, use_container_width=True)

def display_statistical_charts(data):
    """显示统计图"""
    st.markdown("#### 📊 统计图")
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) == 0:
        st.warning("⚠️ 没有数值变量可供分析")
        return
    
    # 选择统计图类型
    chart_type = st.selectbox(
        "选择统计图类型：",
        ["Q-Q图 (正态性检验)", "P-P图 (概率图)", "残差图", "箱线图矩阵", "相关性热力图"],
        key="statistical_chart_type"
    )
    
    if chart_type == "Q-Q图 (正态性检验)":
        display_qq_plot(data, numeric_cols)
    elif chart_type == "P-P图 (概率图)":
        display_pp_plot(data, numeric_cols)
    elif chart_type == "残差图":
        display_residual_plot(data, numeric_cols)
    elif chart_type == "箱线图矩阵":
        display_boxplot_matrix(data, numeric_cols)
    elif chart_type == "相关性热力图":
        display_correlation_heatmap(data, numeric_cols)

def display_qq_plot(data, numeric_cols):
    """显示Q-Q图"""
    st.markdown("**Q-Q图 (正态性检验)**")
    
    selected_var = st.selectbox("选择变量", numeric_cols, key="qq_var")
    
    if selected_var:
        # 计算Q-Q图
        from scipy import stats
        
        # 移除缺失值
        clean_data = data[selected_var].dropna()
        
        if len(clean_data) > 0:
            # 计算理论分位数
            theoretical_quantiles = stats.norm.ppf(np.linspace(0.01, 0.99, len(clean_data)))
            sample_quantiles = np.sort(clean_data)
            
            # 创建Q-Q图
            fig = px.scatter(x=theoretical_quantiles, y=sample_quantiles,
                           title=f"Q-Q图: {selected_var}的正态性检验",
                           labels={'x': '理论分位数', 'y': '样本分位数'})
            
            # 添加对角线
            min_val = min(theoretical_quantiles.min(), sample_quantiles.min())
            max_val = max(theoretical_quantiles.max(), sample_quantiles.max())
            fig.add_trace(px.line(x=[min_val, max_val], y=[min_val, max_val]).data[0])
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 正态性检验
            shapiro_stat, shapiro_p = stats.shapiro(clean_data)
            st.markdown(f"**Shapiro-Wilk正态性检验：**")
            st.write(f"- 统计量: {shapiro_stat:.4f}")
            st.write(f"- p值: {shapiro_p:.4f}")
            
            if shapiro_p > 0.05:
                st.success("✅ 数据符合正态分布 (p > 0.05)")
            else:
                st.warning("⚠️ 数据不符合正态分布 (p ≤ 0.05)")

def display_pp_plot(data, numeric_cols):
    """显示P-P图"""
    st.markdown("**P-P图 (概率图)**")
    
    selected_var = st.selectbox("选择变量", numeric_cols, key="pp_var")
    
    if selected_var:
        from scipy import stats
        
        # 移除缺失值
        clean_data = data[selected_var].dropna()
        
        if len(clean_data) > 0:
            # 计算累积概率
            sorted_data = np.sort(clean_data)
            empirical_cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
            theoretical_cdf = stats.norm.cdf(sorted_data, np.mean(sorted_data), np.std(sorted_data))
            
            # 创建P-P图
            fig = px.scatter(x=theoretical_cdf, y=empirical_cdf,
                           title=f"P-P图: {selected_var}的概率图",
                           labels={'x': '理论累积概率', 'y': '经验累积概率'})
            
            # 添加对角线
            fig.add_trace(px.line(x=[0, 1], y=[0, 1]).data[0])
            
            st.plotly_chart(fig, use_container_width=True)

def display_residual_plot(data, numeric_cols):
    """显示残差图"""
    st.markdown("**残差图**")
    
    if len(numeric_cols) < 2:
        st.warning("⚠️ 需要至少2个数值变量进行回归分析")
        return
    
    col1, col2 = st.columns(2)
    with col1:
        x_var = st.selectbox("选择X变量", numeric_cols, key="residual_x")
    with col2:
        y_var = st.selectbox("选择Y变量", numeric_cols, key="residual_y")
    
    if x_var != y_var:
        # 执行简单线性回归
        from sklearn.linear_model import LinearRegression
        
        X = data[[x_var, y_var]].dropna()
        
        if len(X) > 0:
            model = LinearRegression()
            model.fit(X[x_var].values.reshape(-1, 1), X[y_var])
            y_pred = model.predict(X[x_var].values.reshape(-1, 1))
            residuals = X[y_var] - y_pred
            
            # 残差图
            fig = px.scatter(x=y_pred, y=residuals,
                           title=f"残差图: {y_var} vs {x_var}",
                           labels={'x': '预测值', 'y': '残差'})
            fig.add_hline(y=0, line_dash="dash", line_color="red")
            st.plotly_chart(fig, use_container_width=True)

def display_boxplot_matrix(data, numeric_cols):
    """显示箱线图矩阵"""
    st.markdown("**箱线图矩阵**")
    
    if len(numeric_cols) > 10:
        st.info("ℹ️ 变量数量较多，显示前10个变量的箱线图")
        display_cols = numeric_cols[:10]
    else:
        display_cols = numeric_cols
    
    # 创建箱线图矩阵
    fig = px.box(data[display_cols], title="数值变量箱线图矩阵")
    st.plotly_chart(fig, use_container_width=True)

def display_correlation_heatmap(data, numeric_cols):
    """显示相关性热力图"""
    st.markdown("**相关性热力图**")
    
    if len(numeric_cols) < 2:
        st.warning("⚠️ 需要至少2个数值变量计算相关性")
        return
    
    # 计算相关性矩阵
    corr_matrix = data[numeric_cols].corr()
    
    # 创建热力图
    fig = px.imshow(corr_matrix, 
                   title="变量相关性热力图",
                   color_continuous_scale='RdBu',
                   aspect='auto')
    st.plotly_chart(fig, use_container_width=True)
    
    # 显示相关性矩阵
    st.markdown("**相关性矩阵：**")
    st.dataframe(corr_matrix.round(3), use_container_width=True)

def display_advanced_charts(data):
    """显示高级图表"""
    st.markdown("#### 🚀 高级图表")
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    categorical_cols = data.select_dtypes(include=['object']).columns
    
    if len(numeric_cols) == 0:
        st.warning("⚠️ 没有数值变量可供分析")
        return
    
    # 选择高级图表类型
    chart_type = st.selectbox(
        "选择高级图表类型：",
        ["3D散点图", "小提琴图", "密度图", "雷达图", "树状图"],
        key="advanced_chart_type"
    )
    
    if chart_type == "3D散点图":
        display_3d_scatter(data, numeric_cols)
    elif chart_type == "小提琴图":
        display_violin_plot(data, numeric_cols, categorical_cols)
    elif chart_type == "密度图":
        display_density_plot(data, numeric_cols)
    elif chart_type == "雷达图":
        display_radar_chart(data, numeric_cols)
    elif chart_type == "树状图":
        display_tree_map(data, numeric_cols, categorical_cols)

def display_3d_scatter(data, numeric_cols):
    """显示3D散点图"""
    st.markdown("**3D散点图**")
    
    if len(numeric_cols) < 3:
        st.warning("⚠️ 需要至少3个数值变量创建3D散点图")
        return
    
    col1, col2, col3 = st.columns(3)
    with col1:
        x_var = st.selectbox("选择X轴变量", numeric_cols, key="3d_x")
    with col2:
        y_var = st.selectbox("选择Y轴变量", numeric_cols, key="3d_y")
    with col3:
        z_var = st.selectbox("选择Z轴变量", numeric_cols, key="3d_z")
    
    if x_var != y_var and y_var != z_var and x_var != z_var:
        # 创建3D散点图
        fig = px.scatter_3d(data, x=x_var, y=y_var, z=z_var,
                           title=f"3D散点图: {x_var} vs {y_var} vs {z_var}")
        st.plotly_chart(fig, use_container_width=True)

def display_violin_plot(data, numeric_cols, categorical_cols):
    """显示小提琴图"""
    st.markdown("**小提琴图**")
    
    if len(categorical_cols) == 0:
        st.warning("⚠️ 需要分类变量创建小提琴图")
        return
    
    col1, col2 = st.columns(2)
    with col1:
        numeric_var = st.selectbox("选择数值变量", numeric_cols, key="violin_numeric")
    with col2:
        categorical_var = st.selectbox("选择分类变量", categorical_cols, key="violin_categorical")
    
    if numeric_var and categorical_var:
        # 检查分类变量的唯一值数量
        unique_values = data[categorical_var].nunique()
        if unique_values > 10:
            st.warning(f"⚠️ 分类变量 '{categorical_var}' 有 {unique_values} 个唯一值，建议选择唯一值较少的变量")
            return
        
        # 创建小提琴图
        fig = px.violin(data, x=categorical_var, y=numeric_var,
                       title=f"小提琴图: {numeric_var} 按 {categorical_var} 分组")
        st.plotly_chart(fig, use_container_width=True)

def display_density_plot(data, numeric_cols):
    """显示密度图"""
    st.markdown("**密度图**")
    
    selected_vars = st.multiselect("选择变量", numeric_cols, key="density_vars")
    
    if selected_vars:
        # 创建密度图
        fig = px.histogram(data, x=selected_vars, nbins=30, 
                          title="密度分布图",
                          opacity=0.7)
        fig.update_traces(opacity=0.7)
        st.plotly_chart(fig, use_container_width=True)

def display_radar_chart(data, numeric_cols):
    """显示雷达图"""
    st.markdown("**雷达图**")
    
    if len(numeric_cols) < 3:
        st.warning("⚠️ 需要至少3个数值变量创建雷达图")
        return
    
    selected_vars = st.multiselect("选择变量", numeric_cols, key="radar_vars", max_selections=8)
    
    if len(selected_vars) >= 3:
        # 计算每个变量的均值
        means = data[selected_vars].mean()
        
        # 创建雷达图数据
        fig = px.line_polar(r=means.values, theta=means.index, 
                           title="变量均值雷达图",
                           line_close=True)
        fig.update_traces(fill='toself')
        st.plotly_chart(fig, use_container_width=True)

def display_tree_map(data, numeric_cols, categorical_cols):
    """显示树状图"""
    st.markdown("**树状图**")
    
    if len(categorical_cols) == 0:
        st.warning("⚠️ 需要分类变量创建树状图")
        return
    
    col1, col2 = st.columns(2)
    with col1:
        categorical_var = st.selectbox("选择分类变量", categorical_cols, key="treemap_categorical")
    with col2:
        numeric_var = st.selectbox("选择数值变量", numeric_cols, key="treemap_numeric")
    
    if categorical_var and numeric_var:
        # 计算每个分类的均值
        grouped_data = data.groupby(categorical_var)[numeric_var].mean().reset_index()
        
        # 创建树状图
        fig = px.treemap(grouped_data, path=[categorical_var], values=numeric_var,
                        title=f"树状图: {numeric_var} 按 {categorical_var} 分组")
        st.plotly_chart(fig, use_container_width=True)

def display_report_generation():
    """显示报告生成页面"""
    st.markdown('<h2 class="sub-header">📄 报告生成</h2>', unsafe_allow_html=True)
    
    if st.session_state.research_data is None:
        st.warning("⚠️ 请先上传或加载数据")
        if st.button("📊 数据管理", use_container_width=True, key="report_data_management"):
            st.session_state.current_step = 2
            st.rerun()
        return
    
    data = st.session_state.research_data
    
    st.markdown("### 📋 学术报告生成")
    
    # 报告类型选择
    report_type = st.selectbox(
        "选择报告类型：",
        [
            "实验研究报告",
            "调查研究报告",
            "数据分析报告",
            "方法学报告"
        ],
        key="report_type"
    )
    
    # 报告内容
    st.markdown("#### 📝 报告内容")
    
    # 基本信息
    st.markdown("**研究基本信息：**")
    col1, col2 = st.columns(2)
    with col1:
        study_title = st.text_input("研究标题：", value="数据分析研究", key="study_title")
        researcher = st.text_input("研究者：", value="研究生", key="researcher")
    with col2:
        date = st.date_input("研究日期：", key="study_date")
        sample_size = st.number_input("样本量：", value=len(data), min_value=1, key="sample_size")
    
    # 生成报告
    if st.button("📄 生成学术报告", use_container_width=True, key="generate_academic_report"):
        generate_academic_report(data, report_type, study_title, researcher, date, sample_size)
    
    # 综合报告导出功能
    st.markdown("---")
    st.subheader("📄 导出完整分析报告")
    st.markdown("""
    <div class="info-box">
    <h4>📋 完整报告包含：</h4>
    <ul>
    <li>📊 数据概览和质量评估</li>
    <li>🧹 数据清洗结果和处理历史</li>
    <li>📈 可视化图表和数据洞察</li>
    <li>📊 统计分析结果</li>
    <li>🤖 AI分析建议</li>
    <li>🔬 科研分析成果</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # 调用综合报告导出功能
    render_comprehensive_report_export("中级模式")
    
    # 返回工作台
    if st.button("🏠 返回工作台", use_container_width=True, key="report_return_workbench"):
        st.session_state.current_step = 1
        st.rerun()

def export_analysis_results():
    """导出分析结果"""
    import io
    import base64
    from datetime import datetime
    
    if not st.session_state.analysis_results:
        st.sidebar.warning("⚠️ 没有可导出的分析结果")
        return
    
    # 创建报告内容
    report_content = "# 数据分析报告\n\n"
    report_content += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # 添加数据基本信息
    if st.session_state.research_data is not None:
        data = st.session_state.research_data
        report_content += f"## 数据基本信息\n\n"
        report_content += f"- 数据行数: {len(data)}\n"
        report_content += f"- 数据列数: {len(data.columns)}\n"
        report_content += f"- 变量名称: {', '.join(data.columns)}\n\n"
    
    # 添加分析结果
    report_content += f"## 分析结果\n\n"
    for analysis_type, results in st.session_state.analysis_results.items():
        report_content += f"### {analysis_type.upper()} 分析结果\n\n"
        
        if analysis_type == 'regression':
            report_content += f"- 因变量: {results['target']}\n"
            report_content += f"- 自变量: {', '.join(results['features'])}\n"
            report_content += f"- R²: {results['r2']:.4f}\n"
            report_content += f"- RMSE: {results['rmse']:.4f}\n"
            report_content += f"- MAE: {results['mae']:.4f}\n"
            report_content += f"- 回归方程: {results['equation']}\n\n"
            
        elif analysis_type == 'clustering':
            report_content += f"- 聚类算法: {results['algorithm']}\n"
            report_content += f"- 聚类数量: {results['n_clusters']}\n"
            report_content += f"- 聚类变量: {', '.join(results['variables'])}\n"
            report_content += f"- 轮廓系数: {results['silhouette_score']:.4f}\n"
            report_content += f"- 聚类大小: {results['cluster_sizes']}\n\n"
            
        elif analysis_type == 'ttest':
            report_content += f"- t统计量: {results['t_stat']:.4f}\n"
            report_content += f"- p值: {results['p_value']:.4f}\n"
            report_content += f"- Cohen's d: {results['cohens_d']:.4f}\n\n"
            
        elif analysis_type == 'anova':
            report_content += f"- F统计量: {results['f_stat']:.4f}\n"
            report_content += f"- p值: {results['p_value']:.4f}\n"
            report_content += f"- η²: {results['eta_squared']:.4f}\n\n"
            
        elif analysis_type == 'chi_square':
            report_content += f"- χ²统计量: {results['chi2']:.4f}\n"
            report_content += f"- p值: {results['p_value']:.4f}\n"
            report_content += f"- 自由度: {results['dof']}\n\n"
        
        else:
            for key, value in results.items():
                report_content += f"- {key}: {value}\n"
            report_content += "\n"
    
    # 创建下载按钮
    b64 = base64.b64encode(report_content.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="analysis_report.txt">📥 下载分析报告</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)
    st.sidebar.success("✅ 导出功能已准备就绪！")

def generate_academic_report(data, report_type, study_title, researcher, date, sample_size):
    """生成学术报告"""
    st.markdown("### 📄 生成的学术报告")
    
    # 报告标题
    st.markdown(f"# {study_title}")
    st.markdown(f"**研究者：** {researcher}  \n**日期：** {date}  \n**样本量：** {sample_size}")
    
    # 摘要
    st.markdown("## 摘要")
    st.markdown(f"""
    本研究对{sample_size}个样本进行了数据分析。数据集包含{len(data.columns)}个变量，
    涵盖了{', '.join(data.columns[:3])}等关键指标。通过系统的统计分析，
    本研究旨在探索数据中的模式和关系，为相关领域提供实证依据。
    """)
    
    # 方法
    st.markdown("## 方法")
    st.markdown("### 参与者")
    st.markdown(f"本研究共收集了{sample_size}个有效样本。")
    
    st.markdown("### 材料")
    st.markdown(f"数据集包含以下变量：{', '.join(data.columns)}")
    
    st.markdown("### 程序")
    st.markdown("数据分析采用以下步骤：")
    st.markdown("1. 数据预处理和质量检查")
    st.markdown("2. 描述性统计分析")
    st.markdown("3. 推断性统计分析")
    st.markdown("4. 数据可视化")
    
    # 结果
    st.markdown("## 结果")
    st.markdown("### 描述性统计")
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        desc_stats = data[numeric_cols].describe()
        st.dataframe(desc_stats, use_container_width=True)
    
    # 如果有分析结果，显示结果
    if st.session_state.analysis_results:
        st.markdown("### 推断性统计")
        for analysis_type, results in st.session_state.analysis_results.items():
            if analysis_type == 'ttest':
                st.markdown(f"""
                **独立样本t检验结果：**
                - t统计量 = {results['t_stat']:.4f}
                - p值 = {results['p_value']:.4f}
                - Cohen's d = {results['cohens_d']:.4f}
                """)
            elif analysis_type == 'anova':
                st.markdown(f"""
                **方差分析结果：**
                - F统计量 = {results['f_stat']:.4f}
                - p值 = {results['p_value']:.4f}
                - η² = {results['eta_squared']:.4f}
                """)
            elif analysis_type == 'chi_square':
                st.markdown(f"""
                **卡方检验结果：**
                - χ²统计量 = {results['chi2']:.4f}
                - p值 = {results['p_value']:.4f}
                - 自由度 = {results['dof']}
                """)
    
    # 讨论
    st.markdown("## 讨论")
    st.markdown("""
    本研究通过系统的数据分析，发现了数据中的重要模式和关系。
    这些发现为相关领域的研究提供了重要的实证依据。
    
    研究的局限性包括样本的代表性和变量的测量精度等方面。
    未来研究可以进一步扩大样本量，增加更多相关变量。
    """)
    
    # 结论
    st.markdown("## 结论")
    st.markdown("""
    本研究通过严谨的数据分析，为相关领域提供了有价值的发现。
    这些结果对理论发展和实践应用都具有重要意义。
    """)
    
    st.success("✅ 学术报告生成完成！")
