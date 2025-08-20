"""
重构后的智能数据分析平台主应用
将页面绘制功能与实际程序功能分开管理
"""

import streamlit as st
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# 导入配置和模块
from src.config.settings import PAGE_CONFIG, NAV_PAGES, CUSTOM_CSS, ANALYSIS_MODES
from src.modules.pages import render_home_page, render_sidebar, render_footer, render_mode_selection_page
from src.modules.beginner_mode import render_beginner_mode
from src.modules.intermediate_mode import render_intermediate_mode
from src.utils.data_processing import (
    load_data, calculate_data_quality_score, get_data_info,
    handle_missing_values, handle_duplicates, handle_outliers,
    clean_string_data, get_outlier_statistics, convert_data_format,
    get_missing_value_summary, get_data_type_summary, calculate_correlation_matrix
)
from src.utils.visualization_helpers import (
    create_bar_chart, create_line_chart, create_scatter_chart, create_pie_chart,
    create_histogram, create_box_chart, create_correlation_heatmap, create_violin_chart,
    create_3d_scatter, create_radar_chart, create_missing_values_chart,
    create_data_type_chart, create_distribution_comparison, create_learning_curve,
    create_confusion_matrix, create_feature_importance
)
from src.utils.ml_helpers import (
    validate_data_for_ml, preprocess_data_for_ml, train_classification_model,
    train_regression_model, perform_clustering, perform_cross_validation,
    generate_learning_curve, perform_feature_engineering, analyze_feature_importance,
    detect_outliers_iqr, perform_statistical_tests, calculate_elbow_curve
)
from src.utils.ai_assistant import get_ai_assistant
# 导入云端AI助手支持
try:
    from src.utils.ai_assistant_cloud import get_cloud_ai_assistant, get_ai_config_status
    CLOUD_AI_AVAILABLE = True
except ImportError:
    CLOUD_AI_AVAILABLE = False

# 导入报告导出功能
from src.utils.report_exporter import ReportExporter, get_download_link, get_download_link_bytes
# 导入综合报告导出组件
from src.modules.comprehensive_report_export import render_comprehensive_report_export

# 智能AI助手获取函数
def get_smart_ai_assistant():
    """
    智能获取AI助手实例，优先使用云端配置
    """
    # 优先尝试云端AI助手
    if CLOUD_AI_AVAILABLE:
        try:
            config_status = get_ai_config_status()
            if config_status["api_key_available"]:
                ai_assistant = get_cloud_ai_assistant()
                if ai_assistant is not None:
                    return ai_assistant
        except Exception:
            pass
    
    # 回退到本地AI助手
    try:
        return get_ai_assistant()
    except Exception:
        return None

# 设置页面配置
st.set_page_config(**PAGE_CONFIG)

# 应用自定义CSS样式
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# 主标题
st.markdown('<h1 class="main-header">👁️ 数眸 - 智能数据分析平台</h1>', unsafe_allow_html=True)
st.markdown('<p class="brand-slogan">让数据洞察如眸般清澈明亮</p>', unsafe_allow_html=True)

# 顶部横向导航
# 初始化页面状态和模式选择
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 首页"
if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = "professional"  # 默认为专业模式

# 检查模式
is_beginner_mode = st.session_state.get('selected_mode') == 'beginner'
is_intermediate_mode = st.session_state.get('selected_mode') == 'intermediate'
is_professional_mode = st.session_state.get('selected_mode') == 'professional'

# 只在专业模式下显示横向导航和侧边栏
if is_professional_mode:
    # 创建横向导航（移除模式选择页面）
    nav_pages_without_mode = [page for page in NAV_PAGES if page != "🎯 模式选择"]
    selected_page = st.radio(
        "选择功能模块",
        nav_pages_without_mode,
        horizontal=True,
        key="page_navigation"
    )

    # 更新当前页面
    if selected_page != st.session_state.current_page:
        st.session_state.current_page = selected_page
        st.rerun()

    page = st.session_state.current_page
    st.markdown("---")

    # 渲染侧边栏
    render_sidebar()
elif is_beginner_mode:
    # 新手模式下使用固定的页面
    page = "🏠 首页"
elif is_intermediate_mode:
    # 普通模式下使用固定的页面
    page = "🏠 首页"
else:
    # 专业模式下使用固定的页面
    page = "🏠 首页"

# 初始化session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'data_cleaned' not in st.session_state:
    st.session_state.data_cleaned = None
if 'profile_report' not in st.session_state:
    st.session_state.profile_report = None

# 页面路由
if page == "🎯 模式选择":
    render_mode_selection_page()

elif page == "🏠 首页":
    # 根据选择的模式渲染不同页面
    if st.session_state.get('selected_mode') == 'beginner':
        render_beginner_mode()
    elif st.session_state.get('selected_mode') == 'intermediate':
        render_intermediate_mode()
    else:
        render_home_page()

