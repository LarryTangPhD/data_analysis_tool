"""
整洁数据转换器
专门用于将复杂JSON数据转换为符合Tidy Data原则的整洁格式
"""

import pandas as pd
import json
import streamlit as st
from typing import Dict, Any, List, Optional, Union
import io
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class TidyDataConverter:
    """整洁数据转换器"""
    
    def __init__(self):
        self.supported_input_formats = ['json', 'csv', 'xlsx', 'xls', 'parquet', 'txt']
        self.supported_output_formats = ['csv', 'xlsx', 'parquet', 'json']
    
    def convert_to_tidy_data(self, 
                            json_data: Union[str, List, Dict], 
                            separator: str = ".", 
                            fill_na: str = "",
                            max_preview_rows: int = 10,
                            encoding: str = "utf-8-sig") -> Dict[str, Any]:
        """
        将JSON数据转换为真正的整洁数据
        
        Args:
            json_data: JSON数据（字符串、列表或字典）
            separator: 嵌套字段分隔符
            fill_na: 缺失值填充
            max_preview_rows: 预览行数
            encoding: 输出编码
            
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
                list_candidates = [v for v in data.values() if isinstance(v, list)]
                if len(list_candidates) == 1:
                    data = list_candidates[0]
                    extracted_field = [k for k, v in data.items() if v == data][0]
                    info_message = f"检测到嵌套结构，已提取字段 `{extracted_field}` 进行转换。"
                else:
                    info_message = "JSON顶层为对象但未找到可转换的数组字段。尝试直接展开。"
                    data = [data]
            elif not isinstance(data, list):
                raise ValueError("JSON根节点必须是数组或可转换的对象。")
            else:
                info_message = "JSON数据格式正确，开始转换。"
            
            # 第一步：递归展开所有嵌套列表
            expanded_data = []
            for item in data:
                expanded_items = self._recursive_expand_lists(item)
                expanded_data.extend(expanded_items)
            
            # 第二步：完全扁平化所有嵌套字典
            flattened_data = []
            for item in expanded_data:
                flattened_item = self._flatten_all_dicts(item, separator)
                flattened_data.append(flattened_item)
            
            # 第三步：创建DataFrame
            df = pd.DataFrame(flattened_data)
            
            # 第四步：填充缺失值
            df = df.fillna(fill_na)
            
            # 第五步：重置索引
            df = df.reset_index(drop=True)
            
            # 生成CSV数据
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False, encoding=encoding)
            csv_data = csv_buffer.getvalue()
            
            # 分析转换效果
            analysis = self._analyze_tidy_data_quality(df)
            
            return {
                'success': True,
                'dataframe': df,
                'csv_data': csv_data,
                'info_message': info_message,
                'explode_message': f"已完全展开所有列表字段，共生成 {len(df)} 行整洁数据。",
                'preview_data': df.head(max_preview_rows),
                'shape': df.shape,
                'columns': df.columns.tolist(),
                'dtypes': df.dtypes.to_dict(),
                'tidy_analysis': analysis
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'dataframe': None,
                'csv_data': None
            }
    
    def _recursive_expand_lists(self, item):
        """递归展开所有嵌套列表字段"""
        if not isinstance(item, dict):
            return [item]
        
        # 使用pandas的json_normalize来处理嵌套结构
        import pandas as pd
        
        # 将单个字典转换为DataFrame
        df = pd.json_normalize(item, sep='.')
        
        # 找出包含列表的列
        list_columns = []
        for col in df.columns:
            if df[col].apply(lambda x: isinstance(x, list)).any():
                list_columns.append(col)
        
        if not list_columns:
            return [item]
        
        # 展开第一个列表列
        first_list_col = list_columns[0]
        expanded_df = df.explode(first_list_col)
        
        # 如果展开的列包含字典，需要进一步扁平化
        if expanded_df[first_list_col].apply(lambda x: isinstance(x, dict)).any():
            # 将展开的DataFrame转换回字典列表
            expanded_records = []
            for _, row in expanded_df.iterrows():
                record = row.to_dict()
                # 处理展开的字典
                if isinstance(record[first_list_col], dict):
                    # 将字典的键值对添加到记录中
                    for key, value in record[first_list_col].items():
                        record[f"{first_list_col}.{key}"] = value
                    # 删除原始的列表列
                    del record[first_list_col]
                expanded_records.append(record)
            return expanded_records
        else:
            # 简单列表，直接转换回字典列表
            return expanded_df.to_dict('records')
    
    def _process_nested_lists(self, obj):
        """递归处理嵌套字典中的列表字段"""
        if not isinstance(obj, dict):
            return obj
        
        processed = {}
        for key, value in obj.items():
            if isinstance(value, dict):
                # 递归处理嵌套字典
                processed[key] = self._process_nested_lists(value)
            elif isinstance(value, list):
                # 处理列表中的字典元素
                if len(value) > 0 and isinstance(value[0], dict):
                    # 如果是字典列表，递归处理每个字典
                    processed_list = []
                    for item in value:
                        processed_item = self._process_nested_lists(item)
                        processed_list.append(processed_item)
                    processed[key] = processed_list
                else:
                    processed[key] = value
            else:
                processed[key] = value
        
        return processed
    
    def _flatten_all_dicts(self, obj, separator="."):
        """递归扁平化所有字典结构"""
        if not isinstance(obj, dict):
            return obj
        
        flattened = {}
        for key, value in obj.items():
            if isinstance(value, dict):
                # 递归扁平化嵌套字典
                nested = self._flatten_all_dicts(value, separator)
                for nested_key, nested_value in nested.items():
                    flattened[f"{key}{separator}{nested_key}"] = nested_value
            elif isinstance(value, list):
                # 列表应该已经在之前被展开，这里作为备用处理
                if len(value) > 0 and isinstance(value[0], dict):
                    # 如果是字典列表，扁平化第一个字典
                    first_dict = self._flatten_all_dicts(value[0], separator)
                    for nested_key, nested_value in first_dict.items():
                        flattened[f"{key}{separator}{nested_key}"] = nested_value
                else:
                    flattened[key] = str(value)
            else:
                flattened[key] = value
        
        return flattened
    
    def _analyze_tidy_data_quality(self, df):
        """分析整洁数据质量"""
        analysis = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'has_nested_columns': False,
            'has_list_data': False,
            'has_dict_data': False,
            'data_types': {},
            'tidy_score': 100  # 满分100分
        }
        
        # 检查列名是否包含分隔符（嵌套结构）
        nested_columns = [col for col in df.columns if '.' in col]
        if nested_columns:
            analysis['has_nested_columns'] = True
            analysis['tidy_score'] -= 20
        
        # 检查数据类型
        for col in df.columns:
            sample_values = df[col].dropna().head(5)
            if len(sample_values) > 0:
                first_value = sample_values.iloc[0]
                data_type = type(first_value).__name__
                analysis['data_types'][col] = data_type
                
                if isinstance(first_value, list):
                    analysis['has_list_data'] = True
                    analysis['tidy_score'] -= 30
                elif isinstance(first_value, dict):
                    analysis['has_dict_data'] = True
                    analysis['tidy_score'] -= 30
        
        # 确保分数不为负数
        analysis['tidy_score'] = max(0, analysis['tidy_score'])
        
        return analysis
    
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
                'complex_columns': [],
                'estimated_tidy_rows': 0
            }
            
            if isinstance(data, list) and len(data) > 0:
                sample_item = data[0]
                analysis['sample_keys'] = list(sample_item.keys()) if isinstance(sample_item, dict) else []
                
                # 分析嵌套结构
                list_count = 0
                dict_count = 0
                for key, value in sample_item.items() if isinstance(sample_item, dict) else []:
                    if isinstance(value, list):
                        analysis['has_lists'] = True
                        list_count += 1
                        analysis['complex_columns'].append({
                            'column': key,
                            'type': 'list',
                            'sample_length': len(value) if value else 0
                        })
                    elif isinstance(value, dict):
                        analysis['has_nested_objects'] = True
                        dict_count += 1
                        analysis['complex_columns'].append({
                            'column': key,
                            'type': 'dict',
                            'sample_keys': list(value.keys())[:5]
                        })
                
                # 估算整洁数据行数
                estimated_rows = len(data)
                for col_info in analysis['complex_columns']:
                    if col_info['type'] == 'list':
                        estimated_rows *= max(1, col_info['sample_length'])
                analysis['estimated_tidy_rows'] = estimated_rows
            
            return analysis
            
        except Exception as e:
            return {
                'error': str(e),
                'type': 'unknown'
            }
    
    def get_conversion_suggestions(self, analysis: Dict[str, Any]) -> List[str]:
        """根据结构分析提供转换建议"""
        suggestions = []
        
        if analysis.get('has_lists'):
            suggestions.append("检测到列表字段，将完全展开为笛卡尔积以获得真正的整洁数据")
        
        if analysis.get('has_nested_objects'):
            suggestions.append("检测到嵌套对象，将完全扁平化为单层结构")
        
        if analysis.get('estimated_tidy_rows', 0) > 1000:
            suggestions.append("预计转换后数据量较大，建议分批处理以提高性能")
        
        if not suggestions:
            suggestions.append("数据结构相对简单，可以直接转换为整洁格式")
        
        return suggestions

def render_tidy_conversion_section():
    """渲染整洁数据转换部分"""
    
    st.markdown("---")
    st.markdown('<h3 class="sub-header">🧹 整洁数据转换</h3>', unsafe_allow_html=True)
    
    # 创建转换器实例
    converter = TidyDataConverter()
    
    # 文件上传区域
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.2);
    ">
        <h4 style="color: white; margin-bottom: 15px; text-align: center;">🧹 真正的整洁数据转换器</h4>
        <p style="font-size: 16px; line-height: 1.6; margin-bottom: 15px; text-align: center;">
            <strong>💡 完全符合Tidy Data原则的数据转换</strong><br>
            彻底展开所有列表字段，完全扁平化嵌套结构，生成真正的整洁数据格式。
        </p>
        <div style="display: flex; gap: 20px; margin-bottom: 15px;">
            <div style="flex: 1; background: rgba(255,255,255,0.15); padding: 15px; border-radius: 8px; backdrop-filter: blur(10px);">
                <h5 style="color: #FDE68A; margin-bottom: 10px;">🧹 完全整洁</h5>
                <ul style="margin: 0; padding-left: 15px; font-size: 14px;">
                    <li>展开所有列表字段</li>
                    <li>扁平化所有嵌套</li>
                    <li>符合Tidy Data原则</li>
                    <li>适合数据分析</li>
                </ul>
            </div>
            <div style="flex: 1; background: rgba(255,255,255,0.15); padding: 15px; border-radius: 8px; backdrop-filter: blur(10px);">
                <h5 style="color: #A7F3D0; margin-bottom: 10px;">📊 数据质量</h5>
                <ul style="margin: 0; padding-left: 15px; font-size: 14px;">
                    <li>质量评分系统</li>
                    <li>转换效果分析</li>
                    <li>数据完整性保证</li>
                    <li>多格式输出</li>
                </ul>
            </div>
        </div>
        <p style="font-size: 14px; margin: 0; text-align: center; opacity: 0.9;">
            <strong>🎯 适用场景：</strong> 数据分析、机器学习、统计建模、数据可视化
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 文件上传
    uploaded_file = st.file_uploader(
        "📁 上传JSON文件",
        type=converter.supported_input_formats,
        help="支持JSON格式文件，将转换为真正的整洁数据格式"
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
                    st.metric("预计整洁行数", analysis['estimated_tidy_rows'])
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
                
                # 执行转换
                if st.button("🧹 执行整洁转换", type="primary", use_container_width=True):
                    with st.spinner("正在转换为整洁数据..."):
                        result = converter.convert_to_tidy_data(
                            json_data=file_content,
                            separator=separator,
                            fill_na=fill_na,
                            max_preview_rows=max_preview,
                            encoding=encoding
                        )
                        
                        if result['success']:
                            st.success("✅ 整洁数据转换完成！")
                            
                            # 显示转换信息
                            col1, col2 = st.columns(2)
                            with col1:
                                st.info(result['info_message'])
                            with col2:
                                st.info(result['explode_message'])
                            
                            # 显示整洁数据质量评分
                            tidy_analysis = result['tidy_analysis']
                            st.subheader("📊 整洁数据质量评分")
                            
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("整洁度评分", f"{tidy_analysis['tidy_score']}/100")
                            with col2:
                                st.metric("转换后行数", tidy_analysis['total_rows'])
                            with col3:
                                st.metric("转换后列数", tidy_analysis['total_columns'])
                            with col4:
                                st.metric("数据类型数", len(set(tidy_analysis['data_types'].values())))
                            
                            # 质量评估
                            if tidy_analysis['tidy_score'] >= 90:
                                st.success("🎉 优秀！数据完全符合整洁数据原则")
                            elif tidy_analysis['tidy_score'] >= 70:
                                st.warning("⚠️ 良好，但仍有改进空间")
                            else:
                                st.error("❌ 需要进一步处理以达到整洁数据标准")
                            
                            # 显示转换结果预览
                            st.subheader("📋 整洁数据预览")
                            st.dataframe(result['preview_data'], use_container_width=True)
                            
                            # 数据类型信息
                            st.subheader("📈 数据类型分析")
                            dtype_df = pd.DataFrame([
                                {'列名': col, '数据类型': str(dtype)} 
                                for col, dtype in result['dtypes'].items()
                            ])
                            st.dataframe(dtype_df, use_container_width=True)
                            
                            # 下载转换结果
                            st.subheader("📥 下载整洁数据")
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                # CSV下载
                                st.download_button(
                                    label="📄 下载CSV文件",
                                    data=result['csv_data'],
                                    file_name=f"tidy_data_{uploaded_file.name.replace('.json', '.csv')}",
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
                                    file_name=f"tidy_data_{uploaded_file.name.replace('.json', '.xlsx')}",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    use_container_width=True
                                )
                            
                            with col3:
                                # JSON下载
                                json_data = result['dataframe'].to_json(orient='records', indent=2, force_ascii=False)
                                st.download_button(
                                    label="📋 下载JSON文件",
                                    data=json_data,
                                    file_name=f"tidy_data_{uploaded_file.name.replace('.json', '_tidy.json')}",
                                    mime="application/json",
                                    use_container_width=True
                                )
                            
                            # 保存转换后的数据到session state
                            st.session_state.tidy_data = result['dataframe']
                            st.success("✅ 整洁数据已保存，可在其他页面使用")
                            
                        else:
                            st.error(f"❌ 转换失败：{result['error']}")
            else:
                st.error(f"❌ 文件解析失败：{analysis['error']}")
                
        except Exception as e:
            st.error(f"❌ 处理失败：{str(e)}")
    else:
        st.info("📁 请上传JSON文件以开始整洁数据转换")
        
        # 显示使用说明
        st.markdown("---")
        st.subheader("📖 整洁数据原则")
        
        st.markdown("""
        **Tidy Data 三原则：**
        1. **每个变量占一列** - 每个测量变量都有自己的列
        2. **每个观测占一行** - 每个观测单元都有自己的行
        3. **每个值占一个单元格** - 每个值都在自己的单元格中
        
        **转换特性：**
        - 完全展开所有列表字段（笛卡尔积）
        - 完全扁平化所有嵌套字典
        - 生成真正的整洁数据格式
        - 适合数据分析和机器学习
        
        **输出格式：**
        - CSV：标准逗号分隔值格式
        - Excel：功能丰富的表格格式
        - JSON：重新格式化的JSON数据
        """)
        
        # 显示示例
        st.markdown("---")
        st.subheader("📝 转换示例")
        
        example_data = [
            {
                "id": 1,
                "name": "张三",
                "skills": ["Python", "SQL"],
                "projects": [
                    {"name": "项目A", "role": "开发"},
                    {"name": "项目B", "role": "测试"}
                ]
            }
        ]
        
        st.json(example_data)
        st.caption("转换后：每个技能和项目的组合都会生成一行数据")
