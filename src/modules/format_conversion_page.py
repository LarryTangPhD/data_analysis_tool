"""
数据格式转换页面模块
提供独立的数据格式转换功能
"""

import streamlit as st
import pandas as pd
import json
import io
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
import logging

from src.utils.advanced_format_converter import AdvancedFormatConverter
from src.utils.tidy_data_converter import TidyDataConverter

logger = logging.getLogger(__name__)

def render_format_conversion_page():
    """渲染数据格式转换页面"""
    
    # 页面标题
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(30, 64, 175, 0.3);
    ">
        <h1 style="color: white; margin-bottom: 20px; text-align: center;">🔄 数据格式转换</h1>
        <p style="font-size: 18px; line-height: 1.8; margin-bottom: 20px; text-align: center;">
            <strong>💡 智能数据格式转换工具</strong><br>
            支持复杂数据结构的智能转换，自动处理嵌套字段、列表展开等，生成符合Tidy Data原则的整洁格式。
        </p>
        <div style="display: flex; gap: 25px; margin-bottom: 20px;">
            <div style="flex: 1; background: rgba(255,255,255,0.15); padding: 20px; border-radius: 12px; backdrop-filter: blur(10px);">
                <h4 style="color: #FDE68A; margin-bottom: 15px;">🚀 快速转换</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 15px;">
                    <li>直接上传数据文件</li>
                    <li>一键智能转换</li>
                    <li>即时预览结果</li>
                    <li>多格式下载</li>
                </ul>
            </div>
            <div style="flex: 1; background: rgba(255,255,255,0.15); padding: 20px; border-radius: 12px; backdrop-filter: blur(10px);">
                <h4 style="color: #A7F3D0; margin-bottom: 15px;">🧠 智能处理</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 15px;">
                    <li>自动检测数据结构</li>
                    <li>嵌套字段智能展开</li>
                    <li>列表字段多行展开</li>
                    <li>数据完整性保证</li>
                </ul>
            </div>
        </div>
        <p style="font-size: 16px; margin: 0; text-align: center; opacity: 0.9;">
            <strong>🎯 适用场景：</strong> API数据处理、复杂JSON转换、数据标准化、Tidy Data生成
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 转换模式选择
    st.subheader("🎯 选择转换模式")
    
    conversion_mode = st.radio(
        "转换模式",
        ["🔄 标准转换", "🧹 整洁数据转换"],
        help="标准转换：快速转换，保持部分结构；整洁数据转换：完全符合Tidy Data原则"
    )
    
    # 根据模式选择转换器
    if conversion_mode == "🔄 标准转换":
        converter = AdvancedFormatConverter()
        converter_name = "标准转换器"
        converter_description = "快速转换，适合一般数据处理需求"
    else:
        converter = TidyDataConverter()
        converter_name = "整洁数据转换器"
        converter_description = "完全符合Tidy Data原则，适合数据分析和机器学习"
    
    st.info(f"📋 当前使用：{converter_name} - {converter_description}")
    
    # 文件上传
    uploaded_file = st.file_uploader(
        "📁 上传数据文件",
        type=converter.supported_input_formats,
        help="支持JSON、CSV、Excel等格式文件，将自动转换为目标格式"
    )
    
    if uploaded_file is not None:
        try:
            # 读取文件内容
            file_content = uploaded_file.read().decode("utf-8")
            
            # 分析数据结构
            analysis = converter.analyze_json_structure(file_content)
            
            if 'error' not in analysis:
                st.success(f"✅ 文件解析成功！数据类型: {analysis['type']}, 大小: {analysis['size']}")
                
                # 显示数据结构信息
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("数据类型", analysis['type'])
                with col2:
                    st.metric("原始记录数", analysis['size'])
                with col3:
                    if 'estimated_tidy_rows' in analysis:
                        st.metric("预计整洁行数", analysis['estimated_tidy_rows'])
                    else:
                        st.metric("包含列表", "是" if analysis['has_lists'] else "否")
                with col4:
                    st.metric("复杂字段数", len(analysis['complex_columns']))
                
                # 显示复杂字段信息
                if analysis['complex_columns']:
                    st.write("**🔍 复杂字段分析：**")
                    for col_info in analysis['complex_columns']:
                        if col_info['type'] == 'list':
                            st.write(f"• {col_info['column']}: 列表类型 (示例长度: {col_info['sample_length']})")
                        elif col_info['type'] == 'dict':
                            st.write(f"• {col_info['column']}: 字典类型 (包含键: {', '.join(col_info['sample_keys'][:5])}{'...' if len(col_info['sample_keys']) > 5 else ''})")
                
                # 转换选项
                st.markdown("---")
                st.subheader("⚙️ 转换配置")
                
                col1, col2 = st.columns(2)
                with col1:
                    separator = st.text_input(
                        "嵌套字段分隔符", 
                        value=".",
                        help="用于展开嵌套字段，如 info.age"
                    )
                    fill_na = st.text_input(
                        "缺失值填充", 
                        value="",
                        help="用于填充转换后的缺失值"
                    )
                
                with col2:
                    encoding = st.selectbox(
                        "文件编码",
                        ["utf-8-sig", "utf-8", "gbk", "gb2312"],
                        help="选择输出文件的编码格式，推荐使用utf-8-sig以支持中文"
                    )
                    max_preview = st.number_input(
                        "预览行数", 
                        min_value=5, 
                        max_value=50, 
                        value=10,
                        help="转换结果预览的行数"
                    )
                
                # 标准转换的额外选项
                if conversion_mode == "🔄 标准转换":
                    explode_lists = st.checkbox(
                        "展开列表字段（Tidy Data）", 
                        value=True,
                        help="将数据中的列表字段展开为多行，符合整洁数据原则"
                    )
                
                # 执行转换
                if st.button("🔄 执行转换", type="primary", use_container_width=True):
                    with st.spinner("正在转换..."):
                        if conversion_mode == "🔄 标准转换":
                            result = converter.convert_json_to_csv(
                                json_data=file_content,
                                explode_lists=explode_lists,
                                separator=separator,
                                fill_na=fill_na,
                                max_preview_rows=max_preview,
                                encoding=encoding
                            )
                        else:
                            result = converter.convert_to_tidy_data(
                                json_data=file_content,
                                separator=separator,
                                fill_na=fill_na,
                                max_preview_rows=max_preview,
                                encoding=encoding
                            )
                        
                        if result['success']:
                            st.success("✅ 转换完成！")
                            
                            # 显示转换信息
                            col1, col2 = st.columns(2)
                            with col1:
                                st.info(result['info_message'])
                            with col2:
                                st.info(result['explode_message'])
                            
                            # 显示转换结果统计
                            st.subheader("📊 转换结果统计")
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("转换后行数", result['shape'][0])
                            with col2:
                                st.metric("转换后列数", result['shape'][1])
                            with col3:
                                st.metric("数据类型", len(set(result['dtypes'].values())))
                            with col4:
                                if 'list_columns' in result:
                                    st.metric("列表字段", len(result['list_columns']))
                                elif 'tidy_analysis' in result:
                                    st.metric("整洁度评分", f"{result['tidy_analysis']['tidy_score']}/100")
                            
                            # 整洁数据质量评估（仅对整洁转换）
                            if conversion_mode == "🧹 整洁数据转换" and 'tidy_analysis' in result:
                                tidy_analysis = result['tidy_analysis']
                                st.subheader("📊 整洁数据质量评分")
                                
                                # 质量评估
                                if tidy_analysis['tidy_score'] >= 90:
                                    st.success("🎉 优秀！数据完全符合整洁数据原则")
                                elif tidy_analysis['tidy_score'] >= 70:
                                    st.warning("⚠️ 良好，但仍有改进空间")
                                else:
                                    st.error("❌ 需要进一步处理以达到整洁数据标准")
                            
                            # 显示转换结果预览
                            st.subheader("📋 转换结果预览")
                            st.dataframe(result['preview_data'], use_container_width=True)
                            
                            # 数据类型信息
                            st.subheader("📈 数据类型分析")
                            dtype_df = pd.DataFrame([
                                {'列名': col, '数据类型': str(dtype)} 
                                for col, dtype in result['dtypes'].items()
                            ])
                            st.dataframe(dtype_df, use_container_width=True)
                            
                            # 下载转换结果
                            st.subheader("📥 下载转换结果")
                            
                            col1, col2, col3 = st.columns(3)
                            
                            # 生成文件名
                            base_name = uploaded_file.name.replace('.json', '')
                            if conversion_mode == "🧹 整洁数据转换":
                                file_prefix = "tidy_data"
                            else:
                                file_prefix = "converted"
                            
                            with col1:
                                # CSV下载
                                st.download_button(
                                    label="📄 下载CSV文件",
                                    data=result['csv_data'],
                                    file_name=f"{file_prefix}_{base_name}.csv",
                                    mime="text/csv",
                                    use_container_width=True
                                )
                            
                            with col2:
                                # Excel下载
                                excel_buffer = io.BytesIO()
                                result['dataframe'].to_excel(excel_buffer, index=False, engine='openpyxl')
                                excel_data = excel_buffer.getvalue()
                                st.download_button(
                                    label="📊 下载Excel文件",
                                    data=excel_data,
                                    file_name=f"{file_prefix}_{base_name}.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    use_container_width=True
                                )
                            
                            with col3:
                                # JSON下载
                                json_data = result['dataframe'].to_json(orient='records', indent=2, force_ascii=False)
                                json_suffix = "_tidy.json" if conversion_mode == "🧹 整洁数据转换" else "_flattened.json"
                                st.download_button(
                                    label="📋 下载JSON文件",
                                    data=json_data,
                                    file_name=f"{file_prefix}_{base_name}{json_suffix}",
                                    mime="application/json",
                                    use_container_width=True
                                )
                            
                            # 转换建议
                            st.markdown("---")
                            st.subheader("💡 转换建议")
                            
                            if conversion_mode == "🔄 标准转换":
                                if 'list_columns' in result and result['list_columns']:
                                    st.success("✅ 检测到列表字段并已展开，数据符合Tidy Data原则")
                                else:
                                    st.info("ℹ️ 数据中没有检测到列表字段，转换后的数据已经是整洁格式")
                                
                                if len(result['columns']) > 10:
                                    st.warning("⚠️ 转换后列数较多，建议检查数据是否需要进一步处理")
                                
                                # 建议使用整洁转换
                                st.info("💡 提示：如需更彻底的整洁数据转换，请选择'整洁数据转换'模式")
                            
                            else:  # 整洁数据转换
                                if 'tidy_analysis' in result:
                                    tidy_analysis = result['tidy_analysis']
                                    if tidy_analysis['tidy_score'] >= 90:
                                        st.success("🎉 数据完全符合整洁数据原则，可直接用于数据分析和机器学习")
                                    elif tidy_analysis['tidy_score'] >= 70:
                                        st.warning("⚠️ 数据基本符合整洁原则，但建议进一步优化")
                                    else:
                                        st.error("❌ 数据需要进一步处理以达到整洁数据标准")
                            
                            # 保存转换后的数据到session state
                            if conversion_mode == "🧹 整洁数据转换":
                                st.session_state.tidy_data = result['dataframe']
                                st.success("✅ 整洁数据已保存，可在其他页面使用")
                            else:
                                st.session_state.converted_data = result['dataframe']
                                st.success("✅ 转换后的数据已保存，可在其他页面使用")
                            
                        else:
                            st.error(f"❌ 转换失败：{result['error']}")
            else:
                st.error(f"❌ 文件解析失败：{analysis['error']}")
                
        except Exception as e:
            st.error(f"❌ 处理失败：{str(e)}")
    else:
        st.info("📁 请上传数据文件以开始转换")
        
        # 显示使用说明
        st.markdown("---")
        st.subheader("📖 转换模式说明")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🔄 标准转换**
            - 快速转换，保持部分结构
            - 展开第一个列表字段
            - 扁平化嵌套字典
            - 适合一般数据处理需求
            """)
        
        with col2:
            st.markdown("""
            **🧹 整洁数据转换**
            - 完全符合Tidy Data原则
            - 展开所有列表字段（笛卡尔积）
            - 完全扁平化所有嵌套结构
            - 适合数据分析和机器学习
            """)
        
        # 显示使用说明
        st.markdown("---")
        st.subheader("📖 使用说明")
        
        st.markdown("""
        **支持的数据格式：**
        - JSON格式：`[{}, {}, {}]` 或 `{"data": [{}, {}, {}]}`
        - CSV格式：标准逗号分隔值文件
        - Excel格式：.xlsx 和 .xls 文件
        - 其他格式：Parquet、TXT等
        
        **转换特性：**
        - 自动检测数据结构
        - 智能展开嵌套字段
        - 列表字段多行展开
        - 保持数据完整性
        
        **输出格式：**
        - CSV：标准逗号分隔值格式
        - Excel：功能丰富的表格格式
        - JSON：重新格式化的JSON数据
        """)
        
        # 显示示例
        st.markdown("---")
        st.subheader("📝 示例数据")
        
        example_data = [
            {
                "id": 1,
                "name": "张三",
                "skills": ["Python", "SQL"],
                "contact": {"email": "zhangsan@example.com"}
            },
            {
                "id": 2,
                "name": "李四",
                "skills": ["JavaScript", "React"],
                "contact": {"email": "lisi@example.com"}
            }
        ]
        
        st.json(example_data)
        st.caption("上传类似格式的数据文件即可进行转换")
        
        # 功能特性展示
        st.markdown("---")
        st.subheader("🎯 功能特性")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🔍 智能分析**
            - 自动识别数据结构
            - 检测复杂字段类型
            - 提供转换建议
            - 数据质量评估
            """)
        
        with col2:
            st.markdown("""
            **🔄 灵活转换**
            - 多格式输入支持
            - 多格式输出选择
            - 自定义转换参数
            - 批量处理能力
            """)
