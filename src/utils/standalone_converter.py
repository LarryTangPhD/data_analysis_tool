"""
独立的JSON到CSV转换工具
专注于快速、高效的格式转换功能
"""

import streamlit as st
import pandas as pd
import json
import io
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
import logging

logger = logging.getLogger(__name__)

class StandaloneJSONConverter:
    """独立的JSON转换器"""
    
    def __init__(self):
        self.supported_formats = ['json', 'txt']
    
    def convert_json_to_csv(self, 
                           json_data: Union[str, List, Dict], 
                           explode_lists: bool = True,
                           separator: str = ".",
                           fill_na: str = "",
                           max_preview_rows: int = 10) -> Dict[str, Any]:
        """
        将JSON数据转换为CSV格式
        
        Args:
            json_data: JSON数据（字符串、列表或字典）
            explode_lists: 是否将列表字段展开为多行
            separator: 嵌套字段分隔符
            fill_na: 缺失值填充
            max_preview_rows: 预览行数
            
        Returns:
            包含转换结果和元数据的字典
        """
        try:
            # 解析JSON数据
            if isinstance(json_data, str):
                data = json.loads(json_data)
            else:
                data = json_data
            
            # 确保是列表格式
            if isinstance(data, dict):
                # 如果顶层是字典，尝试提取值为列表的字段
                list_candidates = [v for v in data.values() if isinstance(v, list)]
                if len(list_candidates) == 1:
                    data = list_candidates[0]
                    extracted_field = [k for k, v in data.items() if v == data][0]
                    info_message = f"检测到嵌套结构，已提取字段 `{extracted_field}` 进行转换。"
                else:
                    info_message = "JSON顶层为对象但未找到可转换的数组字段。尝试直接展开。"
                    data = [data]  # 包装成列表
            elif not isinstance(data, list):
                raise ValueError("JSON根节点必须是数组或可转换的对象。")
            else:
                info_message = "JSON数据格式正确，开始转换。"
            
            # 使用pandas进行标准化
            df = pd.json_normalize(data, sep=separator)
            
            # 处理列表字段展开
            list_columns = []
            if explode_lists:
                # 找出包含列表的列
                list_columns = [col for col in df.columns if df[col].apply(lambda x: isinstance(x, list)).any()]
                if list_columns:
                    # 展开第一个列表字段
                    df = df.explode(list_columns[0])
                    df = df.reset_index(drop=True)
                    explode_message = f"已将字段 `{list_columns[0]}` 展开为多行。"
                else:
                    explode_message = "未检测到列表字段，跳过展开。"
            else:
                explode_message = "跳过列表字段展开。"
            
            # 填充缺失值
            df = df.fillna(fill_na)
            
            # 生成CSV数据
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False, encoding='utf-8')
            csv_data = csv_buffer.getvalue()
            
            return {
                'success': True,
                'dataframe': df,
                'csv_data': csv_data,
                'info_message': info_message,
                'explode_message': explode_message,
                'list_columns': list_columns,
                'preview_data': df.head(max_preview_rows),
                'shape': df.shape,
                'columns': df.columns.tolist(),
                'dtypes': df.dtypes.to_dict()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'dataframe': None,
                'csv_data': None
            }
    
    def analyze_json_structure(self, json_data: Union[str, List, Dict]) -> Dict[str, Any]:
        """分析JSON数据结构"""
        try:
            if isinstance(json_data, str):
                data = json.loads(json_data)
            else:
                data = json_data
            
            analysis = {
                'type': type(data).__name__,
                'size': len(data) if isinstance(data, (list, dict)) else 1,
                'has_lists': False,
                'has_nested_objects': False,
                'sample_keys': [],
                'complex_columns': []
            }
            
            if isinstance(data, list) and len(data) > 0:
                sample_item = data[0]
                analysis['sample_keys'] = list(sample_item.keys()) if isinstance(sample_item, dict) else []
                
                # 分析嵌套结构
                for key, value in sample_item.items() if isinstance(sample_item, dict) else []:
                    if isinstance(value, list):
                        analysis['has_lists'] = True
                        analysis['complex_columns'].append({
                            'column': key,
                            'type': 'list',
                            'sample_length': len(value) if value else 0
                        })
                    elif isinstance(value, dict):
                        analysis['has_nested_objects'] = True
                        analysis['complex_columns'].append({
                            'column': key,
                            'type': 'dict',
                            'sample_keys': list(value.keys())[:5]
                        })
            
            return analysis
            
        except Exception as e:
            return {
                'error': str(e),
                'type': 'unknown'
            }

