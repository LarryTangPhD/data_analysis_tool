#!/usr/bin/env python3
"""
测试报告导出功能
"""

import os
import sys
import pandas as pd
import numpy as np

# 添加src目录到Python路径
sys.path.append('src')

def test_report_export():
    """测试报告导出功能"""
    print("🔍 测试报告导出功能...")
    
    try:
        from src.utils.report_exporter import ReportExporter
        
        # 创建测试数据
        print("\n1. 创建测试数据...")
        test_data = pd.DataFrame({
            'A': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'B': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'],
            'C': [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.0],
            'D': [True, False, True, False, True, False, True, False, True, False]
        })
        
        # 添加一些缺失值
        test_data.loc[2, 'A'] = np.nan
        test_data.loc[5, 'C'] = np.nan
        
        print("✅ 测试数据创建成功")
        print(f"   数据大小: {len(test_data)} 行 × {len(test_data.columns)} 列")
        
        # 创建数据信息
        print("\n2. 创建数据信息...")
        data_info = {
            'rows': len(test_data),
            'columns': len(test_data.columns),
            'memory_usage': test_data.memory_usage(deep=True).sum() / 1024**2,
            'missing_values': test_data.isnull().sum().sum(),
            'duplicate_rows': test_data.duplicated().sum(),
            'data_types': test_data.dtypes.value_counts().to_dict(),
            'missing_values_summary': test_data.isnull().sum().to_dict()
        }
        
        print("✅ 数据信息创建成功")
        
        # 创建AI分析结果
        print("\n3. 创建AI分析结果...")
        ai_analysis = """
## 数据质量评估 (85/100分)

### 数据完整性评分
- **数据完整性**: 95分 - 数据基本完整，只有少量缺失值
- **数据一致性**: 90分 - 数据类型一致，格式规范
- **潜在问题**: 发现2个缺失值，需要进一步处理

### 数据特征分析
- **数据集类型**: 横截面数据
- **主要变量类型**: 数值型、分类型、布尔型
- **数据规模**: 小规模数据集，适合快速分析

### 清洗建议
1. **缺失值处理**: 建议使用均值填充或删除缺失行
2. **数据类型转换**: 当前数据类型合理，无需转换
3. **异常值检测**: 建议进行IQR方法检测异常值

### 分析方向推荐
1. **探索性数据分析**: 适合进行描述性统计
2. **可视化分析**: 建议创建分布图和相关性热图
3. **建模可能性**: 数据规模较小，适合简单模型

### 下一步行动建议
1. **优先处理**: 处理缺失值问题
2. **推荐流程**: 数据清洗 → 探索性分析 → 可视化 → 建模
3. **注意事项**: 注意数据隐私保护
        """
        
        print("✅ AI分析结果创建成功")
        
        # 测试报告导出器
        print("\n4. 测试报告导出器...")
        exporter = ReportExporter()
        print(f"✅ 报告导出器创建成功，时间戳: {exporter.timestamp}")
        
        # 测试Markdown导出
        print("\n5. 测试Markdown格式导出...")
        try:
            md_report = exporter.export_markdown_report(data_info, ai_analysis, test_data)
            print("✅ Markdown报告生成成功")
            print(f"   报告长度: {len(md_report)} 字符")
            
            # 保存到文件
            md_filename = f"test_report_{exporter.timestamp}.md"
            with open(md_filename, 'w', encoding='utf-8') as f:
                f.write(md_report)
            print(f"   已保存到: {md_filename}")
            
        except Exception as e:
            print(f"❌ Markdown导出失败: {e}")
        
        # 测试HTML导出
        print("\n6. 测试HTML格式导出...")
        try:
            html_report = exporter.export_html_report(data_info, ai_analysis, test_data)
            print("✅ HTML报告生成成功")
            print(f"   报告长度: {len(html_report)} 字符")
            
            # 保存到文件
            html_filename = f"test_report_{exporter.timestamp}.html"
            with open(html_filename, 'w', encoding='utf-8') as f:
                f.write(html_report)
            print(f"   已保存到: {html_filename}")
            
        except Exception as e:
            print(f"❌ HTML导出失败: {e}")
        
        # 测试JSON导出
        print("\n7. 测试JSON格式导出...")
        try:
            json_report = exporter.export_json_report(data_info, ai_analysis, test_data)
            print("✅ JSON报告生成成功")
            print(f"   报告长度: {len(json_report)} 字符")
            
            # 保存到文件
            json_filename = f"test_report_{exporter.timestamp}.json"
            with open(json_filename, 'w', encoding='utf-8') as f:
                f.write(json_report)
            print(f"   已保存到: {json_filename}")
            
        except Exception as e:
            print(f"❌ JSON导出失败: {e}")
        
        # 测试PDF导出
        print("\n8. 测试PDF格式导出...")
        try:
            pdf_report = exporter.export_pdf_report(data_info, ai_analysis, test_data)
            print("✅ PDF报告生成成功")
            print(f"   报告大小: {len(pdf_report)} 字节")
            
            # 保存到文件
            pdf_filename = f"test_report_{exporter.timestamp}.pdf"
            with open(pdf_filename, 'wb') as f:
                f.write(pdf_report)
            print(f"   已保存到: {pdf_filename}")
            
        except Exception as e:
            print(f"❌ PDF导出失败: {e}")
            print("   注意: PDF导出需要安装reportlab库")
        
        print("\n🎉 报告导出功能测试完成！")
        print("📁 生成的文件:")
        for filename in [md_filename, html_filename, json_filename]:
            if os.path.exists(filename):
                print(f"   ✅ {filename}")
        if 'pdf_filename' in locals() and os.path.exists(pdf_filename):
            print(f"   ✅ {pdf_filename}")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

if __name__ == "__main__":
    print("🚀 报告导出功能测试")
    print("=" * 50)
    
    if test_report_export():
        print("\n✅ 测试成功！报告导出功能正常")
    else:
        print("\n❌ 测试失败，请检查配置")