elif page == "📁 数据上传":
    st.markdown('<h2 class="sub-header">📁 数据上传</h2>', unsafe_allow_html=True)
    
    # 添加数据上传说明
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    ">
        <h3 style="color: white; margin-bottom: 15px;">📁 数据上传指南</h3>
        <p style="font-size: 16px; line-height: 1.6; margin-bottom: 15px;">
            <strong>💡 支持的数据格式：</strong><br>
            本平台支持多种常见的数据文件格式，确保您的数据能够顺利导入并进行分析。
        </p>
        <div style="display: flex; gap: 20px; margin-bottom: 15px;">
            <div style="flex: 1; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                <h4 style="color: #ff6b6b; margin-bottom: 10px;">📋 支持格式</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 14px;">
                    <li>CSV文件 (.csv)</li>
                    <li>Excel文件 (.xlsx, .xls)</li>
                    <li>JSON文件 (.json)</li>
                    <li>Parquet文件 (.parquet)</li>
                </ul>
            </div>
            <div style="flex: 1; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                <h4 style="color: #51cf66; margin-bottom: 10px;">✅ 最佳实践</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 14px;">
                    <li>确保数据格式整洁</li>
                    <li>检查编码格式（UTF-8）</li>
                    <li>避免特殊字符在列名中</li>
                    <li>建议文件大小 < 100MB</li>
                </ul>
            </div>
        </div>
        <p style="font-size: 14px; margin: 0; opacity: 0.9;">
            <strong>🎯 上传后功能：</strong> 数据质量评估、基础分析、可视化预览等
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "选择数据文件",
        type=['csv', 'xlsx', 'xls', 'json', 'parquet'],
        help="支持CSV、Excel、JSON、Parquet格式"
    )
    
    if uploaded_file is not None:
        try:
            # 使用缓存函数读取数据
            data = load_data(uploaded_file)
            st.session_state.data = data
            
            st.success(f"✅ 数眸数据上传成功！共 {len(data)} 行，{len(data.columns)} 列")
            
            # 显示数据基本信息
            data_info = get_data_info(data)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("行数", data_info['rows'])
            with col2:
                st.metric("列数", data_info['columns'])
            with col3:
                st.metric("内存使用", f"{data_info['memory_usage']:.2f} MB")
            with col4:
                st.metric("缺失值", data_info['missing_values'])
            
            # 数据预览
            st.subheader("📋 数据预览")
            st.dataframe(data.head(10), use_container_width=True)
            
            # 基础数据分析
            st.subheader("📊 基础数据分析")
            
            # 数据概览
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write("**描述性统计：**")
                numeric_cols = data.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    st.dataframe(data[numeric_cols].describe(), use_container_width=True)
                else:
                    st.info("数据中没有数值型列")
            
            with col2:
                st.write("**数据类型信息：**")
                dtype_info = get_data_type_summary(data)
                st.dataframe(dtype_info, use_container_width=True)
            
            # 缺失值分析
            st.subheader("🔍 缺失值分析")
            missing_data = data.isnull().sum()
            if missing_data.sum() > 0:
                missing_df = get_missing_value_summary(data)
                st.dataframe(missing_df, use_container_width=True)
                
                # 缺失值可视化
                fig = create_missing_values_chart(data)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.success("✅ 数据中没有缺失值")
            
            # 数据质量评估
            st.subheader("🔍 数据质量评估")
            quality_score = calculate_data_quality_score(data)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if quality_score >= 80:
                    st.success(f"数据质量评分: {quality_score:.1f}/100")
                elif quality_score >= 60:
                    st.warning(f"数据质量评分: {quality_score:.1f}/100")
                else:
                    st.error(f"数据质量评分: {quality_score:.1f}/100")
            
            with col2:
                st.metric("缺失值比例", f"{data.isnull().sum().sum() / (len(data) * len(data.columns)) * 100:.2f}%")
            
            with col3:
                st.metric("重复值比例", f"{data.duplicated().sum() / len(data) * 100:.2f}%")
            
            # AI智能分析建议
            st.subheader("🤖 AI智能分析建议")
            
            # 检查AI助手是否可用
            ai_assistant = get_smart_ai_assistant()
            
            if ai_assistant is None:
                st.warning("""
                ⚠️ **AI助手不可用**
                
                请确保已正确配置以下内容：
                1. 设置环境变量 `DASHSCOPE_API_KEY`
                2. 确保网络连接正常
                3. 检查API密钥是否有效
                
                **配置方法：**
                ```bash
                # Windows
                set DASHSCOPE_API_KEY=your_api_key_here
                
                # Linux/Mac
                export DASHSCOPE_API_KEY=your_api_key_here
                ```
                """)
            else:
                if st.button("🤖 获取AI分析建议", type="primary"):
                    with st.spinner("AI正在分析数据..."):
                        try:
                            analysis_result = ai_assistant.analyze_uploaded_data(data, data_info)
                            
                            st.success("✅ 数眸AI分析完成！")
                            st.markdown("### 🤖 数眸AI智能分析结果")
                            st.markdown(analysis_result)

                            # 添加AI分析报告导出功能
                            st.markdown("---")
                            st.subheader("📄 导出AI分析报告")
                            
                            # 创建报告导出器
                            exporter = ReportExporter()

                            # 导出格式选择
                            export_format = st.selectbox(
                                "选择导出格式：",
                                ["Markdown (.md)", "HTML (.html)", "JSON (.json)", "PDF (.pdf)"],
                                key="export_format"
                            )

                            if st.button("📥 生成并下载AI分析报告", type="secondary"):
                                with st.spinner("正在生成AI分析报告..."):
                                    try:
                                        if export_format == "Markdown (.md)":
                                            report_content = exporter.export_markdown_report(
                                                data_info, analysis_result, data
                                            )
                                            filename = f"AI分析报告_{exporter.timestamp}.md"
                                            st.markdown(get_download_link(report_content, filename, "text/markdown"), unsafe_allow_html=True)

                                        elif export_format == "HTML (.html)":
                                            report_content = exporter.export_html_report(
                                                data_info, analysis_result, data
                                            )
                                            filename = f"AI分析报告_{exporter.timestamp}.html"
                                            st.markdown(get_download_link(report_content, filename, "text/html"), unsafe_allow_html=True)

                                        elif export_format == "JSON (.json)":
                                            report_content = exporter.export_json_report(
                                                data_info, analysis_result, data
                                            )
                                            filename = f"AI分析报告_{exporter.timestamp}.json"
                                            st.markdown(get_download_link(report_content, filename, "application/json"), unsafe_allow_html=True)

                                        elif export_format == "PDF (.pdf)":
                                            report_content = exporter.export_pdf_report(
                                                data_info, analysis_result, data
                                            )
                                            filename = f"AI分析报告_{exporter.timestamp}.pdf"
                                            st.markdown(get_download_link_bytes(report_content, filename, "application/pdf"), unsafe_allow_html=True)

                                        st.success("✅ 数眸AI分析报告生成成功！点击上方链接下载。")

                                    except Exception as e:
                                        st.error(f"❌ AI分析报告生成失败：{str(e)}")

                            # 添加完整分析报告导出功能
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
                            <li>💼 商业价值分析</li>
                            </ul>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # 调用综合报告导出功能
                            render_comprehensive_report_export("专业模式")
                            
                            
                            
                        except Exception as e:
                            st.error(f"❌ 数眸AI分析失败：{str(e)}")
                
                # AI智能问答
                st.write("**💡 有数据分析问题？问问AI助手：**")
                user_question = st.text_area(
                    "请输入您的问题：",
                    placeholder="例如：这个数据集适合做什么分析？如何处理缺失值？",
                    height=80,
                    key="upload_question"
                )
                
                if st.button("🤖 获取AI回答", key="upload_ai_answer") and user_question.strip():
                    with st.spinner("AI正在思考..."):
                        try:
                            data_context = f"数据集包含{len(data)}行{len(data.columns)}列，数据类型包括{', '.join(data.dtypes.value_counts().index.astype(str))}"
                            answer = ai_assistant.answer_data_question(user_question, data_context, "数据上传")
                            
                            st.success("✅ 数眸AI回答完成！")
                            st.markdown("### 🤖 数眸AI回答")
                            st.markdown(answer)
                            
                        except Exception as e:
                            st.error(f"❌ 数眸AI回答失败：{str(e)}")
            
        except Exception as e:
            st.error(f"❌ 数据读取失败：{str(e)}")

