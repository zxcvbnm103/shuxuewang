#!/usr/bin/env python3
"""
应用功能测试脚本
"""
import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """测试核心模块导入"""
    print("🧪 测试模块导入...")
    
    try:
        import streamlit as st
        print(f"✅ Streamlit {st.__version__}")
    except ImportError as e:
        print(f"❌ Streamlit 导入失败: {e}")
        return False
    
    try:
        from math_search.models.search_result import SearchResult
        from math_search.models.search_history import SearchHistory
        from math_search.models.math_term import MathTerm
        print("✅ 数据模型导入成功")
    except ImportError as e:
        print(f"❌ 数据模型导入失败: {e}")
        return False
    
    try:
        from math_search.database.connection import DatabaseConnection
        from math_search.database.history_repository import HistoryRepository
        print("✅ 数据库模块导入成功")
    except ImportError as e:
        print(f"❌ 数据库模块导入失败: {e}")
        return False
    
    try:
        from math_search.config.settings import Settings
        print("✅ 配置模块导入成功")
    except ImportError as e:
        print(f"❌ 配置模块导入失败: {e}")
        return False
    
    return True

def test_models():
    """测试数据模型"""
    print("\n🧪 测试数据模型...")
    
    try:
        from math_search.models.search_result import SearchResult
        from datetime import datetime
        
        # 创建搜索结果
        result = SearchResult(
            title="测试标题",
            url="https://example.com",
            snippet="测试摘要",
            source="测试源",
            relevance_score=0.95,
            timestamp=datetime.now(),
            math_content_detected=True
        )
        
        print(f"✅ SearchResult 创建成功: {result.title}")
        
        from math_search.models.search_history import SearchHistory
        
        # 创建搜索历史
        history = SearchHistory(
            id=1,
            query_text="导数定义",
            search_keywords=["导数", "定义"],
            timestamp=datetime.now(),
            results_count=5,
            top_result_url="https://example.com"
        )
        
        print(f"✅ SearchHistory 创建成功: {history.query_text}")
        
        from math_search.models.math_term import MathTerm
        
        # 创建数学术语
        term = MathTerm(
            term="导数",
            latex_representation="f'(x)",
            category="微积分",
            definition="函数变化率的度量"
        )
        
        print(f"✅ MathTerm 创建成功: {term.term}")
        
        return True
        
    except Exception as e:
        print(f"❌ 数据模型测试失败: {e}")
        return False

def test_database():
    """测试数据库功能"""
    print("\n🧪 测试数据库功能...")
    
    try:
        from math_search.database.connection import DatabaseConnection
        
        # 测试数据库连接
        db = DatabaseConnection()
        conn = db.get_connection()
        
        # 执行简单查询
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result and result[0] == 1:
            print("✅ 数据库连接测试成功")
        else:
            print("❌ 数据库查询结果异常")
            return False
        
        cursor.close()
        db.close_connection()
        
        return True
        
    except Exception as e:
        print(f"❌ 数据库测试失败: {e}")
        return False

def test_config():
    """测试配置功能"""
    print("\n🧪 测试配置功能...")
    
    try:
        from math_search.config.settings import Settings
        
        # 创建设置实例
        settings = Settings()
        
        print(f"✅ 配置加载成功")
        print(f"   缓存目录: {settings.cache.cache_dir}")
        print(f"   缓存大小: {settings.cache.max_cache_size_mb}MB")
        print(f"   搜索超时: {settings.search_api.request_timeout}秒")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🧮 数学笔记智能搜索系统 - 功能测试")
    print("=" * 50)
    
    tests = [
        ("模块导入", test_imports),
        ("数据模型", test_models),
        ("数据库功能", test_database),
        ("配置功能", test_config),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！应用可以正常启动")
        print("\n🚀 启动应用:")
        print("   python start_app.py")
        print("   或")
        print("   streamlit run app.py")
        return 0
    else:
        print("⚠️  部分测试失败，请检查依赖和配置")
        return 1

if __name__ == "__main__":
    sys.exit(main())