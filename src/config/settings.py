"""
应用配置文件
包含页面配置、样式配置和功能配置
"""

# 页面配置
PAGE_CONFIG = {
    "page_title": "智能数据分析平台",
    "page_icon": "📊",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "menu_items": {
        'Get Help': 'https://docs.streamlit.io/',
        'Report a bug': None,
        'About': '# 智能数据分析平台\n基于Streamlit构建的数据分析应用'
    }
}

# 导航页面配置
NAV_PAGES = [
    "🎯 模式选择",
    "🏠 首页",
    "📁 数据上传", 
    "🧹 数据清洗",
    "🔍 自动数据分析",
    "📈 高级可视化",
    "📊 统计分析",
    "🤖 机器学习",
    "📋 报告生成"
]

# 分析模式配置
ANALYSIS_MODES = {
    "beginner": {
        "name": "新手模式",
        "description": "适合数据分析初学者，提供简化的操作界面和基础功能",
        "icon": "🌱",
        "features": [
            "简化的数据上传界面",
            "基础数据预览",
            "简单图表生成",
            "AI智能指导"
        ]
    },
    "intermediate": {
        "name": "普通模式", 
        "description": "适合有一定数据分析经验的用户，提供完整的功能集",
        "icon": "🚀",
        "features": [
            "完整的数据处理功能",
            "多种可视化选项",
            "基础统计分析",
            "AI智能建议"
        ]
    },
    "professional": {
        "name": "专业模式",
        "description": "适合专业数据分析师，提供高级功能和完整工具集",
        "icon": "⚡",
        "features": [
            "高级数据处理工具",
            "专业可视化图表",
            "完整统计分析",
            "机器学习算法",
            "AI深度分析"
        ]
    }
}

