"""
用户界面管理器接口
UI Manager Interface
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from ..models import SearchResult, SearchHistory


class IUIManager(ABC):
    """用户界面管理器接口"""
    
    @abstractmethod
    def render_editor_with_selection(self) -> Tuple[str, Optional[str]]:
        """
        渲染带选择功能的编辑器
        
        Returns:
            (content, selected_text) 内容和选中文本
        """
        pass
    
    @abstractmethod
    def render_search_panel(self, results: List[SearchResult]) -> None:
        """
        渲染搜索结果面板
        
        Args:
            results: 搜索结果列表
        """
        pass
    
    @abstractmethod
    def render_history_panel(self, history: List[SearchHistory]) -> None:
        """
        渲染历史记录面板
        
        Args:
            history: 搜索历史列表
        """
        pass
    
    @abstractmethod
    def handle_search_trigger(self, selected_text: str) -> None:
        """
        处理搜索触发事件
        
        Args:
            selected_text: 选中的文本
        """
        pass