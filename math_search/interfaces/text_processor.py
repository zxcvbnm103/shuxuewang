"""
文本处理器接口
Text Processor Interface
"""

from abc import ABC, abstractmethod
from typing import List, Tuple
from ..models import MathTerm


class ITextProcessor(ABC):
    """文本处理器接口"""
    
    @abstractmethod
    def extract_selected_text(self, content: str, selection_range: Tuple[int, int]) -> str:
        """
        提取选中的文本
        
        Args:
            content: 完整文本内容
            selection_range: 选择范围 (start, end)
            
        Returns:
            选中的文本
        """
        pass
    
    @abstractmethod
    def identify_math_terms(self, text: str) -> List[MathTerm]:
        """
        识别数学术语
        
        Args:
            text: 输入文本
            
        Returns:
            识别出的数学术语列表
        """
        pass
    
    @abstractmethod
    def parse_latex_formulas(self, text: str) -> List[str]:
        """
        解析LaTeX公式
        
        Args:
            text: 包含LaTeX公式的文本
            
        Returns:
            解析出的LaTeX公式列表
        """
        pass
    
    @abstractmethod
    def generate_search_keywords(self, text: str) -> List[str]:
        """
        生成搜索关键词
        
        Args:
            text: 输入文本
            
        Returns:
            生成的搜索关键词列表
        """
        pass