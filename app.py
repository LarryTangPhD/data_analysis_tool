import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import warnings
import io
warnings.filterwarnings('ignore')

# 性能优化：添加缓存装饰器
@st.cache_data
def load_data(uploaded_file):
    """缓存数据加载函数"""
    if uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(('.xlsx', '.xls')):
        return pd.read_excel(uploaded_file)
    elif uploaded_file.name.endswith('.json'):
        return pd.read_json(uploaded_file)
    elif uploaded_file.name.endswith('.parquet'):
        return pd.read_parquet(uploaded_file)

@st.cache_data
def calculate_correlation_matrix(data):
    """缓存相关性矩阵计算"""
    return data.corr()

@st.cache_data
def calculate_data_quality_score(data):
    """缓存数据质量评分计算"""
    score = 100
    total_rows, total_cols = len(data), len(data.columns)
    
    # 缺失值扣分
    missing_ratio = data.isnull().sum().sum() / (total_rows * total_cols)
    score -= missing_ratio * 30
    
    # 重复值扣分
    duplicate_ratio = data.duplicated().sum() / total_rows
    score -= duplicate_ratio * 20
    
    # 数据类型合理性检查
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns
    
    # 如果数值型列过多，可能存在问题
    if len(numeric_cols) / total_cols > 0.8:
        score -= 10
    
    # 检查异常值
    outlier_score = 0
    for col in numeric_cols:
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = data[(data[col] < Q1 - 1.5 * IQR) | (data[col] > Q3 + 1.5 * IQR)]
        outlier_ratio = len(outliers) / total_rows
        outlier_score += outlier_ratio
    
    score -= min(outlier_score * 15, 20)
    
    return max(score, 0)

# 由于Python 3.13兼容性问题，暂时禁用这些包
YDATA_AVAILABLE = False
SWEETVIZ_AVAILABLE = False
PANDAS_PROFILING_AVAILABLE = False
ST_PROFILE_REPORT_AVAILABLE = False

# 设置页面配置
st.set_page_config(
    page_title="智能数据分析平台",
    page_icon="📊",
    layout="wide",  # 可选: "centered" 或 "wide"
    initial_sidebar_state="expanded",  # 可选: "expanded" 或 "collapsed"
    menu_items={
        'Get Help': 'https://docs.streamlit.io/',
        'Report a bug': None,
        'About': '# 智能数据分析平台\n基于Streamlit构建的数据分析应用'
    }
)

# 自定义CSS样式
st.markdown("""
<style>
    /* 自定义侧边栏宽度 */
    [data-testid="stSidebar"] {
        width: 200px !important;
    }
    
    /* 调整主内容区域宽度 */
    .main .block-container {
        max-width: 1200px;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 主标题
st.markdown('<h1 class="main-header">📊 智能数据分析平台</h1>', unsafe_allow_html=True)

# 顶部横向导航
NAV_PAGES = ["🏠 首页", "📁 数据上传", "🧹 数据清洗", "🔍 自动数据分析", "📈 高级可视化", "📊 统计分析", "🤖 机器学习", "📋 报告生成"]

# 初始化页面状态
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 首页"

# 创建横向导航
selected_page = st.radio(
    "选择功能模块",
    NAV_PAGES,
    horizontal=True,
    key="page_navigation"
)

# 更新当前页面
if selected_page != st.session_state.current_page:
    st.session_state.current_page = selected_page
    st.rerun()

page = st.session_state.current_page
st.markdown("---")

# 侧边栏
with st.sidebar:
    st.markdown("### 📋 使用说明")
    st.markdown("""
    1. 首先上传您的数据文件
    2. 清洗和预处理数据
    3. 使用自动数据分析工具快速了解数据
    4. 创建高级可视化图表
    5. 进行专业统计分析
    6. 应用机器学习算法
    7. 生成完整分析报告
    """)
    
    # 显示可用组件状态
    st.markdown("---")
    st.markdown("### 🔧 组件状态")
    if YDATA_AVAILABLE:
        st.success("✅ ydata-profiling")
    else:
        st.error("❌ ydata-profiling")
    
    if SWEETVIZ_AVAILABLE:
        st.success("✅ sweetviz")
    else:
        st.error("❌ sweetviz")
    
    if ST_PROFILE_REPORT_AVAILABLE:
        st.success("✅ streamlit-pandas-profiling")
    else:
        st.error("❌ streamlit-pandas-profiling")
    
    # 检查scikit-learn
    try:
        import sklearn
        st.success("✅ scikit-learn")
    except ImportError:
        st.error("❌ scikit-learn")
    
    # 作者信息
    st.markdown("---")
    st.markdown("### 👨‍💻 开发团队")
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 8px;
        color: white;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    ">
        <p style="margin: 0; font-size: 14px; font-weight: bold;">📧 技术负责人</p>
        <p style="margin: 5px 0 0 0; font-size: 13px;">LarryTang</p>
        <p style="margin: 5px 0 0 0; font-size: 12px; opacity: 0.9;">tjn.chaos@qq.com</p>
    </div>
    """, unsafe_allow_html=True)

# 初始化session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'data_cleaned' not in st.session_state:
    st.session_state.data_cleaned = None
if 'profile_report' not in st.session_state:
    st.session_state.profile_report = None

# 首页
if page == "🏠 首页":
    st.markdown('<h2 class="sub-header">欢迎使用智能数据分析平台</h2>', unsafe_allow_html=True)
    

    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📁 数据上传</h3>
            <p>支持CSV、Excel、JSON等多种格式</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🧹 数据清洗</h3>
            <p>智能处理缺失值、异常值和重复值</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🔍 自动分析</h3>
            <p>使用ydata-profiling等专业工具</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>🤖 机器学习</h3>
            <p>分类、回归、聚类等算法</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 第二行功能卡片
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📈 高级可视化</h3>
            <p>创建交互式图表和仪表板</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 统计分析</h3>
            <p>描述性统计和假设检验</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>📋 报告生成</h3>
            <p>自动生成专业分析报告</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>⚡ 性能优化</h3>
            <p>缓存机制和智能处理</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h4>🚀 平台特色功能</h4>
        <ul>
            <li><strong>专业数据分析：</strong>集成ydata-profiling、sweetviz等成熟组件</li>
            <li><strong>智能数据清洗：</strong>多维度数据质量评估和清洗策略</li>
            <li><strong>机器学习集成：</strong>分类、回归、聚类等算法支持</li>
            <li><strong>交互式可视化：</strong>支持多种图表类型和自定义选项</li>
            <li><strong>统计分析：</strong>提供描述性统计和假设检验</li>
            <li><strong>性能优化：</strong>缓存机制和智能处理提升效率</li>
            <li><strong>自动报告生成：</strong>一键生成完整的数据分析报告</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # 组件兼容性说明
    st.markdown("""
    <div class="warning-box">
        <h4>⚠️ 兼容性说明</h4>
        <p>由于Python 3.13兼容性问题，部分高级分析功能暂时不可用：</p>
        <ul>
            <li>YData Profiling - 自动化数据分析</li>
            <li>Sweetviz - 数据概览和比较</li>
            <li>Pandas Profiling - 经典分析报告</li>
        </ul>
        <p>💡 建议使用'基础分析'功能进行数据分析。</p>
    </div>
    """, unsafe_allow_html=True)