elif page == "🧹 数据清洗":
    st.markdown('<h2 class="sub-header">🧹 数据清洗</h2>', unsafe_allow_html=True)
    
    # 添加整洁数据说明
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    ">
        <h3 style="color: white; margin-bottom: 15px;">📊 整洁数据（Tidy Data）指南</h3>
        <p style="font-size: 16px; line-height: 1.6; margin-bottom: 15px;">
            <strong>💡 什么是整洁数据？</strong><br>
            整洁数据是一种标准化的数据格式，遵循"每行一个观测值，每列一个变量"的原则，让数据分析变得更加高效和准确。
        </p>
        <div style="display: flex; gap: 20px; margin-bottom: 15px;">
            <div style="flex: 1; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                <h4 style="color: #ff6b6b; margin-bottom: 10px;">❌ 避免这样的数据格式</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 14px;">
                    <li>变量信息混合在列名中</li>
                    <li>相同类型的变量分散在不同列</li>
                    <li>一个单元格包含多个值</li>
                    <li>列名不清晰或不一致</li>
                </ul>
            </div>
            <div style="flex: 1; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                <h4 style="color: #51cf66; margin-bottom: 10px;">✅ 推荐这样的数据格式</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 14px;">
                    <li>每行代表一个观测值</li>
                    <li>每列代表一个变量</li>
                    <li>每个单元格只包含一个值</li>
                    <li>变量名清晰明确</li>
                </ul>
            </div>
        </div>
        <p style="font-size: 14px; margin: 0; opacity: 0.9;">
            <strong>🎯 为什么重要？</strong> 整洁数据让统计分析、可视化和机器学习变得更加简单高效！
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not hasattr(st.session_state, 'data') or st.session_state.data is None:
        st.warning("⚠️ 请先上传数据文件")
    else:
        data = st.session_state.data
        
        # 数据概览
        st.subheader("📋 数据概览")
        data_info = get_data_info(data)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("总行数", data_info['rows'])
        with col2:
            st.metric("总列数", data_info['columns'])
        with col3:
            st.metric("缺失值总数", data_info['missing_values'])
        with col4:
            st.metric("重复行数", data_info['duplicate_rows'])
        
        # 数据质量评分
        quality_score = calculate_data_quality_score(data)
        st.write(f"**数据质量评分：** {quality_score:.1f}/100")
        
        # 数据清洗功能
        st.subheader("🔧 数据清洗")
        
        # 缺失值处理
        st.write("**1. 缺失值处理**")
        missing_strategy = st.selectbox(
            "选择缺失值处理策略",
            ["删除行", "删除列", "均值填充", "中位数填充", "众数填充", "前向填充", "后向填充"]
        )
        
        if st.button("处理缺失值", type="primary"):
            with st.spinner("正在处理缺失值..."):
                data_cleaned = data.copy()
                data_cleaned = handle_missing_values(data_cleaned, missing_strategy)
                st.session_state.data_cleaned = data_cleaned
                st.success("✅ 数眸缺失值处理完成！")
        
        # 重复值处理
        st.write("**2. 重复值处理**")
        if st.button("删除重复行"):
            with st.spinner("正在删除重复行..."):
                if st.session_state.data_cleaned is not None:
                    data_cleaned = st.session_state.data_cleaned
                else:
                    data_cleaned = data.copy()
                data_cleaned = handle_duplicates(data_cleaned)
                st.session_state.data_cleaned = data_cleaned
                st.success("✅ 数眸重复值处理完成！")
        
        # 异常值处理
        st.write("**3. 异常值处理**")
        outlier_strategy = st.selectbox(
            "选择异常值处理策略",
            ["IQR方法", "Z-score方法", "百分位法"]
        )
        
        if st.button("处理异常值"):
            with st.spinner("正在处理异常值..."):
                if st.session_state.data_cleaned is not None:
                    data_cleaned = st.session_state.data_cleaned
                else:
                    data_cleaned = data.copy()
                data_cleaned = handle_outliers(data_cleaned, outlier_strategy)
                st.session_state.data_cleaned = data_cleaned
                st.success("✅ 数眸异常值处理完成！")
        
        # 显示清洗结果
        if st.session_state.data_cleaned is not None:
            st.subheader("📊 清洗结果对比")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**原始数据：**")
                st.write(f"行数：{len(data)}")
                st.write(f"列数：{len(data.columns)}")
                st.write(f"缺失值：{data.isnull().sum().sum()}")
                st.write(f"重复行：{data.duplicated().sum()}")
            
            with col2:
                st.write("**清洗后数据：**")
                st.write(f"行数：{len(st.session_state.data_cleaned)}")
                st.write(f"列数：{len(st.session_state.data_cleaned.columns)}")
                st.write(f"缺失值：{st.session_state.data_cleaned.isnull().sum().sum()}")
                st.write(f"重复行：{st.session_state.data_cleaned.duplicated().sum()}")
        
        # AI智能清洗建议
        st.subheader("🤖 AI智能清洗建议")
        
        # 检查AI助手是否可用
        ai_assistant = get_ai_assistant()
        
        if ai_assistant is None:
            st.warning("⚠️ AI助手不可用，请检查API配置")
        else:
            # 选择清洗问题类型
            cleaning_issue = st.selectbox(
                "选择需要AI建议的清洗问题",
                ["missing_values", "duplicates", "outliers", "data_types"],
                format_func=lambda x: {
                    "missing_values": "缺失值处理",
                    "duplicates": "重复值处理", 
                    "outliers": "异常值处理",
                    "data_types": "数据类型转换"
                }[x]
            )
            
            if st.button("🤖 获取AI清洗建议", type="primary"):
                with st.spinner("AI正在分析清洗策略..."):
                    try:
                        cleaning_advice = ai_assistant.suggest_cleaning_strategy(data, cleaning_issue)
                        
                        st.success("✅ 数眸AI清洗建议完成！")
                        st.markdown("### 🤖 数眸AI清洗策略建议")
                        st.markdown(cleaning_advice)
                        
                    except Exception as e:
                        st.error(f"❌ 数眸AI建议失败：{str(e)}")
            
            # AI智能问答
            st.write("**💡 有数据清洗问题？问问数眸AI助手：**")
            user_question = st.text_area(
                "请输入您的问题：",
                placeholder="例如：如何处理这个数据集的缺失值？异常值检测用什么方法？",
                height=80,
                key="cleaning_question"
            )
            
            if st.button("🤖 获取AI回答", key="cleaning_ai_answer") and user_question.strip():
                with st.spinner("AI正在思考..."):
                    try:
                        data_context = f"数据集包含{len(data)}行{len(data.columns)}列，缺失值{data.isnull().sum().sum()}个，重复行{data.duplicated().sum()}个"
                        answer = ai_assistant.answer_data_question(user_question, data_context, "数据清洗")
                        
                        st.success("✅ 数眸AI回答完成！")
                        st.markdown("### 🤖 数眸AI回答")
                        st.markdown(answer)
                        
                    except Exception as e:
                        st.error(f"❌ 数眸AI回答失败：{str(e)}")

elif page == "🔍 自动数据分析":
    st.markdown('<h2 class="sub-header">🔍 自动数据分析</h2>', unsafe_allow_html=True)
    
    if not hasattr(st.session_state, 'data') or st.session_state.data is None:
        st.warning("⚠️ 请先上传数据文件")
    else:
        data = st.session_state.data
        
        st.subheader("📊 数据概览")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("行数", len(data))
        with col2:
            st.metric("列数", len(data.columns))
        with col3:
            st.metric("缺失值", data.isnull().sum().sum())
        with col4:
            st.metric("重复行", data.duplicated().sum())
        
        # 基础统计分析
        st.subheader("📈 描述性统计")
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            st.dataframe(data[numeric_cols].describe(), use_container_width=True)
        else:
            st.info("数据中没有数值型列")
        
        # 相关性分析
        if len(numeric_cols) > 1:
            st.subheader("🔗 相关性分析")
            correlation_matrix = calculate_correlation_matrix(data)
            fig = create_correlation_heatmap(correlation_matrix)
            st.plotly_chart(fig, use_container_width=True)
        
        # 数据分布分析
        st.subheader("📊 数据分布分析")
        if len(numeric_cols) > 0:
            selected_col = st.selectbox("选择要分析的列", numeric_cols)
            if selected_col:
                fig = create_histogram(data, selected_col, title=f"{selected_col} 分布直方图")
                st.plotly_chart(fig, use_container_width=True)
        
        # AI智能分析解释
        st.subheader("🤖 AI智能分析解释")
        
        # 检查AI助手是否可用
        ai_assistant = get_ai_assistant()
        
        if ai_assistant is None:
            st.warning("⚠️ AI助手不可用，请检查API配置")
        else:
            # 收集分析结果
            analysis_results = {
                "数据规模": f"{len(data)}行 × {len(data.columns)}列",
                "数值型列数": len(numeric_cols),
                "缺失值情况": data.isnull().sum().sum(),
                "重复行数": data.duplicated().sum(),
                "数据质量评分": calculate_data_quality_score(data)
            }
            
            if len(numeric_cols) > 0:
                analysis_results["描述性统计"] = data[numeric_cols].describe().to_dict()
            
            if st.button("🤖 获取AI分析解释", type="primary"):
                with st.spinner("AI正在解释分析结果..."):
                    try:
                        interpretation = ai_assistant.interpret_auto_analysis(data, analysis_results)
                        
                        st.success("✅ AI分析解释完成！")
                        st.markdown("### 🤖 AI分析结果解释")
                        st.markdown(interpretation)
                        
                    except Exception as e:
                        st.error(f"❌ AI解释失败：{str(e)}")
            
            # AI智能问答
            st.write("**💡 有数据分析问题？问问AI助手：**")
            user_question = st.text_area(
                "请输入您的问题：",
                placeholder="例如：这个分析结果说明了什么？如何进一步分析？",
                height=80,
                key="analysis_question"
            )
            
            if st.button("🤖 获取AI回答", key="analysis_ai_answer") and user_question.strip():
                with st.spinner("AI正在思考..."):
                    try:
                        data_context = f"数据集包含{len(data)}行{len(data.columns)}列，数值型列{len(numeric_cols)}个，数据质量评分{calculate_data_quality_score(data):.1f}分"
                        answer = ai_assistant.answer_data_question(user_question, data_context, "自动数据分析")
                        
                        st.success("✅ AI回答完成！")
                        st.markdown("### 🤖 AI回答")
                        st.markdown(answer)
                        
                    except Exception as e:
                        st.error(f"❌ AI回答失败：{str(e)}")

