# 📊 智能数据分析平台 / Intelligent Data Analysis Platform

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🇨🇳 中文介绍

### 项目概述
智能数据分析平台是一个基于Streamlit构建的专业级数据分析工具，集成了ydata-profiling、sweetviz等业界领先的数据分析组件。该平台提供从数据上传到报告生成的完整数据分析流程，支持多种数据格式和丰富的可视化功能。

### 🚀 核心功能
- **📁 多格式数据上传**: 支持CSV、Excel、JSON、Parquet等格式
- **🔍 自动化数据分析**: 集成YData Profiling、Sweetviz、Pandas Profiling
- **📈 交互式可视化**: 提供10种图表类型，支持3D可视化
- **📊 统计分析**: 描述性统计、假设检验、相关性分析
- **🧹 数据清洗**: 缺失值处理、异常值检测、数据类型转换
- **📋 报告生成**: 自动生成专业HTML分析报告

### 🛠️ 技术栈
- **前端框架**: Streamlit
- **数据处理**: Pandas, NumPy
- **可视化**: Plotly, Seaborn, Matplotlib
- **统计分析**: SciPy, Scikit-learn
- **专业分析**: YData Profiling, Sweetviz

---

## 🇺🇸 English Introduction

### Project Overview
The Intelligent Data Analysis Platform is a professional-grade data analysis tool built on Streamlit, integrating industry-leading data analysis components such as ydata-profiling and sweetviz. This platform provides a complete data analysis workflow from data upload to report generation, supporting multiple data formats and rich visualization capabilities.

### 🚀 Core Features
- **📁 Multi-format Data Upload**: Supports CSV, Excel, JSON, Parquet formats
- **🔍 Automated Data Analysis**: Integrates YData Profiling, Sweetviz, Pandas Profiling
- **📈 Interactive Visualization**: 10 chart types with 3D visualization support
- **📊 Statistical Analysis**: Descriptive statistics, hypothesis testing, correlation analysis
- **🧹 Data Cleaning**: Missing value handling, outlier detection, data type conversion
- **📋 Report Generation**: Automatic professional HTML analysis reports

### 🛠️ Tech Stack
- **Frontend Framework**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Seaborn, Matplotlib
- **Statistical Analysis**: SciPy, Scikit-learn
- **Professional Analysis**: YData Profiling, Sweetviz

---

## 🚀 快速开始 / Quick Start

### 安装依赖 / Install Dependencies

```bash
# 克隆项目 / Clone the repository
git clone https://github.com/LarryTangPhD/data_analysis_tool
cd intelligent-data-analysis-platform

# 安装依赖 / Install dependencies
pip install -r requirements.txt
```

### 运行应用 / Run Application

```bash
# 启动应用 / Start the application
streamlit run app.py
```

### 访问应用 / Access Application

打开浏览器访问 / Open browser and visit: http://localhost:8501

---

## 📋 功能详情 / Feature Details

### 📁 数据上传 / Data Upload
- 支持多种格式 / Multiple format support: CSV, Excel, JSON, Parquet
- 自动数据预览 / Automatic data preview
- 内存使用监控 / Memory usage monitoring
- 数据质量评分 / Data quality scoring

### 🔍 自动数据分析 / Automated Data Analysis
- **YData Profiling**: 最全面的自动化分析 / Most comprehensive automated analysis
- **Sweetviz**: 美观的数据概览 / Beautiful data overview
- **Pandas Profiling**: 经典分析报告 / Classic analysis reports
- **基础分析**: 快速数据概览 / Quick data overview

### 📈 可视化功能 / Visualization Features
- **基础图表**: 柱状图、折线图、散点图、饼图、直方图、箱线图、热力图、小提琴图
- **高级图表**: 3D散点图、雷达图
- **交互功能**: 缩放、平移、悬停、选择
- **完全定制**: 颜色、大小、标题等参数可调

### 📊 统计分析 / Statistical Analysis
- **描述性统计**: 均值、标准差、分位数、偏度、峰度
- **假设检验**: 正态性检验、t检验、方差分析、相关性检验、卡方检验
- **高级指标**: 变异系数、IQR、异常值检测

### 🧹 数据清洗 / Data Cleaning
- **缺失值处理**: 删除、均值填充、中位数填充、众数填充
- **异常值处理**: IQR方法、Z-score方法
- **数据类型转换**: 自动检测和智能转换
- **清洗对比**: 清洗前后数据对比

---

## 🎯 使用指南 / Usage Guide

### 1. 数据上传 / Data Upload
1. 点击"📁 数据上传"模块 / Click "📁 Data Upload" module
2. 选择数据文件 / Select your data file
3. 查看数据基本信息 / View basic data information

### 2. 选择分析工具 / Choose Analysis Tool
1. 点击"🔍 自动数据分析" / Click "🔍 Automated Data Analysis"
2. 选择分析组件 / Select analysis component
3. 配置分析参数 / Configure analysis parameters
4. 生成分析报告 / Generate analysis report

### 3. 创建可视化 / Create Visualizations
1. 点击"📈 高级可视化" / Click "📈 Advanced Visualization"
2. 选择图表类型 / Select chart type
3. 配置图表参数 / Configure chart parameters
4. 查看交互式图表 / View interactive charts

### 4. 统计分析 / Statistical Analysis
1. 点击"📊 统计分析" / Click "📊 Statistical Analysis"
2. 选择统计方法 / Select statistical method
3. 配置分析参数 / Configure analysis parameters
4. 查看统计结果 / View statistical results

---

## 📦 依赖组件 / Dependencies

