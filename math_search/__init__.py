"""
数学笔记智能检索功能模块
Math Notes Intelligent Search Module
"""

from .models import SearchResult, SearchHistory, MathTerm
from .interfaces import ITextProcessor, ISearchManager, IRelevanceCalculator, IUIManager
from .config import Settings

__version__ = "1.0.0"
__author__ = "Math Notes Search Team"

__all__ = [
    # 数据模型
    'SearchResult', 'SearchHistory', 'MathTerm',
    # 核心接口
    'ITextProcessor', 'ISearchManager', 'IRelevanceCalculator', 'IUIManager',
    # 配置
    'Settings'
]