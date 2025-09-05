"""
AI助手工具模块
提供智能AI助手获取和配置功能
"""

import os
import streamlit as st
from typing import Optional
from src.utils.ai_assistant import get_ai_assistant, DataAnalysisAI

# 导入云端AI助手支持
try:
    from src.utils.ai_assistant_cloud import get_cloud_ai_assistant, get_ai_config_status
    CLOUD_AI_AVAILABLE = True
except ImportError:
    CLOUD_AI_AVAILABLE = False


def get_smart_ai_assistant() -> Optional[DataAnalysisAI]:
    """
    智能获取AI助手实例，优先使用云端配置，回退到演示AI
    
    Returns:
        DataAnalysisAI: AI助手实例，如果都不可用则返回演示AI
    """
    # 优先尝试云端AI助手
    if CLOUD_AI_AVAILABLE:
        try:
            config_status = get_ai_config_status()
            if config_status["api_key_available"]:
                ai_assistant = get_cloud_ai_assistant()
                if ai_assistant is not None:
                    return ai_assistant
        except Exception as e:
            st.warning(f"⚠️ 云端AI助手不可用: {str(e)}")
    
    # 回退到本地AI助手
    try:
        return get_ai_assistant()
    except Exception as e:
        st.warning(f"⚠️ 本地AI助手不可用: {str(e)}")
    
    # 最后回退到演示AI助手
    try:
        from src.utils.demo_ai_assistant import get_demo_ai_assistant
        demo_ai = get_demo_ai_assistant()
        st.info("ℹ️ 使用演示版AI助手（无需API密钥）")
        return demo_ai
    except Exception as e:
        st.error(f"❌ 所有AI助手都不可用: {str(e)}")
        return None


def check_ai_availability() -> dict:
    """
    检查AI助手的可用性
    
    Returns:
        dict: 包含各种AI助手可用性的字典
    """
    availability = {
        "cloud_ai_available": CLOUD_AI_AVAILABLE,
        "local_ai_available": False,
        "smart_ai_available": False,
        "api_key_configured": bool(os.getenv("DASHSCOPE_API_KEY"))
    }
    
    # 检查本地AI助手
    try:
        local_ai = get_ai_assistant()
        availability["local_ai_available"] = local_ai is not None
    except Exception:
        pass
    
    # 检查智能AI助手
    try:
        smart_ai = get_smart_ai_assistant()
        availability["smart_ai_available"] = smart_ai is not None
    except Exception:
        pass
    
    return availability


def get_ai_config_info() -> dict:
    """
    获取AI配置信息
    
    Returns:
        dict: AI配置信息
    """
    config_info = {
        "api_key_set": bool(os.getenv("DASHSCOPE_API_KEY")),
        "cloud_ai_available": CLOUD_AI_AVAILABLE,
        "recommended_setup": []
    }
    
    if not config_info["api_key_set"]:
        config_info["recommended_setup"].append("设置环境变量 DASHSCOPE_API_KEY")
    
    if not CLOUD_AI_AVAILABLE:
        config_info["recommended_setup"].append("安装云端AI助手依赖")
    
    return config_info


def render_ai_status():
    """
    渲染AI助手状态信息
    """
    availability = check_ai_availability()
    
    st.subheader("🤖 AI助手状态")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if availability["api_key_configured"]:
            st.success("✅ API密钥已配置")
        else:
            st.error("❌ API密钥未配置")
    
    with col2:
        if availability["cloud_ai_available"]:
            st.success("✅ 云端AI可用")
        else:
            st.warning("⚠️ 云端AI不可用")
    
    with col3:
        if availability["local_ai_available"]:
            st.success("✅ 本地AI可用")
        else:
            st.warning("⚠️ 本地AI不可用")
    
    with col4:
        if availability["smart_ai_available"]:
            st.success("✅ AI助手就绪")
        else:
            st.error("❌ AI助手不可用")
    
    # 显示配置建议
    if not availability["api_key_configured"]:
        st.info("""
        💡 **配置AI助手：**
        
        1. 获取阿里云DashScope API密钥
        2. 设置环境变量：`DASHSCOPE_API_KEY=your_api_key`
        3. 重启应用
        
        或者使用以下命令设置：
        ```bash
        export DASHSCOPE_API_KEY=your_api_key
        ```
        """)
    
    return availability["smart_ai_available"]


def safe_ai_call(ai_function, *args, **kwargs):
    """
    安全调用AI函数，提供错误处理和用户反馈
    
    Args:
        ai_function: AI函数
        *args: 函数参数
        **kwargs: 函数关键字参数
        
    Returns:
        str: AI响应或错误信息
    """
    try:
        # 检查AI助手是否可用
        ai_assistant = get_smart_ai_assistant()
        if ai_assistant is None:
            return "❌ AI助手不可用，请检查配置。\n\n💡 **解决方案：**\n1. 确保已设置 `DASHSCOPE_API_KEY` 环境变量\n2. 检查网络连接\n3. 重启应用"
        
        # 调用AI函数
        with st.spinner("🤖 AI正在思考中..."):
            result = ai_function(*args, **kwargs)
            return result
            
    except Exception as e:
        error_msg = f"❌ AI调用失败：{str(e)}\n\n"
        error_msg += "💡 **可能的原因：**\n"
        error_msg += "1. API密钥无效或过期\n"
        error_msg += "2. 网络连接问题\n"
        error_msg += "3. API服务暂时不可用\n"
        error_msg += "4. 请求超时\n\n"
        error_msg += "🔄 **建议操作：**\n"
        error_msg += "1. 检查API密钥配置\n"
        error_msg += "2. 稍后重试\n"
        error_msg += "3. 联系技术支持"
        
        return error_msg


def create_ai_button(label, ai_function, *args, **kwargs):
    """
    创建AI按钮，提供统一的用户体验
    
    Args:
        label: 按钮标签
        ai_function: AI函数
        *args: 函数参数
        **kwargs: 函数关键字参数
        
    Returns:
        bool: 是否成功调用AI
    """
    # 检查AI助手状态
    ai_available = render_ai_status()
    
    if not ai_available:
        st.warning("⚠️ AI助手不可用，无法使用此功能")
        return False
    
    # 创建按钮
    if st.button(label, type="primary"):
        result = safe_ai_call(ai_function, *args, **kwargs)
        
        if result.startswith("❌"):
            st.error(result)
            return False
        else:
            st.success("✅ AI分析完成！")
            st.markdown("### 🤖 AI分析结果")
            st.markdown(result)
            return True
    
    return False
