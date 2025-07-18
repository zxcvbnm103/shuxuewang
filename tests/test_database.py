"""
数据库操作单元测试
Database Operations Unit Tests
"""

import pytest
import tempfile
import os
from datetime import datetime, timedelta
from pathlib import Path

from math_search.database.connection import DatabaseConnection
from math_search.database.history_repository import HistoryRepository
from math_search.models.search_history import SearchHistory


class TestDatabaseConnection:
    """数据库连接测试类"""
    
    def setup_method(self):
        """测试前设置"""
        # 创建临时数据库文件
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name
        self.db_conn = DatabaseConnection(self.db_path)
    
    def teardown_method(self):
        """测试后清理"""
        self.db_conn.close_connection()
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)
    
    def test_database_creation(self):
        """测试数据库创建"""
        assert Path(self.db_path).exists()
        
        # 检查表是否创建成功
        tables = self.db_conn.execute_query(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        table_names = [table['name'] for table in tables]
        assert 'search_history' in table_names
    
    def test_connection_thread_safety(self):
        """测试连接的线程安全性"""
        conn1 = self.db_conn.get_connection()
        conn2 = self.db_conn.get_connection()
        assert conn1 is conn2  # 同一线程应该返回相同连接
    
    def test_cursor_context_manager(self):
        """测试游标上下文管理器"""
        with self.db_conn.get_cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            assert result[0] == 1
    
    def test_execute_query(self):
        """测试查询执行"""
        results = self.db_conn.execute_query("SELECT 1 as test_value")
        assert len(results) == 1
        assert results[0]['test_value'] == 1
    
    def test_execute_update(self):
        """测试更新执行"""
        # 插入测试数据
        affected_rows = self.db_conn.execute_update(
            "INSERT INTO search_history (query_text, search_keywords, timestamp, results_count) VALUES (?, ?, ?, ?)",
            ("test query", '["test"]', datetime.now().isoformat(), 5)
        )
        assert affected_rows == 1
    
    def test_last_insert_id(self):
        """测试获取最后插入ID"""
        self.db_conn.execute_update(
            "INSERT INTO search_history (query_text, search_keywords, timestamp, results_count) VALUES (?, ?, ?, ?)",
            ("test query", '["test"]', datetime.now().isoformat(), 5)
        )
        last_id = self.db_conn.get_last_insert_id()
        assert last_id > 0


class TestHistoryRepository:
    """搜索历史仓库测试类"""
    
    def setup_method(self):
        """测试前设置"""
        # 创建临时数据库文件
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name
        self.db_conn = DatabaseConnection(self.db_path)
        self.repo = HistoryRepository(self.db_conn)
        
        # 创建测试数据
        self.test_history = SearchHistory(
            id=0,  # 将在创建时分配
            query_text="测试查询文本",
            search_keywords=["数学", "微积分", "导数"],
            timestamp=datetime.now(),
            results_count=10,
            top_result_url="https://example.com/result1"
        )
    
    def teardown_method(self):
        """测试后清理"""
        self.db_conn.close_connection()
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)
    
    def test_create_history(self):
        """测试创建历史记录"""
        history_id = self.repo.create(self.test_history)
        assert history_id > 0
        
        # 验证记录是否正确创建
        created_history = self.repo.get_by_id(history_id)
        assert created_history is not None
        assert created_history.query_text == self.test_history.query_text
        assert created_history.search_keywords == self.test_history.search_keywords
        assert created_history.results_count == self.test_history.results_count
        assert created_history.top_result_url == self.test_history.top_result_url
    
    def test_get_by_id(self):
        """测试根据ID获取历史记录"""
        # 创建记录
        history_id = self.repo.create(self.test_history)
        
        # 获取记录
        retrieved_history = self.repo.get_by_id(history_id)
        assert retrieved_history is not None
        assert retrieved_history.id == history_id
        assert retrieved_history.query_text == self.test_history.query_text
        
        # 测试不存在的ID
        non_existent = self.repo.get_by_id(99999)
        assert non_existent is None
    
    def test_get_all(self):
        """测试获取所有历史记录"""
        # 创建多个记录
        histories = []
        for i in range(5):
            history = SearchHistory(
                id=0,
                query_text=f"查询文本 {i}",
                search_keywords=[f"关键词{i}"],
                timestamp=datetime.now() - timedelta(hours=i),
                results_count=i + 1,
                top_result_url=f"https://example.com/result{i}"
            )
            history_id = self.repo.create(history)
            history.id = history_id
            histories.append(history)
        
        # 获取所有记录
        all_histories = self.repo.get_all()
        assert len(all_histories) == 5
        
        # 验证按时间倒序排列
        for i in range(len(all_histories) - 1):
            assert all_histories[i].timestamp >= all_histories[i + 1].timestamp
        
        # 测试限制和偏移
        limited_histories = self.repo.get_all(limit=3, offset=1)
        assert len(limited_histories) == 3
    
    def test_get_recent(self):
        """测试获取最近的历史记录"""
        # 创建不同时间的记录
        old_history = SearchHistory(
            id=0,
            query_text="旧查询",
            search_keywords=["旧关键词"],
            timestamp=datetime.now() - timedelta(days=10),
            results_count=1,
            top_result_url="https://example.com/old"
        )
        self.repo.create(old_history)
        
        recent_history = SearchHistory(
            id=0,
            query_text="新查询",
            search_keywords=["新关键词"],
            timestamp=datetime.now() - timedelta(hours=1),
            results_count=2,
            top_result_url="https://example.com/recent"
        )
        self.repo.create(recent_history)
        
        # 获取最近7天的记录
        recent_histories = self.repo.get_recent(days=7)
        assert len(recent_histories) == 1
        assert recent_histories[0].query_text == "新查询"
    
    def test_search_by_query(self):
        """测试根据查询文本搜索"""
        # 创建测试记录
        histories = [
            SearchHistory(0, "数学微积分", ["数学"], datetime.now(), 5, ""),
            SearchHistory(0, "物理力学", ["物理"], datetime.now(), 3, ""),
            SearchHistory(0, "数学线性代数", ["代数"], datetime.now(), 7, "")
        ]
        
        for history in histories:
            self.repo.create(history)
        
        # 搜索包含"数学"的记录
        math_histories = self.repo.search_by_query("数学")
        assert len(math_histories) == 2
        
        # 搜索包含"物理"的记录
        physics_histories = self.repo.search_by_query("物理")
        assert len(physics_histories) == 1
        assert physics_histories[0].query_text == "物理力学"
    
    def test_update_history(self):
        """测试更新历史记录"""
        # 创建记录
        history_id = self.repo.create(self.test_history)
        
        # 获取并修改记录
        history = self.repo.get_by_id(history_id)
        history.query_text = "更新后的查询文本"
        history.results_count = 20
        
        # 更新记录
        success = self.repo.update(history)
        assert success is True
        
        # 验证更新
        updated_history = self.repo.get_by_id(history_id)
        assert updated_history.query_text == "更新后的查询文本"
        assert updated_history.results_count == 20
    
    def test_delete_history(self):
        """测试删除历史记录"""
        # 创建记录
        history_id = self.repo.create(self.test_history)
        
        # 验证记录存在
        assert self.repo.get_by_id(history_id) is not None
        
        # 删除记录
        success = self.repo.delete(history_id)
        assert success is True
        
        # 验证记录已删除
        assert self.repo.get_by_id(history_id) is None
        
        # 测试删除不存在的记录
        success = self.repo.delete(99999)
        assert success is False
    
    def test_delete_old_records(self):
        """测试删除旧记录"""
        # 创建新旧记录
        old_history = SearchHistory(
            id=0,
            query_text="旧记录",
            search_keywords=["旧"],
            timestamp=datetime.now() - timedelta(days=40),
            results_count=1,
            top_result_url=""
        )
        self.repo.create(old_history)
        
        new_history = SearchHistory(
            id=0,
            query_text="新记录",
            search_keywords=["新"],
            timestamp=datetime.now() - timedelta(days=10),
            results_count=1,
            top_result_url=""
        )
        self.repo.create(new_history)
        
        # 删除30天前的记录
        deleted_count = self.repo.delete_old_records(days=30)
        assert deleted_count == 1
        
        # 验证只剩下新记录
        all_histories = self.repo.get_all()
        assert len(all_histories) == 1
        assert all_histories[0].query_text == "新记录"
    
    def test_get_count(self):
        """测试获取记录总数"""
        assert self.repo.get_count() == 0
        
        # 创建几个记录
        for i in range(3):
            history = SearchHistory(
                id=0,
                query_text=f"查询 {i}",
                search_keywords=[f"关键词{i}"],
                timestamp=datetime.now(),
                results_count=1,
                top_result_url=""
            )
            self.repo.create(history)
        
        assert self.repo.get_count() == 3
    
    def test_get_statistics(self):
        """测试获取统计信息"""
        # 创建测试数据
        histories = [
            SearchHistory(0, "查询1", ["关键词"], datetime.now() - timedelta(days=1), 5, ""),
            SearchHistory(0, "查询2", ["关键词"], datetime.now() - timedelta(days=2), 10, ""),
            SearchHistory(0, "查询3", ["关键词"], datetime.now() - timedelta(days=10), 15, "")
        ]
        
        for history in histories:
            self.repo.create(history)
        
        stats = self.repo.get_statistics()
        
        assert stats['total_count'] == 3
        assert stats['recent_count'] == 2  # 最近7天的记录
        assert stats['avg_results'] == 10.0  # (5+10+15)/3
        assert 'earliest_record' in stats
        assert 'latest_record' in stats
    
    def test_data_validation(self):
        """测试数据验证"""
        # 测试空查询文本
        with pytest.raises(ValueError, match="查询文本不能为空"):
            SearchHistory(
                id=1,
                query_text="",  # 空查询文本
                search_keywords=["valid"],
                timestamp=datetime.now(),
                results_count=1,
                top_result_url=""
            )
        
        # 测试空关键词列表
        with pytest.raises(ValueError, match="搜索关键词不能为空"):
            SearchHistory(
                id=1,
                query_text="valid",
                search_keywords=[],  # 空关键词
                timestamp=datetime.now(),
                results_count=1,
                top_result_url=""
            )
        
        # 测试负数结果数
        with pytest.raises(ValueError, match="结果数量不能为负数"):
            SearchHistory(
                id=1,
                query_text="valid",
                search_keywords=["valid"],
                timestamp=datetime.now(),
                results_count=-1,  # 负数结果数
                top_result_url=""
            )
        
        # 测试负数ID
        with pytest.raises(ValueError, match="ID不能为负数"):
            SearchHistory(
                id=-1,  # 无效ID
                query_text="valid",
                search_keywords=["valid"],
                timestamp=datetime.now(),
                results_count=1,
                top_result_url=""
            )
    
    def test_json_serialization(self):
        """测试JSON序列化和反序列化"""
        # 创建包含中文关键词的记录
        history = SearchHistory(
            id=0,
            query_text="中文查询测试",
            search_keywords=["数学", "微积分", "中文关键词"],
            timestamp=datetime.now(),
            results_count=8,
            top_result_url="https://example.com/chinese"
        )
        
        history_id = self.repo.create(history)
        retrieved_history = self.repo.get_by_id(history_id)
        
        assert retrieved_history.search_keywords == history.search_keywords
        assert all(isinstance(keyword, str) for keyword in retrieved_history.search_keywords)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])