# 自定义CSS样式 - Material Design 3
CUSTOM_CSS = """
<style>
    /* Material Design 3 设计系统 - 现代高级配色 */
    :root {
        /* 主色调 - 深蓝紫渐变系统 */
        --md-primary: #6366F1;
        --md-primary-container: linear-gradient(135deg, #E0E7FF 0%, #C7D2FE 100%);
        --md-on-primary: #FFFFFF;
        --md-on-primary-container: #1E1B4B;
        
        /* 次要色调 - 青绿渐变系统 */
        --md-secondary: #10B981;
        --md-secondary-container: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
        --md-on-secondary: #FFFFFF;
        --md-on-secondary-container: #064E3B;
        
        /* 第三色调 - 橙金渐变系统 */
        --md-tertiary: #F59E0B;
        --md-tertiary-container: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        --md-on-tertiary: #FFFFFF;
        --md-on-tertiary-container: #451A03;
        
        /* 语义色彩 - 现代感配色 */
        --md-success: #10B981;
        --md-success-container: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
        --md-warning: #F59E0B;
        --md-warning-container: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        --md-error: #EF4444;
        --md-error-container: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
        --md-info: #3B82F6;
        --md-info-container: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%);
        
        /* 中性色 - 高级灰调系统 */
        --md-surface: #FAFAFA;
        --md-surface-variant: #F3F4F6;
        --md-background: linear-gradient(135deg, #FAFAFA 0%, #F9FAFB 100%);
        --md-on-surface: #111827;
        --md-on-surface-variant: #374151;
        
        /* 轮廓和阴影 - 现代阴影系统 */
        --md-outline: #D1D5DB;
        --md-outline-variant: #E5E7EB;
        --md-shadow-1: 0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06);
        --md-shadow-2: 0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.06);
        --md-shadow-3: 0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05);
        --md-shadow-4: 0 20px 25px rgba(0,0,0,0.1), 0 10px 10px rgba(0,0,0,0.04);
        
        /* 圆角 */
        --md-radius-small: 8px;
        --md-radius-medium: 12px;
        --md-radius-large: 16px;
        --md-radius-extra-large: 28px;
        
        /* 间距 */
        --md-spacing-xs: 4px;
        --md-spacing-sm: 8px;
        --md-spacing-md: 16px;
        --md-spacing-lg: 24px;
        --md-spacing-xl: 32px;
        --md-spacing-xxl: 48px;
        
        /* 字体 */
        --md-font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        --md-font-size-small: 12px;
        --md-font-size-body: 14px;
        --md-font-size-title: 16px;
        --md-font-size-headline: 20px;
        --md-font-size-display: 24px;
    }
    
    /* 全局样式重置 */
    * {
        box-sizing: border-box;
    }
    
    body {
        font-family: var(--md-font-family);
        background-color: var(--md-background);
        color: var(--md-on-surface);
        line-height: 1.5;
        margin: 0;
        padding: 0;
    }
    
    /* 自定义侧边栏宽度 */
    [data-testid="stSidebar"] {
        width: 320px !important;
        background: var(--md-surface) !important;
        border-right: 1px solid var(--md-outline-variant);
    }
    
    /* 调整主内容区域宽度 */
    .main .block-container {
        max-width: 1400px;
        padding-left: var(--md-spacing-xl);
        padding-right: var(--md-spacing-xl);
        padding-top: var(--md-spacing-lg);
        padding-bottom: var(--md-spacing-lg);
    }
    
    /* Material Design 3 卡片组件 - 现代渐变设计 */
    .md-card {
        background: var(--md-surface);
        border-radius: var(--md-radius-large);
        box-shadow: var(--md-shadow-1);
        padding: var(--md-spacing-lg);
        margin: var(--md-spacing-md) 0;
        border: 1px solid var(--md-outline-variant);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    .md-card:hover {
        box-shadow: var(--md-shadow-2);
        transform: translateY(-2px);
        border-color: var(--md-primary);
    }
    
    .md-card.elevated {
        box-shadow: var(--md-shadow-3);
        background: linear-gradient(135deg, var(--md-surface) 0%, var(--md-surface-variant) 100%);
    }
    
    .md-card.filled {
        background: var(--md-surface-variant);
        border: 1px solid var(--md-outline);
    }
    
    .md-card.outlined {
        border: 2px solid var(--md-outline);
        box-shadow: none;
        background: transparent;
    }
    
    .md-card.gradient-primary {
        background: var(--md-primary-container);
        border: 1px solid var(--md-primary);
        color: var(--md-on-primary-container);
    }
    
    .md-card.gradient-secondary {
        background: var(--md-secondary-container);
        border: 1px solid var(--md-secondary);
        color: var(--md-on-secondary-container);
    }
    
    .md-card.gradient-tertiary {
        background: var(--md-tertiary-container);
        border: 1px solid var(--md-tertiary);
        color: var(--md-on-tertiary-container);
    }
    
    /* Material Design 3 按钮组件 */
    .md-button {
        background: var(--md-primary);
        color: var(--md-on-primary);
        border: none;
        border-radius: var(--md-radius-extra-large);
        padding: var(--md-spacing-sm) var(--md-spacing-lg);
        font-family: var(--md-font-family);
        font-size: var(--md-font-size-body);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        cursor: pointer;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        min-height: 40px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        text-decoration: none;
    }
    
    .md-button:hover {
        box-shadow: var(--md-shadow-2);
        transform: translateY(-1px);
    }
    
    .md-button:active {
        transform: translateY(0);
        box-shadow: var(--md-shadow-1);
    }
    
    .md-button.secondary {
        background: var(--md-secondary);
        color: var(--md-on-secondary);
    }
    
    .md-button.tertiary {
        background: var(--md-tertiary);
        color: var(--md-on-tertiary);
    }
    
    .md-button.outlined {
        background: transparent;
        color: var(--md-primary);
        border: 1px solid var(--md-primary);
    }
    
    .md-button.text {
        background: transparent;
        color: var(--md-primary);
        box-shadow: none;
    }
    
    .md-button.text:hover {
        background: rgba(103, 80, 164, 0.08);
    }
    
    /* Material Design 3 文本样式 */
    .md-headline {
        font-size: var(--md-font-size-display);
        font-weight: 400;
        line-height: 1.25;
        color: var(--md-on-surface);
        margin: var(--md-spacing-md) 0;
    }
    
    .md-title {
        font-size: var(--md-font-size-headline);
        font-weight: 500;
        line-height: 1.4;
        color: var(--md-on-surface);
        margin: var(--md-spacing-sm) 0;
    }
    
    .md-body {
        font-size: var(--md-font-size-body);
        font-weight: 400;
        line-height: 1.5;
        color: var(--md-on-surface);
        margin: var(--md-spacing-xs) 0;
    }
    
    .md-label {
        font-size: var(--md-font-size-small);
        font-weight: 500;
        line-height: 1.4;
        color: var(--md-on-surface-variant);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin: var(--md-spacing-xs) 0;
    }
    
    /* Material Design 3 状态指示器 */
    .md-status-indicator {
        display: inline-flex;
        align-items: center;
        padding: var(--md-spacing-xs) var(--md-spacing-sm);
        border-radius: var(--md-radius-extra-large);
        font-size: var(--md-font-size-small);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    .md-status-indicator.success {
        background: var(--md-success-container);
        color: var(--md-success);
    }
    
    .md-status-indicator.warning {
        background: var(--md-warning-container);
        color: var(--md-warning);
    }
    
    .md-status-indicator.error {
        background: var(--md-error-container);
        color: var(--md-error);
    }
    
    .md-status-indicator.info {
        background: var(--md-info-container);
        color: var(--md-info);
    }
    
    /* Material Design 3 进度指示器 */
    .md-progress {
        width: 100%;
        height: 4px;
        background: var(--md-outline-variant);
        border-radius: 2px;
        overflow: hidden;
        position: relative;
    }
    
    .md-progress-bar {
        height: 100%;
        background: var(--md-primary);
        border-radius: 2px;
        transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    
    .md-progress-bar::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Material Design 3 分割线 */
    .md-divider {
        height: 1px;
        background: var(--md-outline-variant);
        margin: var(--md-spacing-md) 0;
        border: none;
    }
    
    /* Material Design 3 图标样式 */
    .md-icon {
        width: 24px;
        height: 24px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .md-icon:hover {
        background: rgba(103, 80, 164, 0.08);
    }
    
    /* Material Design 3 输入框样式 */
    .md-input {
        background: var(--md-surface);
        border: 1px solid var(--md-outline-variant);
        border-radius: var(--md-radius-small);
        padding: var(--md-spacing-sm) var(--md-spacing-md);
        font-family: var(--md-font-family);
        font-size: var(--md-font-size-body);
        color: var(--md-on-surface);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        outline: none;
    }
    
    .md-input:focus {
        border-color: var(--md-primary);
        box-shadow: 0 0 0 2px rgba(103, 80, 164, 0.2);
    }
    
    /* Material Design 3 选择框样式 */
    .md-select {
        background: var(--md-surface);
        border: 1px solid var(--md-outline-variant);
        border-radius: var(--md-radius-small);
        padding: var(--md-spacing-sm) var(--md-spacing-md);
        font-family: var(--md-font-family);
        font-size: var(--md-font-size-body);
        color: var(--md-on-surface);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        outline: none;
        cursor: pointer;
    }
    
    .md-select:focus {
        border-color: var(--md-primary);
        box-shadow: 0 0 0 2px rgba(103, 80, 164, 0.2);
    }
    
    /* Material Design 3 标签样式 */
    .md-chip {
        display: inline-flex;
        align-items: center;
        background: var(--md-surface-variant);
        color: var(--md-on-surface-variant);
        border-radius: var(--md-radius-extra-large);
        padding: var(--md-spacing-xs) var(--md-spacing-sm);
        font-size: var(--md-font-size-small);
        font-weight: 500;
        margin: var(--md-spacing-xs);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .md-chip:hover {
        background: var(--md-primary-container);
        color: var(--md-on-primary-container);
    }
    
    /* Material Design 3 警告框样式 */
    .md-alert {
        padding: var(--md-spacing-md);
        border-radius: var(--md-radius-medium);
        margin: var(--md-spacing-md) 0;
        border-left: 4px solid;
        display: flex;
        align-items: flex-start;
        gap: var(--md-spacing-sm);
    }
    
    .md-alert.info {
        background: var(--md-info-container);
        border-left-color: var(--md-info);
        color: var(--md-info);
    }
    
    .md-alert.success {
        background: var(--md-success-container);
        border-left-color: var(--md-success);
        color: var(--md-success);
    }
    
    .md-alert.warning {
        background: var(--md-warning-container);
        border-left-color: var(--md-warning);
        color: var(--md-warning);
    }
    
    .md-alert.error {
        background: var(--md-error-container);
        border-left-color: var(--md-error);
        color: var(--md-error);
    }
    
    /* Material Design 3 导航样式 */
    .md-nav-item {
        display: flex;
        align-items: center;
        padding: var(--md-spacing-sm) var(--md-spacing-md);
        border-radius: var(--md-radius-medium);
        color: var(--md-on-surface-variant);
        text-decoration: none;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        margin: var(--md-spacing-xs) 0;
    }
    
    .md-nav-item:hover {
        background: rgba(103, 80, 164, 0.08);
        color: var(--md-primary);
    }
    
    .md-nav-item.active {
        background: var(--md-primary-container);
        color: var(--md-on-primary-container);
    }
    
    /* Material Design 3 侧边栏样式 */
    .md-sidebar {
        background: var(--md-surface);
        border-right: 1px solid var(--md-outline-variant);
        padding: var(--md-spacing-lg);
    }
    
    .md-sidebar-card {
        background: var(--md-surface);
        border-radius: var(--md-radius-large);
        padding: var(--md-spacing-lg);
        margin: var(--md-spacing-md) 0;
        box-shadow: var(--md-shadow-1);
        border: 1px solid var(--md-outline-variant);
    }
    
    /* Material Design 3 数据表格样式 */
    .md-table {
        width: 100%;
        border-collapse: collapse;
        background: var(--md-surface);
        border-radius: var(--md-radius-medium);
        overflow: hidden;
        box-shadow: var(--md-shadow-1);
    }
    
    .md-table th {
        background: var(--md-surface-variant);
        color: var(--md-on-surface-variant);
        font-weight: 500;
        text-align: left;
        padding: var(--md-spacing-md);
        border-bottom: 1px solid var(--md-outline-variant);
    }
    
    .md-table td {
        padding: var(--md-spacing-md);
        border-bottom: 1px solid var(--md-outline-variant);
        color: var(--md-on-surface);
    }
    
    .md-table tr:hover {
        background: rgba(103, 80, 164, 0.04);
    }
    
    /* Material Design 3 工具提示 */
    .md-tooltip {
        position: relative;
        display: inline-block;
    }
    
    .md-tooltip .md-tooltip-text {
        visibility: hidden;
        background: var(--md-on-surface);
        color: var(--md-surface);
        text-align: center;
        border-radius: var(--md-radius-small);
        padding: var(--md-spacing-sm);
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        opacity: 0;
        transition: opacity 0.3s;
        font-size: var(--md-font-size-small);
        white-space: nowrap;
    }
    
    .md-tooltip:hover .md-tooltip-text {
        visibility: visible;
        opacity: 1;
    }
    
    /* Material Design 3 动画 */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { transform: translateX(-100%); }
        to { transform: translateX(0); }
    }
    
    @keyframes scaleIn {
        from { transform: scale(0.9); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }
    
    .md-animate-fade-in {
        animation: fadeIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .md-animate-slide-in {
        animation: slideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .md-animate-scale-in {
        animation: scaleIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: var(--md-spacing-md);
            padding-right: var(--md-spacing-md);
        }
        
        [data-testid="stSidebar"] {
            width: 280px !important;
        }
        
        .md-card {
            padding: var(--md-spacing-md);
        }
    }
    
    /* Streamlit 组件样式覆盖 - 现代渐变设计 */
    .stButton > button {
        background: linear-gradient(135deg, var(--md-primary) 0%, #7C3AED 100%) !important;
        color: var(--md-on-primary) !important;
        border: none !important;
        border-radius: var(--md-radius-extra-large) !important;
        padding: var(--md-spacing-sm) var(--md-spacing-lg) !important;
        font-family: var(--md-font-family) !important;
        font-size: var(--md-font-size-body) !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        min-height: 40px !important;
        box-shadow: var(--md-shadow-1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent) !important;
        transition: left 0.5s !important;
    }
    
    .stButton > button:hover::before {
        left: 100% !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #7C3AED 0%, var(--md-primary) 100%) !important;
        box-shadow: var(--md-shadow-2) !important;
        transform: translateY(-2px) !important;
    }
    
    .stSelectbox > div > div {
        background: var(--md-surface) !important;
        border: 1px solid var(--md-outline-variant) !important;
        border-radius: var(--md-radius-small) !important;
        color: var(--md-on-surface) !important;
    }
    
    .stTextInput > div > div > input {
        background: var(--md-surface) !important;
        border: 1px solid var(--md-outline-variant) !important;
        border-radius: var(--md-radius-small) !important;
        color: var(--md-on-surface) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--md-primary) !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }
    
    .stMetric {
        background: var(--md-surface) !important;
        border-radius: var(--md-radius-medium) !important;
        padding: var(--md-spacing-md) !important;
        box-shadow: var(--md-shadow-1) !important;
        border: 1px solid var(--md-outline-variant) !important;
    }
    
    .stDataFrame {
        border-radius: var(--md-radius-medium) !important;
        overflow: hidden !important;
        box-shadow: var(--md-shadow-1) !important;
    }
    
    .stExpander {
        border: 1px solid var(--md-outline-variant) !important;
        border-radius: var(--md-radius-medium) !important;
        box-shadow: var(--md-shadow-1) !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background: var(--md-surface) !important;
        border-bottom: 1px solid var(--md-outline-variant) !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: var(--md-on-surface-variant) !important;
        border-radius: var(--md-radius-medium) var(--md-radius-medium) 0 0 !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, var(--md-primary-container) 0%, #E0E7FF 100%) !important;
        color: var(--md-on-primary-container) !important;
    }
    
    .stProgress > div > div > div {
        background: var(--md-primary) !important;
        border-radius: 2px !important;
    }
    
    .stProgress > div > div > div > div {
        background: var(--md-outline-variant) !important;
        border-radius: 2px !important;
    }
</style>
"""