# 数据上传页面
elif page == "📁 数据上传":
    st.markdown('<h2 class="sub-header">📁 数据上传</h2>', unsafe_allow_html=True)
    
    # 添加数据上传说明
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
    
    uploaded_file = st.file_uploader(
        "选择数据文件",
        type=['csv', 'xlsx', 'xls', 'json', 'parquet'],
        help="支持CSV、Excel、JSON、Parquet格式"
    )
    
    if uploaded_file is not None:
        try:
            # 使用缓存函数读取数据
            data = load_data(uploaded_file)
            st.session_state.data = data
            
            st.success(f"✅ 数据上传成功！共 {len(data)} 行，{len(data.columns)} 列")
            
            # 显示数据基本信息
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("行数", len(data))
            with col2:
                st.metric("列数", len(data.columns))
            with col3:
                st.metric("内存使用", f"{data.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
            with col4:
                missing_values = data.isnull().sum().sum()
                st.metric("缺失值", missing_values)
            
            # 数据预览
            st.subheader("📋 数据预览")
            st.dataframe(data.head(10), use_container_width=True)
            
            # 基础数据分析
            st.subheader("📊 基础数据分析")
            
            # 数据概览
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write("**描述性统计：**")
                st.dataframe(data.describe(), use_container_width=True)
            
            with col2:
                st.write("**数据类型信息：**")
                dtype_info = pd.DataFrame({
                    '数据类型': [str(dtype) for dtype in data.dtypes],
                    '非空值数量': data.count(),
                    '空值数量': data.isnull().sum()
                })
                st.dataframe(dtype_info)
            
            # 缺失值分析
            st.subheader("🔍 缺失值分析")
            missing_data = data.isnull().sum()
            missing_percent = (missing_data / len(data)) * 100
            
            fig_missing = go.Figure()
            fig_missing.add_trace(go.Bar(
                x=data.columns,
                y=missing_data,
                name='缺失值数量',
                marker_color='#ff7f0e'
            ))
            fig_missing.add_trace(go.Scatter(
                x=data.columns,
                y=missing_percent,
                name='缺失值百分比',
                yaxis='y2'
            ))
            
            fig_missing.update_layout(
                title='缺失值分析',
                xaxis_title='列名',
                yaxis=dict(title='缺失值数量'),
                yaxis2=dict(title='缺失值百分比 (%)', overlaying='y', side='right'),
                height=400
            )
            st.plotly_chart(fig_missing, use_container_width=True)
            
            # 数据类型分布
            st.subheader("📈 数据类型分布")
            dtype_counts = data.dtypes.value_counts()
            # 将数据类型转换为字符串并创建简单的饼图数据
            dtype_labels = [str(dtype) for dtype in dtype_counts.index]
            dtype_values = dtype_counts.values.tolist()
            
            fig_dtype = go.Figure(data=[go.Pie(
                labels=dtype_labels,
                values=dtype_values,
                hole=0.3
            )])
            fig_dtype.update_layout(
                title='数据类型分布',
                showlegend=True
            )
            st.plotly_chart(fig_dtype, use_container_width=True)
            
            # 高级数据探索
            st.subheader("🔬 高级数据探索")
            
            # 数据分布分析
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                explore_col = st.selectbox("选择要深入分析的数值列", numeric_cols)
                
                if explore_col:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # 分布图
                        fig_dist = px.histogram(data, x=explore_col, nbins=30, 
                                              title=f"{explore_col} 分布直方图")
                        st.plotly_chart(fig_dist, use_container_width=True)
                    
                    with col2:
                        # 箱线图
                        fig_box = px.box(data, y=explore_col, title=f"{explore_col} 箱线图")
                        st.plotly_chart(fig_box, use_container_width=True)
                    
                    # 统计摘要
                    st.write(f"**{explore_col} 详细统计：**")
                    stats_summary = {
                        '均值': data[explore_col].mean(),
                        '中位数': data[explore_col].median(),
                        '标准差': data[explore_col].std(),
                        '偏度': data[explore_col].skew(),
                        '峰度': data[explore_col].kurtosis(),
                        '最小值': data[explore_col].min(),
                        '最大值': data[explore_col].max(),
                        'Q1': data[explore_col].quantile(0.25),
                        'Q3': data[explore_col].quantile(0.75)
                    }
                    
                    stats_df = pd.DataFrame(list(stats_summary.items()), columns=['统计量', '值'])
                    st.dataframe(stats_df, use_container_width=True)
                    
                    # 异常值检测
                    Q1 = data[explore_col].quantile(0.25)
                    Q3 = data[explore_col].quantile(0.75)
                    IQR = Q3 - Q1
                    outliers = data[(data[explore_col] < Q1 - 1.5 * IQR) | (data[explore_col] > Q3 + 1.5 * IQR)]
                    
                    st.write(f"**异常值检测 (IQR方法)：**")
                    st.write(f"异常值数量：{len(outliers)} ({len(outliers)/len(data)*100:.2f}%)")
                    if len(outliers) > 0:
                        st.dataframe(outliers[[explore_col]].head(10), use_container_width=True)
            
            # 数值型数据相关性分析
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 1:
                st.subheader("🔗 相关性分析")
                corr_matrix = calculate_correlation_matrix(data[numeric_cols])
                
                fig_corr = px.imshow(
                    corr_matrix,
                    title='相关性热力图',
                    color_continuous_scale='RdBu',
                    aspect='auto'
                )
                st.plotly_chart(fig_corr, use_container_width=True)
            
            # 数据质量评估
            st.subheader("🔍 数据质量评估")
            
            # 使用缓存函数计算数据质量分数
            quality_score = calculate_data_quality_score(data)
            
            # 显示质量评分
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
            
            # 数据质量建议
            st.write("**数据质量建议：**")
            if quality_score < 80:
                if data.isnull().sum().sum() > 0:
                    st.info("🔧 建议处理缺失值以提高数据质量")
                if data.duplicated().sum() > 0:
                    st.info("🔧 建议删除重复值以提高数据质量")
                if len(data.select_dtypes(include=[np.number]).columns) / len(data.columns) > 0.8:
                    st.info("🔧 建议检查数据类型，可能存在分类变量被误识别为数值型")
            else:
                st.success("✅ 数据质量良好，可以直接进行分析")
            
        except Exception as e:
            st.error(f"❌ 数据读取失败：{str(e)}")

# 数据清洗页面
elif page == "🧹 数据清洗":
    st.markdown('<h2 class="sub-header">🧹 数据清洗</h2>', unsafe_allow_html=True)
    
    # 添加整洁数据说明 - 始终显示
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    ">
        <h3 style="color: white; margin-bottom: 15px;">📊 整洁数据（Tidy Data）指南</h3>
        <p style="font-size: 16px; line-height: 1.6; margin-bottom: 15px;">
            <strong>💡 什么是整洁数据？</strong><br>
            整洁数据是一种标准化的数据格式，遵循"每行一个观测值，每列一个变量"的原则，让数据分析变得更加高效和准确。
        </p>
        <div style="display: flex; gap: 20px; margin-bottom: 15px;">
            <div style="flex: 1; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                <h4 style="color: #ff6b6b; margin-bottom: 10px;">❌ 避免这样的数据格式</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 14px;">
                    <li>变量信息混合在列名中</li>
                    <li>相同类型的变量分散在不同列</li>
                    <li>一个单元格包含多个值</li>
                    <li>列名不清晰或不一致</li>
                </ul>
            </div>
            <div style="flex: 1; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                <h4 style="color: #51cf66; margin-bottom: 10px;">✅ 推荐这样的数据格式</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 14px;">
                    <li>每行代表一个观测值</li>
                    <li>每列代表一个变量</li>
                    <li>每个单元格只包含一个值</li>
                    <li>变量名清晰明确</li>
                </ul>
            </div>
        </div>
        <p style="font-size: 14px; margin: 0; opacity: 0.9;">
            <strong>🎯 为什么重要？</strong> 整洁数据让统计分析、可视化和机器学习变得更加简单高效！
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 添加数据格式示例 - 始终显示
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        ">
            <h4 style="color: #856404; margin-bottom: 10px;">📋 数据格式示例</h4>
            <p style="color: #856404; font-size: 14px; margin-bottom: 10px;">
                <strong>不整洁数据（宽格式）：</strong>
            </p>
            <div style="background: white; padding: 10px; border-radius: 3px; font-family: monospace; font-size: 12px;">
                | 年份 | 北京_GDP | 上海_GDP | 广州_GDP |<br>
                |------|----------|----------|----------|<br>
                | 2020 | 36102    | 38701    | 25019    |<br>
                | 2021 | 40269    | 43215    | 28232    |
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background: #d4edda;
            border-left: 4px solid #28a745;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        ">
            <h4 style="color: #155724; margin-bottom: 10px;">📋 数据格式示例</h4>
            <p style="color: #155724; font-size: 14px; margin-bottom: 10px;">
                <strong>整洁数据（长格式）：</strong>
            </p>
            <div style="background: white; padding: 10px; border-radius: 3px; font-family: monospace; font-size: 12px;">
                | 年份 | 城市 | GDP |<br>
                |------|------|-----|<br>
                | 2020 | 北京 | 36102 |<br>
                | 2020 | 上海 | 38701 |<br>
                | 2020 | 广州 | 25019 |<br>
                | 2021 | 北京 | 40269 |<br>
                | 2021 | 上海 | 43215 |<br>
                | 2021 | 广州 | 28232 |
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.data is None:
        st.warning("⚠️ 请先上传数据文件")
    else:
        data = st.session_state.data
        
        # 数据概览
        st.subheader("📋 数据概览")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("总行数", len(data))
        with col2:
            st.metric("总列数", len(data.columns))
        with col3:
            st.metric("缺失值总数", data.isnull().sum().sum())
        with col4:
            st.metric("重复行数", data.duplicated().sum())
        
        # 数据质量评分
        quality_score = calculate_data_quality_score(data)
        st.write(f"**数据质量评分：** {quality_score:.1f}/100")
        
        # 数据清洗选项
        st.subheader("🔧 清洗选项")
        
        # 创建选项卡
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["缺失值处理", "异常值处理", "重复值处理", "数据类型转换", "高级清洗"])
        
        with tab1:
            st.write("**缺失值处理：**")
            missing_strategy = st.selectbox(
                "选择缺失值处理策略",
                ["不处理", "删除行", "删除列", "均值填充", "中位数填充", "众数填充", "前向填充", "后向填充", "插值填充"],
                key="missing_strategy"
            )
            
            # 显示缺失值详情
            missing_data = data.isnull().sum()
            missing_percent = (missing_data / len(data)) * 100
            missing_df = pd.DataFrame({
                '列名': missing_data.index,
                '缺失值数量': missing_data.values,
                '缺失值百分比': missing_percent.values
            }).sort_values('缺失值数量', ascending=False)
            
            st.write("**缺失值详情：**")
            st.dataframe(missing_df[missing_df['缺失值数量'] > 0], use_container_width=True)
        
        with tab2:
            st.write("**异常值处理：**")
            outlier_strategy = st.selectbox(
                "选择异常值处理策略",
                ["不处理", "IQR方法删除", "IQR方法截断", "Z-score方法删除", "Z-score方法截断"],
                key="outlier_strategy"
            )
            
            if outlier_strategy != "不处理":
                numeric_cols = data.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    outlier_cols = st.multiselect("选择要处理异常值的列", numeric_cols, key="outlier_cols")
                    
                    if outlier_cols:
                        # 显示异常值统计
                        outlier_stats = []
                        for col in outlier_cols:
                            Q1 = data[col].quantile(0.25)
                            Q3 = data[col].quantile(0.75)
                            IQR = Q3 - Q1
                            lower_bound = Q1 - 1.5 * IQR
                            upper_bound = Q3 + 1.5 * IQR
                            outliers = data[(data[col] < lower_bound) | (data[col] > upper_bound)]
                            
                            outlier_stats.append({
                                '列名': col,
                                '异常值数量': len(outliers),
                                '异常值百分比': len(outliers)/len(data)*100,
                                '下界': lower_bound,
                                '上界': upper_bound
                            })
                        
                        outlier_df = pd.DataFrame(outlier_stats)
                        st.write("**异常值统计：**")
                        st.dataframe(outlier_df, use_container_width=True)
        
        with tab3:
            st.write("**重复值处理：**")
            duplicate_strategy = st.selectbox(
                "选择重复值处理策略",
                ["不处理", "删除重复行", "保留第一次出现", "保留最后一次出现"],
                key="duplicate_strategy"
            )
            
            # 显示重复值详情
            duplicate_count = data.duplicated().sum()
            st.write(f"**重复行数量：** {duplicate_count} ({duplicate_count/len(data)*100:.2f}%)")
            
            if duplicate_count > 0:
                st.write("**重复行示例：**")
                st.dataframe(data[data.duplicated()].head(5), use_container_width=True)
        
        with tab4:
            st.write("**数据类型转换：**")
            convert_types = st.checkbox("启用数据类型转换", key="convert_types")
            
            if convert_types:
                # 显示当前数据类型
                dtype_info = pd.DataFrame({
                    '列名': data.columns,
                    '当前类型': data.dtypes.astype(str),
                    '唯一值数量': [data[col].nunique() for col in data.columns],
                    '建议类型': ['object' if data[col].nunique()/len(data) < 0.1 else str(data[col].dtype) for col in data.columns]
                })
                st.write("**数据类型分析：**")
                st.dataframe(dtype_info, use_container_width=True)
        
        with tab5:
            st.write("**高级清洗选项：**")
            
            # 字符串清洗
            string_clean = st.checkbox("字符串清洗", key="string_clean")
            if string_clean:
                string_cols = data.select_dtypes(include=['object']).columns
                if len(string_cols) > 0:
                    selected_string_cols = st.multiselect("选择要清洗的字符串列", string_cols, key="string_cols")
                    
                    if selected_string_cols:
                        col1, col2 = st.columns(2)
                        with col1:
                            remove_whitespace = st.checkbox("去除首尾空格", value=True)
                            lowercase = st.checkbox("转换为小写")
                        with col2:
                            remove_special_chars = st.checkbox("去除特殊字符")
                            normalize_unicode = st.checkbox("Unicode标准化")
            
            # 数值范围限制
            range_limit = st.checkbox("数值范围限制", key="range_limit")
            if range_limit:
                numeric_cols = data.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    range_col = st.selectbox("选择要限制范围的列", numeric_cols, key="range_col")
                    if range_col:
                        col1, col2 = st.columns(2)
                        with col1:
                            min_val = st.number_input("最小值", value=float(data[range_col].min()), key="min_val")
                        with col2:
                            max_val = st.number_input("最大值", value=float(data[range_col].max()), key="max_val")
            
            # 数据格式转换
            st.markdown("---")
            st.write("**🔄 数据格式转换（宽转长/长转宽）：**")
            format_convert = st.checkbox("启用数据格式转换", key="format_convert")
            
            if format_convert:
                convert_type = st.radio(
                    "选择转换类型",
                    ["宽转长（Wide to Long）", "长转宽（Long to Wide）"],
                    key="convert_type"
                )
                
                if convert_type == "宽转长（Wide to Long）":
                    st.info("💡 宽转长：将多列合并为一列，适合变量信息混合在列名中的数据")
                    
                    # 选择ID列（保持不变的列）
                    id_cols = st.multiselect("选择ID列（保持不变的列）", data.columns, key="id_cols")
                    
                    # 选择要转换的列
                    value_cols = st.multiselect("选择要转换的列", data.columns, key="value_cols")
                    
                    if id_cols and value_cols:
                        # 设置新列名
                        col1, col2 = st.columns(2)
                        with col1:
                            var_name = st.text_input("变量名列名", value="变量", key="var_name")
                        with col2:
                            value_name = st.text_input("值列名", value="数值", key="value_name")
                        
                        # 预览转换结果
                        if st.button("预览转换结果", key="preview_wide_to_long"):
                            try:
                                preview_data = data.melt(
                                    id_vars=id_cols,
                                    value_vars=value_cols,
                                    var_name=var_name,
                                    value_name=value_name
                                )
                                st.write("**转换预览：**")
                                st.dataframe(preview_data.head(10), use_container_width=True)
                                st.info(f"转换后数据形状：{preview_data.shape}")
                            except Exception as e:
                                st.error(f"转换失败：{str(e)}")
                
                elif convert_type == "长转宽（Long to Wide）":
                    st.info("💡 长转宽：将一列展开为多列，适合需要横向展示的数据")
                    
                    # 选择索引列
                    index_col = st.selectbox("选择索引列", data.columns, key="index_col")
                    
                    # 选择列名列
                    columns_col = st.selectbox("选择列名列", data.columns, key="columns_col")
                    
                    # 选择值列
                    values_col = st.selectbox("选择值列", data.columns, key="values_col")
                    
                    if index_col and columns_col and values_col:
                        # 预览转换结果
                        if st.button("预览转换结果", key="preview_long_to_wide"):
                            try:
                                preview_data = data.pivot(
                                    index=index_col,
                                    columns=columns_col,
                                    values=values_col
                                )
                                st.write("**转换预览：**")
                                st.dataframe(preview_data.head(10), use_container_width=True)
                                st.info(f"转换后数据形状：{preview_data.shape}")
                            except Exception as e:
                                st.error(f"转换失败：{str(e)}")
        
        # 执行清洗
        st.subheader("🚀 执行清洗")
        
        if st.button("开始数据清洗", type="primary"):
            with st.spinner("正在执行数据清洗..."):
                data_cleaned = data.copy()
                
                # 缺失值处理
                if missing_strategy != "不处理":
                    if missing_strategy == "删除行":
                        data_cleaned = data_cleaned.dropna()
                    elif missing_strategy == "删除列":
                        data_cleaned = data_cleaned.dropna(axis=1)
                    elif missing_strategy == "均值填充":
                        numeric_cols = data_cleaned.select_dtypes(include=[np.number]).columns
                        for col in numeric_cols:
                            if data_cleaned[col].isnull().any():
                                data_cleaned[col] = data_cleaned[col].fillna(data_cleaned[col].mean())
                    elif missing_strategy == "中位数填充":
                        numeric_cols = data_cleaned.select_dtypes(include=[np.number]).columns
                        for col in numeric_cols:
                            if data_cleaned[col].isnull().any():
                                data_cleaned[col] = data_cleaned[col].fillna(data_cleaned[col].median())
                    elif missing_strategy == "众数填充":
                        for col in data_cleaned.columns:
                            if data_cleaned[col].isnull().any():
                                mode_values = data_cleaned[col].mode()
                                if len(mode_values) > 0:
                                    data_cleaned[col] = data_cleaned[col].fillna(mode_values.iloc[0])
                    elif missing_strategy == "前向填充":
                        data_cleaned = data_cleaned.fillna(method='ffill')
                    elif missing_strategy == "后向填充":
                        data_cleaned = data_cleaned.fillna(method='bfill')
                    elif missing_strategy == "插值填充":
                        data_cleaned = data_cleaned.interpolate()
                
                # 异常值处理
                if outlier_strategy != "不处理" and 'outlier_cols' in locals() and outlier_cols:
                    if outlier_strategy == "IQR方法删除":
                        for col in outlier_cols:
                            Q1 = data_cleaned[col].quantile(0.25)
                            Q3 = data_cleaned[col].quantile(0.75)
                            IQR = Q3 - Q1
                            lower_bound = Q1 - 1.5 * IQR
                            upper_bound = Q3 + 1.5 * IQR
                            data_cleaned = data_cleaned[(data_cleaned[col] >= lower_bound) & (data_cleaned[col] <= upper_bound)]
                    elif outlier_strategy == "IQR方法截断":
                        for col in outlier_cols:
                            Q1 = data_cleaned[col].quantile(0.25)
                            Q3 = data_cleaned[col].quantile(0.75)
                            IQR = Q3 - Q1
                            lower_bound = Q1 - 1.5 * IQR
                            upper_bound = Q3 + 1.5 * IQR
                            data_cleaned[col] = data_cleaned[col].clip(lower=lower_bound, upper=upper_bound)
                    elif outlier_strategy == "Z-score方法删除":
                        for col in outlier_cols:
                            z_scores = np.abs(stats.zscore(data_cleaned[col].dropna()))
                            data_cleaned = data_cleaned[z_scores < 3]
                    elif outlier_strategy == "Z-score方法截断":
                        for col in outlier_cols:
                            z_scores = stats.zscore(data_cleaned[col].dropna())
                            data_cleaned[col] = data_cleaned[col].clip(lower=-3, upper=3)
                
                # 重复值处理
                if duplicate_strategy != "不处理":
                    if duplicate_strategy == "删除重复行":
                        data_cleaned = data_cleaned.drop_duplicates()
                    elif duplicate_strategy == "保留第一次出现":
                        data_cleaned = data_cleaned.drop_duplicates(keep='first')
                    elif duplicate_strategy == "保留最后一次出现":
                        data_cleaned = data_cleaned.drop_duplicates(keep='last')
                
                # 数据类型转换
                if convert_types:
                    for col in data_cleaned.columns:
                        if data_cleaned[col].dtype == 'object':
                            try:
                                data_cleaned[col] = pd.to_numeric(data_cleaned[col], errors='coerce')
                            except:
                                pass
                
                # 高级清洗
                if string_clean and 'selected_string_cols' in locals() and selected_string_cols:
                    for col in selected_string_cols:
                        if remove_whitespace:
                            data_cleaned[col] = data_cleaned[col].astype(str).str.strip()
                        if lowercase:
                            data_cleaned[col] = data_cleaned[col].astype(str).str.lower()
                        if remove_special_chars:
                            data_cleaned[col] = data_cleaned[col].astype(str).str.replace(r'[^\w\s]', '', regex=True)
                        if normalize_unicode:
                            import unicodedata
                            data_cleaned[col] = data_cleaned[col].astype(str).apply(lambda x: unicodedata.normalize('NFKD', x))
                
                if range_limit and 'range_col' in locals() and 'min_val' in locals() and 'max_val' in locals():
                    data_cleaned[range_col] = data_cleaned[range_col].clip(lower=min_val, upper=max_val)
                
                # 数据格式转换
                if format_convert and 'convert_type' in locals():
                    if convert_type == "宽转长（Wide to Long）" and 'id_cols' in locals() and 'value_cols' in locals() and id_cols and value_cols:
                        try:
                            data_cleaned = data_cleaned.melt(
                                id_vars=id_cols,
                                value_vars=value_cols,
                                var_name=var_name if 'var_name' in locals() else '变量',
                                value_name=value_name if 'value_name' in locals() else '数值'
                            )
                            st.info("✅ 数据格式转换（宽转长）完成")
                        except Exception as e:
                            st.error(f"数据格式转换失败：{str(e)}")
                    
                    elif convert_type == "长转宽（Long to Wide）" and 'index_col' in locals() and 'columns_col' in locals() and 'values_col' in locals():
                        try:
                            data_cleaned = data_cleaned.pivot(
                                index=index_col,
                                columns=columns_col,
                                values=values_col
                            )
                            st.info("✅ 数据格式转换（长转宽）完成")
                        except Exception as e:
                            st.error(f"数据格式转换失败：{str(e)}")
                
                # 保存清洗后的数据
                st.session_state.data_cleaned = data_cleaned
                st.success("✅ 数据清洗完成！")
        
        # 显示清洗结果
        if st.session_state.data_cleaned is not None:
            st.subheader("📊 清洗结果对比")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**原始数据：**")
                st.write(f"行数：{len(data)}")
                st.write(f"列数：{len(data.columns)}")
                st.write(f"缺失值：{data.isnull().sum().sum()}")
                st.write(f"重复行：{data.duplicated().sum()}")
            
            with col2:
                st.write("**清洗后数据：**")
                st.write(f"行数：{len(st.session_state.data_cleaned)}")
                st.write(f"列数：{len(st.session_state.data_cleaned.columns)}")
                st.write(f"缺失值：{st.session_state.data_cleaned.isnull().sum().sum()}")
                st.write(f"重复行：{st.session_state.data_cleaned.duplicated().sum()}")
            
            # 清洗效果可视化
            st.subheader("📈 清洗效果可视化")
            
            # 缺失值对比
            fig_missing = go.Figure()
            fig_missing.add_trace(go.Bar(
                x=['原始数据', '清洗后数据'],
                y=[data.isnull().sum().sum(), st.session_state.data_cleaned.isnull().sum().sum()],
                name='缺失值数量',
                marker_color=['#ff7f0e', '#2ca02c']
            ))
            fig_missing.update_layout(title='缺失值对比', xaxis_title='数据集', yaxis_title='缺失值数量')
            st.plotly_chart(fig_missing, use_container_width=True)
            
            # 数据预览
            st.subheader("👀 清洗后数据预览")
            st.dataframe(st.session_state.data_cleaned.head(10), use_container_width=True)
            
            # 下载清洗后的数据
            st.subheader("📥 下载数据")
            col1, col2 = st.columns(2)
            
            with col1:
                csv = st.session_state.data_cleaned.to_csv(index=False)
                st.download_button(
                    label="下载CSV文件",
                    data=csv,
                    file_name="cleaned_data.csv",
                    mime="text/csv"
                )
            
            with col2:
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    st.session_state.data_cleaned.to_excel(writer, index=False, sheet_name='Cleaned_Data')
                excel_data = excel_buffer.getvalue()
                st.download_button(
                    label="下载Excel文件",
                    data=excel_data,
                    file_name="cleaned_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

# 自动数据分析页面
elif page == "🔍 自动数据分析":
    st.markdown('<h2 class="sub-header">🔍 自动数据分析</h2>', unsafe_allow_html=True)
    
    # 添加自动数据分析说明
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    ">
        <h3 style="color: white; margin-bottom: 15px;">🔍 自动数据分析指南</h3>
        <p style="font-size: 16px; line-height: 1.6; margin-bottom: 15px;">
            <strong>💡 专业分析工具：</strong><br>
            集成多种专业数据分析工具，自动生成全面的数据概览报告，帮助您快速了解数据特征和潜在问题。
        </p>
        <div style="display: flex; gap: 20px; margin-bottom: 15px;">
            <div style="flex: 1; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                <h4 style="color: #ff6b6b; margin-bottom: 10px;">🛠️ 分析工具</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 14px;">
                    <li>YData Profiling - 全面数据概览</li>
                    <li>Sweetviz - 数据对比分析</li>
                    <li>Pandas Profiling - 基础数据报告</li>
                </ul>
            </div>
            <div style="flex: 1; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                <h4 style="color: #51cf66; margin-bottom: 10px;">📊 分析内容</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 14px;">
                    <li>数据质量评估</li>
                    <li>变量分布分析</li>
                    <li>相关性检测</li>
                    <li>异常值识别</li>
                    <li>交互式报告</li>
                </ul>
            </div>
        </div>
        <p style="font-size: 14px; margin: 0; opacity: 0.9;">
            <strong>🎯 适用场景：</strong> 数据探索、质量检查、初步分析、报告生成
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.data is None:
        st.warning("⚠️ 请先上传数据文件")
    else:
        data = st.session_state.data
        
        # 选择分析工具
        analysis_tool = st.selectbox(
            "选择分析工具",
            ["ydata-profiling", "sweetviz", "pandas-profiling"]
        )
        
        if analysis_tool == "ydata-profiling":
            st.subheader("📊 高级数据分析 (YData Profiling)")
            st.warning("⚠️ 由于Python 3.13兼容性问题，YData Profiling功能暂时不可用。")
            st.info("💡 请使用'基础分析'功能进行数据分析。")
            
            # 显示基础统计信息作为替代
            st.subheader("📈 数据概览")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("行数", len(data))
            with col2:
                st.metric("列数", len(data.columns))
            with col3:
                st.metric("缺失值", data.isnull().sum().sum())
            with col4:
                st.metric("重复行", data.duplicated().sum())
            
            # 显示数据类型分布
            st.subheader("📋 数据类型分布")
            dtype_counts = data.dtypes.value_counts()
            # 将numpy数据类型转换为字符串，避免JSON序列化错误
            dtype_names = [str(dtype) for dtype in dtype_counts.index]
            fig = px.pie(values=dtype_counts.values, names=dtype_names, title="数据类型分布")
            st.plotly_chart(fig, use_container_width=True)
        
        elif analysis_tool == "sweetviz":
            st.subheader("🍯 数据概览分析 (Sweetviz)")
            st.warning("⚠️ 由于Python 3.13兼容性问题，Sweetviz功能暂时不可用。")
            st.info("💡 请使用'基础分析'功能进行数据分析。")
            
            # 显示数据质量评分
            st.subheader("📊 数据质量评分")
            quality_score = calculate_data_quality_score(data)
            st.progress(quality_score / 100)
            st.metric("数据质量评分", f"{quality_score:.1f}/100")
        
        elif analysis_tool == "pandas-profiling":
            st.subheader("🐼 数据分析报告 (Pandas Profiling)")
            st.warning("⚠️ 由于Python 3.13兼容性问题，Pandas Profiling功能暂时不可用。")
            st.info("💡 请使用'基础分析'功能进行数据分析。")
            
            # 显示相关性矩阵
            st.subheader("🔗 相关性分析")
            numeric_data = data.select_dtypes(include=[np.number])
            if len(numeric_data.columns) > 1:
                corr_matrix = numeric_data.corr()
                fig = px.imshow(corr_matrix, 
                              title="数值变量相关性矩阵",
                              color_continuous_scale='RdBu',
                              aspect='auto')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("数据中数值变量不足，无法进行相关性分析。")

# 高级可视化页面
elif page == "📈 高级可视化":
    st.markdown('<h2 class="sub-header">📈 高级可视化</h2>', unsafe_allow_html=True)
    
    # 添加高级可视化说明
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    ">
        <h3 style="color: white; margin-bottom: 15px;">📈 高级可视化指南</h3>
        <p style="font-size: 16px; line-height: 1.6; margin-bottom: 15px;">
            <strong>💡 交互式图表：</strong><br>
            基于Plotly构建的交互式可视化系统，支持多种图表类型，让数据故事更加生动直观。
        </p>
        <div style="display: flex; gap: 20px; margin-bottom: 15px;">
            <div style="flex: 1; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                <h4 style="color: #ff6b6b; margin-bottom: 10px;">📊 图表类型</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 14px;">
                    <li>基础图表：柱状图、折线图、散点图</li>
                    <li>分布图表：直方图、箱线图、小提琴图</li>
                    <li>关系图表：热力图、相关性图</li>
                    <li>高级图表：3D散点图、雷达图</li>
                </ul>
            </div>
            <div style="flex: 1; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                <h4 style="color: #51cf66; margin-bottom: 10px;">✨ 交互功能</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 14px;">
                    <li>缩放和平移</li>
                    <li>悬停显示详情</li>
                    <li>图例交互</li>
                    <li>数据筛选</li>
                    <li>自定义颜色</li>
                </ul>
            </div>
        </div>
        <p style="font-size: 14px; margin: 0; opacity: 0.9;">
            <strong>🎯 适用场景：</strong> 数据展示、趋势分析、对比分析、报告制作
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.data is None:
        st.warning("⚠️ 请先上传数据文件")
    else:
        data = st.session_state.data
        
        # 图表类型选择
        chart_type = st.selectbox(
            "选择图表类型",
            ["柱状图", "折线图", "散点图", "饼图", "直方图", "箱线图", "热力图", "小提琴图", "3D散点图", "雷达图"]
        )
        
        # 获取数值型和分类型列
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if chart_type == "柱状图":
            st.subheader("📊 柱状图")
            col1, col2 = st.columns(2)
            
            with col1:
                x_col = st.selectbox("选择X轴列", data.columns.tolist())
                y_col = st.selectbox("选择Y轴列", numeric_cols if numeric_cols else data.columns.tolist())
            
            with col2:
                color_col = st.selectbox("选择颜色分组列", ['无'] + categorical_cols)
                agg_func = st.selectbox("聚合函数", ['sum', 'mean', 'count', 'max', 'min'])
            
            if color_col == '无':
                fig = px.bar(data, x=x_col, y=y_col, title=f'{y_col} vs {x_col}')
            else:
                fig = px.bar(data, x=x_col, y=y_col, color=color_col, title=f'{y_col} vs {x_col}')
            
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "3D散点图":
            st.subheader("🌐 3D散点图")
            col1, col2 = st.columns(2)
            
            with col1:
                x_col = st.selectbox("选择X轴列", numeric_cols if numeric_cols else data.columns.tolist())
                y_col = st.selectbox("选择Y轴列", numeric_cols if numeric_cols else data.columns.tolist())
            
            with col2:
                z_col = st.selectbox("选择Z轴列", numeric_cols if numeric_cols else data.columns.tolist())
                color_col = st.selectbox("选择颜色列", ['无'] + categorical_cols)
            
            if color_col == '无':
                fig = px.scatter_3d(data, x=x_col, y=y_col, z=z_col, title=f'3D散点图: {x_col} vs {y_col} vs {z_col}')
            else:
                fig = px.scatter_3d(data, x=x_col, y=y_col, z=z_col, color=color_col, title=f'3D散点图: {x_col} vs {y_col} vs {z_col}')
            
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "雷达图":
            st.subheader("🎯 雷达图")
            if len(numeric_cols) >= 3:
                selected_cols = st.multiselect("选择要显示的列（至少3个）", numeric_cols, default=numeric_cols[:5])
                
                if len(selected_cols) >= 3:
                    # 计算平均值用于雷达图
                    avg_values = data[selected_cols].mean()
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatterpolar(
                        r=avg_values.values,
                        theta=selected_cols,
                        fill='toself',
                        name='平均值'
                    ))
                    
                    fig.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, avg_values.max() * 1.2]
                            )),
                        showlegend=True,
                        title="雷达图 - 各变量平均值"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("请选择至少3个数值型列")
            else:
                st.warning("需要至少3个数值型列来创建雷达图")
        
        else:
            # 其他图表类型的实现（保持原有代码）
            if chart_type == "折线图":
                st.subheader("📈 折线图")
                col1, col2 = st.columns(2)
                
                with col1:
                    x_col = st.selectbox("选择X轴列", data.columns.tolist())
                    y_col = st.selectbox("选择Y轴列", numeric_cols if numeric_cols else data.columns.tolist())
                
                with col2:
                    color_col = st.selectbox("选择颜色分组列", ['无'] + categorical_cols)
                
                if color_col == '无':
                    fig = px.line(data, x=x_col, y=y_col, title=f'{y_col} vs {x_col}')
                else:
                    fig = px.line(data, x=x_col, y=y_col, color=color_col, title=f'{y_col} vs {x_col}')
                
                st.plotly_chart(fig, use_container_width=True)
            
            elif chart_type == "散点图":
                st.subheader("🔍 散点图")
                col1, col2 = st.columns(2)
                
                with col1:
                    x_col = st.selectbox("选择X轴列", numeric_cols if numeric_cols else data.columns.tolist())
                    y_col = st.selectbox("选择Y轴列", numeric_cols if numeric_cols else data.columns.tolist())
                
                with col2:
                    color_col = st.selectbox("选择颜色分组列", ['无'] + categorical_cols)
                    size_col = st.selectbox("选择大小列", ['无'] + numeric_cols)
                
                if color_col == '无' and size_col == '无':
                    fig = px.scatter(data, x=x_col, y=y_col, title=f'{y_col} vs {x_col}')
                elif color_col != '无' and size_col == '无':
                    fig = px.scatter(data, x=x_col, y=y_col, color=color_col, title=f'{y_col} vs {x_col}')
                elif color_col == '无' and size_col != '无':
                    fig = px.scatter(data, x=x_col, y=y_col, size=size_col, title=f'{y_col} vs {x_col}')
                else:
                    fig = px.scatter(data, x=x_col, y=y_col, color=color_col, size=size_col, title=f'{y_col} vs {x_col}')
                
                st.plotly_chart(fig, use_container_width=True)
            
            elif chart_type == "饼图":
                st.subheader("🥧 饼图")
                col_name = st.selectbox("选择要分析的列", categorical_cols if categorical_cols else data.columns.tolist())
                
                value_counts = data[col_name].value_counts()
                fig = px.pie(values=value_counts.values, names=value_counts.index, title=f'{col_name} 分布')
                st.plotly_chart(fig, use_container_width=True)
            
            elif chart_type == "直方图":
                st.subheader("📊 直方图")
                col_name = st.selectbox("选择要分析的列", numeric_cols if numeric_cols else data.columns.tolist())
                bins = st.slider("选择直方图箱数", 5, 50, 20)
                
                fig = px.histogram(data, x=col_name, nbins=bins, title=f'{col_name} 分布直方图')
                st.plotly_chart(fig, use_container_width=True)
            
            elif chart_type == "箱线图":
                st.subheader("📦 箱线图")
                col1, col2 = st.columns(2)
                
                with col1:
                    y_col = st.selectbox("选择Y轴列", numeric_cols if numeric_cols else data.columns.tolist())
                
                with col2:
                    x_col = st.selectbox("选择X轴分组列", ['无'] + categorical_cols)
                
                if x_col == '无':
                    fig = px.box(data, y=y_col, title=f'{y_col} 箱线图')
                else:
                    fig = px.box(data, x=x_col, y=y_col, title=f'{y_col} 按 {x_col} 分组的箱线图')
                
                st.plotly_chart(fig, use_container_width=True)
            
            elif chart_type == "热力图":
                st.subheader("🔥 热力图")
                if len(numeric_cols) > 1:
                    corr_matrix = data[numeric_cols].corr()
                    fig = px.imshow(
                        corr_matrix,
                        title='相关性热力图',
                        color_continuous_scale='RdBu',
                        aspect='auto'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("需要至少2个数值型列来创建热力图")
            
            elif chart_type == "小提琴图":
                st.subheader("🎻 小提琴图")
                col1, col2 = st.columns(2)
                
                with col1:
                    y_col = st.selectbox("选择Y轴列", numeric_cols if numeric_cols else data.columns.tolist())
                
                with col2:
                    x_col = st.selectbox("选择X轴分组列", ['无'] + categorical_cols)
                
                if x_col == '无':
                    fig = px.violin(data, y=y_col, title=f'{y_col} 小提琴图')
                else:
                    fig = px.violin(data, x=x_col, y=y_col, title=f'{y_col} 按 {x_col} 分组的小提琴图')
                
                st.plotly_chart(fig, use_container_width=True)

# 机器学习页面
elif page == "🤖 机器学习":
    st.markdown('<h2 class="sub-header">🤖 机器学习</h2>', unsafe_allow_html=True)
    
    # 添加机器学习说明
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    ">
        <h3 style="color: white; margin-bottom: 15px;">🤖 机器学习指南</h3>
        <p style="font-size: 16px; line-height: 1.6; margin-bottom: 15px;">
            <strong>💡 智能算法：</strong><br>
            基于scikit-learn的机器学习平台，提供分类、回归、聚类等多种算法，支持模型训练、评估和预测。
        </p>
        <div style="display: flex; gap: 20px; margin-bottom: 15px;">
            <div style="flex: 1; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                <h4 style="color: #ff6b6b; margin-bottom: 10px;">🎯 任务类型</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 14px;">
                    <li>分类任务 - 预测类别标签</li>
                    <li>回归任务 - 预测连续数值</li>
                    <li>聚类任务 - 数据分组分析</li>
                    <li>特征工程 - 特征优化</li>
                    <li>模型评估 - 性能分析</li>
                </ul>
            </div>
            <div style="flex: 1; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                <h4 style="color: #51cf66; margin-bottom: 10px;">🔧 核心功能</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 14px;">
                    <li>自动数据预处理</li>
                    <li>模型参数调优</li>
                    <li>交叉验证评估</li>
                    <li>特征重要性分析</li>
                    <li>预测结果可视化</li>
                </ul>
            </div>
        </div>
        <p style="font-size: 14px; margin: 0; opacity: 0.9;">
            <strong>🎯 适用场景：</strong> 预测建模、模式识别、数据挖掘、业务智能
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 调试信息
    st.info("🔍 正在加载机器学习模块...")
    
    # 导入机器学习库
    try:
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import LabelEncoder, StandardScaler, PolynomialFeatures
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.linear_model import LinearRegression
        from sklearn.cluster import KMeans
        from sklearn.metrics import classification_report, confusion_matrix, mean_squared_error, r2_score
        SKLEARN_AVAILABLE = True
        st.success("✅ sklearn库导入成功")
    except ImportError as e:
        st.error(f"❌ scikit-learn未安装或导入失败: {e}")
        st.info("请运行: pip install scikit-learn")
        SKLEARN_AVAILABLE = False
    
    if not SKLEARN_AVAILABLE:
        st.stop()
    
    if st.session_state.data is None:
        st.warning("⚠️ 请先上传数据文件")
        st.info("💡 请先到'数据上传'页面上传数据文件")
    else:
        data = st.session_state.data
        st.success(f"✅ 数据加载成功: {len(data)} 行 × {len(data.columns)} 列")
        
        # 机器学习任务选择
        ml_task = st.selectbox(
            "选择机器学习任务",
            ["分类", "回归", "聚类", "特征工程", "模型评估"]
        )
        
        st.info(f"🎯 当前选择的任务: {ml_task}")
        
        if ml_task == "分类":
            st.subheader("🎯 分类任务")
            
            # 选择特征和目标变量
            numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
            
            if len(numeric_cols) == 0:
                st.warning("⚠️ 数据中没有数值型列，无法进行分类任务")
            elif len(categorical_cols) == 0:
                st.warning("⚠️ 数据中没有分类列，无法进行分类任务")
            else:
                col1, col2 = st.columns(2)
                with col1:
                    target_col = st.selectbox("选择目标变量", categorical_cols)
                with col2:
                    feature_cols = st.multiselect("选择特征变量", numeric_cols, default=numeric_cols[:min(3, len(numeric_cols))])
                
                if target_col and feature_cols:
                    # 数据预处理
                    st.write("**数据预处理：**")
                    
                    # 检查数据质量
                    missing_count = data[feature_cols + [target_col]].isnull().sum().sum()
                    if missing_count > 0:
                        st.warning(f"⚠️ 发现 {missing_count} 个缺失值，将自动处理")
                    
                    # 准备数据
                    X = data[feature_cols].fillna(data[feature_cols].mean())
                    le = LabelEncoder()
                    y = le.fit_transform(data[target_col].fillna('Unknown'))
                    
                    # 显示数据信息
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("特征数量", len(feature_cols))
                    with col2:
                        st.metric("样本数量", len(X))
                    with col3:
                        st.metric("类别数量", len(le.classes_))
                    
                    # 数据分割
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                    
                    # 特征缩放
                    scaler = StandardScaler()
                    X_train_scaled = scaler.fit_transform(X_train)
                    X_test_scaled = scaler.transform(X_test)
                    
                    # 模型配置
                    st.write("**模型配置：**")
                    col1, col2 = st.columns(2)
                    with col1:
                        n_estimators = st.slider("决策树数量", 50, 200, 100)
                        max_depth = st.slider("最大深度", 3, 20, 10)
                    with col2:
                        min_samples_split = st.slider("最小分裂样本数", 2, 10, 2)
                        min_samples_leaf = st.slider("最小叶子样本数", 1, 5, 1)
                    
                    if st.button("🚀 训练分类模型", type="primary"):
                        with st.spinner("正在训练模型..."):
                            try:
                                # 训练模型
                                model = RandomForestClassifier(
                                    n_estimators=n_estimators,
                                    max_depth=max_depth,
                                    min_samples_split=min_samples_split,
                                    min_samples_leaf=min_samples_leaf,
                                    random_state=42
                                )
                                model.fit(X_train_scaled, y_train)
                                
                                # 预测
                                y_pred = model.predict(X_test_scaled)
                                y_pred_proba = model.predict_proba(X_test_scaled)
                                
                                # 模型评估
                                st.success("✅ 模型训练完成！")
                                
                                # 评估指标
                                col1, col2, col3, col4 = st.columns(4)
                                with col1:
                                    accuracy = (y_test == y_pred).mean()
                                    st.metric("准确率", f"{accuracy:.4f}")
                                with col2:
                                    from sklearn.metrics import precision_score, recall_score, f1_score
                                    precision = precision_score(y_test, y_pred, average='weighted')
                                    st.metric("精确率", f"{precision:.4f}")
                                with col3:
                                    recall = recall_score(y_test, y_pred, average='weighted')
                                    st.metric("召回率", f"{recall:.4f}")
                                with col4:
                                    f1 = f1_score(y_test, y_pred, average='weighted')
                                    st.metric("F1分数", f"{f1:.4f}")
                                
                                # 分类报告
                                st.write("**详细分类报告：**")
                                st.text(classification_report(y_test, y_pred, target_names=le.classes_))
                                
                                # 混淆矩阵
                                st.write("**混淆矩阵：**")
                                cm = confusion_matrix(y_test, y_pred)
                                fig_cm = px.imshow(
                                    cm, 
                                    labels=dict(x="预测", y="实际", color="数量"),
                                    x=le.classes_,
                                    y=le.classes_,
                                    title="混淆矩阵",
                                    color_continuous_scale='Blues'
                                )
                                st.plotly_chart(fig_cm, use_container_width=True)
                                
                                # 特征重要性
                                feature_importance = pd.DataFrame({
                                    '特征': feature_cols,
                                    '重要性': model.feature_importances_
                                }).sort_values('重要性', ascending=False)
                                
                                st.write("**特征重要性：**")
                                fig_importance = px.bar(
                                    feature_importance, 
                                    x='重要性', 
                                    y='特征', 
                                    title="特征重要性排序", 
                                    orientation='h',
                                    color='重要性',
                                    color_continuous_scale='Viridis'
                                )
                                st.plotly_chart(fig_importance, use_container_width=True)
                                
                                # 预测概率分布
                                if len(le.classes_) == 2:
                                    st.write("**预测概率分布：**")
                                    fig_proba = px.histogram(
                                        x=y_pred_proba[:, 1],
                                        nbins=20,
                                        title="正类预测概率分布",
                                        labels={'x': '预测概率', 'y': '频数'}
                                    )
                                    st.plotly_chart(fig_proba, use_container_width=True)
                                
                            except Exception as e:
                                st.error(f"❌ 模型训练失败：{str(e)}")
                                st.info("💡 请检查数据质量和特征选择")
        
        elif ml_task == "回归":
            st.subheader("📈 回归任务")
            
            numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_cols) < 2:
                st.warning("⚠️ 需要至少2个数值型列进行回归分析")
            else:
                col1, col2 = st.columns(2)
                with col1:
                    target_col = st.selectbox("选择目标变量", numeric_cols)
                with col2:
                    available_features = [col for col in numeric_cols if col != target_col]
                    feature_cols = st.multiselect("选择特征变量", available_features, 
                                                default=available_features[:min(3, len(available_features))])
                
                if target_col and feature_cols:
                    # 数据预处理
                    st.write("**数据预处理：**")
                    
                    # 检查数据质量
                    missing_count = data[feature_cols + [target_col]].isnull().sum().sum()
                    if missing_count > 0:
                        st.warning(f"⚠️ 发现 {missing_count} 个缺失值，将自动处理")
                    
                    # 准备数据
                    X = data[feature_cols].fillna(data[feature_cols].mean())
                    y = data[target_col].fillna(data[target_col].mean())
                    
                    # 显示数据信息
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("特征数量", len(feature_cols))
                    with col2:
                        st.metric("样本数量", len(X))
                    with col3:
                        st.metric("目标变量范围", f"{y.min():.2f} - {y.max():.2f}")
                    
                    # 数据分割
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                    
                    # 模型选择
                    st.write("**模型配置：**")
                    model_type = st.selectbox("选择回归模型", ["线性回归", "随机森林回归", "支持向量回归"])
                    
                    if st.button("🚀 训练回归模型", type="primary"):
                        with st.spinner("正在训练模型..."):
                            try:
                                if model_type == "线性回归":
                                    from sklearn.linear_model import LinearRegression
                                    model = LinearRegression()
                                elif model_type == "随机森林回归":
                                    from sklearn.ensemble import RandomForestRegressor
                                    n_estimators = st.slider("决策树数量", 50, 200, 100)
                                    model = RandomForestRegressor(n_estimators=n_estimators, random_state=42)
                                elif model_type == "支持向量回归":
                                    from sklearn.svm import SVR
                                    model = SVR(kernel='rbf')
                                
                                # 训练模型
                                model.fit(X_train, y_train)
                                
                                # 预测
                                y_pred = model.predict(X_test)
                                
                                # 模型评估
                                st.success("✅ 模型训练完成！")
                                
                                # 评估指标
                                mse = mean_squared_error(y_test, y_pred)
                                rmse = np.sqrt(mse)
                                r2 = r2_score(y_test, y_pred)
                                mae = np.mean(np.abs(y_test - y_pred))
                                
                                col1, col2, col3, col4 = st.columns(4)
                                with col1:
                                    st.metric("R² 分数", f"{r2:.4f}")
                                with col2:
                                    st.metric("均方误差 (MSE)", f"{mse:.4f}")
                                with col3:
                                    st.metric("均方根误差 (RMSE)", f"{rmse:.4f}")
                                with col4:
                                    st.metric("平均绝对误差 (MAE)", f"{mae:.4f}")
                                
                                # 预测vs实际图
                                st.write("**预测效果可视化：**")
                                fig_reg = px.scatter(
                                    x=y_test, 
                                    y=y_pred, 
                                    labels={'x': '实际值', 'y': '预测值'},
                                    title="预测值 vs 实际值"
                                )
                                
                                # 添加完美预测线
                                min_val = min(y_test.min(), y_pred.min())
                                max_val = max(y_test.max(), y_pred.max())
                                fig_reg.add_trace(px.line(x=[min_val, max_val], y=[min_val, max_val]).data[0])
                                
                                st.plotly_chart(fig_reg, use_container_width=True)
                                
                                # 残差图
                                residuals = y_test - y_pred
                                fig_residuals = px.scatter(
                                    x=y_pred,
                                    y=residuals,
                                    labels={'x': '预测值', 'y': '残差'},
                                    title="残差图"
                                )
                                fig_residuals.add_hline(y=0, line_dash="dash", line_color="red")
                                st.plotly_chart(fig_residuals, use_container_width=True)
                                
                                # 特征重要性（如果模型支持）
                                if hasattr(model, 'feature_importances_'):
                                    feature_importance = pd.DataFrame({
                                        '特征': feature_cols,
                                        '重要性': model.feature_importances_
                                    }).sort_values('重要性', ascending=False)
                                    
                                    st.write("**特征重要性：**")
                                    fig_importance = px.bar(
                                        feature_importance, 
                                        x='重要性', 
                                        y='特征', 
                                        title="特征重要性排序", 
                                        orientation='h',
                                        color='重要性',
                                        color_continuous_scale='Viridis'
                                    )
                                    st.plotly_chart(fig_importance, use_container_width=True)
                                
                            except Exception as e:
                                st.error(f"❌ 模型训练失败：{str(e)}")
                                st.info("💡 请检查数据质量和特征选择")
        
        elif ml_task == "聚类":
            st.subheader("🎯 聚类分析")
            
            numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_cols) < 2:
                st.warning("⚠️ 需要至少2个数值型列进行聚类分析")
            else:
                feature_cols = st.multiselect("选择特征变量", numeric_cols, default=numeric_cols[:min(3, len(numeric_cols))])
                
                if feature_cols:
                    # 数据预处理
                    st.write("**数据预处理：**")
                    
                    # 检查数据质量
                    missing_count = data[feature_cols].isnull().sum().sum()
                    if missing_count > 0:
                        st.warning(f"⚠️ 发现 {missing_count} 个缺失值，将自动处理")
                    
                    # 准备数据
                    X = data[feature_cols].fillna(data[feature_cols].mean())
                    scaler = StandardScaler()
                    X_scaled = scaler.fit_transform(X)
                    
                    # 显示数据信息
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("特征数量", len(feature_cols))
                    with col2:
                        st.metric("样本数量", len(X))
                    with col3:
                        st.metric("数据维度", X_scaled.shape[1])
                    
                    # 聚类配置
                    st.write("**聚类配置：**")
                    col1, col2 = st.columns(2)
                    with col1:
                        n_clusters = st.slider("选择聚类数量", 2, 10, 3)
                    with col2:
                        max_iter = st.slider("最大迭代次数", 100, 500, 300)
                    
                    # 肘部法则
                    if st.checkbox("显示肘部法则图"):
                        from sklearn.cluster import KMeans
                        inertias = []
                        K_range = range(1, min(11, len(X_scaled) // 10 + 1))
                        
                        for k in K_range:
                            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                            kmeans.fit(X_scaled)
                            inertias.append(kmeans.inertia_)
                        
                        fig_elbow = px.line(
                            x=list(K_range), 
                            y=inertias,
                            title="肘部法则图",
                            labels={'x': '聚类数量', 'y': '惯性'}
                        )
                        st.plotly_chart(fig_elbow, use_container_width=True)
                    
                    if st.button("🚀 执行聚类分析", type="primary"):
                        with st.spinner("正在执行聚类分析..."):
                            try:
                                # 执行聚类
                                kmeans = KMeans(n_clusters=n_clusters, max_iter=max_iter, random_state=42, n_init=10)
                                clusters = kmeans.fit_predict(X_scaled)
                                
                                # 添加聚类标签到数据
                                data_with_clusters = data.copy()
                                data_with_clusters['Cluster'] = clusters
                                
                                st.success("✅ 聚类分析完成！")
                                
                                # 聚类结果统计
                                st.write("**聚类结果统计：**")
                                cluster_counts = pd.Series(clusters).value_counts().sort_index()
                                
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.write("**各聚类样本数量：**")
                                    cluster_df = pd.DataFrame({
                                        '聚类': cluster_counts.index,
                                        '样本数量': cluster_counts.values,
                                        '占比': (cluster_counts.values / len(clusters) * 100).round(2)
                                    })
                                    st.dataframe(cluster_df, use_container_width=True)
                                
                                with col2:
                                    # 聚类饼图
                                    fig_pie = px.pie(
                                        values=cluster_counts.values,
                                        names=[f'聚类 {i}' for i in cluster_counts.index],
                                        title="聚类分布"
                                    )
                                    st.plotly_chart(fig_pie, use_container_width=True)
                                
                                # 可视化聚类结果
                                if len(feature_cols) >= 2:
                                    st.write("**聚类可视化：**")
                                    
                                    # 2D散点图
                                    fig_cluster = px.scatter(
                                        data_with_clusters, 
                                        x=feature_cols[0], 
                                        y=feature_cols[1], 
                                        color='Cluster',
                                        title=f"K-means聚类结果 (k={n_clusters})",
                                        color_continuous_scale='Viridis'
                                    )
                                    st.plotly_chart(fig_cluster, use_container_width=True)
                                    
                                    # 3D散点图（如果有3个或更多特征）
                                    if len(feature_cols) >= 3:
                                        fig_3d = px.scatter_3d(
                                            data_with_clusters,
                                            x=feature_cols[0],
                                            y=feature_cols[1],
                                            z=feature_cols[2],
                                            color='Cluster',
                                            title=f"3D聚类可视化 (k={n_clusters})"
                                        )
                                        st.plotly_chart(fig_3d, use_container_width=True)
                                
                                # 聚类中心分析
                                st.write("**聚类中心分析：**")
                                cluster_centers = pd.DataFrame(
                                    kmeans.cluster_centers_,
                                    columns=feature_cols
                                )
                                cluster_centers.index = [f'聚类 {i}' for i in range(n_clusters)]
                                st.dataframe(cluster_centers, use_container_width=True)
                                
                                # 特征重要性热力图
                                fig_heatmap = px.imshow(
                                    cluster_centers.T,
                                    title="聚类中心热力图",
                                    color_continuous_scale='RdBu',
                                    aspect='auto'
                                )
                                st.plotly_chart(fig_heatmap, use_container_width=True)
                                
                                # 聚类统计
                                st.write("**各聚类特征统计：**")
                                cluster_stats = data_with_clusters.groupby('Cluster')[feature_cols].agg(['mean', 'std']).round(3)
                                st.dataframe(cluster_stats, use_container_width=True)
                                
                                # 下载聚类结果
                                st.write("**下载聚类结果：**")
                                csv = data_with_clusters.to_csv(index=False)
                                st.download_button(
                                    label="下载聚类结果CSV",
                                    data=csv,
                                    file_name="clustering_results.csv",
                                    mime="text/csv"
                                )
                                
                            except Exception as e:
                                st.error(f"❌ 聚类分析失败：{str(e)}")
                                st.info("💡 请检查数据质量和特征选择")
        
        elif ml_task == "特征工程":
            st.subheader("🔧 特征工程")
            
            numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_cols) == 0:
                st.warning("⚠️ 数据中没有数值型列，无法进行特征工程")
            else:
                selected_cols = st.multiselect("选择要处理的列", numeric_cols, default=numeric_cols[:min(3, len(numeric_cols))])
                
                if selected_cols:
                    st.write("**特征工程选项：**")
                    
                    # 创建选项卡
                    tab1, tab2, tab3, tab4 = st.tabs(["特征缩放", "特征选择", "特征变换", "特征组合"])
                    
                    with tab1:
                        st.write("**特征缩放方法：**")
                        
                        # 标准化
                        if st.checkbox("标准化 (StandardScaler)", key="standardize"):
                            scaler = StandardScaler()
                            data_scaled = data.copy()
                            data_scaled[selected_cols] = scaler.fit_transform(data[selected_cols])
                            st.success("✅ 特征标准化完成")
                            
                            # 显示对比
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write("**原始数据统计：**")
                                st.dataframe(data[selected_cols].describe(), use_container_width=True)
                            with col2:
                                st.write("**标准化后统计：**")
                                st.dataframe(data_scaled[selected_cols].describe(), use_container_width=True)
                        
                        # 归一化
                        if st.checkbox("归一化 (MinMaxScaler)", key="normalize"):
                            from sklearn.preprocessing import MinMaxScaler
                            minmax_scaler = MinMaxScaler()
                            data_normalized = data.copy()
                            data_normalized[selected_cols] = minmax_scaler.fit_transform(data[selected_cols])
                            st.success("✅ 特征归一化完成")
                            
                            # 显示对比
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write("**原始数据范围：**")
                                range_df = pd.DataFrame({
                                    '特征': selected_cols,
                                    '最小值': data[selected_cols].min(),
                                    '最大值': data[selected_cols].max()
                                })
                                st.dataframe(range_df, use_container_width=True)
                            with col2:
                                st.write("**归一化后范围：**")
                                norm_range_df = pd.DataFrame({
                                    '特征': selected_cols,
                                    '最小值': data_normalized[selected_cols].min(),
                                    '最大值': data_normalized[selected_cols].max()
                                })
                                st.dataframe(norm_range_df, use_container_width=True)
                    
                    with tab2:
                        st.write("**特征选择方法：**")
                        
                        # 相关性分析
                        if st.checkbox("相关性分析", key="correlation"):
                            corr_matrix = data[selected_cols].corr().abs()
                            
                            # 相关性热力图
                            fig_corr = px.imshow(
                                corr_matrix,
                                title="特征相关性热力图",
                                color_continuous_scale='RdBu',
                                aspect='auto'
                            )
                            st.plotly_chart(fig_corr, use_container_width=True)
                            
                            # 高相关性特征识别
                            upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
                            high_corr_pairs = []
                            for i in range(len(corr_matrix.columns)):
                                for j in range(i+1, len(corr_matrix.columns)):
                                    if corr_matrix.iloc[i, j] > 0.8:
                                        high_corr_pairs.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_matrix.iloc[i, j]))
                            
                            if high_corr_pairs:
                                st.write("**高相关性特征对 (相关系数>0.8)：**")
                                high_corr_df = pd.DataFrame(high_corr_pairs, columns=['特征1', '特征2', '相关系数'])
                                st.dataframe(high_corr_df, use_container_width=True)
                            else:
                                st.info("✅ 没有发现高相关性特征对")
                        
                        # 方差分析
                        if st.checkbox("方差分析", key="variance"):
                            from sklearn.feature_selection import VarianceThreshold
                            
                            # 计算方差
                            variances = data[selected_cols].var()
                            low_var_features = variances[variances < 0.01].index.tolist()
                            
                            st.write("**特征方差分析：**")
                            variance_df = pd.DataFrame({
                                '特征': selected_cols,
                                '方差': variances.values
                            }).sort_values('方差', ascending=False)
                            st.dataframe(variance_df, use_container_width=True)
                            
                            if low_var_features:
                                st.warning(f"⚠️ 低方差特征 (方差<0.01)：{low_var_features}")
                            else:
                                st.success("✅ 所有特征方差都较高")
                    
                    with tab3:
                        st.write("**特征变换方法：**")
                        
                        # 对数变换
                        if st.checkbox("对数变换", key="log_transform"):
                            data_log = data.copy()
                            for col in selected_cols:
                                if (data[col] > 0).all():
                                    data_log[col] = np.log(data[col])
                                    st.success(f"✅ {col} 对数变换完成")
                                else:
                                    st.warning(f"⚠️ {col} 包含非正值，无法进行对数变换")
                            
                            # 显示变换效果
                            if st.checkbox("显示变换效果"):
                                fig_log = px.histogram(
                                    data_log[selected_cols],
                                    title="对数变换后的分布",
                                    nbins=20
                                )
                                st.plotly_chart(fig_log, use_container_width=True)
                        
                        # 多项式特征
                        if st.checkbox("多项式特征", key="polynomial"):
                            degree = st.slider("多项式次数", 2, 3, 2)
                            poly = PolynomialFeatures(degree=degree, include_bias=False)
                            poly_features = poly.fit_transform(data[selected_cols])
                            
                            st.write(f"**多项式特征信息：**")
                            st.write(f"原始特征数量：{len(selected_cols)}")
                            st.write(f"多项式特征数量：{poly_features.shape[1]}")
                            st.write(f"特征名称：{poly.get_feature_names_out(selected_cols)}")
                    
                    with tab4:
                        st.write("**特征组合方法：**")
                        
                        # 特征交互
                        if st.checkbox("特征交互", key="interaction"):
                            if len(selected_cols) >= 2:
                                interaction_cols = st.multiselect("选择要交互的特征", selected_cols, max_selections=2)
                                if len(interaction_cols) == 2:
                                    data_interaction = data.copy()
                                    interaction_name = f"{interaction_cols[0]}_{interaction_cols[1]}_interaction"
                                    data_interaction[interaction_name] = data[interaction_cols[0]] * data[interaction_cols[1]]
                                    st.success(f"✅ 创建交互特征：{interaction_name}")
                                    
                                    # 显示交互特征统计
                                    st.write("**交互特征统计：**")
                                    st.dataframe(data_interaction[interaction_name].describe(), use_container_width=True)
                            else:
                                st.warning("⚠️ 需要至少2个特征进行交互")
                        
                        # 特征比率
                        if st.checkbox("特征比率", key="ratio"):
                            if len(selected_cols) >= 2:
                                ratio_cols = st.multiselect("选择要计算比率的特征", selected_cols, max_selections=2)
                                if len(ratio_cols) == 2:
                                    data_ratio = data.copy()
                                    ratio_name = f"{ratio_cols[0]}_{ratio_cols[1]}_ratio"
                                    # 避免除零
                                    data_ratio[ratio_name] = data[ratio_cols[0]] / (data[ratio_cols[1]] + 1e-8)
                                    st.success(f"✅ 创建比率特征：{ratio_name}")
                                    
                                    # 显示比率特征统计
                                    st.write("**比率特征统计：**")
                                    st.dataframe(data_ratio[ratio_name].describe(), use_container_width=True)
                            else:
                                st.warning("⚠️ 需要至少2个特征计算比率")
        
        elif ml_task == "模型评估":
            st.subheader("📊 模型评估")
            
            st.write("**模型评估工具：**")
            
            # 交叉验证
            st.write("**交叉验证：**")
            numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_cols) >= 2:
                col1, col2 = st.columns(2)
                with col1:
                    cv_target = st.selectbox("选择目标变量", numeric_cols)
                with col2:
                    cv_features = st.multiselect("选择特征变量", [col for col in numeric_cols if col != cv_target])
                
                if cv_target and cv_features:
                    from sklearn.model_selection import cross_val_score
                    from sklearn.ensemble import RandomForestRegressor
                    
                    # 准备数据
                    X_cv = data[cv_features].fillna(data[cv_features].mean())
                    y_cv = data[cv_target].fillna(data[cv_target].mean())
                    
                    # 交叉验证配置
                    cv_folds = st.slider("交叉验证折数", 3, 10, 5)
                    
                    if st.button("🚀 执行交叉验证"):
                        with st.spinner("正在执行交叉验证..."):
                            try:
                                # 执行交叉验证
                                model_cv = RandomForestRegressor(n_estimators=100, random_state=42)
                                cv_scores = cross_val_score(model_cv, X_cv, y_cv, cv=cv_folds, scoring='r2')
                                
                                st.success("✅ 交叉验证完成！")
                                
                                # 显示结果
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("平均R²分数", f"{cv_scores.mean():.4f}")
                                with col2:
                                    st.metric("标准差", f"{cv_scores.std():.4f}")
                                with col3:
                                    st.metric("分数范围", f"{cv_scores.min():.4f} - {cv_scores.max():.4f}")
                                
                                # 交叉验证分数可视化
                                fig_cv = px.bar(
                                    x=list(range(1, cv_folds + 1)),
                                    y=cv_scores,
                                    title=f"{cv_folds}折交叉验证R²分数",
                                    labels={'x': '折数', 'y': 'R²分数'}
                                )
                                fig_cv.add_hline(y=cv_scores.mean(), line_dash="dash", line_color="red", 
                                               annotation_text=f"平均值: {cv_scores.mean():.4f}")
                                st.plotly_chart(fig_cv, use_container_width=True)
                                
                            except Exception as e:
                                st.error(f"❌ 交叉验证失败：{str(e)}")
            else:
                st.warning("⚠️ 需要至少2个数值型列进行模型评估")
            
            # 学习曲线
            st.write("**学习曲线分析：**")
            if st.checkbox("显示学习曲线"):
                if len(numeric_cols) >= 2:
                    col1, col2 = st.columns(2)
                    with col1:
                        lc_target = st.selectbox("选择目标变量", numeric_cols, key="lc_target")
                    with col2:
                        lc_features = st.multiselect("选择特征变量", [col for col in numeric_cols if col != lc_target], key="lc_features")
                    
                    if lc_target and lc_features:
                        from sklearn.model_selection import learning_curve
                        
                        # 准备数据
                        X_lc = data[lc_features].fillna(data[lc_features].mean())
                        y_lc = data[lc_target].fillna(data[lc_target].mean())
                        
                        if st.button("🚀 生成学习曲线"):
                            with st.spinner("正在生成学习曲线..."):
                                try:
                                    model_lc = RandomForestRegressor(n_estimators=100, random_state=42)
                                    train_sizes, train_scores, val_scores = learning_curve(
                                        model_lc, X_lc, y_lc, cv=5, n_jobs=-1,
                                        train_sizes=np.linspace(0.1, 1.0, 10)
                                    )
                                    
                                    # 计算平均值和标准差
                                    train_mean = np.mean(train_scores, axis=1)
                                    train_std = np.std(train_scores, axis=1)
                                    val_mean = np.mean(val_scores, axis=1)
                                    val_std = np.std(val_scores, axis=1)
                                    
                                    # 绘制学习曲线
                                    fig_lc = go.Figure()
                                    
                                    fig_lc.add_trace(go.Scatter(
                                        x=train_sizes,
                                        y=train_mean,
                                        mode='lines+markers',
                                        name='训练分数',
                                        line=dict(color='blue')
                                    ))
                                    
                                    fig_lc.add_trace(go.Scatter(
                                        x=train_sizes,
                                        y=val_mean,
                                        mode='lines+markers',
                                        name='验证分数',
                                        line=dict(color='red')
                                    ))
                                    
                                    fig_lc.update_layout(
                                        title="学习曲线",
                                        xaxis_title="训练样本数",
                                        yaxis_title="R²分数",
                                        showlegend=True
                                    )
                                    
                                    st.plotly_chart(fig_lc, use_container_width=True)
                                    
                                    # 分析结果
                                    if val_mean[-1] < train_mean[-1] - 0.1:
                                        st.warning("⚠️ 模型可能存在过拟合")
                                    elif val_mean[-1] < 0.5:
                                        st.warning("⚠️ 模型性能较差，可能需要更多特征或调整模型")
                                    else:
                                        st.success("✅ 模型性能良好")
                                        
                                except Exception as e:
                                    st.error(f"❌ 学习曲线生成失败：{str(e)}")
                else:
                    st.warning("⚠️ 需要至少2个数值型列进行学习曲线分析")

