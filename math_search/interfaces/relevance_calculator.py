"""
相关度计算器接口
Relevance Calculator Interface
"""

from abc import ABC, abstractmethod
from typing import List
from ..models import SearchResult


class IRelevanceCalculator(ABC):
    """相关度计算器接口"""
    
    @abstractmethod
    def calculate_relevance(self, query: str, result: SearchResult) -> float:
        """
        计算相关度
        
        Args:
            query: 查询文本
            result: 搜索结果
            
        Returns:
            相关度评分 (0-1)
        """
        pass
    
    @abstractmethod
    def rank_results(self, results: List[SearchResult]) -> List[SearchResult]:
        """
        对结果进行排序
        
        Args:
            results: 搜索结果列表
            
        Returns:
            按相关度排序的结果列表
        """
        pass
    
    @abstractmethod
    def apply_math_domain_boost(self, results: List[SearchResult]) -> List[SearchResult]:
        """
        应用数学领域权重提升
        
        Args:
            results: 搜索结果列表
            
        Returns:
            应用权重提升后的结果列表
        """
        pass