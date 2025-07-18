"""
核心接口模块
Core Interfaces Module
"""

from .text_processor import ITextProcessor
from .search_manager import ISearchManager
from .relevance_calculator import IRelevanceCalculator
from .ui_manager import IUIManager

__all__ = ['ITextProcessor', 'ISearchManager', 'IRelevanceCalculator', 'IUIManager']