"""
搜索历史数据仓库
Search History Repository
"""

import json
from datetime import datetime
from typing import List, Optional
from ..models.search_history import SearchHistory
from .connection import DatabaseConnection


class HistoryRepository:
    """搜索历史数据仓库，负责搜索历史的CRUD操作"""
    
    def __init__(self, db_connection: DatabaseConnection):
        """
        初始化历史记录仓库
        
        Args:
            db_connection: 数据库连接管理器
        """
        self.db = db_connection
    
    def create(self, history: SearchHistory) -> int:
        """
        创建新的搜索历史记录
        
        Args:
            history: 搜索历史对象
            
        Returns:
            新创建记录的ID
        """
        query = '''
            INSERT INTO search_history 
            (query_text, search_keywords, timestamp, results_count, top_result_url)
            VALUES (?, ?, ?, ?, ?)
        '''
        
        params = (
            history.query_text,
            json.dumps(history.search_keywords, ensure_ascii=False),
            history.timestamp.isoformat(),
            history.results_count,
            history.top_result_url
        )
        
        self.db.execute_update(query, params)
        return self.db.get_last_insert_id()
    
    def get_by_id(self, history_id: int) -> Optional[SearchHistory]:
        """
        根据ID获取搜索历史记录
        
        Args:
            history_id: 历史记录ID
            
        Returns:
            搜索历史对象，如果不存在则返回None
        """
        query = '''
            SELECT id, query_text, search_keywords, timestamp, results_count, top_result_url
            FROM search_history
            WHERE id = ?
        '''
        
        results = self.db.execute_query(query, (history_id,))
        if not results:
            return None
        
        return self._row_to_history(results[0])
    
    def get_all(self, limit: int = 100, offset: int = 0) -> List[SearchHistory]:
        """
        获取所有搜索历史记录
        
        Args:
            limit: 返回记录数限制
            offset: 偏移量
            
        Returns:
            搜索历史记录列表
        """
        query = '''
            SELECT id, query_text, search_keywords, timestamp, results_count, top_result_url
            FROM search_history
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?
        '''
        
        results = self.db.execute_query(query, (limit, offset))
        return [self._row_to_history(row) for row in results]
    
    def get_recent(self, days: int = 7, limit: int = 50) -> List[SearchHistory]:
        """
        获取最近几天的搜索历史记录
        
        Args:
            days: 天数
            limit: 返回记录数限制
            
        Returns:
            最近的搜索历史记录列表
        """
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days)
        query = '''
            SELECT id, query_text, search_keywords, timestamp, results_count, top_result_url
            FROM search_history
            WHERE timestamp >= ?
            ORDER BY timestamp DESC
            LIMIT ?
        '''
        
        results = self.db.execute_query(query, (cutoff_date.isoformat(), limit))
        return [self._row_to_history(row) for row in results]
    
    def search_by_query(self, query_text: str, limit: int = 20) -> List[SearchHistory]:
        """
        根据查询文本搜索历史记录
        
        Args:
            query_text: 查询文本（支持模糊匹配）
            limit: 返回记录数限制
            
        Returns:
            匹配的搜索历史记录列表
        """
        query = '''
            SELECT id, query_text, search_keywords, timestamp, results_count, top_result_url
            FROM search_history
            WHERE query_text LIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
        '''
        
        search_pattern = f"%{query_text}%"
        results = self.db.execute_query(query, (search_pattern, limit))
        return [self._row_to_history(row) for row in results]
    
    def update(self, history: SearchHistory) -> bool:
        """
        更新搜索历史记录
        
        Args:
            history: 搜索历史对象
            
        Returns:
            是否更新成功
        """
        query = '''
            UPDATE search_history
            SET query_text = ?, search_keywords = ?, timestamp = ?, 
                results_count = ?, top_result_url = ?
            WHERE id = ?
        '''
        
        params = (
            history.query_text,
            json.dumps(history.search_keywords, ensure_ascii=False),
            history.timestamp.isoformat(),
            history.results_count,
            history.top_result_url,
            history.id
        )
        
        affected_rows = self.db.execute_update(query, params)
        return affected_rows > 0
    
    def delete(self, history_id: int) -> bool:
        """
        删除搜索历史记录
        
        Args:
            history_id: 历史记录ID
            
        Returns:
            是否删除成功
        """
        query = "DELETE FROM search_history WHERE id = ?"
        affected_rows = self.db.execute_update(query, (history_id,))
        return affected_rows > 0
    
    def delete_old_records(self, days: int = 30) -> int:
        """
        删除指定天数之前的历史记录
        
        Args:
            days: 保留天数
            
        Returns:
            删除的记录数
        """
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days)
        query = "DELETE FROM search_history WHERE timestamp < ?"
        return self.db.execute_update(query, (cutoff_date.isoformat(),))
    
    def get_count(self) -> int:
        """
        获取历史记录总数
        
        Returns:
            历史记录总数
        """
        query = "SELECT COUNT(*) FROM search_history"
        results = self.db.execute_query(query)
        return results[0][0] if results else 0
    
    def get_statistics(self) -> dict:
        """
        获取搜索历史统计信息
        
        Returns:
            统计信息字典
        """
        stats = {}
        
        # 总记录数
        stats['total_count'] = self.get_count()
        
        # 最近7天的记录数
        recent_records = self.get_recent(days=7)
        stats['recent_count'] = len(recent_records)
        
        # 平均结果数
        query = "SELECT AVG(results_count) FROM search_history"
        results = self.db.execute_query(query)
        stats['avg_results'] = round(results[0][0], 2) if results and results[0][0] else 0
        
        # 最早和最晚的记录时间
        query = "SELECT MIN(timestamp), MAX(timestamp) FROM search_history"
        results = self.db.execute_query(query)
        if results and results[0][0]:
            stats['earliest_record'] = results[0][0]
            stats['latest_record'] = results[0][1]
        
        return stats
    
    def _row_to_history(self, row) -> SearchHistory:
        """
        将数据库行转换为SearchHistory对象
        
        Args:
            row: 数据库行对象
            
        Returns:
            SearchHistory对象
        """
        return SearchHistory(
            id=row['id'],
            query_text=row['query_text'],
            search_keywords=json.loads(row['search_keywords']),
            timestamp=datetime.fromisoformat(row['timestamp']),
            results_count=row['results_count'],
            top_result_url=row['top_result_url'] or ""
        )