# 统计分析页面
elif page == "📊 统计分析":
    st.markdown('<h2 class="sub-header">📊 统计分析</h2>', unsafe_allow_html=True)
    
    # 添加统计分析说明
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    ">
        <h3 style="color: white; margin-bottom: 15px;">📊 统计分析指南</h3>
        <p style="font-size: 16px; line-height: 1.6; margin-bottom: 15px;">
            <strong>💡 专业统计方法：</strong><br>
            提供全面的统计分析工具，包括描述性统计和推断性统计，帮助您从数据中发现有意义的模式和关系。
        </p>
        <div style="display: flex; gap: 20px; margin-bottom: 15px;">
            <div style="flex: 1; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                <h4 style="color: #ff6b6b; margin-bottom: 10px;">📈 描述性统计</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 14px;">
                    <li>集中趋势：均值、中位数、众数</li>
                    <li>离散程度：方差、标准差、IQR</li>
                    <li>分布特征：偏度、峰度</li>
                    <li>数据概览：分位数、极值</li>
                </ul>
            </div>
            <div style="flex: 1; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                <h4 style="color: #51cf66; margin-bottom: 10px;">🔬 假设检验</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 14px;">
                    <li>正态性检验 - Shapiro-Wilk</li>
                    <li>t检验 - 均值比较</li>
                    <li>方差分析 - ANOVA</li>
                    <li>相关性检验 - Pearson/Spearman</li>
                    <li>卡方检验 - 独立性检验</li>
                </ul>
            </div>
        </div>
        <p style="font-size: 14px; margin: 0; opacity: 0.9;">
            <strong>🎯 适用场景：</strong> 数据探索、假设验证、科学研究、决策支持
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.data is None:
        st.warning("⚠️ 请先上传数据文件")
    else:
        data = st.session_state.data
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        
        if not numeric_cols:
            st.warning("⚠️ 数据中没有数值型列，无法进行统计分析")
        else:
            # 描述性统计
            st.subheader("📈 描述性统计")
            selected_cols = st.multiselect("选择要分析的列", numeric_cols, default=numeric_cols[:3])
            
            if selected_cols:
                desc_stats = data[selected_cols].describe()
                st.dataframe(desc_stats, use_container_width=True)
                
                # 添加更多统计指标
                additional_stats = pd.DataFrame({
                    '偏度': data[selected_cols].skew(),
                    '峰度': data[selected_cols].kurtosis(),
                    '变异系数': data[selected_cols].std() / data[selected_cols].mean(),
                    'Q1': data[selected_cols].quantile(0.25),
                    'Q3': data[selected_cols].quantile(0.75),
                    'IQR': data[selected_cols].quantile(0.75) - data[selected_cols].quantile(0.25)
                })
                st.write("**额外统计指标：**")
                st.dataframe(additional_stats, use_container_width=True)
            
            # 假设检验
            st.subheader("🔬 假设检验")
            test_type = st.selectbox("选择检验类型", ["正态性检验", "t检验", "方差分析", "相关性检验", "卡方检验"])
            
            if test_type == "正态性检验":
                col_name = st.selectbox("选择要检验的列", numeric_cols)
                if st.button("进行正态性检验"):
                    statistic, p_value = stats.shapiro(data[col_name].dropna())
                    st.write(f"**Shapiro-Wilk 正态性检验结果：**")
                    st.write(f"统计量：{statistic:.4f}")
                    st.write(f"p值：{p_value:.4f}")
                    if p_value > 0.05:
                        st.success("✅ 数据符合正态分布 (p > 0.05)")
                    else:
                        st.warning("⚠️ 数据不符合正态分布 (p ≤ 0.05)")
            
            elif test_type == "t检验":
                col1, col2 = st.columns(2)
                with col1:
                    col_name = st.selectbox("选择要检验的列", numeric_cols)
                with col2:
                    group_col = st.selectbox("选择分组列", data.select_dtypes(include=['object', 'category']).columns.tolist())
                
                if st.button("进行t检验"):
                    groups = data[group_col].unique()
                    if len(groups) == 2:
                        group1 = data[data[group_col] == groups[0]][col_name].dropna()
                        group2 = data[data[group_col] == groups[1]][col_name].dropna()
                        
                        statistic, p_value = stats.ttest_ind(group1, group2)
                        st.write(f"**独立样本t检验结果：**")
                        st.write(f"统计量：{statistic:.4f}")
                        st.write(f"p值：{p_value:.4f}")
                        if p_value > 0.05:
                            st.success("✅ 两组间无显著差异 (p > 0.05)")
                        else:
                            st.success("✅ 两组间存在显著差异 (p ≤ 0.05)")
                    else:
                        st.warning("分组列必须恰好有2个唯一值")
            
            elif test_type == "方差分析":
                col1, col2 = st.columns(2)
                with col1:
                    col_name = st.selectbox("选择要检验的列", numeric_cols)
                with col2:
                    group_col = st.selectbox("选择分组列", data.select_dtypes(include=['object', 'category']).columns.tolist())
                
                if st.button("进行方差分析"):
                    groups = data[group_col].unique()
                    if len(groups) > 2:
                        group_data = [data[data[group_col] == group][col_name].dropna() for group in groups]
                        statistic, p_value = stats.f_oneway(*group_data)
                        st.write(f"**单因素方差分析结果：**")
                        st.write(f"F统计量：{statistic:.4f}")
                        st.write(f"p值：{p_value:.4f}")
                        if p_value > 0.05:
                            st.success("✅ 各组间无显著差异 (p > 0.05)")
                        else:
                            st.success("✅ 各组间存在显著差异 (p ≤ 0.05)")
                    else:
                        st.warning("分组列必须至少有3个唯一值")
            
            elif test_type == "相关性检验":
                col1, col2 = st.columns(2)
                with col1:
                    col1_name = st.selectbox("选择第一个列", numeric_cols)
                with col2:
                    col2_name = st.selectbox("选择第二个列", numeric_cols)
                
                if st.button("进行相关性检验"):
                    corr, p_value = stats.pearsonr(data[col1_name].dropna(), data[col2_name].dropna())
                    st.write(f"**Pearson相关性检验结果：**")
                    st.write(f"相关系数：{corr:.4f}")
                    st.write(f"p值：{p_value:.4f}")
                    if p_value > 0.05:
                        st.success("✅ 两变量间无显著相关性 (p > 0.05)")
                    else:
                        st.success("✅ 两变量间存在显著相关性 (p ≤ 0.05)")
            
            elif test_type == "卡方检验":
                col1, col2 = st.columns(2)
                with col1:
                    col1_name = st.selectbox("选择第一个分类列", categorical_cols)
                with col2:
                    col2_name = st.selectbox("选择第二个分类列", categorical_cols)
                
                if st.button("进行卡方检验"):
                    contingency_table = pd.crosstab(data[col1_name], data[col2_name])
                    chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
                    st.write(f"**卡方检验结果：**")
                    st.write(f"卡方统计量：{chi2:.4f}")
                    st.write(f"p值：{p_value:.4f}")
                    st.write(f"自由度：{dof}")
                    if p_value > 0.05:
                        st.success("✅ 两变量间无显著关联 (p > 0.05)")
                    else:
                        st.success("✅ 两变量间存在显著关联 (p ≤ 0.05)")

