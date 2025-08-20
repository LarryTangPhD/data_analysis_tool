#!/usr/bin/env python3
"""
AI助手诊断脚本
用于诊断Streamlit环境中AI助手的问题
"""

import os
import sys
import streamlit as st
import pandas as pd
import numpy as np

# 添加src目录到Python路径
sys.path.append('src')

def debug_ai_assistant():
    """诊断AI助手问题"""
    st.title("🔍 AI助手诊断工具")
    
    st.write("### 1. 环境变量检查")
    
    # 检查环境变量
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if api_key:
        st.success(f"✅ DASHSCOPE_API_KEY 已设置: {api_key[:10]}...")
    else:
        st.error("❌ DASHSCOPE_API_KEY 未设置")
        st.info("请设置环境变量：")
        st.code("""
# Windows
set DASHSCOPE_API_KEY=your_api_key_here

# Linux/Mac
export DASHSCOPE_API_KEY=your_api_key_here
        """)
        return
    
    st.write("### 2. 模块导入检查")
    
    try:
        from src.utils.ai_assistant import get_ai_assistant, DataAnalysisAI
        st.success("✅ AI助手模块导入成功")
    except ImportError as e:
        st.error(f"❌ AI助手模块导入失败: {e}")
        return
    except Exception as e:
        st.error(f"❌ 其他导入错误: {e}")
        return
    
    st.write("### 3. AI助手实例创建检查")
    
    try:
        ai_assistant = get_ai_assistant()
        if ai_assistant is None:
            st.error("❌ AI助手实例创建失败，返回None")
            st.info("可能的原因：")
            st.write("- 环境变量未正确设置")
            st.write("- API密钥无效")
            st.write("- 网络连接问题")
            return
        else:
            st.success("✅ AI助手实例创建成功")
    except Exception as e:
        st.error(f"❌ AI助手实例创建失败: {e}")
        return
    
    st.write("### 4. 测试数据创建")
    
    try:
        # 创建测试数据
        test_data = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': ['a', 'b', 'c', 'd', 'e'],
            'C': [1.1, 2.2, 3.3, 4.4, 5.5]
        })
        
        data_info = {
            'rows': len(test_data),
            'columns': len(test_data.columns),
            'memory_usage': test_data.memory_usage(deep=True).sum() / 1024**2,
            'missing_values': test_data.isnull().sum().sum(),
            'duplicate_rows': test_data.duplicated().sum()
        }
        
        st.success("✅ 测试数据创建成功")
        st.write(f"数据大小: {data_info['rows']} 行 × {data_info['columns']} 列")
        
    except Exception as e:
        st.error(f"❌ 测试数据创建失败: {e}")
        return
    
    st.write("### 5. AI功能测试")
    
    # 添加测试按钮
    if st.button("🤖 测试AI分析功能"):
        with st.spinner("正在测试AI功能..."):
            try:
                # 测试AI分析功能
                analysis_result = ai_assistant.analyze_uploaded_data(test_data, data_info)
                
                st.success("✅ AI分析功能测试成功！")
                st.write("### AI分析结果预览:")
                st.markdown(analysis_result[:500] + "..." if len(analysis_result) > 500 else analysis_result)
                
            except Exception as e:
                st.error(f"❌ AI分析功能测试失败: {e}")
                st.info("可能的原因：")
                st.write("- API密钥无效或过期")
                st.write("- 网络连接问题")
                st.write("- API服务不可用")
                st.write("- 请求频率限制")
    
    # 添加问答测试
    st.write("### 6. AI问答功能测试")
    
    test_question = st.text_input(
        "输入测试问题：",
        value="这个数据集有什么特点？",
        key="test_question"
    )
    
    if st.button("🤖 测试AI问答功能") and test_question.strip():
        with st.spinner("正在测试AI问答功能..."):
            try:
                data_context = f"数据集包含{len(test_data)}行{len(test_data.columns)}列，数据类型包括{', '.join(test_data.dtypes.value_counts().index.astype(str))}"
                answer = ai_assistant.answer_data_question(test_question, data_context, "诊断测试")
                
                st.success("✅ AI问答功能测试成功！")
                st.write("### AI回答:")
                st.markdown(answer)
                
            except Exception as e:
                st.error(f"❌ AI问答功能测试失败: {e}")
    
    st.write("### 7. 诊断总结")
    
    st.success("🎉 诊断完成！")
    st.write("如果所有测试都通过，说明AI助手功能正常。")
    st.write("如果出现错误，请检查：")
    st.write("1. 环境变量设置")
    st.write("2. 网络连接")
    st.write("3. API密钥有效性")
    st.write("4. 依赖包安装")

if __name__ == "__main__":
    debug_ai_assistant()