elif page == "📈 高级可视化":
    st.markdown('<h2 class="sub-header">📈 高级可视化</h2>', unsafe_allow_html=True)
    
    if not hasattr(st.session_state, 'data') or st.session_state.data is None:
        st.warning("⚠️ 请先上传数据文件")
    else:
        data = st.session_state.data
        
        st.subheader("📊 图表类型选择")
        chart_type = st.selectbox(
            "选择图表类型",
            ["柱状图", "折线图", "散点图", "饼图", "直方图", "箱线图", "小提琴图", "3D散点图", "热力图"]
        )
        
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if chart_type == "柱状图":
            x_col = st.selectbox("选择X轴列", data.columns.tolist())
            y_col = st.selectbox("选择Y轴列", numeric_cols)
            if x_col and y_col:
                fig = create_bar_chart(data, x_col, y_col, title=f'{y_col} vs {x_col}')
                st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "散点图":
            x_col = st.selectbox("选择X轴列", numeric_cols)
            y_col = st.selectbox("选择Y轴列", numeric_cols)
            color_col = st.selectbox("选择颜色列（可选）", [None] + categorical_cols)
            if x_col and y_col:
                fig = create_scatter_chart(data, x_col, y_col, color_col, title=f'{y_col} vs {x_col}')
                st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "直方图":
            col_name = st.selectbox("选择要分析的列", numeric_cols)
            if col_name:
                fig = create_histogram(data, col_name, title=f'{col_name} 分布直方图')
                st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "箱线图":
            x_col = st.selectbox("选择分组列", categorical_cols)
            y_col = st.selectbox("选择数值列", numeric_cols)
            if x_col and y_col:
                fig = create_box_chart(data, x_col, y_col, title=f'{y_col} 按 {x_col} 分组的箱线图')
                st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "热力图":
            if len(numeric_cols) > 1:
                correlation_matrix = calculate_correlation_matrix(data)
                fig = create_correlation_heatmap(correlation_matrix)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("需要至少2个数值型列来创建热力图")
        
        # AI智能可视化建议
        st.subheader("🤖 AI智能可视化建议")
        
        # 检查AI助手是否可用
        ai_assistant = get_ai_assistant()
        
        if ai_assistant is None:
            st.warning("⚠️ AI助手不可用，请检查API配置")
        else:
            # 选择分析目标
            analysis_goal = st.selectbox(
                "选择分析目标",
                ["trend_analysis", "distribution_comparison", "correlation_analysis", "pattern_detection"],
                format_func=lambda x: {
                    "trend_analysis": "趋势分析",
                    "distribution_comparison": "分布比较",
                    "correlation_analysis": "相关性分析",
                    "pattern_detection": "模式检测"
                }[x]
            )
            
            if st.button("🤖 获取AI可视化建议", type="primary"):
                with st.spinner("AI正在分析可视化方案..."):
                    try:
                        viz_advice = ai_assistant.suggest_visualization(data, analysis_goal)
                        
                        st.success("✅ AI可视化建议完成！")
                        st.markdown("### 🤖 AI可视化建议")
                        st.markdown(viz_advice)
                        
                    except Exception as e:
                        st.error(f"❌ AI建议失败：{str(e)}")
            
            # 图表洞察解释
            if chart_type in ["柱状图", "散点图", "箱线图", "直方图"]:
                st.write("**💡 需要AI解释图表洞察？**")
                if st.button("🤖 获取AI图表解释", key="viz_ai_explain"):
                    with st.spinner("AI正在分析图表..."):
                        try:
                            # 获取图表配置和统计信息
                            chart_config = {"chart_type": chart_type}
                            chart_stats = {}
                            
                            if chart_type == "散点图" and len(numeric_cols) >= 2:
                                chart_stats["相关性"] = data[numeric_cols[0]].corr(data[numeric_cols[1]])
                            
                            explanation = ai_assistant.explain_chart_insights(
                                chart_type, data, chart_config, chart_stats
                            )
                            
                            st.success("✅ AI图表解释完成！")
                            st.markdown("### 🤖 AI图表洞察")
                            st.markdown(explanation)
                            
                        except Exception as e:
                            st.error(f"❌ AI解释失败：{str(e)}")
            
            # AI智能问答
            st.write("**💡 有可视化问题？问问AI助手：**")
            user_question = st.text_area(
                "请输入您的问题：",
                placeholder="例如：如何选择合适的图表类型？如何优化图表效果？",
                height=80,
                key="viz_question"
            )
            
            if st.button("🤖 获取AI回答", key="viz_ai_answer") and user_question.strip():
                with st.spinner("AI正在思考..."):
                    try:
                        data_context = f"数据集包含{len(data)}行{len(data.columns)}列，数值型列{len(numeric_cols)}个，分类型列{len(categorical_cols)}个"
                        answer = ai_assistant.answer_data_question(user_question, data_context, "高级可视化")
                        
                        st.success("✅ AI回答完成！")
                        st.markdown("### 🤖 AI回答")
                        st.markdown(answer)
                        
                    except Exception as e:
                        st.error(f"❌ AI回答失败：{str(e)}")

