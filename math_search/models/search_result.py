"""
搜索结果数据模型
Search Result Data Model
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class SearchResult:
    """搜索结果数据类"""
    title: str
    url: str
    snippet: str
    source: str
    relevance_score: float
    timestamp: datetime
    math_content_detected: bool
    
    def __post_init__(self):
        """数据验证"""
        if not self.title or not self.url:
            raise ValueError("标题和URL不能为空")
        if not 0 <= self.relevance_score <= 1:
            raise ValueError("相关度评分必须在0-1之间")
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            'title': self.title,
            'url': self.url,
            'snippet': self.snippet,
            'source': self.source,
            'relevance_score': self.relevance_score,
            'timestamp': self.timestamp.isoformat(),
            'math_content_detected': self.math_content_detected
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'SearchResult':
        """从字典创建实例"""
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)