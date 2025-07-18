"""
搜索管理器接口
Search Manager Interface
"""

from abc import ABC, abstractmethod
from typing import List
from ..models import SearchResult


class ISearchManager(ABC):
    """搜索管理器接口"""
    
    @abstractmethod
    def search_web(self, keywords: List[str]) -> List[SearchResult]:
        """
        网页搜索
        
        Args:
            keywords: 搜索关键词列表
            
        Returns:
            搜索结果列表
        """
        pass
    
    @abstractmethod
    def search_academic(self, keywords: List[str]) -> List[SearchResult]:
        """
        学术搜索
        
        Args:
            keywords: 搜索关键词列表
            
        Returns:
            学术搜索结果列表
        """
        pass
    
    @abstractmethod
    def combine_results(self, results: List[List[SearchResult]]) -> List[SearchResult]:
        """
        合并搜索结果
        
        Args:
            results: 多个搜索结果列表
            
        Returns:
            合并后的搜索结果列表
        """
        pass