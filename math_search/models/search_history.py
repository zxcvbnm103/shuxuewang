"""
搜索历史数据模型
Search History Data Model
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class SearchHistory:
    """搜索历史数据类"""
    id: int
    query_text: str
    search_keywords: List[str]
    timestamp: datetime
    results_count: int
    top_result_url: str
    
    def __post_init__(self):
        """数据验证"""
        if not self.query_text:
            raise ValueError("查询文本不能为空")
        if self.results_count < 0:
            raise ValueError("结果数量不能为负数")
        if not self.search_keywords:
            raise ValueError("搜索关键词不能为空")
        if self.id < 0:
            raise ValueError("ID不能为负数")
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            'id': self.id,
            'query_text': self.query_text,
            'search_keywords': self.search_keywords,
            'timestamp': self.timestamp.isoformat(),
            'results_count': self.results_count,
            'top_result_url': self.top_result_url
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'SearchHistory':
        """从字典创建实例"""
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)
    
    def get_summary(self) -> str:
        """获取搜索历史摘要"""
        keywords_str = ', '.join(self.search_keywords[:3])  # 只显示前3个关键词
        if len(self.search_keywords) > 3:
            keywords_str += '...'
        return f"查询: {self.query_text[:50]}{'...' if len(self.query_text) > 50 else ''} | 关键词: {keywords_str} | 结果: {self.results_count}个"