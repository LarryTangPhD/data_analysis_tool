"""
新手模式模块
提供引导式的数据分析流程，适合初学者使用
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

# 导入新手模式AI助手
from src.utils.ai_assistant_beginner import get_beginner_ai_assistant

def create_sample_data():
    """创建示例数据集"""
    np.random.seed(42)
    n = 100
    
    # 创建学生成绩数据集
    data = {
        '学生ID': range(1, n+1),
        '数学成绩': np.random.normal(75, 15, n),
        '英语成绩': np.random.normal(80, 12, n),
        '物理成绩': np.random.normal(70, 18, n),
        '性别': np.random.choice(['男', '女'], n),
        '班级': np.random.choice(['A班', 'B班', 'C班'], n),
        '学习时间': np.random.normal(3, 1, n),
        '出勤率': np.random.uniform(0.7, 1.0, n)
    }
    
    # 添加一些缺失值
    data['数学成绩'][np.random.choice(n, 5, replace=False)] = np.nan
    data['英语成绩'][np.random.choice(n, 3, replace=False)] = np.nan
    
    return pd.DataFrame(data)

def display_welcome():
    """显示欢迎界面"""
    st.markdown('<h1 class="main-header">🎓 数据科学分析助手 - 新手模式</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="info-box">
        <h3>👋 欢迎使用数据科学分析助手！</h3>
        <p>这个工具将帮助您学习数据分析的基础知识，通过交互式的方式掌握数据科学的核心技能。</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="step-box">
        <h4>📋 学习目标：</h4>
        <ul>
        <li>理解数据结构类型</li>
        <li>学习数据清洗方法</li>
        <li>掌握基础可视化技巧</li>
        <li>进行描述性统计分析</li>
        <li>探索变量间相关性</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 开始学习之旅", use_container_width=True):
            st.session_state.current_step = 2
            st.rerun()
        
        # AI智能助手功能
        st.markdown("---")
        st.markdown("### 🤖 AI智能学习助手")
        
        # 获取AI助手实例
        ai_assistant = get_beginner_ai_assistant()
        
        if ai_assistant:
            # 预设问题选择
            st.markdown("**💡 常见问题：**")
            preset_questions = ai_assistant.get_preset_questions("welcome")
            
            col1, col2 = st.columns(2)
            with col1:
                selected_preset = st.selectbox(
                    "选择预设问题：",
                    ["自定义问题"] + preset_questions,
                    key="welcome_preset_question"
                )
            
            with col2:
                if selected_preset == "自定义问题":
                    user_question = st.text_input(
                        "输入您的问题：",
                        placeholder="例如：我应该如何开始学习数据分析？",
                        key="welcome_custom_question"
                    )
                else:
                    user_question = selected_preset
            
            # AI回答按钮
            if st.button("🤖 获取AI回答", key="welcome_ai_answer") and user_question.strip():
                with st.spinner("AI导师正在思考..."):
                    try:
                        answer = ai_assistant.answer_beginner_question(
                            user_question, 
                            "欢迎页面",
                            "初学者刚开始学习数据分析"
                        )
                        
                        st.success("✅ AI导师回答完成！")
                        st.markdown("### 🤖 AI导师回答")
                        st.markdown(answer)
                        
                    except Exception as e:
                        st.error(f"❌ AI回答失败：{str(e)}")
            
            # 学习指导按钮
            if st.button("📚 获取学习指导", key="welcome_guidance"):
                with st.spinner("AI导师正在为您制定学习计划..."):
                    try:
                        guidance = ai_assistant.provide_learning_guidance(
                            "欢迎页面",
                            {"step": 1, "status": "starting"}
                        )
                        
                        st.success("✅ 学习指导生成完成！")
                        st.markdown("### 📚 个性化学习指导")
                        st.markdown(guidance)
                        
                    except Exception as e:
                        st.error(f"❌ 学习指导生成失败：{str(e)}")
        else:
            st.warning("⚠️ AI助手暂时不可用，请检查网络连接或API配置")

def display_data_upload():
    """数据上传和结构理解"""
    st.markdown('<h2 class="section-header">📁 第一步：数据上传与结构理解</h2>', unsafe_allow_html=True)
    
    # 数据上传选项
    upload_option = st.radio(
        "选择数据来源：",
        ["📊 使用示例数据集", "📤 上传自己的数据文件"],
        horizontal=True
    )
    
    if upload_option == "📊 使用示例数据集":
        st.markdown("""
        <div class="info-box">
        <h4>📚 示例数据集说明：</h4>
        <p>我们将使用一个学生成绩数据集作为示例，包含以下信息：</p>
        <ul>
        <li><strong>数值型数据</strong>：数学成绩、英语成绩、物理成绩、学习时间、出勤率</li>
        <li><strong>分类型数据</strong>：性别、班级</li>
        <li><strong>标识型数据</strong>：学生ID</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📊 加载示例数据", use_container_width=True):
            st.session_state.data = create_sample_data()
            st.session_state.current_step = 3
            st.rerun()
    
    else:
        st.markdown("""
        <div class="warning-box">
        <h4>📋 数据格式要求：</h4>
        <ul>
        <li>支持 CSV、Excel (.xlsx, .xls) 格式</li>
        <li>文件大小不超过 10MB</li>
        <li>建议包含数值型和分类型数据</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "选择数据文件",
            type=['csv', 'xlsx', 'xls'],
            help="上传您的数据文件"
        )
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    st.session_state.data = pd.read_csv(uploaded_file)
                else:
                    st.session_state.data = pd.read_excel(uploaded_file)
                
                st.success("✅ 数据上传成功！")
                st.session_state.current_step = 3
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ 数据上传失败：{str(e)}")
    
    # AI智能助手功能
    st.markdown("---")
    st.markdown("### 🤖 AI智能学习助手")
    
    # 获取AI助手实例
    ai_assistant = get_beginner_ai_assistant()
    
    if ai_assistant:
        # 预设问题选择
        st.markdown("**💡 数据上传相关问题：**")
        preset_questions = ai_assistant.get_preset_questions("data_upload")
        
        col1, col2 = st.columns(2)
        with col1:
            selected_preset = st.selectbox(
                "选择预设问题：",
                ["自定义问题"] + preset_questions,
                key="upload_preset_question"
            )
        
        with col2:
            if selected_preset == "自定义问题":
                user_question = st.text_input(
                    "输入您的问题：",
                    placeholder="例如：如何选择合适的数据文件？",
                    key="upload_custom_question"
                )
            else:
                user_question = selected_preset
        
        # AI回答按钮
        if st.button("🤖 获取AI回答", key="upload_ai_answer") and user_question.strip():
            with st.spinner("AI导师正在思考..."):
                try:
                    data_context = "正在学习数据上传和结构理解"
                    answer = ai_assistant.answer_beginner_question(
                        user_question, 
                        "数据上传页面",
                        data_context
                    )
                    
                    st.success("✅ AI导师回答完成！")
                    st.markdown("### 🤖 AI导师回答")
                    st.markdown(answer)
                    
                except Exception as e:
                    st.error(f"❌ AI回答失败：{str(e)}")
        
        # 概念解释功能
        st.markdown("**📖 概念解释：**")
        concept_to_explain = st.selectbox(
            "选择要解释的概念：",
            ["CSV文件", "Excel文件", "数据格式", "文件编码", "数据预览"],
            key="upload_concept_explanation"
        )
        
        if st.button("📚 解释概念", key="upload_explain_concept"):
            with st.spinner("AI导师正在解释概念..."):
                try:
                    explanation = ai_assistant.explain_concept(
                        concept_to_explain,
                        "数据上传页面"
                    )
                    
                    st.success("✅ 概念解释完成！")
                    st.markdown("### 📖 概念解释")
                    st.markdown(explanation)
                    
                except Exception as e:
                    st.error(f"❌ 概念解释失败：{str(e)}")
    else:
        st.warning("⚠️ AI助手暂时不可用，请检查网络连接或API配置")
    
    # 返回按钮
    if st.button("⬅️ 返回", key="back_to_welcome"):
        st.session_state.current_step = 1
        st.rerun()

def display_data_structure():
    """显示数据结构信息"""
    st.markdown('<h2 class="section-header">🔍 第二步：理解数据结构</h2>', unsafe_allow_html=True)
    
    if st.session_state.data is None:
        st.error("❌ 没有数据，请先上传数据")
        st.session_state.current_step = 2
        st.rerun()
    
    data = st.session_state.data
    
    # 基本信息
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📊 数据行数", f"{len(data):,}")
    
    with col2:
        st.metric("📋 数据列数", f"{len(data.columns)}")
    
    with col3:
        st.metric("💾 内存使用", f"{data.memory_usage(deep=True).sum() / 1024:.1f} KB")
    
    # 数据类型说明
    st.markdown("""
    <div class="info-box">
    <h4>📚 数据类型说明：</h4>
    <ul>
    <li><strong>object</strong>：文本数据或混合类型数据</li>
    <li><strong>int64/float64</strong>：数值型数据</li>
    <li><strong>datetime</strong>：日期时间数据</li>
    <li><strong>bool</strong>：布尔型数据（True/False）</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # 数据类型表格
    st.subheader("📋 数据类型概览")
    dtype_info = pd.DataFrame({
        '列名': data.columns,
        '数据类型': data.dtypes,
        '非空值数量': data.count(),
        '缺失值数量': data.isnull().sum(),
        '缺失值比例': (data.isnull().sum() / len(data) * 100).round(2)
    })
    
    st.dataframe(dtype_info, use_container_width=True)
    
    # 数据预览
    st.subheader("👀 数据预览")
    st.dataframe(data.head(10), use_container_width=True)
    
    # AI智能助手功能
    st.markdown("---")
    st.markdown("### 🤖 AI智能学习助手")
    
    # 获取AI助手实例
    ai_assistant = get_beginner_ai_assistant()
    
    if ai_assistant:
        # 获取当前数据上下文
        data_context = f"当前数据集包含{len(data)}行{len(data.columns)}列数据，包含以下列：{', '.join(data.columns[:5])}{'...' if len(data.columns) > 5 else ''}。数据类型包括：{', '.join([f'{col}({dtype})' for col, dtype in data.dtypes.items()][:3])}{'...' if len(data.columns) > 3 else ''}"
        
        # 预设问题选择
        st.markdown("**💡 常见问题：**")
        preset_questions = ai_assistant.get_preset_questions("data_structure")
        
        col1, col2 = st.columns(2)
        with col1:
            selected_preset = st.selectbox(
                "选择预设问题：",
                ["自定义问题"] + preset_questions,
                key="structure_preset_question"
            )
        
        with col2:
            if selected_preset == "自定义问题":
                user_question = st.text_input(
                    "输入您的问题：",
                    placeholder="例如：什么是数值型数据？",
                    key="structure_custom_question"
                )
            else:
                user_question = selected_preset
        
        # AI回答按钮
        if st.button("🤖 获取AI回答", key="structure_ai_answer") and user_question.strip():
            with st.spinner("AI导师正在思考..."):
                try:
                    answer = ai_assistant.answer_beginner_question(
                        user_question,
                        "数据结构页面",
                        data_context
                    )
                    
                    st.success("✅ AI导师回答完成！")
                    st.markdown("### 🤖 AI导师回答")
                    st.markdown(answer)
                    
                except Exception as e:
                    st.error(f"❌ AI回答失败：{str(e)}")
        
        # 学习指导按钮
        if st.button("📚 获取学习指导", key="structure_guidance"):
            with st.spinner("AI导师正在为您制定学习计划..."):
                try:
                    guidance = ai_assistant.provide_learning_guidance(
                        "数据结构页面",
                        {"step": 2, "status": "understanding", "data_shape": data.shape}
                    )
                    
                    st.success("✅ 学习指导生成完成！")
                    st.markdown("### 📚 个性化学习指导")
                    st.markdown(guidance)
                    
                except Exception as e:
                    st.error(f"❌ 学习指导生成失败：{str(e)}")
        
        # 概念解释按钮
        if st.button("📖 概念解释", key="structure_concept"):
            concept = st.selectbox(
                "选择要解释的概念：",
                ["数据类型", "数值型数据", "分类型数据", "缺失值", "数据预览"],
                key="structure_concept_select"
            )
            
            if st.button("🔍 解释概念", key="structure_explain"):
                with st.spinner("AI导师正在解释..."):
                    try:
                        explanation = ai_assistant.explain_concept(
                            concept,
                            "数据结构页面"
                        )
                        
                        st.success("✅ 概念解释完成！")
                        st.markdown("### 📖 概念解释")
                        st.markdown(explanation)
                        
                    except Exception as e:
                        st.error(f"❌ 概念解释失败：{str(e)}")
    else:
        st.warning("⚠️ AI助手暂时不可用，请检查网络连接或API配置")
    
    # 继续按钮
    if st.button("➡️ 继续下一步：数据清洗", use_container_width=True):
        st.session_state.current_step = 4
        st.rerun()
    
    # 返回按钮
    if st.button("⬅️ 返回", key="back_to_upload"):
        st.session_state.current_step = 2
        st.rerun()

def display_data_cleaning():
    """数据清洗界面 - 新手友好版本（参考优秀设计）"""
    
    # 尝试导入报告生成相关库
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from reportlab.pdfgen import canvas
        from docx import Document
        from docx.shared import Inches
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.oxml.shared import OxmlElement, qn
        REPORT_AVAILABLE = True
    except ImportError:
        REPORT_AVAILABLE = False
        st.warning("⚠️ 报告生成功能需要安装额外的依赖包：pip install reportlab python-docx Pillow")
    st.markdown('<h2 class="section-header">🧹 第三步：数据清洗</h2>', unsafe_allow_html=True)
    
    if st.session_state.data is None:
        st.error("❌ 没有数据，请先上传数据")
        st.session_state.current_step = 2
        st.rerun()
    
    data = st.session_state.data.copy()
    
    # 初始化清洗结果和处理历史
    if 'cleaning_results' not in st.session_state:
        st.session_state.cleaning_results = {}
    if 'cleaning_history' not in st.session_state:
        st.session_state.cleaning_history = []
    
    st.markdown("""
    <div class="info-box">
    <h4>🎓 数据清洗学习指南：</h4>
    <p>数据清洗就像给数据"洗澡"，去除"脏东西"让数据更干净、更可靠。我们将通过4个步骤来学习：</p>
    <ol>
    <li><strong>📊 数据质量评估</strong>：先了解数据有多"脏"</li>
    <li><strong>🔍 问题诊断</strong>：找出具体的问题在哪里</li>
    <li><strong>⚙️ 智能处理</strong>：选择合适的"清洁剂"</li>
    <li><strong>✅ 效果验证</strong>：检查清洗效果</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # 第一步：数据质量评估
    st.markdown("### 📊 第一步：数据质量评估")
    
    # 计算数据质量评分
    total_cells = data.shape[0] * data.shape[1]
    missing_cells = data.isnull().sum().sum()
    duplicate_rows = data.duplicated().sum()
    
    # 质量评分计算（0-100分）
    completeness_score = max(0, 100 - (missing_cells / total_cells * 100))
    uniqueness_score = max(0, 100 - (duplicate_rows / len(data) * 100))
    overall_score = (completeness_score + uniqueness_score) / 2
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 整体质量评分", f"{overall_score:.1f}/100", 
                 delta=f"{'优秀' if overall_score >= 80 else '良好' if overall_score >= 60 else '需要改进'}")
    
    with col2:
        st.metric("✅ 完整性评分", f"{completeness_score:.1f}/100")
    
    with col3:
        st.metric("🔄 唯一性评分", f"{uniqueness_score:.1f}/100")
    
    with col4:
        st.metric("📈 数据规模", f"{data.shape[0]}行 × {data.shape[1]}列")
    
    # 质量评分可视化
    fig = px.bar(
        x=['整体质量', '完整性', '唯一性'],
        y=[overall_score, completeness_score, uniqueness_score],
        title="📊 数据质量评分",
        color=[overall_score, completeness_score, uniqueness_score],
        color_continuous_scale='RdYlGn'
    )
    fig.update_layout(yaxis_title="评分", yaxis_range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)
    
    # 第二步：问题诊断
    st.markdown("### 🔍 第二步：问题诊断")
    
    # 创建问题诊断标签页
    tab1, tab2, tab3 = st.tabs(["🔍 缺失值诊断", "🔄 重复值诊断", "⚠️ 异常值诊断"])
    
    with tab1:
        st.markdown("#### 📋 缺失值分析")
        
        missing_data = data.isnull().sum()
        missing_percent = (missing_data / len(data) * 100).round(2)
        
        if missing_data.sum() > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📊 缺失值统计表：**")
                missing_df = pd.DataFrame({
                    '列名': missing_data.index,
                    '缺失值数量': missing_data.values,
                    '缺失值比例(%)': missing_percent.values,
                    '数据类型': [str(data[col].dtype) for col in missing_data.index]
                })
                st.dataframe(missing_df[missing_df['缺失值数量'] > 0], use_container_width=True)
            
            with col2:
                # 缺失值热力图
                missing_matrix = data.isnull()
                fig = px.imshow(
                    missing_matrix.T,
                    title="🔍 缺失值模式热力图",
                    labels=dict(x="数据行", y="列名", color="是否缺失"),
                    color_continuous_scale=['white', 'red']
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # 缺失值原因分析
            st.markdown("**🤔 缺失值可能的原因：**")
            st.markdown("""
            - **随机缺失**：数据丢失是随机的，不影响分析
            - **系统性缺失**：某些条件下更容易缺失（如设备故障）
            - **人为缺失**：数据录入时的疏忽
            - **业务缺失**：某些情况下数据确实不存在
            """)
        else:
            st.success("🎉 恭喜！没有发现缺失值，数据完整性很好！")
    
    with tab2:
        st.markdown("#### 📋 重复值分析")
        
        duplicate_count = data.duplicated().sum()
        
        if duplicate_count > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("🔄 重复行数量", duplicate_count)
                st.metric("📊 重复率", f"{duplicate_count/len(data)*100:.2f}%")
                
                # 显示重复行示例
                duplicate_rows = data[data.duplicated(keep=False)]
                st.markdown("**📋 重复行示例：**")
                st.dataframe(duplicate_rows.head(5), use_container_width=True)
            
            with col2:
                # 重复值分布
                try:
                    duplicate_counts = duplicate_rows.groupby(duplicate_rows.columns.tolist()).size().reset_index(name='重复次数')
                    fig = px.histogram(
                        duplicate_counts, 
                        x='重复次数',
                        title="🔄 重复次数分布",
                        nbins=10
                    )
                    st.plotly_chart(fig, use_container_width=True)
                except:
                    st.info("重复值分布图暂时无法显示")
            
            st.markdown("**🤔 重复值可能的原因：**")
            st.markdown("""
            - **数据录入错误**：同一记录被重复录入
            - **数据合并问题**：多个数据源合并时产生重复
            - **系统故障**：数据同步或备份时出现问题
            - **业务重复**：某些业务场景下确实存在重复
            """)
        else:
            st.success("🎉 恭喜！没有发现重复值，数据唯一性很好！")
    
    with tab3:
        st.markdown("#### 📋 异常值分析")
        
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) > 0:
            selected_col = st.selectbox("🔍 选择要分析的数值列：", numeric_cols)
            
            if selected_col:
                # 计算异常值
                Q1 = data[selected_col].quantile(0.25)
                Q3 = data[selected_col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = data[(data[selected_col] < lower_bound) | (data[selected_col] > upper_bound)]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("⚠️ 异常值数量", len(outliers))
                    st.metric("📊 异常值比例", f"{len(outliers)/len(data)*100:.2f}%")
                    
                    if len(outliers) > 0:
                        st.markdown("**📋 异常值统计：**")
                        outlier_stats = pd.DataFrame({
                            '统计量': ['最小值', '最大值', '平均值', '标准差'],
                            '异常值': [
                                outliers[selected_col].min(),
                                outliers[selected_col].max(),
                                outliers[selected_col].mean(),
                                outliers[selected_col].std()
                            ]
                        })
                        st.dataframe(outlier_stats, use_container_width=True)
                
                with col2:
                    # 箱线图
                    fig = px.box(
                        data, 
                        y=selected_col,
                        title=f"📊 {selected_col} 的箱线图",
                        points="outliers"
                    )
                    fig.add_hline(y=lower_bound, line_dash="dash", line_color="red", 
                                 annotation_text=f"下界: {lower_bound:.2f}")
                    fig.add_hline(y=upper_bound, line_dash="dash", line_color="red",
                                 annotation_text=f"上界: {upper_bound:.2f}")
                    st.plotly_chart(fig, use_container_width=True)
                
                if len(outliers) > 0:
                    st.markdown("**🤔 异常值可能的原因：**")
                    st.markdown("""
                    - **数据录入错误**：人为输入错误
                    - **测量误差**：设备或方法导致的误差
                    - **真实异常**：业务中的特殊情况
                    - **数据转换错误**：单位转换或格式转换错误
                    """)
                    
                    # 显示异常值详情
                    with st.expander("📋 查看异常值详情"):
                        st.dataframe(outliers, use_container_width=True)
        else:
            st.info("ℹ️ 当前数据中没有数值型列，无法进行异常值分析。")
    
    # 第三步：智能处理
    st.markdown("### ⚙️ 第三步：智能处理")
    
    # 处理策略选择 - 使用卡片式布局
    st.markdown("#### 🎯 选择处理策略")
    
    # 创建三个处理策略卡片
    with st.container():
        # 缺失值处理策略卡片
        with st.expander("🔧 缺失值处理策略", expanded=True):
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 4px solid #007bff;">
            <h5 style="margin: 0 0 10px 0; color: #007bff;">📋 处理选项说明：</h5>
            <ul style="margin: 0; padding-left: 20px;">
            <li><strong>智能自动处理</strong>：根据数据类型自动选择最佳填充方法</li>
            <li><strong>删除包含缺失值的行</strong>：直接删除有缺失值的记录</li>
            <li><strong>手动选择填充方法</strong>：自定义填充策略</li>
            <li><strong>暂时跳过</strong>：保留原始数据，稍后处理</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            missing_strategy = st.selectbox(
                "选择缺失值处理方法：",
                [
                    "🤖 智能自动处理（推荐）",
                    "🗑️ 删除包含缺失值的行",
                    "📊 手动选择填充方法",
                    "⏭️ 暂时跳过"
                ],
                key="missing_strategy"
            )
            
            # 手动选择填充方法的详细选项
            if "手动选择填充方法" in missing_strategy:
                st.markdown("**🔧 手动填充设置：**")
                
                # 获取有缺失值的列
                missing_cols = data.columns[data.isnull().any()].tolist()
                
                if missing_cols:
                    st.markdown("**📋 为每个有缺失值的列选择填充方法：**")
                    
                    # 初始化手动填充设置
                    if 'manual_fill_settings' not in st.session_state:
                        st.session_state.manual_fill_settings = {}
                    
                    for col in missing_cols:
                        col_type = data[col].dtype
                        
                        # 使用容器和边框样式替代嵌套的expander
                        st.markdown(f"""
                        <div style="
                            border: 2px solid #e0e0e0; 
                            border-radius: 10px; 
                            padding: 15px; 
                            margin: 10px 0; 
                            background-color: #f8f9fa;
                        ">
                            <h4 style="margin: 0 0 15px 0; color: #2c3e50;">🔧 {col} (类型: {col_type})</h4>
                        """, unsafe_allow_html=True)
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # 填充方法选择
                            if col_type in ['int64', 'float64']:
                                fill_method = st.selectbox(
                                    f"选择填充方法：",
                                    ["中位数", "均值", "固定值", "前向填充", "后向填充"],
                                    key=f"fill_method_{col}"
                                )
                            else:
                                fill_method = st.selectbox(
                                    f"选择填充方法：",
                                    ["众数", "固定值", "前向填充", "后向填充"],
                                    key=f"fill_method_{col}"
                                )
                            
                            # 固定值输入
                            if fill_method == "固定值":
                                if col_type in ['int64', 'float64']:
                                    fixed_value = st.number_input(
                                        f"输入固定值：",
                                        value=0.0,
                                        key=f"fixed_value_{col}"
                                    )
                                else:
                                    fixed_value = st.text_input(
                                        f"输入固定值：",
                                        value="未知",
                                        key=f"fixed_value_{col}"
                                    )
                            else:
                                fixed_value = None
                        
                        with col2:
                            # 显示当前列的缺失值信息
                            missing_count = data[col].isnull().sum()
                            missing_pct = (missing_count / len(data)) * 100
                            
                            st.metric("缺失值数量", missing_count)
                            st.metric("缺失值比例", f"{missing_pct:.2f}%")
                            
                            # 显示当前列的统计信息
                            if col_type in ['int64', 'float64']:
                                st.markdown("**当前统计：**")
                                st.write(f"均值: {data[col].mean():.2f}")
                                st.write(f"中位数: {data[col].median():.2f}")
                                st.write(f"标准差: {data[col].std():.2f}")
                        
                        # 保存设置
                        st.session_state.manual_fill_settings[col] = {
                            'method': fill_method,
                            'fixed_value': fixed_value
                        }
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.info("ℹ️ 当前数据中没有缺失值，无需手动设置填充方法。")
        
        # 重复值处理策略卡片
        with st.expander("🔄 重复值处理策略", expanded=True):
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 4px solid #28a745;">
            <h5 style="margin: 0 0 10px 0; color: #28a745;">📋 处理选项说明：</h5>
            <ul style="margin: 0; padding-left: 20px;">
            <li><strong>智能自动处理</strong>：自动删除所有重复记录</li>
            <li><strong>删除所有重复行</strong>：删除所有重复数据</li>
            <li><strong>保留第一次出现的行</strong>：保留首次出现的记录</li>
            <li><strong>保留最后一次出现的行</strong>：保留最后出现的记录</li>
            <li><strong>暂时跳过</strong>：保留原始数据，稍后处理</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            duplicate_strategy = st.selectbox(
                "选择重复值处理方法：",
                [
                    "🤖 智能自动处理（推荐）",
                    "🗑️ 删除所有重复行",
                    "📋 保留第一次出现的行",
                    "📋 保留最后一次出现的行",
                    "⏭️ 暂时跳过"
                ],
                key="duplicate_strategy"
            )
        
        # 异常值处理策略卡片
        with st.expander("⚠️ 异常值处理策略", expanded=True):
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 4px solid #ffc107;">
            <h5 style="margin: 0 0 10px 0; color: #ffc107;">📋 处理选项说明：</h5>
            <ul style="margin: 0; padding-left: 20px;">
            <li><strong>智能自动处理</strong>：用中位数替换异常值</li>
            <li><strong>删除异常值</strong>：直接删除异常数据</li>
            <li><strong>用统计值替换异常值</strong>：用均值或中位数替换</li>
            <li><strong>限制在合理范围内</strong>：将异常值限制在正常范围内</li>
            <li><strong>暂时跳过</strong>：保留原始数据，稍后处理</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            outlier_strategy = st.selectbox(
                "选择异常值处理方法：",
                [
                    "🤖 智能自动处理（推荐）",
                    "🗑️ 删除异常值",
                    "📊 用统计值替换异常值",
                    "🔒 限制在合理范围内",
                    "⏭️ 暂时跳过"
                ],
                key="outlier_strategy"
            )
    
    # 执行处理 - 优化按钮布局
    st.markdown("---")
    st.markdown("#### 🚀 执行数据处理")
    
    # 显示处理预览
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="background-color: #e8f5e8; padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #28a745;">
        <h4 style="color: #28a745; margin: 0 0 10px 0;">🎯 处理策略预览</h4>
        <p style="margin: 0; color: #2c3e50;">已选择：<strong>智能自动处理</strong> 模式</p>
        <p style="margin: 5px 0 0 0; font-size: 0.9em; color: #6c757d;">系统将自动选择最佳处理方法</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 突出显示的处理按钮
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        process_button = st.button("🚀 开始智能处理", type="primary", use_container_width=True)
    
    if process_button:
        with st.spinner("🔄 正在处理数据..."):
            cleaned_data = data.copy()
            processing_log = []
            
            # 处理缺失值
            if "智能自动处理" in missing_strategy:
                missing_handled = 0
                for col in cleaned_data.columns:
                    if cleaned_data[col].isnull().sum() > 0:
                        if cleaned_data[col].dtype in ['int64', 'float64']:
                            # 数值型数据用中位数填充
                            cleaned_data[col].fillna(cleaned_data[col].median(), inplace=True)
                            method = "中位数"
                        else:
                            # 分类型数据用众数填充
                            mode_value = cleaned_data[col].mode()[0] if len(cleaned_data[col].mode()) > 0 else '未知'
                            cleaned_data[col].fillna(mode_value, inplace=True)
                            method = "众数"
                        
                        missing_handled += 1
                        processing_log.append(f"✅ {col}列：用{method}填充了缺失值")
                
                if missing_handled > 0:
                    processing_log.append(f"🎉 总共处理了{missing_handled}列的缺失值")
            
            elif "手动选择填充方法" in missing_strategy:
                missing_handled = 0
                if 'manual_fill_settings' in st.session_state:
                    for col, settings in st.session_state.manual_fill_settings.items():
                        if cleaned_data[col].isnull().sum() > 0:
                            method = settings['method']
                            fixed_value = settings.get('fixed_value')
                            
                            if method == "中位数":
                                cleaned_data[col].fillna(cleaned_data[col].median(), inplace=True)
                            elif method == "均值":
                                cleaned_data[col].fillna(cleaned_data[col].mean(), inplace=True)
                            elif method == "众数":
                                mode_value = cleaned_data[col].mode()[0] if len(cleaned_data[col].mode()) > 0 else '未知'
                                cleaned_data[col].fillna(mode_value, inplace=True)
                            elif method == "固定值" and fixed_value is not None:
                                cleaned_data[col].fillna(fixed_value, inplace=True)
                            elif method == "前向填充":
                                cleaned_data[col].fillna(method='ffill', inplace=True)
                            elif method == "后向填充":
                                cleaned_data[col].fillna(method='bfill', inplace=True)
                            
                            missing_handled += 1
                            processing_log.append(f"✅ {col}列：用{method}填充了缺失值")
                
                if missing_handled > 0:
                    processing_log.append(f"🎉 总共处理了{missing_handled}列的缺失值")
            
            elif "删除" in missing_strategy:
                original_rows = len(cleaned_data)
                cleaned_data.dropna(inplace=True)
                deleted_rows = original_rows - len(cleaned_data)
                processing_log.append(f"🗑️ 删除了{deleted_rows}行包含缺失值的数据")
            
            # 处理重复值
            if "智能自动处理" in duplicate_strategy or "删除所有重复行" in duplicate_strategy:
                duplicate_count = cleaned_data.duplicated().sum()
                if duplicate_count > 0:
                    cleaned_data.drop_duplicates(inplace=True)
                    processing_log.append(f"🔄 删除了{duplicate_count}行重复数据")
            
            elif "保留第一次" in duplicate_strategy:
                duplicate_count = cleaned_data.duplicated().sum()
                if duplicate_count > 0:
                    cleaned_data.drop_duplicates(keep='first', inplace=True)
                    processing_log.append(f"📋 删除了{duplicate_count}行重复数据（保留第一次出现）")
            
            elif "保留最后一次" in duplicate_strategy:
                duplicate_count = cleaned_data.duplicated().sum()
                if duplicate_count > 0:
                    cleaned_data.drop_duplicates(keep='last', inplace=True)
                    processing_log.append(f"📋 删除了{duplicate_count}行重复数据（保留最后一次出现）")
            
            # 处理异常值（仅对数值型数据）
            if "智能自动处理" in outlier_strategy:
                numeric_cols = cleaned_data.select_dtypes(include=[np.number]).columns
                outlier_handled = 0
                
                for col in numeric_cols:
                    Q1 = cleaned_data[col].quantile(0.25)
                    Q3 = cleaned_data[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    
                    outliers_mask = (cleaned_data[col] < lower_bound) | (cleaned_data[col] > upper_bound)
                    outlier_count = outliers_mask.sum()
                    
                    if outlier_count > 0:
                        # 用中位数替换异常值
                        cleaned_data.loc[outliers_mask, col] = cleaned_data[col].median()
                        outlier_handled += outlier_count
                        processing_log.append(f"⚠️ {col}列：用中位数替换了{outlier_count}个异常值")
                
                if outlier_handled > 0:
                    processing_log.append(f"🎉 总共处理了{outlier_handled}个异常值")
            
            # 保存处理结果
            st.session_state.cleaned_data = cleaned_data
            
            # 计算处理统计
            missing_handled_total = data.isnull().sum().sum() - cleaned_data.isnull().sum().sum()
            duplicate_count_total = data.duplicated().sum()
            
            st.session_state.cleaning_results = {
                'missing_values_handled': f"处理了 {missing_handled_total} 个缺失值",
                'duplicates_removed': f"移除了 {duplicate_count_total} 行重复数据" if duplicate_count_total > 0 else "无重复数据",
                'outliers_handled': f"处理了异常值" if any("异常值" in log for log in processing_log) else "未处理异常值"
            }
            
            # 记录处理历史
            st.session_state.cleaning_history.append({
                'timestamp': pd.Timestamp.now(),
                'operations': processing_log,
                'data_shape_before': data.shape,
                'data_shape_after': cleaned_data.shape
            })
            
            st.success("✅ 数据处理完成！")
            
            # 显示处理完成提示
            st.markdown("""
            <div style="background-color: #d4edda; padding: 20px; border-radius: 10px; border: 2px solid #28a745; margin: 20px 0;">
            <h4 style="color: #155724; margin: 0 0 15px 0;">🎉 数据清洗成功完成！</h4>
            <p style="margin: 0 0 10px 0; color: #155724;">您的数据已经成功清洗，现在可以继续进行数据可视化分析了。</p>
            <p style="margin: 0; color: #155724;"><strong>处理摘要：</strong></p>
            <ul style="margin: 10px 0 0 0; padding-left: 20px; color: #155724;">
            """, unsafe_allow_html=True)
            
            for log in processing_log:
                st.markdown(f"<li>{log}</li>", unsafe_allow_html=True)
            
            st.markdown("</ul></div>", unsafe_allow_html=True)
            
            # 显示处理日志（可折叠）
            with st.expander("📋 查看详细处理日志"):
                for log in processing_log:
                    st.write(log)
    
    # 第四步：效果验证
    if st.session_state.cleaned_data is not None:
        st.markdown("### ✅ 第四步：效果验证")
        
        cleaned_data = st.session_state.cleaned_data
        
        # 计算处理后的质量评分
        total_cells_after = cleaned_data.shape[0] * cleaned_data.shape[1]
        missing_cells_after = cleaned_data.isnull().sum().sum()
        duplicate_rows_after = cleaned_data.duplicated().sum()
        
        completeness_score_after = max(0, 100 - (missing_cells_after / total_cells_after * 100))
        uniqueness_score_after = max(0, 100 - (duplicate_rows_after / len(cleaned_data) * 100))
        overall_score_after = (completeness_score_after + uniqueness_score_after) / 2
        
        # 使用标签页组织验证内容
        tab1, tab2, tab3, tab4 = st.tabs(["📊 质量评分对比", "📈 详细改善分析", "💡 智能建议", "📋 处理历史"])
        
        with tab1:
            st.markdown("#### 📊 质量评分对比")
            
            # 评分指标卡片
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div style="background-color: #e8f5e8; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #28a745;">
                <h3 style="color: #28a745; margin: 0;">{overall_score_after:.1f}</h3>
                <p style="margin: 5px 0 0 0; color: #2c3e50;">整体质量评分</p>
                <p style="margin: 2px 0 0 0; font-size: 0.8em; color: {'#28a745' if overall_score_after - overall_score >= 0 else '#dc3545'};">
                {f"+{overall_score_after - overall_score:.1f}" if overall_score_after - overall_score >= 0 else f"{overall_score_after - overall_score:.1f}"}
                </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="background-color: #e8f5e8; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #28a745;">
                <h3 style="color: #28a745; margin: 0;">{completeness_score_after:.1f}</h3>
                <p style="margin: 5px 0 0 0; color: #2c3e50;">完整性评分</p>
                <p style="margin: 2px 0 0 0; font-size: 0.8em; color: {'#28a745' if completeness_score_after - completeness_score >= 0 else '#dc3545'};">
                {f"+{completeness_score_after - completeness_score:.1f}" if completeness_score_after - completeness_score >= 0 else f"{completeness_score_after - completeness_score:.1f}"}
                </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div style="background-color: #e8f5e8; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #28a745;">
                <h3 style="color: #28a745; margin: 0;">{uniqueness_score_after:.1f}</h3>
                <p style="margin: 5px 0 0 0; color: #2c3e50;">唯一性评分</p>
                <p style="margin: 2px 0 0 0; font-size: 0.8em; color: {'#28a745' if uniqueness_score_after - uniqueness_score >= 0 else '#dc3545'};">
                {f"+{uniqueness_score_after - uniqueness_score:.1f}" if uniqueness_score_after - uniqueness_score >= 0 else f"{uniqueness_score_after - uniqueness_score:.1f}"}
                </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div style="background-color: #e8f5e8; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #28a745;">
                <h3 style="color: #28a745; margin: 0;">{cleaned_data.shape[0]}×{cleaned_data.shape[1]}</h3>
                <p style="margin: 5px 0 0 0; color: #2c3e50;">数据规模</p>
                <p style="margin: 2px 0 0 0; font-size: 0.8em; color: {'#28a745' if cleaned_data.shape[0] - data.shape[0] >= 0 else '#dc3545'};">
                {f"+{cleaned_data.shape[0] - data.shape[0]}" if cleaned_data.shape[0] - data.shape[0] >= 0 else f"{cleaned_data.shape[0] - data.shape[0]}"}行
                </p>
                </div>
                """, unsafe_allow_html=True)
            
            # 质量改善可视化
            # 创建处理前后的数据
            categories = ['整体质量', '完整性', '唯一性']
            before_scores = [overall_score, completeness_score, uniqueness_score]
            after_scores = [overall_score_after, completeness_score_after, uniqueness_score_after]
            
            # 创建数据框
            comparison_data = pd.DataFrame({
                '指标': categories * 2,
                '评分': before_scores + after_scores,
                '处理阶段': ['处理前'] * 3 + ['处理后'] * 3
            })
            
            fig = px.bar(
                comparison_data,
                x='指标',
                y='评分',
                color='处理阶段',
                title="📊 处理前后质量对比",
                barmode='group'
            )
            
            fig.update_layout(yaxis_title="评分", yaxis_range=[0, 100], barmode='group')
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.markdown("#### 📈 详细改善分析")
            
            # 处理前后对比表格
            comparison_df = pd.DataFrame({
                '指标': ['数据行数', '数据列数', '缺失值数量', '重复行数量', '整体质量评分'],
                '处理前': [data.shape[0], data.shape[1], missing_cells, duplicate_rows, f"{overall_score:.1f}"],
                '处理后': [cleaned_data.shape[0], cleaned_data.shape[1], missing_cells_after, duplicate_rows_after, f"{overall_score_after:.1f}"],
                '改善': [
                    f"{cleaned_data.shape[0] - data.shape[0]:+d}",
                    f"{cleaned_data.shape[1] - data.shape[1]:+d}",
                    f"{missing_cells_after - missing_cells:+d}",
                    f"{duplicate_rows_after - duplicate_rows:+d}",
                    f"{overall_score_after - overall_score:+.1f}"
                ]
            })
            
            st.markdown("**📊 处理前后对比：**")
            st.dataframe(comparison_df, use_container_width=True)
            
            # 改善详情分析
            st.markdown("**🔍 改善详情分析：**")
            
            improvements = []
            if missing_cells_after < missing_cells:
                improvements.append(f"✅ 缺失值减少了 {missing_cells - missing_cells_after} 个")
            if duplicate_rows_after < duplicate_rows:
                improvements.append(f"✅ 重复行减少了 {duplicate_rows - duplicate_rows_after} 行")
            if overall_score_after > overall_score:
                improvements.append(f"✅ 整体质量提升了 {overall_score_after - overall_score:.1f} 分")
            
            if improvements:
                for improvement in improvements:
                    st.success(improvement)
            else:
                st.info("ℹ️ 数据质量保持稳定，没有显著改善")
        
        with tab3:
            st.markdown("#### 💡 智能建议")
            
            # 根据质量评分提供建议
            if overall_score_after >= 90:
                st.markdown("""
                <div style="background-color: #d4edda; padding: 20px; border-radius: 10px; border: 2px solid #28a745;">
                <h4 style="color: #155724; margin: 0 0 15px 0;">🎉 数据质量优秀！</h4>
                <p style="margin: 0 0 10px 0; color: #155724;">您的数据已经达到了很高的质量标准，可以放心进行后续分析。</p>
                <ul style="margin: 0; padding-left: 20px; color: #155724;">
                <li>✅ 数据完整性良好</li>
                <li>✅ 数据唯一性良好</li>
                <li>✅ 可以继续进行数据可视化</li>
                <li>✅ 可以开始统计分析</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
            elif overall_score_after >= 70:
                st.markdown("""
                <div style="background-color: #fff3cd; padding: 20px; border-radius: 10px; border: 2px solid #ffc107;">
                <h4 style="color: #856404; margin: 0 0 15px 0;">⚠️ 数据质量良好，但仍有改进空间</h4>
                <p style="margin: 0 0 10px 0; color: #856404;">建议检查是否还有遗漏的问题，可以考虑以下改进措施：</p>
                <ul style="margin: 0; padding-left: 20px; color: #856404;">
                <li>🔍 检查是否还有未处理的异常值</li>
                <li>🔍 考虑是否需要更精细的数据清洗</li>
                <li>🔍 验证数据的一致性</li>
                <li>✅ 可以继续进行后续分析</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background-color: #f8d7da; padding: 20px; border-radius: 10px; border: 2px solid #dc3545;">
                <h4 style="color: #721c24; margin: 0 0 15px 0;">❌ 数据质量仍需改进</h4>
                <p style="margin: 0 0 10px 0; color: #721c24;">建议重新检查数据源或调整处理策略：</p>
                <ul style="margin: 0; padding-left: 20px; color: #721c24;">
                <li>🔍 检查数据源是否有问题</li>
                <li>🔍 尝试不同的处理策略</li>
                <li>🔍 考虑手动检查数据</li>
                <li>⚠️ 建议在继续分析前解决数据质量问题</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
        
        with tab4:
            st.markdown("#### 📋 处理历史")
            
            if st.session_state.cleaning_history:
                st.markdown("**🕒 数据清洗操作历史：**")
                
                for i, history in enumerate(reversed(st.session_state.cleaning_history), 1):
                    with st.expander(f"📋 第{len(st.session_state.cleaning_history) - i + 1}次处理 - {history['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"):
                        st.markdown(f"**📊 数据规模变化：** {history['data_shape_before']} → {history['data_shape_after']}")
                        st.markdown("**🔧 执行的操作：**")
                        for operation in history['operations']:
                            st.write(f"• {operation}")
            else:
                st.info("ℹ️ 暂无处理历史记录")
    
    # 检查是否已完成数据清洗，如果是则显示下一步按钮
    if st.session_state.cleaned_data is not None:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="background-color: #e8f5e8; padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #28a745;">
            <h4 style="color: #28a745; margin: 0 0 15px 0;">🚀 准备就绪！</h4>
            <p style="margin: 0; color: #2c3e50;">数据清洗已完成，点击下方按钮继续下一步</p>
            </div>
            """, unsafe_allow_html=True)
    
    # AI智能助手功能
    st.markdown("---")
    st.markdown("### 🤖 AI智能学习助手")
    
    # 获取AI助手实例
    ai_assistant = get_beginner_ai_assistant()
    
    if ai_assistant:
        # 获取当前数据上下文
        data_context = f"当前数据集包含{len(data)}行{len(data.columns)}列数据，包含以下列：{', '.join(data.columns[:5])}{'...' if len(data.columns) > 5 else ''}"
        
        # 添加清洗结果上下文
        if st.session_state.cleaned_data is not None:
            cleaned_data = st.session_state.cleaned_data
            data_context += f"。清洗后数据包含{len(cleaned_data)}行{len(cleaned_data.columns)}列。"
        
        # 预设问题选择
        st.markdown("**💡 常见问题：**")
        preset_questions = ai_assistant.get_preset_questions("data_cleaning")
        
        col1, col2 = st.columns(2)
        with col1:
            selected_preset = st.selectbox(
                "选择预设问题：",
                ["自定义问题"] + preset_questions,
                key="cleaning_preset_question"
            )
        
        with col2:
            if selected_preset == "自定义问题":
                user_question = st.text_input(
                    "输入您的问题：",
                    placeholder="例如：如何处理缺失值？",
                    key="cleaning_custom_question"
                )
            else:
                user_question = selected_preset
        
        # AI回答按钮
        if st.button("🤖 获取AI回答", key="cleaning_ai_answer") and user_question.strip():
            with st.spinner("AI导师正在思考..."):
                try:
                    answer = ai_assistant.answer_beginner_question(
                        user_question,
                        "数据清洗页面",
                        data_context
                    )
                    
                    st.success("✅ AI导师回答完成！")
                    st.markdown("### 🤖 AI导师回答")
                    st.markdown(answer)
                    
                except Exception as e:
                    st.error(f"❌ AI回答失败：{str(e)}")
        
        # 学习指导按钮
        if st.button("📚 获取学习指导", key="cleaning_guidance"):
            with st.spinner("AI导师正在为您制定学习计划..."):
                try:
                    guidance = ai_assistant.provide_learning_guidance(
                        "数据清洗页面",
                        {"step": 3, "status": "processing", "data_shape": data.shape}
                    )
                    
                    st.success("✅ 学习指导生成完成！")
                    st.markdown("### 📚 个性化学习指导")
                    st.markdown(guidance)
                    
                except Exception as e:
                    st.error(f"❌ 学习指导生成失败：{str(e)}")
        
        # 概念解释按钮
        if st.button("📖 概念解释", key="cleaning_concept"):
            concept = st.selectbox(
                "选择要解释的概念：",
                ["数据清洗", "缺失值处理", "重复值处理", "异常值检测", "数据质量评估"],
                key="cleaning_concept_select"
            )
            
            if st.button("🔍 解释概念", key="cleaning_explain"):
                with st.spinner("AI导师正在解释..."):
                    try:
                        explanation = ai_assistant.explain_concept(
                            concept,
                            "数据清洗页面"
                        )
                        
                        st.success("✅ 概念解释完成！")
                        st.markdown("### 📖 概念解释")
                        st.markdown(explanation)
                        
                    except Exception as e:
                        st.error(f"❌ 概念解释失败：{str(e)}")
    else:
        st.warning("⚠️ AI助手暂时不可用，请检查网络连接或API配置")
    
    # 继续按钮
    if st.button("➡️ 继续下一步：数据可视化", type="primary", use_container_width=True, key="auto_next_step"):
        st.session_state.current_step = 5
        st.rerun()
    
    # 返回按钮
    if st.button("⬅️ 返回", key="back_to_structure"):
        st.session_state.current_step = 3
        st.rerun()

def display_visualization():
    """数据可视化界面 - 优化版本"""
    st.markdown('<h2 class="section-header">📊 第四步：数据可视化</h2>', unsafe_allow_html=True)
    
    data = st.session_state.cleaned_data if st.session_state.cleaned_data is not None else st.session_state.data
    
    # 初始化可视化结果
    if 'visualization_results' not in st.session_state:
        st.session_state.visualization_results = {'chart_types': [], 'insights': [], 'charts': {}}
    elif 'chart_types' not in st.session_state.visualization_results:
        st.session_state.visualization_results['chart_types'] = []
    elif 'insights' not in st.session_state.visualization_results:
        st.session_state.visualization_results['insights'] = []
    elif 'charts' not in st.session_state.visualization_results:
        st.session_state.visualization_results['charts'] = {}
    
    if data is None:
        st.error("❌ 没有数据，请先上传数据")
        st.session_state.current_step = 2
        st.rerun()
    
    # 数据概览
    st.markdown("""
    <div class="info-box">
    <h4>📊 数据可视化的重要性：</h4>
    <p>可视化是理解数据分布、关系和趋势的重要工具。选择合适的图表类型能够帮助我们更好地理解数据。</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 数据概览卡片
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 数据行数", f"{len(data):,}")
    with col2:
        st.metric("📋 数据列数", f"{len(data.columns)}")
    with col3:
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        st.metric("🔢 数值型变量", len(numeric_cols))
    with col4:
        categorical_cols = data.select_dtypes(include=['object']).columns
        st.metric("📝 分类型变量", len(categorical_cols))
    
    # 图表类型选择
    st.subheader("📈 选择可视化类型")
    
    chart_type = st.selectbox(
        "选择图表类型：",
        [
            "📊 直方图 - 查看数据分布",
            "📈 箱线图 - 查看数据分布和异常值",
            "🔄 散点图 - 查看两个变量关系",
            "📊 条形图 - 查看分类数据",
            "🌊 热力图 - 查看相关性矩阵",
            "📈 折线图 - 查看趋势变化",
            "🎯 饼图 - 查看比例分布",
            "📊 多变量分析 - 综合视图"
        ]
    )
    
    # 创建标签页组织内容
    tab1, tab2, tab3 = st.tabs(["📊 图表展示", "💡 数据洞察", "📋 可视化历史"])
    
    with tab1:
        # 根据图表类型显示相应的可视化
        if "直方图" in chart_type:
            st.markdown("""
            <div class="step-box">
            <h4>📊 直方图说明：</h4>
            <p>直方图用于显示数值型数据的分布情况，帮助了解数据的集中趋势和离散程度。</p>
            </div>
            """, unsafe_allow_html=True)
            
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                col1, col2 = st.columns(2)
                with col1:
                    selected_col = st.selectbox("选择要绘制的列：", numeric_cols)
                with col2:
                    nbins = st.slider("选择分组数量：", min_value=5, max_value=50, value=20)
                
                if selected_col:
                    fig = px.histogram(
                        data, 
                        x=selected_col,
                        title=f"{selected_col} 的分布直方图",
                        nbins=nbins,
                        marginal="box"
                    )
                    fig.update_layout(
                        xaxis_title=selected_col,
                        yaxis_title="频数",
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # 添加统计信息
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("均值", f"{data[selected_col].mean():.2f}")
                    with col2:
                        st.metric("中位数", f"{data[selected_col].median():.2f}")
                    with col3:
                        st.metric("标准差", f"{data[selected_col].std():.2f}")
                    with col4:
                        st.metric("偏度", f"{data[selected_col].skew():.2f}")
                    
                    # 记录可视化结果
                    if '直方图' not in st.session_state.visualization_results['chart_types']:
                        st.session_state.visualization_results['chart_types'].append('直方图')
        
        elif "箱线图" in chart_type:
            st.markdown("""
            <div class="step-box">
            <h4>📈 箱线图说明：</h4>
            <p>箱线图用于显示数据的分布特征，包括中位数、四分位数和异常值。</p>
            </div>
            """, unsafe_allow_html=True)
            
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                selected_col = st.selectbox("选择要绘制的列：", numeric_cols)
                
                if selected_col:
                    fig = px.box(
                        data, 
                        y=selected_col,
                        title=f"{selected_col} 的箱线图",
                        points="outliers"
                    )
                    fig.update_layout(
                        yaxis_title=selected_col,
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # 添加统计信息
                    Q1 = data[selected_col].quantile(0.25)
                    Q3 = data[selected_col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    outliers = data[(data[selected_col] < lower_bound) | (data[selected_col] > upper_bound)]
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Q1 (25%)", f"{Q1:.2f}")
                    with col2:
                        st.metric("Q3 (75%)", f"{Q3:.2f}")
                    with col3:
                        st.metric("IQR", f"{IQR:.2f}")
                    with col4:
                        st.metric("异常值数量", len(outliers))
                    
                    # 记录可视化结果
                    if '箱线图' not in st.session_state.visualization_results['chart_types']:
                        st.session_state.visualization_results['chart_types'].append('箱线图')
        
        elif "散点图" in chart_type:
            st.markdown("""
            <div class="step-box">
            <h4>🔄 散点图说明：</h4>
            <p>散点图用于显示两个数值型变量之间的关系，帮助发现相关性。</p>
            </div>
            """, unsafe_allow_html=True)
            
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) >= 2:
                col1, col2, col3 = st.columns(3)
                with col1:
                    x_col = st.selectbox("选择X轴变量：", numeric_cols)
                with col2:
                    y_col = st.selectbox("选择Y轴变量：", [col for col in numeric_cols if col != x_col])
                with col3:
                    color_col = st.selectbox("选择颜色变量（可选）：", ["无"] + list(data.columns))
                
                if x_col and y_col:
                    if color_col != "无":
                        fig = px.scatter(
                            data, 
                            x=x_col, 
                            y=y_col,
                            color=color_col,
                            title=f"{x_col} vs {y_col} 散点图",
                            trendline="ols"
                        )
                    else:
                        fig = px.scatter(
                            data, 
                            x=x_col, 
                            y=y_col,
                            title=f"{x_col} vs {y_col} 散点图",
                            trendline="ols"
                        )
                    
                    fig.update_layout(
                        xaxis_title=x_col,
                        yaxis_title=y_col
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # 计算相关系数
                    correlation = data[x_col].corr(data[y_col])
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("相关系数", f"{correlation:.3f}")
                    with col2:
                        st.metric("X轴均值", f"{data[x_col].mean():.2f}")
                    with col3:
                        st.metric("Y轴均值", f"{data[y_col].mean():.2f}")
                    
                    # 相关性解释
                    if abs(correlation) > 0.7:
                        st.success(f"💡 强相关关系：{x_col} 和 {y_col} 存在强相关关系 (r = {correlation:.3f})")
                    elif abs(correlation) > 0.3:
                        st.info(f"💡 中等相关关系：{x_col} 和 {y_col} 存在中等相关关系 (r = {correlation:.3f})")
                    else:
                        st.warning(f"💡 弱相关关系：{x_col} 和 {y_col} 相关关系较弱 (r = {correlation:.3f})")
                    
                    # 记录可视化结果
                    if '散点图' not in st.session_state.visualization_results['chart_types']:
                        st.session_state.visualization_results['chart_types'].append('散点图')
        
        elif "条形图" in chart_type:
            st.markdown("""
            <div class="step-box">
            <h4>📊 条形图说明：</h4>
            <p>条形图用于显示分类数据的频数分布，帮助比较不同类别的数量。</p>
            </div>
            """, unsafe_allow_html=True)
            
            categorical_cols = data.select_dtypes(include=['object']).columns
            if len(categorical_cols) > 0:
                selected_col = st.selectbox("选择要绘制的列：", categorical_cols)
                
                if selected_col:
                    # 计算频数
                    value_counts = data[selected_col].value_counts()
                    
                    fig = px.bar(
                        x=value_counts.index,
                        y=value_counts.values,
                        title=f"{selected_col} 的频数分布",
                        labels={'x': selected_col, 'y': '频数'}
                    )
                    fig.update_layout(
                        xaxis_title=selected_col,
                        yaxis_title="频数",
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # 显示统计信息
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("类别数量", len(value_counts))
                    with col2:
                        st.metric("最多频数", value_counts.max())
                    with col3:
                        st.metric("最少频数", value_counts.min())
                    
                    # 显示频数表格
                    st.markdown("**📋 详细频数统计：**")
                    freq_df = pd.DataFrame({
                        '类别': value_counts.index,
                        '频数': value_counts.values,
                        '比例(%)': (value_counts.values / len(data) * 100).round(2)
                    })
                    st.dataframe(freq_df, use_container_width=True)
                    
                    # 记录可视化结果
                    if '条形图' not in st.session_state.visualization_results['chart_types']:
                        st.session_state.visualization_results['chart_types'].append('条形图')
        
        elif "热力图" in chart_type:
            st.markdown("""
            <div class="step-box">
            <h4>🌊 热力图说明：</h4>
            <p>热力图用于显示多个变量之间的相关性，颜色越深表示相关性越强。</p>
            </div>
            """, unsafe_allow_html=True)
            
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 1:
                # 计算相关性矩阵
                corr_matrix = data[numeric_cols].corr()
                
                fig = px.imshow(
                    corr_matrix,
                    title="变量相关性热力图",
                    color_continuous_scale='RdBu',
                    aspect='auto',
                    text_auto=True
                )
                fig.update_layout(
                    xaxis_title="变量",
                    yaxis_title="变量"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # 显示强相关变量对
                strong_corr = []
                for i in range(len(corr_matrix.columns)):
                    for j in range(i+1, len(corr_matrix.columns)):
                        corr_value = corr_matrix.iloc[i, j]
                        if abs(corr_value) > 0.7:
                            strong_corr.append({
                                '变量1': corr_matrix.columns[i],
                                '变量2': corr_matrix.columns[j],
                                '相关系数': corr_value
                            })
                
                if strong_corr:
                    st.markdown("**🔗 强相关变量对 (|r| > 0.7)：**")
                    strong_corr_df = pd.DataFrame(strong_corr)
                    st.dataframe(strong_corr_df.round(3), use_container_width=True)
                
                # 记录可视化结果
                if '热力图' not in st.session_state.visualization_results['chart_types']:
                    st.session_state.visualization_results['chart_types'].append('热力图')
        
        elif "折线图" in chart_type:
            st.markdown("""
            <div class="step-box">
            <h4>📈 折线图说明：</h4>
            <p>折线图用于显示数据随时间或其他连续变量的变化趋势。</p>
            </div>
            """, unsafe_allow_html=True)
            
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                col1, col2 = st.columns(2)
                with col1:
                    y_col = st.selectbox("选择Y轴变量：", numeric_cols)
                with col2:
                    x_col = st.selectbox("选择X轴变量：", ["索引"] + list(data.columns))
                
                if y_col:
                    if x_col == "索引":
                        x_data = range(len(data))
                        x_title = "数据索引"
                    else:
                        x_data = data[x_col]
                        x_title = x_col
                    
                    fig = px.line(
                        x=x_data,
                        y=data[y_col],
                        title=f"{y_col} 的变化趋势",
                        labels={'x': x_title, 'y': y_col}
                    )
                    fig.update_layout(
                        xaxis_title=x_title,
                        yaxis_title=y_col,
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # 记录可视化结果
                    if '折线图' not in st.session_state.visualization_results['chart_types']:
                        st.session_state.visualization_results['chart_types'].append('折线图')
        
        elif "饼图" in chart_type:
            st.markdown("""
            <div class="step-box">
            <h4>🎯 饼图说明：</h4>
            <p>饼图用于显示分类数据的比例分布，直观展示各部分占总体的比例。</p>
            </div>
            """, unsafe_allow_html=True)
            
            categorical_cols = data.select_dtypes(include=['object']).columns
            if len(categorical_cols) > 0:
                selected_col = st.selectbox("选择要绘制的列：", categorical_cols)
                
                if selected_col:
                    value_counts = data[selected_col].value_counts()
                    
                    # 如果类别太多，只显示前10个
                    if len(value_counts) > 10:
                        top_values = value_counts.head(10)
                        other_count = value_counts.iloc[10:].sum()
                        plot_data = pd.concat([top_values, pd.Series([other_count], index=['其他'])])
                    else:
                        plot_data = value_counts
                    
                    fig = px.pie(
                        values=plot_data.values,
                        names=plot_data.index,
                        title=f"{selected_col} 的比例分布"
                    )
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # 记录可视化结果
                    if '饼图' not in st.session_state.visualization_results['chart_types']:
                        st.session_state.visualization_results['chart_types'].append('饼图')
        
        elif "多变量分析" in chart_type:
            st.markdown("""
            <div class="step-box">
            <h4>📊 多变量分析说明：</h4>
            <p>多变量分析提供数据的综合视图，包括分布、相关性和统计摘要。</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 创建多变量分析视图
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                # 选择要分析的变量
                selected_cols = st.multiselect(
                    "选择要分析的数值变量：",
                    numeric_cols,
                    default=numeric_cols[:min(5, len(numeric_cols))]
                )
                
                if selected_cols:
                    # 创建子图
                    import plotly.graph_objects as go
                    from plotly.subplots import make_subplots
                    
                    n_cols = len(selected_cols)
                    fig = make_subplots(
                        rows=2, cols=n_cols,
                        subplot_titles=selected_cols,
                        specs=[[{"secondary_y": False}] * n_cols,
                               [{"secondary_y": False}] * n_cols]
                    )
                    
                    for i, col in enumerate(selected_cols, 1):
                        # 直方图
                        fig.add_trace(
                            go.Histogram(x=data[col], name=f"{col}_hist"),
                            row=1, col=i
                        )
                        # 箱线图
                        fig.add_trace(
                            go.Box(y=data[col], name=f"{col}_box"),
                            row=2, col=i
                        )
                    
                    fig.update_layout(
                        height=600,
                        title_text="多变量分析视图",
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # 统计摘要
                    st.markdown("**📊 统计摘要：**")
                    summary_stats = data[selected_cols].describe()
                    st.dataframe(summary_stats.round(2), use_container_width=True)
                    
                    # 记录可视化结果
                    if '多变量分析' not in st.session_state.visualization_results['chart_types']:
                        st.session_state.visualization_results['chart_types'].append('多变量分析')
    
    with tab2:
        st.markdown("### 💡 数据洞察")
        
        # 自动生成数据洞察
        insights = []
        
        # 数值型变量洞察
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            for col in numeric_cols:
                mean_val = data[col].mean()
                std_val = data[col].std()
                skew_val = data[col].skew()
                
                insights.append(f"📊 **{col}**: 均值={mean_val:.2f}, 标准差={std_val:.2f}")
                
                if abs(skew_val) > 1:
                    insights.append(f"   - 分布偏斜 (偏度={skew_val:.2f})")
                
                # 异常值检测
                Q1 = data[col].quantile(0.25)
                Q3 = data[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = data[(data[col] < Q1 - 1.5*IQR) | (data[col] > Q3 + 1.5*IQR)]
                if len(outliers) > 0:
                    insights.append(f"   - 发现 {len(outliers)} 个异常值")
        
        # 相关性洞察
        if len(numeric_cols) > 1:
            corr_matrix = data[numeric_cols].corr()
            strong_corr = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_value = corr_matrix.iloc[i, j]
                    if abs(corr_value) > 0.7:
                        strong_corr.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_value))
            
            if strong_corr:
                insights.append("🔗 **强相关关系发现：**")
                for var1, var2, corr in strong_corr:
                    insights.append(f"   - {var1} 与 {var2}: r = {corr:.3f}")
        
        # 分类变量洞察
        categorical_cols = data.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            for col in categorical_cols:
                unique_count = data[col].nunique()
                insights.append(f"📝 **{col}**: {unique_count} 个不同类别")
                
                if unique_count <= 10:
                    value_counts = data[col].value_counts()
                    most_common = value_counts.index[0]
                    most_common_pct = (value_counts.iloc[0] / len(data) * 100)
                    insights.append(f"   - 最常见类别: {most_common} ({most_common_pct:.1f}%)")
        
        # 显示洞察
        if insights:
            for insight in insights:
                st.write(insight)
        else:
            st.info("💡 暂无数据洞察")
        
        # 保存洞察
        if insights and insights not in st.session_state.visualization_results['insights']:
            st.session_state.visualization_results['insights'].extend(insights)
    
    with tab3:
        st.markdown("### 📋 可视化历史")
        
        if st.session_state.visualization_results['chart_types']:
            st.markdown("**已创建的图表类型：**")
            for chart_type in st.session_state.visualization_results['chart_types']:
                st.write(f"✅ {chart_type}")
        else:
            st.info("📋 暂无可视化历史")
        
        # 清除历史按钮
        if st.button("🗑️ 清除可视化历史"):
            st.session_state.visualization_results = {'chart_types': [], 'insights': [], 'charts': {}}
            st.rerun()
    
    # AI智能助手功能
    st.markdown("---")
    st.markdown("### 🤖 AI智能学习助手")
    
    # 获取AI助手实例
    ai_assistant = get_beginner_ai_assistant()
    
    if ai_assistant:
        # 获取当前数据上下文
        data_context = f"当前数据集包含{len(data)}行{len(data.columns)}列数据，包含以下列：{', '.join(data.columns[:5])}{'...' if len(data.columns) > 5 else ''}。数值型变量：{len(data.select_dtypes(include=[np.number]).columns)}个，分类型变量：{len(data.select_dtypes(include=['object']).columns)}个。"
        
        # 添加可视化历史上下文
        if st.session_state.visualization_results['chart_types']:
            data_context += f"已创建的可视化图表：{', '.join(st.session_state.visualization_results['chart_types'])}。"
        
        # 预设问题选择
        st.markdown("**💡 常见问题：**")
        preset_questions = ai_assistant.get_preset_questions("visualization")
        
        col1, col2 = st.columns(2)
        with col1:
            selected_preset = st.selectbox(
                "选择预设问题：",
                ["自定义问题"] + preset_questions,
                key="visualization_preset_question"
            )
        
        with col2:
            if selected_preset == "自定义问题":
                user_question = st.text_input(
                    "输入您的问题：",
                    placeholder="例如：什么时候用柱状图？",
                    key="visualization_custom_question"
                )
            else:
                user_question = selected_preset
        
        # AI回答按钮
        if st.button("🤖 获取AI回答", key="visualization_ai_answer") and user_question.strip():
            with st.spinner("AI导师正在思考..."):
                try:
                    answer = ai_assistant.answer_beginner_question(
                        user_question,
                        "数据可视化页面",
                        data_context
                    )
                    
                    st.success("✅ AI导师回答完成！")
                    st.markdown("### 🤖 AI导师回答")
                    st.markdown(answer)
                    
                except Exception as e:
                    st.error(f"❌ AI回答失败：{str(e)}")
        
        # 学习指导按钮
        if st.button("📚 获取学习指导", key="visualization_guidance"):
            with st.spinner("AI导师正在为您制定学习计划..."):
                try:
                    guidance = ai_assistant.provide_learning_guidance(
                        "数据可视化页面",
                        {"step": 4, "status": "visualizing", "data_shape": data.shape, "chart_types": st.session_state.visualization_results['chart_types']}
                    )
                    
                    st.success("✅ 学习指导生成完成！")
                    st.markdown("### 📚 个性化学习指导")
                    st.markdown(guidance)
                    
                except Exception as e:
                    st.error(f"❌ 学习指导生成失败：{str(e)}")
        
        # 概念解释按钮
        if st.button("📖 概念解释", key="visualization_concept"):
            concept = st.selectbox(
                "选择要解释的概念：",
                ["数据可视化", "直方图", "箱线图", "散点图", "条形图", "热力图", "折线图", "饼图"],
                key="visualization_concept_select"
            )
            
            if st.button("🔍 解释概念", key="visualization_explain"):
                with st.spinner("AI导师正在解释..."):
                    try:
                        explanation = ai_assistant.explain_concept(
                            concept,
                            "数据可视化页面"
                        )
                        
                        st.success("✅ 概念解释完成！")
                        st.markdown("### 📖 概念解释")
                        st.markdown(explanation)
                        
                    except Exception as e:
                        st.error(f"❌ 概念解释失败：{str(e)}")
    else:
        st.warning("⚠️ AI助手暂时不可用，请检查网络连接或API配置")
    
    # 继续按钮
    if st.button("➡️ 继续下一步：统计分析", use_container_width=True):
        st.session_state.current_step = 6
        st.rerun()
    
    # 返回按钮
    if st.button("⬅️ 返回", key="back_to_cleaning"):
        st.session_state.current_step = 4
        st.rerun()

def display_statistical_analysis():
    """统计分析界面"""
    st.markdown('<h2 class="section-header">📈 第五步：统计分析</h2>', unsafe_allow_html=True)
    
    data = st.session_state.cleaned_data if st.session_state.cleaned_data is not None else st.session_state.data
    
    # 初始化分析结果
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = {
            'descriptive_stats': {},
            'correlation_analysis': {},
            'grouped_analysis': {}
        }
    else:
        # 确保所有必需的键都存在
        if 'descriptive_stats' not in st.session_state.analysis_results:
            st.session_state.analysis_results['descriptive_stats'] = {}
        if 'correlation_analysis' not in st.session_state.analysis_results:
            st.session_state.analysis_results['correlation_analysis'] = {}
        if 'grouped_analysis' not in st.session_state.analysis_results:
            st.session_state.analysis_results['grouped_analysis'] = {}
    
    if data is None:
        st.error("❌ 没有数据，请先上传数据")
        st.session_state.current_step = 2
        st.rerun()
    
    st.markdown("""
    <div class="info-box">
    <h4>📈 统计分析的重要性：</h4>
    <p>统计分析帮助我们理解数据的特征、分布和关系，为后续的决策提供数据支持。</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 描述性统计分析
    st.subheader("📊 描述性统计分析")
    
    # 数值型数据的描述性统计
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) > 0:
        st.markdown("**数值型变量描述性统计：**")
        desc_stats = data[numeric_cols].describe()
        st.dataframe(desc_stats, use_container_width=True)
    
    # 相关性分析
    st.subheader("🔗 相关性分析")
    
    if len(numeric_cols) > 1:
        st.markdown("""
        <div class="step-box">
        <h4>🔗 相关性分析说明：</h4>
        <p>相关性分析用于衡量两个变量之间的线性关系强度。相关系数范围在 -1 到 1 之间。</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 计算相关性矩阵
        corr_matrix = data[numeric_cols].corr()
        
        # 显示相关性矩阵
        st.markdown("**相关性矩阵：**")
        st.dataframe(corr_matrix.round(3), use_container_width=True)
        
        # 找出强相关的变量对
        strong_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:
                    strong_corr.append({
                        '变量1': corr_matrix.columns[i],
                        '变量2': corr_matrix.columns[j],
                        '相关系数': corr_value
                    })
        
        if strong_corr:
            st.markdown("**强相关变量对 (|r| > 0.7)：**")
            strong_corr_df = pd.DataFrame(strong_corr)
            st.dataframe(strong_corr_df.round(3), use_container_width=True)
        else:
            st.info("💡 没有发现强相关的变量对 (|r| > 0.7)")
    
    # 完成分析
    st.markdown("""
    <div class="success-box">
    <h4>🎉 恭喜！您已完成基础数据分析！</h4>
    <p>您已经学会了数据上传、清洗、可视化和统计分析的基本技能。</p>
    </div>
    """, unsafe_allow_html=True)
    
    # AI智能助手功能
    st.markdown("---")
    st.markdown("### 🤖 AI智能学习助手")
    
    # 获取AI助手实例
    ai_assistant = get_beginner_ai_assistant()
    
    if ai_assistant:
        # 获取当前数据上下文
        data_context = f"当前数据集包含{len(data)}行{len(data.columns)}列数据，包含以下列：{', '.join(data.columns[:5])}{'...' if len(data.columns) > 5 else ''}。数值型变量：{len(data.select_dtypes(include=[np.number]).columns)}个。"
        
        # 添加统计分析结果上下文
        if len(numeric_cols) > 1:
            corr_matrix = data[numeric_cols].corr()
            strong_corr = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_value = corr_matrix.iloc[i, j]
                    if abs(corr_value) > 0.7:
                        strong_corr.append(f"{corr_matrix.columns[i]}和{corr_matrix.columns[j]}({corr_value:.2f})")
            
            if strong_corr:
                data_context += f"发现强相关变量对：{', '.join(strong_corr[:3])}。"
        
        # 预设问题选择
        st.markdown("**💡 常见问题：**")
        preset_questions = ai_assistant.get_preset_questions("statistical_analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            selected_preset = st.selectbox(
                "选择预设问题：",
                ["自定义问题"] + preset_questions,
                key="analysis_preset_question"
            )
        
        with col2:
            if selected_preset == "自定义问题":
                user_question = st.text_input(
                    "输入您的问题：",
                    placeholder="例如：什么是描述性统计？",
                    key="analysis_custom_question"
                )
            else:
                user_question = selected_preset
        
        # AI回答按钮
        if st.button("🤖 获取AI回答", key="analysis_ai_answer") and user_question.strip():
            with st.spinner("AI导师正在思考..."):
                try:
                    answer = ai_assistant.answer_beginner_question(
                        user_question,
                        "统计分析页面",
                        data_context
                    )
                    
                    st.success("✅ AI导师回答完成！")
                    st.markdown("### 🤖 AI导师回答")
                    st.markdown(answer)
                    
                except Exception as e:
                    st.error(f"❌ AI回答失败：{str(e)}")
        
        # 学习指导按钮
        if st.button("📚 获取学习指导", key="analysis_guidance"):
            with st.spinner("AI导师正在为您制定学习计划..."):
                try:
                    guidance = ai_assistant.provide_learning_guidance(
                        "统计分析页面",
                        {"step": 5, "status": "analyzing", "data_shape": data.shape, "numeric_cols": len(numeric_cols)}
                    )
                    
                    st.success("✅ 学习指导生成完成！")
                    st.markdown("### 📚 个性化学习指导")
                    st.markdown(guidance)
                    
                except Exception as e:
                    st.error(f"❌ 学习指导生成失败：{str(e)}")
        
        # 概念解释按钮
        if st.button("📖 概念解释", key="analysis_concept"):
            concept = st.selectbox(
                "选择要解释的概念：",
                ["描述性统计", "相关性分析", "均值", "中位数", "标准差", "相关系数"],
                key="analysis_concept_select"
            )
            
            if st.button("🔍 解释概念", key="analysis_explain"):
                with st.spinner("AI导师正在解释..."):
                    try:
                        explanation = ai_assistant.explain_concept(
                            concept,
                            "统计分析页面"
                        )
                        
                        st.success("✅ 概念解释完成！")
                        st.markdown("### 📖 概念解释")
                        st.markdown(explanation)
                        
                    except Exception as e:
                        st.error(f"❌ 概念解释失败：{str(e)}")
    else:
        st.warning("⚠️ AI助手暂时不可用，请检查网络连接或API配置")
    
    # 生成分析报告
    if st.button("📄 生成分析报告", use_container_width=True):
        st.session_state.analysis_complete = True
        st.session_state.current_step = 7
        st.rerun()
    
    # 返回按钮
    if st.button("⬅️ 返回", key="back_to_viz"):
        st.session_state.current_step = 5
        st.rerun()

def display_report():
    """显示分析报告"""
    st.markdown('<h2 class="section-header">📄 分析报告</h2>', unsafe_allow_html=True)
    
    data = st.session_state.cleaned_data if st.session_state.cleaned_data is not None else st.session_state.data
    
    if data is None:
        st.error("❌ 没有数据，无法生成报告")
        st.session_state.current_step = 2
        st.rerun()
    
    st.markdown("""
    <div class="success-box">
    <h4>📄 数据分析报告</h4>
    <p>以下是您完成的数据分析总结报告。</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 报告内容
    st.subheader("📊 数据集概览")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("数据行数", len(data))
    with col2:
        st.metric("数据列数", len(data.columns))
    with col3:
        st.metric("数值型变量", len(data.select_dtypes(include=[np.number]).columns))
    with col4:
        st.metric("分类型变量", len(data.select_dtypes(include=['object']).columns))
    
    # 数据质量报告
    st.subheader("🔍 数据质量报告")
    
    missing_data = data.isnull().sum()
    missing_percent = (missing_data / len(data) * 100).round(2)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**缺失值情况：**")
        if missing_data.sum() > 0:
            missing_df = pd.DataFrame({
                '变量': missing_data.index,
                '缺失值数量': missing_data.values,
                '缺失值比例(%)': missing_percent.values
            })
            st.dataframe(missing_df[missing_df['缺失值数量'] > 0], use_container_width=True)
        else:
            st.success("✅ 无缺失值")
    
    with col2:
        st.markdown("**重复值情况：**")
        duplicate_count = data.duplicated().sum()
        if duplicate_count > 0:
            st.warning(f"⚠️ 发现 {duplicate_count} 行重复数据")
        else:
            st.success("✅ 无重复值")
    
    # 主要发现
    st.subheader("🔍 主要发现")
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) > 0:
        # 数值型变量的主要统计
        desc_stats = data[numeric_cols].describe()
        
        st.markdown("**数值型变量统计摘要：**")
        st.dataframe(desc_stats.round(2), use_container_width=True)
        
        # 相关性发现
        if len(numeric_cols) > 1:
            corr_matrix = data[numeric_cols].corr()
            
            # 找出最强的相关性
            max_corr = 0
            max_corr_pair = None
            
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_value = abs(corr_matrix.iloc[i, j])
                    if corr_value > max_corr:
                        max_corr = corr_value
                        max_corr_pair = (corr_matrix.columns[i], corr_matrix.columns[j], corr_matrix.iloc[i, j])
            
            if max_corr_pair:
                st.markdown(f"**最强相关性：** {max_corr_pair[0]} 和 {max_corr_pair[1]} 的相关系数为 {max_corr_pair[2]:.3f}")
    
    # 建议
    st.subheader("💡 分析建议")
    
    st.markdown("""
    <div class="info-box">
    <h4>📋 后续分析建议：</h4>
    <ul>
    <li><strong>深入分析</strong>：根据发现的模式进行更深入的统计分析</li>
    <li><strong>假设检验</strong>：使用统计检验验证发现的模式是否显著</li>
    <li><strong>预测建模</strong>：基于相关性分析建立预测模型</li>
    <li><strong>数据收集</strong>：根据分析结果收集更多相关数据</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # 重新开始按钮
    if st.button("🔄 重新开始分析", use_container_width=True):
        st.session_state.current_step = 1
        st.session_state.data = None
        st.session_state.cleaned_data = None
        st.session_state.analysis_complete = False
        st.rerun()
    
    # AI智能助手功能
    st.markdown("---")
    st.markdown("### 🤖 AI智能学习助手")
    
    # 获取AI助手实例
    ai_assistant = get_beginner_ai_assistant()
    
    if ai_assistant:
        # 获取当前数据上下文
        data_context = f"当前数据集包含{len(data)}行{len(data.columns)}列数据，包含以下列：{', '.join(data.columns[:5])}{'...' if len(data.columns) > 5 else ''}。数值型变量：{len(data.select_dtypes(include=[np.number]).columns)}个，分类型变量：{len(data.select_dtypes(include=['object']).columns)}个。"
        
        # 添加分析结果上下文
        if len(numeric_cols) > 1:
            corr_matrix = data[numeric_cols].corr()
            max_corr = 0
            max_corr_pair = None
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_value = abs(corr_matrix.iloc[i, j])
                    if corr_value > max_corr:
                        max_corr = corr_value
                        max_corr_pair = (corr_matrix.columns[i], corr_matrix.columns[j], corr_matrix.iloc[i, j])
            
            if max_corr_pair:
                data_context += f"发现最强相关性：{max_corr_pair[0]}和{max_corr_pair[1]}的相关系数为{max_corr_pair[2]:.3f}。"
        
        # 预设问题选择
        st.markdown("**💡 常见问题：**")
        preset_questions = ai_assistant.get_preset_questions("report")
        
        col1, col2 = st.columns(2)
        with col1:
            selected_preset = st.selectbox(
                "选择预设问题：",
                ["自定义问题"] + preset_questions,
                key="report_preset_question"
            )
        
        with col2:
            if selected_preset == "自定义问题":
                user_question = st.text_input(
                    "输入您的问题：",
                    placeholder="例如：如何写数据分析报告？",
                    key="report_custom_question"
                )
            else:
                user_question = selected_preset
        
        # AI回答按钮
        if st.button("🤖 获取AI回答", key="report_ai_answer") and user_question.strip():
            with st.spinner("AI导师正在思考..."):
                try:
                    answer = ai_assistant.answer_beginner_question(
                        user_question,
                        "分析报告页面",
                        data_context
                    )
                    
                    st.success("✅ AI导师回答完成！")
                    st.markdown("### 🤖 AI导师回答")
                    st.markdown(answer)
                    
                except Exception as e:
                    st.error(f"❌ AI回答失败：{str(e)}")
        
        # 学习指导按钮
        if st.button("📚 获取学习指导", key="report_guidance"):
            with st.spinner("AI导师正在为您制定学习计划..."):
                try:
                    guidance = ai_assistant.provide_learning_guidance(
                        "分析报告页面",
                        {"step": 6, "status": "completed", "data_shape": data.shape, "analysis_complete": True}
                    )
                    
                    st.success("✅ 学习指导生成完成！")
                    st.markdown("### 📚 个性化学习指导")
                    st.markdown(guidance)
                    
                except Exception as e:
                    st.error(f"❌ 学习指导生成失败：{str(e)}")
        
        # 概念解释按钮
        if st.button("📖 概念解释", key="report_concept"):
            concept = st.selectbox(
                "选择要解释的概念：",
                ["数据分析报告", "数据质量评估", "统计分析", "数据可视化", "相关性分析"],
                key="report_concept_select"
            )
            
            if st.button("🔍 解释概念", key="report_explain"):
                with st.spinner("AI导师正在解释..."):
                    try:
                        explanation = ai_assistant.explain_concept(
                            concept,
                            "分析报告页面"
                        )
                        
                        st.success("✅ 概念解释完成！")
                        st.markdown("### 📖 概念解释")
                        st.markdown(explanation)
                        
                    except Exception as e:
                        st.error(f"❌ 概念解释失败：{str(e)}")
    else:
        st.warning("⚠️ AI助手暂时不可用，请检查网络连接或API配置")
    
    # 完成学习按钮
    st.markdown("---")
    st.markdown("""
    <div class="success-box">
    <h4>🎉 恭喜您完成数据分析学习之旅！</h4>
    <p>您已经成功掌握了数据分析的基础技能，包括数据上传、清洗、可视化和统计分析。</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🏠 返回首页重新开始", use_container_width=True):
        st.session_state.current_step = 1
        st.rerun()
    
    # 返回按钮
    if st.button("⬅️ 返回", key="back_to_analysis"):
        st.session_state.current_step = 6
        st.rerun()

def render_beginner_sidebar():
    """渲染新手模式侧边栏"""
    with st.sidebar:
        st.markdown("## 📊 分析进度")
        
        steps = [
            "🎯 欢迎",
            "📁 数据上传",
            "🔍 数据结构",
            "🧹 数据清洗",
            "📊 数据可视化",
            "📈 统计分析",
            "📄 分析报告"
        ]
        
        for i, step in enumerate(steps, 1):
            if i == st.session_state.current_step:
                st.markdown(f"**{i}. {step}** ✅")
            elif i < st.session_state.current_step:
                st.markdown(f"~~{i}. {step}~~ ✅")
            else:
                st.markdown(f"{i}. {step}")
        
        st.markdown("---")
        
        # 快速导航
        st.markdown("## 🚀 快速导航")
        if st.button("🏠 回到首页"):
            st.session_state.current_step = 1
            st.rerun()
        
        if st.button("📊 查看数据"):
            if st.session_state.data is not None:
                st.session_state.current_step = 3
                st.rerun()
            else:
                st.warning("请先上传数据")
        
        if st.button("📈 查看报告"):
            if st.session_state.analysis_complete:
                st.session_state.current_step = 7
                st.rerun()
            else:
                st.warning("请先完成分析")
        
        # 学习进度分析
        if st.button("📊 学习进度分析"):
            ai_assistant = get_beginner_ai_assistant()
            if ai_assistant:
                with st.spinner("AI导师正在分析您的学习进度..."):
                    try:
                        progress_analysis = ai_assistant.analyze_learning_progress(
                            st.session_state.learning_progress['user_actions'],
                            f"第{st.session_state.current_step}步"
                        )
                        
                        st.success("✅ 学习进度分析完成！")
                        st.markdown("### 📊 学习进度分析")
                        st.markdown(progress_analysis)
                        
                    except Exception as e:
                        st.error(f"❌ 学习进度分析失败：{str(e)}")
            else:
                st.warning("⚠️ AI助手暂时不可用")
        
        # 下一步学习建议
        if st.button("🚀 获取下一步建议"):
            ai_assistant = get_beginner_ai_assistant()
            if ai_assistant:
                with st.spinner("AI导师正在为您规划下一步学习..."):
                    try:
                        next_steps = ai_assistant.suggest_next_steps(
                            f"第{st.session_state.current_step}步",
                            st.session_state.learning_progress
                        )
                        
                        st.success("✅ 学习建议生成完成！")
                        st.markdown("### 🚀 下一步学习建议")
                        st.markdown(next_steps)
                        
                    except Exception as e:
                        st.error(f"❌ 学习建议生成失败：{str(e)}")
            else:
                st.warning("⚠️ AI助手暂时不可用")
        
        st.markdown("---")
        
        # 模式切换
        st.markdown("## 🔄 模式切换")
        if st.button("🎯 返回模式选择"):
            # 清除新手模式状态
            st.session_state.selected_mode = None
            st.session_state.current_page = "🎯 模式选择"
            # 清除新手模式的数据
            if 'current_step' in st.session_state:
                del st.session_state.current_step
            if 'data' in st.session_state:
                del st.session_state.data
            if 'cleaned_data' in st.session_state:
                del st.session_state.cleaned_data
            if 'analysis_complete' in st.session_state:
                del st.session_state.analysis_complete
            if 'analysis_results' in st.session_state:
                del st.session_state.analysis_results
            if 'visualization_results' in st.session_state:
                del st.session_state.visualization_results
            if 'cleaning_results' in st.session_state:
                del st.session_state.cleaning_results
            st.rerun()

def render_beginner_mode():
    """渲染新手模式主界面"""
    # 初始化会话状态
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'cleaned_data' not in st.session_state:
        st.session_state.cleaned_data = None
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = {
            'descriptive_stats': {},
            'correlation_analysis': {},
            'grouped_analysis': {}
        }
    if 'visualization_results' not in st.session_state:
        st.session_state.visualization_results = {
            'chart_types': [],
            'insights': []
        }
    if 'cleaning_results' not in st.session_state:
        st.session_state.cleaning_results = {}
    
    # 新手模式学习进度跟踪
    if 'learning_progress' not in st.session_state:
        st.session_state.learning_progress = {
            'current_step': 1,
            'completed_steps': [],
            'user_actions': [],
            'learning_time': {},
            'performance_scores': {},
            'ai_interactions': 0
        }
    
    # 更新学习进度
    st.session_state.learning_progress['current_step'] = st.session_state.current_step
    
    # 渲染侧边栏
    render_beginner_sidebar()
    
    # 主界面
    if st.session_state.current_step == 1:
        display_welcome()
    elif st.session_state.current_step == 2:
        display_data_upload()
    elif st.session_state.current_step == 3:
        display_data_structure()
    elif st.session_state.current_step == 4:
        display_data_cleaning()
    elif st.session_state.current_step == 5:
        display_visualization()
    elif st.session_state.current_step == 6:
        display_statistical_analysis()
    elif st.session_state.current_step == 7:
        display_report()
    else:
        st.info("新手模式功能正在开发中...")
        if st.button("返回欢迎页面"):
            st.session_state.current_step = 1
            st.rerun()
