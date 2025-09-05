"""
高级配置模块
提供专业级的数据科学应用配置
"""

from typing import Dict, Any, List
import os
from dataclasses import dataclass
from enum import Enum

class Environment(Enum):
    """环境枚举"""
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"

@dataclass
class PerformanceConfig:
    """性能配置"""
    max_memory_usage: float = 0.8  # 最大内存使用率
    cache_ttl: int = 3600  # 缓存过期时间（秒）
    chunk_size: int = 10000  # 分块处理大小
    max_file_size: int = 100 * 1024 * 1024  # 最大文件大小（100MB）

@dataclass
class VisualizationConfig:
    """可视化配置"""
    default_theme: str = "plotly_white"
    color_palette: List[str] = None
    chart_height: int = 600
    chart_width: int = 800
    
    def __post_init__(self):
        if self.color_palette is None:
            self.color_palette = [
                '#1E40AF', '#3B82F6', '#60A5FA', '#93C5FD', '#DBEAFE',
                '#059669', '#10B981', '#34D399', '#6EE7B7', '#A7F3D0',
                '#D97706', '#F59E0B', '#FBBF24', '#FCD34D', '#FDE68A'
            ]

@dataclass
class MLConfig:
    """机器学习配置"""
    random_state: int = 42
    test_size: float = 0.2
    cv_folds: int = 5
    max_iter: int = 1000
    n_jobs: int = -1

@dataclass
class AIConfig:
    """AI助手配置"""
    model_name: str = "qwen-turbo"
    max_tokens: int = 2000
    temperature: float = 0.7
    api_timeout: int = 30

@dataclass
class SecurityConfig:
    """安全配置"""
    enable_rate_limiting: bool = True
    max_requests_per_minute: int = 60
    allowed_file_types: List[str] = None
    max_file_uploads: int = 5
    
    def __post_init__(self):
        if self.allowed_file_types is None:
            self.allowed_file_types = ['csv', 'xlsx', 'xls', 'json', 'parquet']

class AdvancedSettings:
    """高级设置类"""
    
    def __init__(self, environment: Environment = Environment.DEVELOPMENT):
        self.environment = environment
        self.performance = PerformanceConfig()
        self.visualization = VisualizationConfig()
        self.ml = MLConfig()
        self.ai = AIConfig()
        self.security = SecurityConfig()
        
        # 根据环境调整配置
        self._adjust_for_environment()
    
    def _adjust_for_environment(self):
        """根据环境调整配置"""
        if self.environment == Environment.PRODUCTION:
            self.performance.max_memory_usage = 0.7
            self.performance.cache_ttl = 7200
            self.ai.max_tokens = 1000
            self.security.enable_rate_limiting = True
        elif self.environment == Environment.TESTING:
            self.performance.chunk_size = 1000
            self.ml.cv_folds = 3
            self.ai.temperature = 0.1
    
    def get_database_config(self) -> Dict[str, Any]:
        """获取数据库配置"""
        return {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": int(os.getenv("DB_PORT", "5432")),
            "database": os.getenv("DB_NAME", "datascience"),
            "username": os.getenv("DB_USER", "user"),
            "password": os.getenv("DB_PASSWORD", "password")
        }
    
    def get_cache_config(self) -> Dict[str, Any]:
        """获取缓存配置"""
        return {
            "type": os.getenv("CACHE_TYPE", "memory"),
            "ttl": self.performance.cache_ttl,
            "max_size": int(os.getenv("CACHE_MAX_SIZE", "1000"))
        }
    
    def get_logging_config(self) -> Dict[str, Any]:
        """获取日志配置"""
        return {
            "level": os.getenv("LOG_LEVEL", "INFO"),
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "file": os.getenv("LOG_FILE", "app.log")
        }

# 全局配置实例
def get_advanced_settings(environment: Environment = None) -> AdvancedSettings:
    """获取高级设置实例"""
    if environment is None:
        env_str = os.getenv("ENVIRONMENT", "development")
        environment = Environment(env_str)
    
    return AdvancedSettings(environment)

# 便捷配置获取函数
def get_performance_config() -> PerformanceConfig:
    """获取性能配置"""
    return get_advanced_settings().performance

def get_visualization_config() -> VisualizationConfig:
    """获取可视化配置"""
    return get_advanced_settings().visualization

def get_ml_config() -> MLConfig:
    """获取机器学习配置"""
    return get_advanced_settings().ml

def get_ai_config() -> AIConfig:
    """获取AI配置"""
    return get_advanced_settings().ai

def get_security_config() -> SecurityConfig:
    """获取安全配置"""
    return get_advanced_settings().security
