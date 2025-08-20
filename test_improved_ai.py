#!/usr/bin/env python3
"""
测试改进的AI助手功能
"""

import os
import sys
import pandas as pd
import numpy as np

# 添加src目录到Python路径
sys.path.append('src')

def test_improved_ai():
    """测试改进的AI助手"""
    print("🔍 测试改进的AI助手...")
    
    try:
        from src.utils.ai_assistant_improved import get_ai_assistant, test_ai_assistant_connection
        
        # 1. 测试连接
        print("\n1. 测试AI助手连接...")
        connection_result = test_ai_assistant_connection()
        
        if connection_result["success"]:
            print("✅ AI助手连接测试成功")
        else:
            print(f"❌ AI助手连接测试失败: {connection_result['error']}")
            return False
        
        # 2. 获取AI助手实例
        print("\n2. 获取AI助手实例...")
        ai_assistant = get_ai_assistant()
        
        if ai_assistant is None:
            print("❌ AI助手实例获取失败")
            return False
        else:
            print("✅ AI助手实例获取成功")
        
        # 3. 创建测试数据
        print("\n3. 创建测试数据...")
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
        
        print("✅ 测试数据创建成功")
        
        # 4. 测试数据分析功能
        print("\n4. 测试数据分析功能...")
        try:
            analysis_result = ai_assistant.analyze_uploaded_data(test_data, data_info)
            print("✅ 数据分析功能测试成功")
            print(f"分析结果长度: {len(analysis_result)} 字符")
        except Exception as e:
            print(f"❌ 数据分析功能测试失败: {e}")
            return False
        
        # 5. 测试问答功能
        print("\n5. 测试问答功能...")
        try:
            question = "这个数据集有什么特点？"
            data_context = f"数据集包含{len(test_data)}行{len(test_data.columns)}列"
            answer = ai_assistant.answer_data_question(question, data_context, "测试")
            print("✅ 问答功能测试成功")
            print(f"回答长度: {len(answer)} 字符")
        except Exception as e:
            print(f"❌ 问答功能测试失败: {e}")
            return False
        
        print("\n🎉 所有测试通过！改进的AI助手功能正常")
        return True
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

if __name__ == "__main__":
    print("🚀 改进的AI助手功能测试")
    print("=" * 50)
    
    if test_improved_ai():
        print("\n✅ 测试成功！AI助手可以正常使用")
    else:
        print("\n❌ 测试失败，请检查配置")
