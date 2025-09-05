"""
数据上传页面模块
负责数据上传、预览和基础分析功能
"""

import streamlit as st
import pandas as pd
import numpy as np
from src.utils.data_processing import (
    load_data, calculate_data_quality_score, get_data_info,
    get_missing_value_summary, get_data_type_summary, validate_json_structure
)
from src.utils.visualization_helpers import create_missing_values_chart
from src.utils.ai_assistant_utils import get_smart_ai_assistant
from src.utils.report_exporter import ReportExporter, get_download_link, get_download_link_bytes
from src.modules.comprehensive_report_export import render_comprehensive_report_export
from src.utils.session_manager import SessionManager
from src.utils.ux_enhancements import get_ux_enhancements


def render_data_upload_page():
    """渲染数据上传页面"""
    st.markdown('<h2 class="sub-header">📁 数据上传</h2>', unsafe_allow_html=True)
    
    # 获取会话管理器和用户体验增强
    session_manager = SessionManager()
    ux_enhancements = get_ux_enhancements()
    
    # 渲染欢迎屏幕（如果没有数据）
    if not session_manager.has_data():
        ux_enhancements.render_welcome_screen()
    
    # 添加数据上传说明
    _render_upload_guide()
    
    # 文件上传
    uploaded_file = st.file_uploader(
        "选择数据文件",
        type=['csv', 'xlsx', 'xls', 'json', 'parquet'],
        help="支持CSV、Excel、JSON、Parquet格式"
    )
    
    if uploaded_file is not None:
        _handle_file_upload(uploaded_file, session_manager)


def _render_upload_guide():
    """渲染上传指南"""
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


def _handle_file_upload(uploaded_file, session_manager):
    """处理文件上传"""
    try:
        # 使用缓存函数读取数据
        data = load_data(uploaded_file)
        session_manager.set_data(data)
        
        st.success(f"✅ 数眸数据上传成功！共 {len(data)} 行，{len(data.columns)} 列")
        
        # 添加到操作历史
        ux_enhancements.add_to_history(f"上传文件: {uploaded_file.name}")
        
        # 特殊处理JSON文件
        if uploaded_file.name.endswith('.json'):
            _handle_json_file(data)
        
        # 显示数据基本信息
        _display_data_info(data, session_manager)
        
        # 数据预览
        _display_data_preview(data)
        
        st.markdown("---")
        
        # 基础数据分析
        _render_basic_analysis(data)
        
        # 数据质量评估
        _render_data_quality_assessment(data)
        
        # 智能分析建议
        ux_enhancements = get_ux_enhancements()
        ux_enhancements.render_analysis_suggestions(data)
        
        # 数据格式转换提示
        st.info('💡 数据格式转换功能已移至独立的"🔄 数据格式转换"页面，请使用顶部导航访问。')
        
        # AI智能分析建议
        _render_ai_analysis(data, session_manager)
        
    except Exception as e:
        st.error(f"❌ 数据读取失败：{str(e)}")


def _handle_json_file(data):
    """处理JSON文件的特殊逻辑"""
    validation_result = validate_json_structure(data)
    
    if validation_result["complex_columns"]:
        st.info("📋 JSON数据结构分析")
        st.write("**发现复杂对象列：**")
        for col_info in validation_result["complex_columns"]:
            if col_info["type"] == "dict":
                st.write(f"• {col_info['column']}: 字典类型 (包含键: {', '.join(col_info['sample_keys'][:5])}{'...' if len(col_info['sample_keys']) > 5 else ''})")
            elif col_info["type"] == "list":
                st.write(f"• {col_info['column']}: 列表类型 (示例长度: {col_info['sample_length']})")
        
        if validation_result["suggestions"]:
            st.write("**处理建议：**")
            for suggestion in validation_result["suggestions"]:
                st.write(f"• {suggestion}")


def _display_data_info(data, session_manager):
    """显示数据基本信息"""
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


def _display_data_preview(data):
    """显示数据预览"""
    # 使用增强的数据预览
    ux_enhancements = get_ux_enhancements()
    ux_enhancements.render_data_preview_enhanced(data, max_rows=10)


def _render_basic_analysis(data):
    """渲染基础数据分析"""
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


def _render_data_quality_assessment(data):
    """渲染数据质量评估"""
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


def _render_ai_analysis(data, session_manager):
    """渲染AI智能分析"""
    st.subheader("🤖 AI智能分析建议")
    
    # 检查AI助手是否可用
    ai_assistant = get_smart_ai_assistant()
    
    if ai_assistant is None:
        _render_ai_config_warning()
    else:
        _render_ai_analysis_content(data, ai_assistant, session_manager)


def _render_ai_config_warning():
    """渲染AI配置警告"""
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


def _render_ai_analysis_content(data, ai_assistant, session_manager):
    """渲染AI分析内容"""
    if st.button("🤖 获取AI分析建议", type="primary"):
        with st.spinner("AI正在分析数据..."):
            try:
                data_info = session_manager.get_data_info()
                analysis_result = ai_assistant.analyze_uploaded_data(data, data_info)
                
                st.success("✅ 数眸AI分析完成！")
                st.markdown("### 🤖 数眸AI智能分析结果")
                st.markdown(analysis_result)

                # 添加AI分析报告导出功能
                _render_ai_report_export(data, analysis_result, data_info)
                
            except Exception as e:
                st.error(f"❌ 数眸AI分析失败：{str(e)}")
    
    # AI智能问答
    _render_ai_qa(ai_assistant, data)


def _render_ai_report_export(data, analysis_result, data_info):
    """渲染AI报告导出"""
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
                _generate_ai_report(exporter, export_format, data_info, analysis_result, data)
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


def _generate_ai_report(exporter, export_format, data_info, analysis_result, data):
    """生成AI报告"""
    if export_format == "Markdown (.md)":
        report_content = exporter.export_markdown_report(data_info, analysis_result, data)
        filename = f"AI分析报告_{exporter.timestamp}.md"
        st.markdown(get_download_link(report_content, filename, "text/markdown"), unsafe_allow_html=True)
    elif export_format == "HTML (.html)":
        report_content = exporter.export_html_report(data_info, analysis_result, data)
        filename = f"AI分析报告_{exporter.timestamp}.html"
        st.markdown(get_download_link(report_content, filename, "text/html"), unsafe_allow_html=True)
    elif export_format == "JSON (.json)":
        report_content = exporter.export_json_report(data_info, analysis_result, data)
        filename = f"AI分析报告_{exporter.timestamp}.json"
        st.markdown(get_download_link(report_content, filename, "application/json"), unsafe_allow_html=True)
    elif export_format == "PDF (.pdf)":
        report_content = exporter.export_pdf_report(data_info, analysis_result, data)
        filename = f"AI分析报告_{exporter.timestamp}.pdf"
        st.markdown(get_download_link_bytes(report_content, filename, "application/pdf"), unsafe_allow_html=True)


def _render_ai_qa(ai_assistant, data):
    """渲染AI问答"""
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
