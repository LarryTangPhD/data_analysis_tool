#!/usr/bin/env python3
"""
测试修复后的AI助手
"""

import os
import sys
import pandas as pd
import numpy as np

# 添加src目录到Python路径
sys.path.append('src')

def test_fixed_ai():
    """测试修复后的AI助手"""
    print("🔍 测试修复后的AI助手...")
    
    try:
        from src.utils.ai_assistant import get_ai_assistant
        
        # 获取AI助手实例
        print("\n1. 获取AI助手实例...")
        ai_assistant = get_ai_assistant()
        
        if ai_assistant is None:
            print("❌ AI助手实例获取失败")
            return False
        else:
            print("✅ AI助手实例获取成功")
        
        # 创建测试数据
        print("\n2. 创建测试数据...")
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
        
        # 测试数据分析功能
        print("\n3. 测试数据分析功能...")
        try:
            analysis_result = ai_assistant.analyze_uploaded_data(test_data, data_info)
            print("✅ 数据分析功能测试成功")
            print(f"分析结果长度: {len(analysis_result)} 字符")
        except Exception as e:
            print(f"❌ 数据分析功能测试失败: {e}")
            return False
        
        print("\n🎉 修复后的AI助手功能正常")
        return True
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

if __name__ == "__main__":
    print("🚀 修复后的AI助手功能测试")
    print("=" * 50)
    
    if test_fixed_ai():
        print("\n✅ 测试成功！AI助手可以正常使用")
    else:
        print("\n❌ 测试失败，请检查配置")