# 报告生成页面
elif page == "📋 报告生成":
    st.markdown('<h2 class="sub-header">📋 报告生成</h2>', unsafe_allow_html=True)
    
    # 添加报告生成说明
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    ">
        <h3 style="color: white; margin-bottom: 15px;">📋 报告生成指南</h3>
        <p style="font-size: 16px; line-height: 1.6; margin-bottom: 15px;">
            <strong>💡 专业报告：</strong><br>
            自动生成结构化的数据分析报告，整合数据概览、统计分析、可视化图表和业务建议，便于分享和决策。
        </p>
        <div style="display: flex; gap: 20px; margin-bottom: 15px;">
            <div style="flex: 1; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                <h4 style="color: #ff6b6b; margin-bottom: 10px;">📄 报告内容</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 14px;">
                    <li>数据概览和基本信息</li>
                    <li>描述性统计分析</li>
                    <li>可视化图表展示</li>
                    <li>数据质量评估</li>
                    <li>业务洞察和建议</li>
                </ul>
            </div>
            <div style="flex: 1; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                <h4 style="color: #51cf66; margin-bottom: 10px;">✨ 报告特色</h4>
                <ul style="margin: 0; padding-left: 20px; font-size: 14px;">
                    <li>HTML格式输出</li>
                    <li>响应式设计</li>
                    <li>专业样式模板</li>
                    <li>一键下载功能</li>
                    <li>时间戳记录</li>
                </ul>
            </div>
        </div>
        <p style="font-size: 14px; margin: 0; opacity: 0.9;">
            <strong>🎯 适用场景：</strong> 项目汇报、客户展示、决策支持、文档存档
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.data is None:
        st.warning("⚠️ 请先上传数据文件")
    else:
        data = st.session_state.data
        
        st.subheader("📄 生成完整分析报告")
        
        # 报告配置
        col1, col2 = st.columns(2)
        with col1:
            report_title = st.text_input("报告标题", "数据分析报告")
            include_visualizations = st.checkbox("包含可视化图表", value=True)
        with col2:
            include_statistics = st.checkbox("包含统计分析", value=True)
            include_recommendations = st.checkbox("包含建议", value=True)
        
        if st.button("🚀 生成完整报告"):
            with st.spinner("正在生成完整报告..."):
                try:
                    # 创建HTML报告
                    html_content = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>{report_title}</title>
                        <style>
                            body {{ font-family: Arial, sans-serif; margin: 40px; }}
                            h1 {{ color: #1f77b4; text-align: center; }}
                            h2 {{ color: #2c3e50; border-bottom: 2px solid #1f77b4; }}
                            .metric {{ background-color: #f8f9fa; padding: 10px; margin: 10px 0; border-radius: 5px; }}
                            .section {{ margin: 30px 0; }}
                        </style>
                    </head>
                    <body>
                        <h1>{report_title}</h1>
                        
                        <div class="section">
                            <h2>📊 数据概览</h2>
                            <div class="metric">
                                <strong>数据集大小：</strong> {len(data)} 行 × {len(data.columns)} 列<br>
                                <strong>内存使用：</strong> {data.memory_usage(deep=True).sum() / 1024**2:.2f} MB<br>
                                <strong>缺失值总数：</strong> {data.isnull().sum().sum()}<br>
                                <strong>数据类型：</strong> {', '.join([f'{str(dtype)}({count})' for dtype, count in data.dtypes.value_counts().items()])}
                            </div>
                        </div>
                    """
                    
                    if include_statistics:
                        numeric_cols = data.select_dtypes(include=[np.number]).columns
                        if len(numeric_cols) > 0:
                            html_content += f"""
                            <div class="section">
                                <h2>📈 描述性统计</h2>
                                <div class="metric">
                                    {data[numeric_cols].describe().to_html()}
                                </div>
                            </div>
                            """
                    
                    if include_visualizations:
                        html_content += f"""
                        <div class="section">
                            <h2>📊 数据可视化</h2>
                            <p>请参考应用中的可视化模块查看详细图表。</p>
                        </div>
                        """
                    
                    if include_recommendations:
                        html_content += f"""
                        <div class="section">
                            <h2>💡 分析建议</h2>
                            <ul>
                                <li>数据质量：{'良好' if data.isnull().sum().sum() / (len(data) * len(data.columns)) < 0.1 else '需要清洗'}</li>
                                <li>建议进行数据清洗以处理缺失值和异常值</li>
                                <li>考虑使用机器学习模型进行进一步分析</li>
                                <li>定期更新数据以保持分析的时效性</li>
                            </ul>
                        </div>
                        """
                    
                    html_content += """
                        <div class="section">
                            <h2>📅 报告生成时间</h2>
                            <p>生成时间：""" + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
                        </div>
                    </body>
                    </html>
                    """
                    
                    # 显示报告
                    st.components.v1.html(html_content, height=600, scrolling=True)
                    
                    # 下载报告
                    st.download_button(
                        label="📥 下载完整报告",
                        data=html_content,
                        file_name=f"{report_title.replace(' ', '_')}.html",
                        mime="text/html"
                    )
                    
                except Exception as e:
                    st.error(f"❌ 报告生成失败：{str(e)}")

# 页脚
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; font-size: 0.8rem;">
        🚀 智能数据分析平台 | LarryTang | tjn.chaos@qq.com | 版本 3.0
    </div>
    """,
    unsafe_allow_html=True
)
