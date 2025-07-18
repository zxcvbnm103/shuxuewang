"""
SQLite数据库连接管理器
SQLite Database Connection Manager
"""

import sqlite3
import threading
from pathlib import Path
from typing import Optional
from contextlib import contextmanager


class DatabaseConnection:
    """SQLite数据库连接管理器"""
    
    def __init__(self, db_path: str = "math_search.db"):
        """
        初始化数据库连接管理器
        
        Args:
            db_path: 数据库文件路径
        """
        self.db_path = Path(db_path)
        self._local = threading.local()
        self._ensure_database_exists()
    
    def _ensure_database_exists(self):
        """确保数据库文件存在并创建必要的表"""
        # 创建数据库目录（如果不存在）
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 创建数据库表
        with self.get_connection() as conn:
            self._create_tables(conn)
    
    def _create_tables(self, conn: sqlite3.Connection):
        """创建数据库表"""
        cursor = conn.cursor()
        
        # 创建搜索历史表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_text TEXT NOT NULL,
                search_keywords TEXT NOT NULL,  -- JSON格式存储关键词列表
                timestamp TEXT NOT NULL,
                results_count INTEGER NOT NULL DEFAULT 0,
                top_result_url TEXT
            )
        ''')
        
        # 创建索引以提高查询性能
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_search_history_timestamp 
            ON search_history(timestamp)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_search_history_query_text 
            ON search_history(query_text)
        ''')
        
        conn.commit()
    
    def get_connection(self) -> sqlite3.Connection:
        """
        获取数据库连接（线程安全）
        
        Returns:
            SQLite连接对象
        """
        if not hasattr(self._local, 'connection'):
            self._local.connection = sqlite3.connect(
                str(self.db_path),
                check_same_thread=False
            )
            # 启用外键约束
            self._local.connection.execute("PRAGMA foreign_keys = ON")
            # 设置行工厂以便返回字典格式的结果
            self._local.connection.row_factory = sqlite3.Row
        
        return self._local.connection
    
    @contextmanager
    def get_cursor(self):
        """
        获取数据库游标的上下文管理器
        
        Yields:
            SQLite游标对象
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
    
    def close_connection(self):
        """关闭当前线程的数据库连接"""
        if hasattr(self._local, 'connection'):
            self._local.connection.close()
            delattr(self._local, 'connection')
    
    def execute_query(self, query: str, params: tuple = ()) -> list:
        """
        执行查询并返回结果
        
        Args:
            query: SQL查询语句
            params: 查询参数
            
        Returns:
            查询结果列表
        """
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """
        执行更新操作并返回影响的行数
        
        Args:
            query: SQL更新语句
            params: 更新参数
            
        Returns:
            影响的行数
        """
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.rowcount
    
    def get_last_insert_id(self) -> int:
        """
        获取最后插入记录的ID
        
        Returns:
            最后插入的记录ID
        """
        with self.get_cursor() as cursor:
            cursor.execute("SELECT last_insert_rowid()")
            result = cursor.fetchone()
            return result[0] if result else 0
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close_connection()