def render_standalone_converter():
    """渲染独立的JSON转换工具"""
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px rgba(30, 64, 175, 0.3);
    ">
        <h2 style="color: white; margin-bottom: 20px; text-align: center;">🔄 JSON 转 CSV 转换器</h2>
        <p style="font-size: 18px; line-height: 1.8; margin-bottom: 20px; text-align: center;">
            <strong>💡 快速、高效的JSON格式转换工具</strong><br>
            支持复杂JSON结构的智能转换，自动处理嵌套字段、列表展开等，生成符合Tidy Data原则的整洁CSV格式。
        </p>
        <div style="display: flex; gap: 25px; margin-bottom: 20px;">
            <div style="flex: 1; background: rgba(255,255,255,0.15); padding: 20px; border-radius: 12px; backdrop-filter: blur(10px);">
                <h4 style="color: #FDE68A; margin-bottom: 15px;">🚀 快速转换</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 15px;">
                    <li>直接上传JSON文件</li>
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
    
    # 创建转换器实例
    converter = StandaloneJSONConverter()
    
    # 文件上传
    uploaded_file = st.file_uploader(
        "📁 上传JSON文件",
        type=converter.supported_formats,
        help="支持JSON格式文件，将自动转换为CSV格式"
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
                    st.metric("数据大小", analysis['size'])
                with col3:
                    st.metric("包含列表", "是" if analysis['has_lists'] else "否")
                with col4:
                    st.metric("嵌套对象", "是" if analysis['has_nested_objects'] else "否")
                
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
                    explode_lists = st.checkbox(
                        "展开列表字段（Tidy Data）", 
                        value=True,
                        help="将JSON中的列表字段展开为多行，符合整洁数据原则"
                    )
                    separator = st.text_input(
                        "嵌套字段分隔符", 
                        value=".",
                        help="用于展开嵌套字段，如 info.age"
                    )
                
                with col2:
                    fill_na = st.text_input(
                        "缺失值填充", 
                        value="",
                        help="用于填充转换后的缺失值"
                    )
                    max_preview = st.number_input(
                        "预览行数", 
                        min_value=5, 
                        max_value=50, 
                        value=10,
                        help="转换结果预览的行数"
                    )
                
                # 执行转换
                if st.button("🔄 执行转换", type="primary", use_container_width=True):
                    with st.spinner("正在转换..."):
                        result = converter.convert_json_to_csv(
                            json_data=file_content,
                            explode_lists=explode_lists,
                            separator=separator,
                            fill_na=fill_na,
                            max_preview_rows=max_preview
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
                                st.metric("列表字段", len(result['list_columns']))
                            
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
                            
                            with col1:
                                # CSV下载
                                st.download_button(
                                    label="📄 下载CSV文件",
                                    data=result['csv_data'],
                                    file_name=f"converted_{uploaded_file.name.replace('.json', '.csv')}",
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
                                    file_name=f"converted_{uploaded_file.name.replace('.json', '.xlsx')}",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    use_container_width=True
                                )
                            
                            with col3:
                                # JSON下载
                                json_data = result['dataframe'].to_json(orient='records', indent=2, force_ascii=False)
                                st.download_button(
                                    label="📋 下载JSON文件",
                                    data=json_data,
                                    file_name=f"converted_{uploaded_file.name.replace('.json', '_flattened.json')}",
                                    mime="application/json",
                                    use_container_width=True
                                )
                            
                            # 转换建议
                            st.markdown("---")
                            st.subheader("💡 转换建议")
                            
                            if result['list_columns']:
                                st.success("✅ 检测到列表字段并已展开，数据符合Tidy Data原则")
                            else:
                                st.info("ℹ️ 数据中没有检测到列表字段，转换后的数据已经是整洁格式")
                            
                            if len(result['columns']) > 10:
                                st.warning("⚠️ 转换后列数较多，建议检查数据是否需要进一步处理")
                            
                        else:
                            st.error(f"❌ 转换失败：{result['error']}")
            else:
                st.error(f"❌ 文件解析失败：{analysis['error']}")
                
        except Exception as e:
            st.error(f"❌ 处理失败：{str(e)}")
    else:
        st.info("📁 请上传JSON文件以开始转换")
        
        # 显示使用说明
        st.markdown("---")
        st.subheader("📖 使用说明")
        
        st.markdown("""
        **支持的JSON格式：**
        - 数组格式：`[{}, {}, {}]`
        - 对象格式：`{"data": [{}, {}, {}]}`
        - 嵌套对象：包含复杂嵌套结构的数据
        
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

def main():
    """主函数 - 独立运行"""
    st.set_page_config(
        page_title="JSON转CSV转换器",
        page_icon="🔄",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    render_standalone_converter()

if __name__ == "__main__":
    main()
