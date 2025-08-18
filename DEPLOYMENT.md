# 🚀 部署说明 / Deployment Guide

## ⚠️ 重要兼容性说明 / Important Compatibility Notice

### Python版本兼容性 / Python Version Compatibility

本项目已针对 **Python 3.13** 进行了优化，但部分高级分析工具存在兼容性问题：

#### 不可用的组件 / Unavailable Components
- **ydata-profiling**: 依赖的htmlmin包在Python 3.13中缺少cgi模块
- **sweetviz**: 存在Python 3.13兼容性问题
- **pandas-profiling**: 存在Python 3.13兼容性问题
- **streamlit-pandas-profiling**: 依赖pandas-profiling

#### 解决方案 / Solutions

1. **使用Python 3.11或3.12** (推荐)
   ```bash
   # 创建Python 3.11环境
   conda create -n data_analysis python=3.11
   conda activate data_analysis
   pip install -r requirements.txt
   ```

2. **使用当前版本** (已优化)
   - 移除了不兼容的依赖
   - 保留了核心功能
   - 提供了替代分析方案

## 🛠️ 部署步骤 / Deployment Steps

### 1. 本地部署 / Local Deployment

```bash
# 克隆项目
git clone https://github.com/LarryTangPhD/data_analysis_tool
cd data_analysis_tool

# 安装依赖
pip install -r requirements.txt

# 运行应用
streamlit run app.py
```

### 2. Streamlit Cloud部署 / Streamlit Cloud Deployment

1. 将代码推送到GitHub
2. 在Streamlit Cloud中连接仓库
3. 设置主文件为 `app.py`
4. 部署

### 3. 其他平台部署 / Other Platform Deployment

#### Heroku
```bash
# 创建Procfile
echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# 创建runtime.txt
echo "python-3.11.0" > runtime.txt
```

#### Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🔧 故障排除 / Troubleshooting

### 常见问题 / Common Issues

1. **依赖安装失败**
   ```bash
   # 升级pip
   pip install --upgrade pip
   
   # 清理缓存
   pip cache purge
   
   # 重新安装
   pip install -r requirements.txt
   ```

2. **内存不足**
   - 减少数据文件大小
   - 使用数据采样
   - 增加服务器内存

3. **端口冲突**
   ```bash
   # 指定端口
   streamlit run app.py --server.port=8502
   ```

### 性能优化 / Performance Optimization

1. **数据预处理**
   - 清理数据格式
   - 移除不必要的列
   - 压缩数据文件

2. **缓存设置**
   - 使用Streamlit缓存装饰器
   - 避免重复计算

3. **资源限制**
   - 限制上传文件大小
   - 设置处理超时

## 📊 功能状态 / Feature Status

| 功能 / Feature | 状态 / Status | 说明 / Notes |
|---------------|---------------|-------------|
| 数据上传 | ✅ 可用 | 支持多种格式 |
| 基础分析 | ✅ 可用 | 描述性统计 |
| 可视化 | ✅ 可用 | 10种图表类型 |
| 统计分析 | ✅ 可用 | 假设检验等 |
| 数据清洗 | ✅ 可用 | 缺失值处理 |
| YData Profiling | ❌ 不可用 | Python 3.13兼容性问题 |
| Sweetviz | ❌ 不可用 | Python 3.13兼容性问题 |
| Pandas Profiling | ❌ 不可用 | Python 3.13兼容性问题 |

## 🔄 更新计划 / Update Plan

### 短期计划 / Short-term Plans
- [ ] 寻找Python 3.13兼容的替代方案
- [ ] 优化现有功能性能
- [ ] 添加更多可视化选项

### 长期计划 / Long-term Plans
- [ ] 支持更多数据格式
- [ ] 添加机器学习功能
- [ ] 实现云端部署优化

## 📞 技术支持 / Technical Support

如果遇到部署问题，请：

1. 检查Python版本 (推荐3.11)
2. 查看错误日志
3. 确认依赖安装
4. 联系技术支持: tjn.chaos@qq.com

---

**最后更新**: 2025年8月 / Last Updated: August 2025