### 核心组件 / Core Components
```
streamlit>=1.28.0      # Web应用框架 / Web application framework
pandas>=1.5.0          # 数据处理 / Data processing
numpy>=1.21.0          # 数值计算 / Numerical computing
plotly>=5.15.0         # 交互式可视化 / Interactive visualization
scipy>=1.9.0           # 统计分析 / Statistical analysis
```

### 专业分析组件 / Professional Analysis Components
```
ydata-profiling>=4.5.0     # 自动化数据分析 / Automated data analysis
sweetviz>=2.2.0            # 数据概览和比较 / Data overview and comparison
pandas-profiling>=3.6.0    # 经典数据分析 / Classic data analysis
```

### 可选组件 / Optional Components
```
seaborn>=0.12.0        # 统计可视化 / Statistical visualization
matplotlib>=3.6.0      # 基础绘图 / Basic plotting
openpyxl>=3.0.0        # Excel文件支持 / Excel file support
pyarrow>=10.0.0        # Parquet文件支持 / Parquet file support
scikit-learn>=1.3.0    # 机器学习 / Machine learning
```

---

## 🔧 配置选项 / Configuration Options

### YData Profiling配置 / YData Profiling Configuration
- **最小化模式**: 生成简洁报告 / Generate concise reports
- **探索性分析**: 包含详细数据探索 / Include detailed data exploration
- **深色主题**: 使用深色主题 / Use dark theme
- **样本大小**: 控制分析样本数量 / Control analysis sample size

### Sweetviz配置 / Sweetviz Configuration
- **目标变量**: 选择目标变量进行分析 / Select target variable for analysis
- **比较数据集**: 支持数据集比较 / Support dataset comparison

### 可视化配置 / Visualization Configuration
- **图表类型**: 8种基础图表 + 2种高级图表 / 8 basic charts + 2 advanced charts
- **参数定制**: 完全可定制的图表参数 / Fully customizable chart parameters
- **交互功能**: 支持缩放、平移、悬停等 / Support zoom, pan, hover, etc.

---

## 🚀 性能优化 / Performance Optimization

### 数据处理优化 / Data Processing Optimization
- 内存使用监控 / Memory usage monitoring
- 大数据集采样 / Large dataset sampling
- 异步处理 / Asynchronous processing
- 缓存机制 / Caching mechanism

### 可视化优化 / Visualization Optimization
- 交互式图表 / Interactive charts
- 自适应布局 / Adaptive layout
- 性能监控 / Performance monitoring
- 响应式设计 / Responsive design

---

## 🔒 安全特性 / Security Features

### 数据安全 / Data Security
- 本地数据处理 / Local data processing
- 无数据上传到外部服务器 / No data upload to external servers
- 会话状态管理 / Session state management
- 数据验证 / Data validation

### 错误处理 / Error Handling
- 完善的异常处理 / Comprehensive exception handling
- 用户友好的错误提示 / User-friendly error messages
- 数据格式验证 / Data format validation
- 系统状态监控 / System status monitoring

---

## 📞 技术支持 / Technical Support

### 常见问题 / Common Issues
1. 检查依赖是否正确安装 / Check if dependencies are correctly installed
2. 确认数据格式是否支持 / Confirm if data format is supported
3. 查看错误日志 / Check error logs
4. 联系技术支持 / Contact technical support

### 获取帮助 / Get Help
- 📧 Email: your-email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/intelligent-data-analysis-platform/issues)
- 📖 Documentation: [项目文档](https://github.com/yourusername/intelligent-data-analysis-platform/wiki)

---

## 📄 许可证 / License

本项目采用MIT许可证 / This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 贡献 / Contributing

我们欢迎所有形式的贡献！/ We welcome all forms of contributions!

### 如何贡献 / How to Contribute
1. Fork 项目 / Fork the project
2. 创建功能分支 / Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. 提交更改 / Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 / Push to the branch (`git push origin feature/AmazingFeature`)
5. 打开Pull Request / Open a Pull Request

### 贡献指南 / Contributing Guidelines
- 请遵循代码规范 / Please follow code standards
- 添加适当的测试 / Add appropriate tests
- 更新文档 / Update documentation
- 确保所有测试通过 / Ensure all tests pass

---

## 📈 项目统计 / Project Statistics

![GitHub stars](https://img.shields.io/github/stars/yourusername/intelligent-data-analysis-platform)
![GitHub forks](https://img.shields.io/github/forks/yourusername/intelligent-data-analysis-platform)
![GitHub issues](https://img.shields.io/github/issues/yourusername/intelligent-data-analysis-platform)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/intelligent-data-analysis-platform)

---

## 🏆 致谢 / Acknowledgments

感谢以下开源项目的支持 / Thanks to the following open source projects:

- [Streamlit](https://streamlit.io/) - Web应用框架 / Web application framework
- [YData Profiling](https://github.com/ydataai/ydata-profiling) - 自动化数据分析 / Automated data analysis
- [Sweetviz](https://github.com/fbdesignpro/sweetviz) - 数据概览和比较 / Data overview and comparison
- [Plotly](https://plotly.com/) - 交互式可视化 / Interactive visualization
- [Pandas](https://pandas.pydata.org/) - 数据处理 / Data processing

---

**版本 / Version**: 3.0  
**最后更新 / Last Updated**: 2025年8月 / 2025.8  
**作者 / Author**: Larry Tang / Intelligent Data Analysis Team
**联系方式 / Contact Details**: tjn.chaos@qq.com

---

<div align="center">

⭐ 如果这个项目对您有帮助，请给我们一个星标！/ If this project helps you, please give us a star! ⭐

</div>
