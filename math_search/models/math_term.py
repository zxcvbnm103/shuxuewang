"""
数学术语数据模型
Math Term Data Model
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class MathTerm:
    """数学术语数据类"""
    term: str
    latex_representation: str
    category: str  # algebra, calculus, geometry, etc.
    confidence: float
    
    def __post_init__(self):
        """数据验证"""
        if not self.term:
            raise ValueError("术语不能为空")
        if not 0 <= self.confidence <= 1:
            raise ValueError("置信度必须在0-1之间")
        
        # 验证类别
        valid_categories = {
            'algebra', 'calculus', 'geometry', 'statistics', 
            'linear_algebra', 'differential_equations', 'topology',
            'number_theory', 'discrete_math', 'analysis', 'other'
        }
        if self.category not in valid_categories:
            raise ValueError(f"无效的数学类别: {self.category}")
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            'term': self.term,
            'latex_representation': self.latex_representation,
            'category': self.category,
            'confidence': self.confidence
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'MathTerm':
        """从字典创建实例"""
        return cls(**data)
    
    def is_high_confidence(self) -> bool:
        """判断是否为高置信度术语"""
        return self.confidence >= 0.8