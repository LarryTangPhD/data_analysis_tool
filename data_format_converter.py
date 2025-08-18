"""
数据格式转换工具
演示如何将不整洁数据转换为整洁数据（Tidy Data）
"""
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def load_sample_data():
    """加载示例数据"""
    # 不整洁的数据（宽格式）
    untidy_data = pd.read_csv('sample_untidy_data.csv')
    
    # 整洁的数据（长格式）
    tidy_data = pd.read_csv('sample_tidy_data.csv')
    
    return untidy_data, tidy_data

def demonstrate_data_formats():
    """演示数据格式对比"""
    st.markdown("## 📊 数据格式对比演示")
    
    untidy_data, tidy_data = load_sample_data()
    
    # 创建两列布局
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ❌ 不整洁数据（宽格式）")
        st.write("**问题：**")
        st.write("- 变量名包含多个信息（城市_指标）")
        st.write("- 相同类型的变量分散在不同列")
        st.write("- 不利于统计分析和可视化")
        st.dataframe(untidy_data, use_container_width=True)
        
        # 显示数据形状
        st.info(f"**数据形状：** {untidy_data.shape}")
    
    with col2:
        st.markdown("### ✅ 整洁数据（长格式）")
        st.write("**优势：**")
        st.write("- 每行一个观测值")
        st.write("- 每列一个变量")
        st.write("- 便于分析和可视化")
        st.dataframe(tidy_data, use_container_width=True)
        
        # 显示数据形状
        st.info(f"**数据形状：** {tidy_data.shape}")

def demonstrate_conversion_process():
    """演示转换过程"""
    st.markdown("## 🔄 数据格式转换过程")
    
    untidy_data, _ = load_sample_data()
    
    st.markdown("### 步骤1：识别问题")
    st.write("原始数据的问题：")
    st.write("1. 城市和指标信息混合在列名中")
    st.write("2. GDP和人口数据分散在不同列")
    st.write("3. 无法直接进行城市间的比较分析")
    
    st.markdown("### 步骤2：执行转换")
    
    # 转换GDP数据
    st.write("**转换GDP数据：**")
    gdp_cols = [col for col in untidy_data.columns if 'GDP' in col]
    gdp_data = untidy_data[['年份'] + gdp_cols].copy()
    
    # 使用melt进行宽转长转换
    gdp_tidy = gdp_data.melt(
        id_vars=['年份'],
        value_vars=gdp_cols,
        var_name='城市',
        value_name='GDP'
    )
    
    # 清理城市名
    gdp_tidy['城市'] = gdp_tidy['城市'].str.replace('_GDP', '')
    
    st.dataframe(gdp_tidy, use_container_width=True)
    
    # 转换人口数据
    st.write("**转换人口数据：**")
    pop_cols = [col for col in untidy_data.columns if '人口' in col]
    pop_data = untidy_data[['年份'] + pop_cols].copy()
    
    pop_tidy = pop_data.melt(
        id_vars=['年份'],
        value_vars=pop_cols,
        var_name='城市',
        value_name='人口'
    )
    
    pop_tidy['城市'] = pop_tidy['城市'].str.replace('_人口', '')
    
    st.dataframe(pop_tidy, use_container_width=True)
    
    # 合并数据
    st.write("**合并GDP和人口数据：**")
    final_tidy = pd.merge(gdp_tidy, pop_tidy, on=['年份', '城市'])
    st.dataframe(final_tidy, use_container_width=True)

def demonstrate_analysis_benefits():
    """演示整洁数据的分析优势"""
    st.markdown("## 📈 整洁数据的分析优势")
    
    _, tidy_data = load_sample_data()
    
    # 创建子图
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('GDP趋势对比', '人口趋势对比', 'GDP vs 人口散点图', '城市GDP分布'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # 1. GDP趋势对比
    for city in tidy_data['城市'].unique():
        city_data = tidy_data[tidy_data['城市'] == city]
        fig.add_trace(
            go.Scatter(x=city_data['年份'], y=city_data['GDP'], 
                      name=f'{city} GDP', mode='lines+markers'),
            row=1, col=1
        )
    
    # 2. 人口趋势对比
    for city in tidy_data['城市'].unique():
        city_data = tidy_data[tidy_data['城市'] == city]
        fig.add_trace(
            go.Scatter(x=city_data['年份'], y=city_data['人口'], 
                      name=f'{city} 人口', mode='lines+markers'),
            row=1, col=2
        )
    
    # 3. GDP vs 人口散点图
    fig.add_trace(
        go.Scatter(x=tidy_data['人口'], y=tidy_data['GDP'], 
                  mode='markers', name='GDP vs 人口',
                  text=tidy_data['城市'] + ' (' + tidy_data['年份'].astype(str) + ')',
                  hovertemplate='城市: %{text}<br>人口: %{x}<br>GDP: %{y}<extra></extra>'),
        row=2, col=1
    )
    
    # 4. 城市GDP分布（箱线图）
    for city in tidy_data['城市'].unique():
        city_data = tidy_data[tidy_data['城市'] == city]['GDP']
        fig.add_trace(
            go.Box(y=city_data, name=city, boxpoints='all'),
            row=2, col=2
        )
    
    fig.update_layout(height=800, title_text="整洁数据支持的多维度分析")
    st.plotly_chart(fig, use_container_width=True)
    
    # 统计分析
    st.markdown("### 📊 统计分析示例")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**各城市GDP统计：**")
        gdp_stats = tidy_data.groupby('城市')['GDP'].agg(['mean', 'std', 'min', 'max']).round(2)
        st.dataframe(gdp_stats)
    
    with col2:
        st.write("**各城市人口统计：**")
        pop_stats = tidy_data.groupby('城市')['人口'].agg(['mean', 'std', 'min', 'max']).round(2)
        st.dataframe(pop_stats)
    
    # 相关性分析
    st.write("**GDP与人口相关性：**")
    correlation = tidy_data['GDP'].corr(tidy_data['人口'])
    st.metric("相关系数", f"{correlation:.3f}")

def main():
    """主函数"""
    st.set_page_config(page_title="数据格式转换演示", layout="wide")
    
    st.markdown("# 🔄 数据格式转换演示")
    st.markdown("## 从"不整洁数据"到"整洁数据"的转换过程")
    
    # 添加导航
    page = st.sidebar.selectbox(
        "选择演示内容",
        ["数据格式对比", "转换过程", "分析优势"]
    )
    
    if page == "数据格式对比":
        demonstrate_data_formats()
    elif page == "转换过程":
        demonstrate_conversion_process()
    elif page == "分析优势":
        demonstrate_analysis_benefits()
    
    # 侧边栏说明
    st.sidebar.markdown("### 💡 整洁数据原则")
    st.sidebar.markdown("""
    1. **每行一个观测值**
    2. **每列一个变量**
    3. **每个单元格一个值**
    4. **变量名清晰明确**
    5. **便于统计分析**
    """)
    
    st.sidebar.markdown("### 🛠️ 常用转换操作")
    st.sidebar.markdown("""
    - **宽转长**: `pd.melt()`
    - **长转宽**: `pd.pivot()`
    - **分离列**: `str.split()`
    - **合并列**: `str.cat()`
    - **重塑数据**: `pd.pivot_table()`
    """)

if __name__ == "__main__":
    main()