elif page == "📊 统计分析":
    st.markdown('<h2 class="sub-header">📊 统计分析</h2>', unsafe_allow_html=True)
    
    # 添加统计分析说明
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    ">
        <h3 style="color: white; margin-bottom: 15px;">📊 统计分析指南</h3>
        <p style="font-size: 16px; line-height: 1.6; margin-bottom: 15px;">
            <strong>💡 专业统计方法：</strong><br>
            提供全面的统计分析工具，包括描述性统计和推断性统计，帮助您从数据中发现有意义的模式和关系。
        </p>
        <div style="display: flex; gap: 20px; margin-bottom: 15px;">
            <div style="flex: 1; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                <h4 style="color: #ff6b6b; margin-bottom: 10px;">📈 描述性统计</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 14px;">
                    <li>集中趋势：均值、中位数、众数</li>
                    <li>离散程度：方差、标准差、IQR</li>
                    <li>分布特征：偏度、峰度</li>
                    <li>数据概览：分位数、极值</li>
                </ul>
            </div>
            <div style="flex: 1; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                <h4 style="color: #51cf66; margin-bottom: 10px;">🔬 假设检验</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 14px;">
                    <li>正态性检验 - Shapiro-Wilk</li>
                    <li>t检验 - 均值比较</li>
                    <li>方差分析 - ANOVA</li>
                    <li>相关性检验 - Pearson/Spearman</li>
                    <li>卡方检验 - 独立性检验</li>
                </ul>
            </div>
        </div>
        <p style="font-size: 14px; margin: 0; opacity: 0.9;">
            <strong>🎯 适用场景：</strong> 数据探索、假设验证、科学研究、决策支持
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not hasattr(st.session_state, 'data') or st.session_state.data is None:
        st.warning("⚠️ 请先上传数据文件")
    else:
        data = st.session_state.data
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        
        if not numeric_cols:
            st.warning("⚠️ 数据中没有数值型列，无法进行统计分析")
        else:
            # 描述性统计
            st.subheader("📈 描述性统计")
            selected_cols = st.multiselect("选择要分析的列", numeric_cols, default=numeric_cols[:3])
            
            if selected_cols:
                desc_stats = data[selected_cols].describe()
                st.dataframe(desc_stats, use_container_width=True)
                
                # 添加更多统计指标
                additional_stats = pd.DataFrame({
                    '偏度': data[selected_cols].skew(),
                    '峰度': data[selected_cols].kurtosis(),
                    '变异系数': data[selected_cols].std() / data[selected_cols].mean(),
                    'Q1': data[selected_cols].quantile(0.25),
                    'Q3': data[selected_cols].quantile(0.75),
                    'IQR': data[selected_cols].quantile(0.75) - data[selected_cols].quantile(0.25)
                })
                st.write("**额外统计指标：**")
                st.dataframe(additional_stats, use_container_width=True)
            
            # 假设检验
            st.subheader("🔬 假设检验")
            test_type = st.selectbox("选择检验类型", ["正态性检验", "t检验", "方差分析", "相关性检验", "卡方检验"])
            
            if test_type == "正态性检验":
                col_name = st.selectbox("选择要检验的列", numeric_cols)
                if st.button("进行正态性检验"):
                    from scipy import stats
                    statistic, p_value = stats.shapiro(data[col_name].dropna())
                    st.write(f"**Shapiro-Wilk 正态性检验结果：**")
                    st.write(f"统计量：{statistic:.4f}")
                    st.write(f"p值：{p_value:.4f}")
                    if p_value > 0.05:
                        st.success("✅ 数据符合正态分布 (p > 0.05)")
                    else:
                        st.warning("⚠️ 数据不符合正态分布 (p ≤ 0.05)")
            
            elif test_type == "t检验":
                col1, col2 = st.columns(2)
                with col1:
                    col_name = st.selectbox("选择要检验的列", numeric_cols)
                with col2:
                    group_col = st.selectbox("选择分组列", data.select_dtypes(include=['object', 'category']).columns.tolist())
                
                if st.button("进行t检验"):
                    from scipy import stats
                    groups = data[group_col].unique()
                    if len(groups) == 2:
                        group1 = data[data[group_col] == groups[0]][col_name].dropna()
                        group2 = data[data[group_col] == groups[1]][col_name].dropna()
                        statistic, p_value = stats.ttest_ind(group1, group2)
                        st.write(f"**独立样本t检验结果：**")
                        st.write(f"统计量：{statistic:.4f}")
                        st.write(f"p值：{p_value:.4f}")
                        if p_value < 0.05:
                            st.success("✅ 两组间存在显著差异 (p < 0.05)")
                        else:
                            st.warning("⚠️ 两组间无显著差异 (p ≥ 0.05)")
                    else:
                        st.error("分组列必须恰好有2个不同的值")
        
        # AI智能统计建议
        st.subheader("🤖 AI智能统计建议")
        
        # 检查AI助手是否可用
        ai_assistant = get_ai_assistant()
        
        if ai_assistant is None:
            st.warning("⚠️ AI助手不可用，请检查API配置")
        else:
            # 统计检验建议
            st.write("**💡 需要AI推荐统计检验方法？**")
            analysis_question = st.text_area(
                "描述您的分析问题：",
                placeholder="例如：我想比较两组数据的均值是否有显著差异",
                height=80,
                key="stats_question"
            )
            
            if st.button("🤖 获取AI统计建议", key="stats_ai_advice") and analysis_question.strip():
                with st.spinner("AI正在分析统计方法..."):
                    try:
                        stats_advice = ai_assistant.suggest_statistical_tests(data, analysis_question)
                        
                        st.success("✅ AI统计建议完成！")
                        st.markdown("### 🤖 AI统计检验建议")
                        st.markdown(stats_advice)
                        
                    except Exception as e:
                        st.error(f"❌ AI建议失败：{str(e)}")
            
            # 统计结果解释
            if test_type in ["正态性检验", "t检验"]:
                st.write("**💡 需要AI解释统计结果？**")
                if st.button("🤖 获取AI结果解释", key="stats_ai_explain"):
                    with st.spinner("AI正在解释统计结果..."):
                        try:
                            # 这里可以收集实际的检验结果
                            test_results = {
                                "检验类型": test_type,
                                "数据规模": f"{len(data)}行 × {len(data.columns)}列",
                                "数值型列数": len(numeric_cols)
                            }
                            
                            data_context = f"数据集包含{len(data)}行{len(data.columns)}列，数值型列{len(numeric_cols)}个"
                            explanation = ai_assistant.interpret_statistical_results(
                                test_type, test_results, data_context
                            )
                            
                            st.success("✅ AI统计解释完成！")
                            st.markdown("### 🤖 AI统计结果解释")
                            st.markdown(explanation)
                            
                        except Exception as e:
                            st.error(f"❌ AI解释失败：{str(e)}")
            
            # AI智能问答
            st.write("**💡 有统计分析问题？问问AI助手：**")
            user_question = st.text_area(
                "请输入您的问题：",
                placeholder="例如：如何选择合适的统计检验？如何解释p值？",
                height=80,
                key="stats_ai_question"
            )
            
            if st.button("🤖 获取AI回答", key="stats_ai_answer") and user_question.strip():
                with st.spinner("AI正在思考..."):
                    try:
                        data_context = f"数据集包含{len(data)}行{len(data.columns)}列，数值型列{len(numeric_cols)}个"
                        answer = ai_assistant.answer_data_question(user_question, data_context, "统计分析")
                        
                        st.success("✅ AI回答完成！")
                        st.markdown("### 🤖 AI回答")
                        st.markdown(answer)
                        
                    except Exception as e:
                        st.error(f"❌ AI回答失败：{str(e)}")

elif page == "🤖 机器学习":
    st.markdown('<h2 class="sub-header">🤖 机器学习</h2>', unsafe_allow_html=True)
    
    # 添加机器学习说明
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
    
    if not hasattr(st.session_state, 'data') or st.session_state.data is None:
        st.warning("⚠️ 请先上传数据文件")
    else:
        data = st.session_state.data
        st.success(f"✅ 数据加载成功: {len(data)} 行 × {len(data.columns)} 列")
        
        # 机器学习任务选择
        ml_task = st.selectbox(
            "选择机器学习任务",
            ["分类", "回归", "聚类", "特征工程", "模型评估"]
        )
        
        st.info(f"🎯 当前选择的任务: {ml_task}")
        
        if ml_task == "分类":
            st.subheader("🎯 分类任务")
            
            # 选择特征和目标变量
            numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
            
            if len(numeric_cols) == 0:
                st.warning("⚠️ 数据中没有数值型列，无法进行分类任务")
            elif len(categorical_cols) == 0:
                st.warning("⚠️ 数据中没有分类列，无法进行分类任务")
            else:
                target_col = st.selectbox("选择目标变量（分类列）", categorical_cols)
                feature_cols = st.multiselect("选择特征变量（数值列）", numeric_cols, default=numeric_cols[:3])
                
                if target_col and feature_cols:
                    if st.button("训练分类模型"):
                        with st.spinner("正在训练分类模型..."):
                            try:
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
        
        elif ml_task == "回归":
            st.subheader("📈 回归任务")
            
            numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_cols) < 2:
                st.warning("⚠️ 需要至少2个数值型列进行回归任务")
            else:
                target_col = st.selectbox("选择目标变量", numeric_cols)
                feature_cols = st.multiselect("选择特征变量", [col for col in numeric_cols if col != target_col], default=[col for col in numeric_cols[:3] if col != target_col])
                
                if target_col and feature_cols:
                    if st.button("训练回归模型"):
                        with st.spinner("正在训练回归模型..."):
                            try:
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
        
        elif ml_task == "聚类":
            st.subheader("🔍 聚类分析")
            
            numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_cols) < 2:
                st.warning("⚠️ 需要至少2个数值型列进行聚类分析")
            else:
                feature_cols = st.multiselect("选择特征变量", numeric_cols, default=numeric_cols[:3])
                n_clusters = st.slider("选择聚类数量", 2, 10, 3)
                
                if feature_cols:
                    if st.button("执行聚类分析"):
                        with st.spinner("正在执行聚类分析..."):
                            try:
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
        
        # AI智能机器学习建议
        st.subheader("🤖 AI智能机器学习建议")
        
        # 检查AI助手是否可用
        ai_assistant = get_ai_assistant()
        
        if ai_assistant is None:
            st.warning("⚠️ AI助手不可用，请检查API配置")
        else:
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
            
            # 模型结果解释
            if ml_task in ["分类", "回归"] and 'training_info' in locals():
                st.write("**💡 需要AI解释模型结果？**")
                if st.button("🤖 获取AI模型解释", key="ml_ai_explain"):
                    with st.spinner("AI正在解释模型结果..."):
                        try:
                            model_results = {
                                "任务类型": ml_task,
                                "目标变量": target_col,
                                "特征数量": len(feature_cols),
                                "训练结果": training_info
                            }
                            
                            explanation = ai_assistant.interpret_ml_results(
                                ml_task, model_results, training_info.get('feature_importance')
                            )
                            
                            st.success("✅ AI模型解释完成！")
                            st.markdown("### 🤖 AI模型结果解释")
                            st.markdown(explanation)
                            
                        except Exception as e:
                            st.error(f"❌ AI解释失败：{str(e)}")
            
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



