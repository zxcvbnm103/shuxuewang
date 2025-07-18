"""
应用设置配置
Application Settings Configuration
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import os


@dataclass
class SearchAPIConfig:
    """搜索API配置"""
    google_api_key: Optional[str] = None
    google_search_engine_id: Optional[str] = None
    bing_api_key: Optional[str] = None
    arxiv_base_url: str = "http://export.arxiv.org/api/query"
    max_results_per_source: int = 10
    request_timeout: int = 30


@dataclass
class UIConfig:
    """用户界面配置"""
    editor_height: int = 400
    results_panel_width_ratio: float = 0.33  # 结果面板占总宽度的比例
    max_history_display: int = 20
    auto_search_delay: float = 1.0  # 自动搜索延迟（秒）


@dataclass
class CacheConfig:
    """缓存配置"""
    cache_dir: str = ".cache"
    cache_expiry_hours: int = 24
    max_cache_size_mb: int = 100
    enable_cache: bool = True


@dataclass
class MathProcessingConfig:
    """数学处理配置"""
    latex_delimiters: List[str] = None
    math_term_confidence_threshold: float = 0.6
    enable_sympy_parsing: bool = True
    
    def __post_init__(self):
        if self.latex_delimiters is None:
            self.latex_delimiters = ['$', '$$', '\\(', '\\)', '\\[', '\\]']


@dataclass
class Settings:
    """应用主配置类"""
    search_api: SearchAPIConfig = None
    ui: UIConfig = None
    cache: CacheConfig = None
    math_processing: MathProcessingConfig = None
    
    def __post_init__(self):
        if self.search_api is None:
            self.search_api = SearchAPIConfig()
        if self.ui is None:
            self.ui = UIConfig()
        if self.cache is None:
            self.cache = CacheConfig()
        if self.math_processing is None:
            self.math_processing = MathProcessingConfig()
    
    @classmethod
    def from_env(cls) -> 'Settings':
        """从环境变量创建配置"""
        search_api = SearchAPIConfig(
            google_api_key=os.getenv('GOOGLE_API_KEY'),
            google_search_engine_id=os.getenv('GOOGLE_SEARCH_ENGINE_ID'),
            bing_api_key=os.getenv('BING_API_KEY')
        )
        
        return cls(search_api=search_api)
    
    def validate(self) -> List[str]:
        """验证配置并返回错误信息"""
        errors = []
        
        # 检查API密钥
        if not self.search_api.google_api_key and not self.search_api.bing_api_key:
            errors.append("至少需要配置一个搜索API密钥 (Google或Bing)")
        
        # 检查UI配置
        if not 0 < self.ui.results_panel_width_ratio < 1:
            errors.append("结果面板宽度比例必须在0-1之间")
        
        # 检查缓存配置
        if self.cache.max_cache_size_mb <= 0:
            errors.append("缓存大小必须大于0")
        
        return errors