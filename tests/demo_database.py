"""
数据库功能演示脚本
Database Functionality Demo Script
"""

from datetime import datetime, timedelta
from math_search.database.connection import DatabaseConnection
from math_search.database.history_repository import HistoryRepository
from math_search.models.search_history import SearchHistory


def demo_database_operations():
    """演示数据库操作"""
    print("=== 数学笔记搜索历史数据库演示 ===\n")
    
    # 创建数据库连接
    print("1. 创建数据库连接...")
    db_conn = DatabaseConnection("demo_math_search.db")
    repo = HistoryRepository(db_conn)
    print("✓ 数据库连接创建成功\n")
    
    # 创建示例搜索历史记录
    print("2. 创建搜索历史记录...")
    sample_histories = [
        SearchHistory(
            id=0,
            query_text="微积分基本定理",
            search_keywords=["微积分", "基本定理", "牛顿-莱布尼茨公式"],
            timestamp=datetime.now() - timedelta(hours=2),
            results_count=15,
            top_result_url="https://zh.wikipedia.org/wiki/微积分基本定理"
        ),
        SearchHistory(
            id=0,
            query_text="线性代数矩阵运算",
            search_keywords=["线性代数", "矩阵", "运算"],
            timestamp=datetime.now() - timedelta(hours=1),
            results_count=12,
            top_result_url="https://example.com/linear-algebra"
        ),
        SearchHistory(
            id=0,
            query_text="概率论贝叶斯定理",
            search_keywords=["概率论", "贝叶斯定理", "条件概率"],
            timestamp=datetime.now() - timedelta(minutes=30),
            results_count=8,
            top_result_url="https://example.com/bayes-theorem"
        )
    ]
    
    created_ids = []
    for history in sample_histories:
        history_id = repo.create(history)
        created_ids.append(history_id)
        print(f"✓ 创建记录 ID: {history_id}, 查询: {history.query_text}")
    print()
    
    # 查询操作演示
    print("3. 查询操作演示...")
    
    # 根据ID查询
    print("3.1 根据ID查询:")
    first_history = repo.get_by_id(created_ids[0])
    if first_history:
        print(f"   ID {created_ids[0]}: {first_history.query_text}")
        print(f"   关键词: {', '.join(first_history.search_keywords)}")
        print(f"   结果数: {first_history.results_count}")
    print()
    
    # 获取所有记录
    print("3.2 获取所有记录:")
    all_histories = repo.get_all()
    for history in all_histories:
        print(f"   {history.timestamp.strftime('%Y-%m-%d %H:%M')} - {history.query_text}")
    print()
    
    # 搜索功能
    print("3.3 文本搜索:")
    search_results = repo.search_by_query("微积分")
    print(f"   搜索'微积分'找到 {len(search_results)} 条记录:")
    for result in search_results:
        print(f"   - {result.query_text}")
    print()
    
    # 获取最近记录
    print("3.4 获取最近记录:")
    recent_histories = repo.get_recent(days=1)
    print(f"   最近1天内的记录数: {len(recent_histories)}")
    for history in recent_histories:
        print(f"   - {history.query_text} ({history.timestamp.strftime('%H:%M')})")
    print()
    
    # 更新操作演示
    print("4. 更新操作演示...")
    if created_ids:
        update_history = repo.get_by_id(created_ids[0])
        if update_history:
            original_count = update_history.results_count
            update_history.results_count = 20
            update_history.query_text += " (已更新)"
            
            success = repo.update(update_history)
            if success:
                print(f"✓ 更新成功: 结果数从 {original_count} 更新为 {update_history.results_count}")
                print(f"   查询文本: {update_history.query_text}")
    print()
    
    # 统计信息
    print("5. 统计信息:")
    stats = repo.get_statistics()
    print(f"   总记录数: {stats['total_count']}")
    print(f"   最近记录数: {stats['recent_count']}")
    print(f"   平均结果数: {stats['avg_results']}")
    if 'earliest_record' in stats:
        print(f"   最早记录: {stats['earliest_record']}")
        print(f"   最新记录: {stats['latest_record']}")
    print()
    
    # 删除操作演示
    print("6. 删除操作演示...")
    if len(created_ids) > 1:
        delete_id = created_ids[-1]  # 删除最后一个记录
        success = repo.delete(delete_id)
        if success:
            print(f"✓ 删除记录 ID: {delete_id}")
            print(f"   剩余记录数: {repo.get_count()}")
    print()
    
    # 清理演示
    print("7. 数据清理演示...")
    # 删除超过30天的记录（演示用，实际不会有这么旧的记录）
    deleted_count = repo.delete_old_records(days=30)
    print(f"   删除30天前的记录数: {deleted_count}")
    print(f"   当前总记录数: {repo.get_count()}")
    print()
    
    # 关闭连接
    print("8. 关闭数据库连接...")
    db_conn.close_connection()
    print("✓ 数据库连接已关闭")
    print("\n=== 演示完成 ===")


def demo_error_handling():
    """演示错误处理"""
    print("\n=== 错误处理演示 ===\n")
    
    db_conn = DatabaseConnection("demo_error_handling.db")
    repo = HistoryRepository(db_conn)
    
    # 测试数据验证错误
    print("1. 数据验证错误:")
    try:
        invalid_history = SearchHistory(
            id=1,
            query_text="",  # 空查询文本
            search_keywords=["test"],
            timestamp=datetime.now(),
            results_count=1,
            top_result_url=""
        )
    except ValueError as e:
        print(f"   ✓ 捕获验证错误: {e}")
    
    # 测试查询不存在的记录
    print("\n2. 查询不存在的记录:")
    non_existent = repo.get_by_id(99999)
    if non_existent is None:
        print("   ✓ 正确返回 None")
    
    # 测试删除不存在的记录
    print("\n3. 删除不存在的记录:")
    success = repo.delete(99999)
    if not success:
        print("   ✓ 正确返回 False")
    
    db_conn.close_connection()
    print("\n=== 错误处理演示完成 ===")


if __name__ == "__main__":
    demo_database_operations()
    demo_error_handling()