elif page == "📋 报告生成":
    st.markdown('<h2 class="sub-header">📋 报告生成</h2>', unsafe_allow_html=True)
    
    if not hasattr(st.session_state, 'data') or st.session_state.data is None:
        st.warning("⚠️ 请先上传数据文件")
    else:
        data = st.session_state.data
        
        st.subheader("📄 生成分析报告")
        
        if st.button("🚀 生成完整报告"):
            with st.spinner("正在生成报告..."):
                try:
                    # 创建完整的HTML报告
                    html_content = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>智能数据分析报告</title>
                        <style>
                            body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                            h1 {{ color: #1f77b4; text-align: center; border-bottom: 3px solid #1f77b4; padding-bottom: 10px; }}
                            h2 {{ color: #2c3e50; border-bottom: 2px solid #1f77b4; padding-bottom: 5px; margin-top: 30px; }}
                            h3 {{ color: #34495e; margin-top: 25px; }}
                            .metric {{ background-color: #f8f9fa; padding: 15px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #1f77b4; }}
                            .section {{ margin: 30px 0; }}
                            .highlight {{ background-color: #fff3cd; padding: 10px; border-radius: 5px; border-left: 4px solid #ffc107; }}
                            table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
                            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                            th {{ background-color: #f2f2f2; font-weight: bold; }}
                            .footer {{ text-align: center; color: #666; margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; }}
                        </style>
                    </head>
                    <body>
                        <h1>📊 智能数据分析报告</h1>
                        
                        <div class="section">
                            <h2>📋 数据概览</h2>
                            <div class="metric">
                                <strong>数据集大小：</strong> {len(data)} 行 × {len(data.columns)} 列<br>
                                <strong>内存使用：</strong> {data.memory_usage(deep=True).sum() / 1024**2:.2f} MB<br>
                                <strong>缺失值总数：</strong> {data.isnull().sum().sum()}<br>
                                <strong>数据类型分布：</strong> {', '.join([f'{str(dtype)}({count})' for dtype, count in data.dtypes.value_counts().items()])}
                            </div>
                        </div>
                        
                        <div class="section">
                            <h2>🔍 数据质量评估</h2>
                            <div class="metric">
                                <strong>数据质量评分：</strong> {calculate_data_quality_score(data):.1f}/100<br>
                                <strong>缺失值比例：</strong> {data.isnull().sum().sum() / (len(data) * len(data.columns)) * 100:.2f}%<br>
                                <strong>重复行比例：</strong> {data.duplicated().sum() / len(data) * 100:.2f}%
                            </div>
                        </div>
                        
                        <div class="section">
                            <h2>📈 描述性统计</h2>
                            <div class="highlight">
                                <strong>数值型列统计：</strong>
                            </div>
                            {data.select_dtypes(include=[np.number]).describe().to_html() if len(data.select_dtypes(include=[np.number]).columns) > 0 else '<p>数据中没有数值型列</p>'}
                        </div>
                        
                        <div class="section">
                            <h2>📅 报告信息</h2>
                            <div class="metric">
                                <strong>生成时间：</strong> {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")}<br>
                                <strong>分析平台：</strong> 智能数据分析平台 v3.0.0<br>
                                <strong>报告类型：</strong> 自动生成分析报告
                            </div>
                        </div>
                        
                        <div class="footer">
                            <p>🚀 智能数据分析平台 | 版本 3.0.0 (重构版) | 生成时间: {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                        </div>
                    </body>
                    </html>
                    """
                    
                    # 显示报告
                    st.components.v1.html(html_content, height=600, scrolling=True)
                    
                    # 下载报告
                    st.download_button(
                        label="📥 下载完整报告",
                        data=html_content,
                        file_name="data_analysis_report.html",
                        mime="text/html"
                    )
                    
                except Exception as e:
                    st.error(f"❌ 报告生成失败：{str(e)}")
        
        # AI智能报告建议
        st.subheader("🤖 AI智能报告建议")
        
        # 检查AI助手是否可用
        ai_assistant = get_ai_assistant()
        
        if ai_assistant is None:
            st.warning("⚠️ AI助手不可用，请检查API配置")
        else:
            # 收集分析总结
            analysis_summary = {
                "数据规模": f"{len(data)}行 × {len(data.columns)}列",
                "数据质量评分": calculate_data_quality_score(data),
                "数值型列数": len(data.select_dtypes(include=[np.number]).columns),
                "分类型列数": len(data.select_dtypes(include=['object', 'category']).columns),
                "缺失值情况": data.isnull().sum().sum(),
                "重复行数": data.duplicated().sum()
            }
            
            if st.button("🤖 获取AI报告建议", type="primary"):
                with st.spinner("AI正在分析报告结构..."):
                    try:
                        report_advice = ai_assistant.suggest_report_structure(data, analysis_summary)
                        
                        st.success("✅ AI报告建议完成！")
                        st.markdown("### 🤖 AI报告结构建议")
                        st.markdown(report_advice)
                        
                    except Exception as e:
                        st.error(f"❌ AI建议失败：{str(e)}")
            
            # AI智能问答
            st.write("**💡 有报告撰写问题？问问AI助手：**")
            user_question = st.text_area(
                "请输入您的问题：",
                placeholder="例如：如何组织报告结构？如何突出关键发现？",
                height=80,
                key="report_ai_question"
            )
            
            if st.button("🤖 获取AI回答", key="report_ai_answer") and user_question.strip():
                with st.spinner("AI正在思考..."):
                    try:
                        data_context = f"数据集包含{len(data)}行{len(data.columns)}列，数据质量评分{calculate_data_quality_score(data):.1f}分"
                        answer = ai_assistant.answer_data_question(user_question, data_context, "报告生成")
                        
                        st.success("✅ AI回答完成！")
                        st.markdown("### 🤖 AI回答")
                        st.markdown(answer)
                        
                    except Exception as e:
                        st.error(f"❌ AI回答失败：{str(e)}")

elif page == "👁️ 数据洞察":
    st.markdown('<h2 class="sub-header">👁️ 数据洞察</h2>', unsafe_allow_html=True)
    
    # 数眸品牌介绍
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px rgba(30, 64, 175, 0.3);
    ">
        <h3 style="color: white; margin-bottom: 20px; text-align: center;">👁️ 数眸 - 让数据洞察如眸般清澈明亮</h3>
        <p style="font-size: 18px; line-height: 1.8; margin-bottom: 20px; text-align: center;">
            <strong>💡 核心洞察功能：</strong><br>
            通过AI智能分析，发现数据中的隐藏模式、异常趋势和商业价值，让复杂的数据变得清晰可见。
        </p>
        <div style="display: flex; gap: 25px; margin-bottom: 20px;">
            <div style="flex: 1; background: rgba(255,255,255,0.15); padding: 20px; border-radius: 12px; backdrop-filter: blur(10px);">
                <h4 style="color: #FDE68A; margin-bottom: 15px;">🔍 模式发现</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 15px;">
                    <li>隐藏关联关系</li>
                    <li>周期性模式</li>
                    <li>趋势变化点</li>
                    <li>异常值识别</li>
                </ul>
            </div>
            <div style="flex: 1; background: rgba(255,255,255,0.15); padding: 20px; border-radius: 12px; backdrop-filter: blur(10px);">
                <h4 style="color: #A7F3D0; margin-bottom: 15px;">💡 智能洞察</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 15px;">
                    <li>业务价值分析</li>
                    <li>风险预警提示</li>
                    <li>机会识别</li>
                    <li>决策建议</li>
                </ul>
            </div>
            <div style="flex: 1; background: rgba(255,255,255,0.15); padding: 20px; border-radius: 12px; backdrop-filter: blur(10px);">
                <h4 style="color: #FECACA; margin-bottom: 15px;">📊 可视化洞察</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 15px;">
                    <li>交互式图表</li>
                    <li>动态仪表板</li>
                    <li>实时监控</li>
                    <li>故事化展示</li>
                </ul>
            </div>
        </div>
        <p style="font-size: 16px; margin: 0; text-align: center; opacity: 0.9;">
            <strong>🎯 数眸使命：</strong> 让每个人都能像专家一样洞察数据，发现价值
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not hasattr(st.session_state, 'data') or st.session_state.data is None:
        st.warning("⚠️ 请先上传数据文件")
    else:
        data = st.session_state.data
        
        # 洞察类型选择
        insight_type = st.selectbox(
            "选择洞察类型",
            ["🔍 数据模式发现", "📈 趋势分析", "🎯 异常检测", "💡 商业洞察", "📊 综合洞察报告"],
            help="选择您想要进行的洞察分析类型"
        )
        
        if insight_type == "🔍 数据模式发现":
            render_pattern_discovery(data)
        elif insight_type == "📈 趋势分析":
            render_trend_analysis(data)
        elif insight_type == "🎯 异常检测":
            render_anomaly_detection(data)
        elif insight_type == "💡 商业洞察":
            render_business_insights(data)
        elif insight_type == "📊 综合洞察报告":
            render_comprehensive_insights(data)

# 渲染页脚
render_footer()

# 数据洞察功能函数
def render_pattern_discovery(data):
    """数据模式发现"""
    st.subheader("🔍 数据模式发现")
    st.info("数眸正在为您分析数据模式...")
    # 这里可以添加具体的模式发现逻辑

def render_trend_analysis(data):
    """趋势分析"""
    st.subheader("📈 趋势分析")
    st.info("数眸正在为您分析数据趋势...")
    # 这里可以添加具体的趋势分析逻辑

def render_anomaly_detection(data):
    """异常检测"""
    st.subheader("🎯 异常检测")
    st.info("数眸正在为您检测异常值...")
    # 这里可以添加具体的异常检测逻辑

def render_business_insights(data):
    """商业洞察"""
    st.subheader("💡 商业洞察")
    st.info("数眸正在为您生成商业洞察...")
    # 这里可以添加具体的商业洞察逻辑

def render_comprehensive_insights(data):
    """综合洞察报告"""
    st.subheader("📊 综合洞察报告")
    st.info("数眸正在为您生成综合洞察报告...")
    # 这里可以添加具体的报告生成逻辑

# 数据洞察功能函数
def render_pattern_discovery(data):
    """数据模式发现"""
    st.subheader("🔍 数据模式发现")
    
    # 相关性模式发现
    st.write("**1. 相关性模式分析**")
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) >= 2:
        # 计算相关性矩阵
        corr_matrix = data[numeric_cols].corr()
        
        # 找出强相关性
        strong_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:
                    strong_corr.append({
                        'var1': corr_matrix.columns[i],
                        'var2': corr_matrix.columns[j],
                        'correlation': corr_value
                    })
        
        if strong_corr:
            st.success(f"✅ 数眸发现 {len(strong_corr)} 个强相关性模式")
            for corr in strong_corr:
                st.write(f"• {corr['var1']} 与 {corr['var2']} 的相关系数为 {corr['correlation']:.3f}")
        else:
            st.info("ℹ️ 数眸未发现强相关性模式")
        
        # 相关性热力图
        fig = px.imshow(corr_matrix, 
                       title="相关性模式热力图",
                       color_continuous_scale='RdBu_r',
                       aspect='auto')
        st.plotly_chart(fig, use_container_width=True)
    
    # 聚类模式发现
    st.write("**2. 聚类模式分析**")
    if len(numeric_cols) >= 2:
        selected_cols = st.multiselect("选择用于聚类的特征", numeric_cols, default=numeric_cols[:3])
        
        if selected_cols and len(selected_cols) >= 2:
            if st.button("🔍 数眸发现聚类模式"):
                with st.spinner("数眸正在分析聚类模式..."):
                    # 数据预处理
                    X = data[selected_cols].dropna()
                    
                    if len(X) > 0:
                        # 标准化
                        from sklearn.preprocessing import StandardScaler
                        scaler = StandardScaler()
                        X_scaled = scaler.fit_transform(X)
                        
                        # 使用肘部法则确定最佳聚类数
                        from sklearn.cluster import KMeans
                        inertias = []
                        K_range = range(2, min(11, len(X)//10 + 1))
                        
                        for k in K_range:
                            kmeans = KMeans(n_clusters=k, random_state=42)
                            kmeans.fit(X_scaled)
                            inertias.append(kmeans.inertia_)
                        
                        # 绘制肘部图
                        fig_elbow = px.line(x=list(K_range), y=inertias, 
                                          title="肘部法则 - 确定最佳聚类数",
                                          labels={'x': '聚类数', 'y': '惯性'})
                        st.plotly_chart(fig_elbow, use_container_width=True)
                        
                        # 执行聚类
                        optimal_k = 3  # 可以根据肘部图自动确定
                        kmeans = KMeans(n_clusters=optimal_k, random_state=42)
                        clusters = kmeans.fit_predict(X_scaled)
                        
                        # 可视化聚类结果
                        if len(selected_cols) >= 2:
                            fig_cluster = px.scatter(
                                x=X.iloc[:, 0], y=X.iloc[:, 1],
                                color=clusters,
                                title=f"聚类模式发现 ({selected_cols[0]} vs {selected_cols[1]})",
                                labels={'x': selected_cols[0], 'y': selected_cols[1], 'color': '聚类'}
                            )
                            st.plotly_chart(fig_cluster, use_container_width=True)
                        
                        st.success(f"✅ 数眸发现 {optimal_k} 个聚类模式")

def render_trend_analysis(data):
    """趋势分析"""
    st.subheader("📈 趋势分析")
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) == 0:
        st.warning("⚠️ 数据中没有数值型列，无法进行趋势分析")
        return
    
    # 选择分析列
    selected_col = st.selectbox("选择要分析的列", numeric_cols)
    
    if selected_col:
        # 基础趋势分析
        values = data[selected_col].dropna()
        
        if len(values) > 0:
            # 计算趋势
            x = np.arange(len(values))
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, values)
            
            # 趋势判断
            if slope > 0:
                trend_direction = "上升趋势"
                trend_icon = "📈"
            elif slope < 0:
                trend_direction = "下降趋势"
                trend_icon = "📉"
            else:
                trend_direction = "无明显趋势"
                trend_icon = "➡️"
            
            # 显示趋势信息
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("趋势方向", f"{trend_icon} {trend_direction}")
            with col2:
                st.metric("趋势强度", f"{abs(slope):.4f}")
            with col3:
                st.metric("相关系数", f"{r_value:.3f}")
            with col4:
                st.metric("显著性", f"{p_value:.4f}")
            
            # 趋势可视化
            fig = go.Figure()
            
            # 原始数据
            fig.add_trace(go.Scatter(
                x=list(range(len(values))),
                y=values,
                mode='lines+markers',
                name='原始数据',
                line=dict(color='#1E40AF', width=2)
            ))
            
            # 趋势线
            trend_line = slope * np.arange(len(values)) + intercept
            fig.add_trace(go.Scatter(
                x=list(range(len(values))),
                y=trend_line,
                mode='lines',
                name='趋势线',
                line=dict(color='#DC2626', width=3, dash='dash')
            ))
            
            fig.update_layout(
                title=f"{selected_col} 趋势分析",
                xaxis_title="数据点",
                yaxis_title=selected_col,
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 趋势解释
            if p_value < 0.05:
                st.success(f"✅ 数眸发现趋势显著 (p < 0.05)，{selected_col} 呈现{trend_direction}")
            else:
                st.warning(f"⚠️ 数眸分析显示趋势不显著 (p ≥ 0.05)，{selected_col} 的{trend_direction}可能不具有统计意义")

def render_anomaly_detection(data):
    """异常检测"""
    st.subheader("🎯 异常检测")
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) == 0:
        st.warning("⚠️ 数据中没有数值型列，无法进行异常检测")
        return
    
    # 选择检测方法
    detection_method = st.selectbox(
        "选择异常检测方法",
        ["IQR方法", "Z-score方法", "百分位法", "隔离森林"]
    )
    
    selected_col = st.selectbox("选择要检测的列", numeric_cols)
    
    if selected_col and detection_method:
        if st.button("🎯 数眸开始异常检测"):
            with st.spinner("数眸正在检测异常值..."):
                values = data[selected_col].dropna()
                
                if len(values) > 0:
                    anomalies = []
                    
                    if detection_method == "IQR方法":
                        Q1 = values.quantile(0.25)
                        Q3 = values.quantile(0.75)
                        IQR = Q3 - Q1
                        lower_bound = Q1 - 1.5 * IQR
                        upper_bound = Q3 + 1.5 * IQR
                        anomalies = values[(values < lower_bound) | (values > upper_bound)]
                        
                    elif detection_method == "Z-score方法":
                        z_scores = np.abs(stats.zscore(values))
                        anomalies = values[z_scores > 3]
                        
                    elif detection_method == "百分位法":
                        lower_bound = values.quantile(0.01)
                        upper_bound = values.quantile(0.99)
                        anomalies = values[(values < lower_bound) | (values > upper_bound)]
                    
                    # 显示异常检测结果
                    st.success(f"✅ 数眸检测到 {len(anomalies)} 个异常值")
                    
                    if len(anomalies) > 0:
                        st.write("**异常值详情：**")
                        st.dataframe(anomalies.to_frame(), use_container_width=True)
                        
                        # 异常值可视化
                        fig = go.Figure()
                        
                        # 正常值
                        normal_values = values[~values.isin(anomalies)]
                        fig.add_trace(go.Scatter(
                            x=list(range(len(normal_values))),
                            y=normal_values,
                            mode='markers',
                            name='正常值',
                            marker=dict(color='#059669', size=6)
                        ))
                        
                        # 异常值
                        if len(anomalies) > 0:
                            anomaly_indices = [i for i, v in enumerate(values) if v in anomalies]
                            fig.add_trace(go.Scatter(
                                x=anomaly_indices,
                                y=anomalies,
                                mode='markers',
                                name='异常值',
                                marker=dict(color='#DC2626', size=10, symbol='x')
                            ))
                        
                        fig.update_layout(
                            title=f"{selected_col} 异常值检测结果",
                            xaxis_title="数据点",
                            yaxis_title=selected_col
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)

def render_business_insights(data):
    """商业洞察"""
    st.subheader("💡 商业洞察")
    
    # 数据概览洞察
    st.write("**1. 数据概览洞察**")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("数据规模", f"{len(data)} 行")
    with col2:
        st.metric("特征数量", f"{len(data.columns)} 列")
    with col3:
        st.metric("数据完整性", f"{((len(data) - data.isnull().sum().sum()) / (len(data) * len(data.columns)) * 100):.1f}%")
    with col4:
        st.metric("数据质量", f"{calculate_data_quality_score(data):.1f}/100")
    
    # 数据类型洞察
    st.write("**2. 数据类型洞察**")
    dtype_counts = data.dtypes.value_counts()
    
    fig = px.pie(
        values=dtype_counts.values,
        names=dtype_counts.index.astype(str),
        title="数据类型分布"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 数值型数据洞察
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) > 0:
        st.write("**3. 数值型数据洞察**")
        
        # 选择关键指标
        key_metrics = st.multiselect("选择关键业务指标", numeric_cols, default=numeric_cols[:3])
        
        if key_metrics:
            # 计算关键统计信息
            insights_data = []
            for col in key_metrics:
                values = data[col].dropna()
                if len(values) > 0:
                    insights_data.append({
                        '指标': col,
                        '平均值': values.mean(),
                        '中位数': values.median(),
                        '标准差': values.std(),
                        '最小值': values.min(),
                        '最大值': values.max(),
                        '变异系数': values.std() / values.mean() if values.mean() != 0 else 0
                    })
            
            if insights_data:
                insights_df = pd.DataFrame(insights_data)
                st.dataframe(insights_df, use_container_width=True)
                
                # 业务洞察建议
                st.write("**4. 数眸商业洞察建议**")
                
                for insight in insights_data:
                    st.write(f"**{insight['指标']}：**")
                    
                    # 变异系数分析
                    if insight['变异系数'] > 1:
                        st.write(f"• 数眸发现数据波动较大 (变异系数: {insight['变异系数']:.2f})，建议关注异常值")
                    elif insight['变异系数'] < 0.1:
                        st.write(f"• 数眸分析显示数据相对稳定 (变异系数: {insight['变异系数']:.2f})，变化较小")
                    
                    # 分布偏斜分析
                    values = data[insight['指标']].dropna()
                    skewness = values.skew()
                    if abs(skewness) > 1:
                        if skewness > 0:
                            st.write(f"• 数眸发现数据右偏分布 (偏度: {skewness:.2f})，存在较多高值")
                        else:
                            st.write(f"• 数眸发现数据左偏分布 (偏度: {skewness:.2f})，存在较多低值")
                    
                    st.write("---")

def render_comprehensive_insights(data):
    """综合洞察报告"""
    st.subheader("📊 综合洞察报告")
    
    if st.button("📊 数眸生成综合洞察报告"):
        with st.spinner("数眸正在生成综合洞察报告..."):
            # 创建综合报告
            report_content = generate_comprehensive_insights_report(data)
            
            # 显示报告
            st.markdown(report_content, unsafe_allow_html=True)
            
            # 下载报告
            st.download_button(
                label="📥 下载数眸洞察报告",
                data=report_content,
                file_name="数眸_数据洞察报告.html",
                mime="text/html"
            )

def generate_comprehensive_insights_report(data):
    """生成综合洞察报告"""
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
    
    report = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>数眸 - 数据洞察报告</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; line-height: 1.6; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }}
            h1 {{ color: #1E40AF; text-align: center; border-bottom: 3px solid #1E40AF; padding-bottom: 20px; font-size: 2.5em; }}
            h2 {{ color: #2563EB; border-bottom: 2px solid #DBEAFE; padding-bottom: 10px; margin-top: 30px; }}
            h3 {{ color: #3B82F6; margin-top: 25px; }}
            .insight-card {{ background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%); padding: 20px; margin: 20px 0; border-radius: 15px; border-left: 5px solid #1E40AF; }}
            .metric {{ background: #f8f9fa; padding: 15px; margin: 15px 0; border-radius: 10px; border-left: 4px solid #059669; }}
            .highlight {{ background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); padding: 15px; border-radius: 10px; border-left: 4px solid #D97706; }}
            .footer {{ text-align: center; color: #6B7280; margin-top: 50px; padding-top: 20px; border-top: 2px solid #E5E7EB; }}
            .brand {{ text-align: center; margin-bottom: 30px; }}
            .brand-logo {{ font-size: 3em; margin-bottom: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="brand">
                <div class="brand-logo">👁️</div>
                <h1>数眸 - 数据洞察报告</h1>
                <p style="font-size: 1.2em; color: #6B7280; text-align: center;">让数据洞察如眸般清澈明亮</p>
            </div>
            
            <div class="insight-card">
                <h2>📊 数据概览洞察</h2>
                <div class="metric">
                    <strong>数据集规模：</strong> {len(data)} 行 × {len(data.columns)} 列<br>
                    <strong>数据完整性：</strong> {((len(data) - data.isnull().sum().sum()) / (len(data) * len(data.columns)) * 100):.1f}%<br>
                    <strong>数据质量评分：</strong> {calculate_data_quality_score(data):.1f}/100<br>
                    <strong>数值型特征：</strong> {len(numeric_cols)} 个<br>
                    <strong>分类型特征：</strong> {len(categorical_cols)} 个
                </div>
            </div>
            
            <div class="insight-card">
                <h2>🔍 关键洞察发现</h2>
                <div class="highlight">
                    <h3>数据质量洞察</h3>
                    <p>• 缺失值总数：{data.isnull().sum().sum()} 个</p>
                    <p>• 重复行数：{data.duplicated().sum()} 行</p>
                    <p>• 数据类型分布：{', '.join([f'{str(dtype)}({count})' for dtype, count in data.dtypes.value_counts().items()])}</p>
                </div>
            </div>
            
            <div class="insight-card">
                <h2>💡 业务价值洞察</h2>
                <div class="metric">
                    <h3>数据特征分析</h3>
                    <p>• 数据集包含 {len(data)} 条记录，适合进行统计分析</p>
                    <p>• 具有 {len(numeric_cols)} 个数值型特征，可用于建模分析</p>
                    <p>• 具有 {len(categorical_cols)} 个分类型特征，可用于分组分析</p>
                </div>
            </div>
            
            <div class="footer">
                <p>👁️ 数眸 - 智能数据分析平台 | 生成时间: {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                <p>让数据洞察如眸般清澈明亮</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return report