# 支持的文件格式
SUPPORTED_FILE_TYPES = ['csv', 'xlsx', 'xls', 'json', 'parquet']

# 组件兼容性配置
COMPONENT_AVAILABILITY = {
    'YDATA_AVAILABLE': False,
    'SWEETVIZ_AVAILABLE': False,
    'PANDAS_PROFILING_AVAILABLE': False,
    'ST_PROFILE_REPORT_AVAILABLE': False
}

# 机器学习配置
ML_CONFIG = {
    'test_size': 0.2,
    'random_state': 42,
    'cv_folds': 5,
    'n_estimators_range': (50, 200),
    'max_depth_range': (3, 20),
    'min_samples_split_range': (2, 10),
    'min_samples_leaf_range': (1, 5)
}

# 可视化配置
VISUALIZATION_CONFIG = {
    'chart_types': [
        "柱状图", "折线图", "散点图", "饼图", "直方图", 
        "箱线图", "热力图", "小提琴图", "3D散点图", "雷达图"
    ],
    'color_scales': ['Viridis', 'Plasma', 'Inferno', 'RdBu', 'Blues'],
    'default_bins': 20
}

# 统计分析配置
STATISTICAL_CONFIG = {
    'test_types': ["正态性检验", "t检验", "方差分析", "相关性检验", "卡方检验"],
    'significance_level': 0.05
}

# 数据清洗配置
DATA_CLEANING_CONFIG = {
    'missing_strategies': [
        "不处理", "删除行", "删除列", "均值填充", "中位数填充", 
        "众数填充", "前向填充", "后向填充", "插值填充"
    ],
    'outlier_strategies': [
        "不处理", "IQR方法删除", "IQR方法截断", 
        "Z-score方法删除", "Z-score方法截断"
    ],
    'duplicate_strategies': [
        "不处理", "删除重复行", "保留第一次出现", "保留最后一次出现"
    ]
}

# 作者信息
AUTHOR_INFO = {
    'name': 'LarryTang',
    'email': 'tjn.chaos@qq.com',
    'title': '技术负责人'
}
