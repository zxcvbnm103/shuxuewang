"""
搜索管理器演示脚本
Search Manager Demo Script
"""

import os
import sys
from datetime import datetime
from typing import List

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from math_search.search_management.search_manager import SearchManager
from math_search.models.search_result import SearchResult
from math_search.config.settings import Settings, SearchAPIConfig


def create_demo_settings() -> Settings:
    """创建演示用的设置"""
    settings = Settings()
    settings.search_api = SearchAPIConfig(
        google_api_key="demo_google_key",  # 实际使用时需要真实的API密钥
        google_search_engine_id="demo_engine_id",
        bing_api_key="demo_bing_key",
        max_results_per_source=5,
        request_timeout=10
    )
    return settings


def create_mock_search_results() -> List[List[SearchResult]]:
    """创建模拟搜索结果用于演示"""
    # 模拟Google搜索结果
    google_results = [
        SearchResult(
            title="微积分基础教程",
            url="https://math.example.com/calculus-basics",
            snippet="这是一个关于微积分基础的教程，包含导数和积分的详细讲解。",
            source="Google",
            relevance_score=0.95,
            timestamp=datetime.now(),
            math_content_detected=True
        ),
        SearchResult(
            title="线性代数与矩阵运算",
            url="https://algebra.example.com/linear-algebra",
            snippet="线性代数是数学的重要分支，本文介绍矩阵运算和向量空间。",
            source="Google",
            relevance_score=0.88,
            timestamp=datetime.now(),
            math_content_detected=True
        ),
        SearchResult(
            title="概率论与数理统计",
            url="https://stats.example.com/probability",
            snippet="概率论是研究随机现象的数学理论，统计学是其重要应用。",
            source="Google",
            relevance_score=0.82,
            timestamp=datetime.now(),
            math_content_detected=True
        )
    ]
    
    # 模拟学术搜索结果
    academic_results = [
        SearchResult(
            title="Advanced Methods in Differential Calculus",
            url="http://arxiv.org/abs/2301.12345",
            snippet="This paper presents advanced techniques for solving complex differential equations using modern computational methods.",
            source="arXiv",
            relevance_score=0.92,
            timestamp=datetime.now(),
            math_content_detected=True
        ),
        SearchResult(
            title="Applications of Linear Algebra in Machine Learning",
            url="http://arxiv.org/abs/2302.67890",
            snippet="We explore how linear algebraic concepts are fundamental to understanding machine learning algorithms.",
            source="arXiv",
            relevance_score=0.89,
            timestamp=datetime.now(),
            math_content_detected=True
        )
    ]
    
    # 模拟Bing搜索结果
    bing_results = [
        SearchResult(
            title="数学公式在线计算器",
            url="https://calculator.example.com/math",
            snippet="在线数学计算器，支持各种数学公式的计算和图形绘制。",
            source="Bing",
            relevance_score=0.75,
            timestamp=datetime.now(),
            math_content_detected=True
        )
    ]
    
    return [google_results, academic_results, bing_results]


def demo_search_manager_basic():
    """演示搜索管理器基本功能"""
    print("=== 搜索管理器基本功能演示 ===\n")
    
    # 创建搜索管理器
    settings = create_demo_settings()
    manager = SearchManager(settings)
    
    print("1. 搜索管理器初始化完成")
    print(f"   - Google API配置: {'已配置' if settings.search_api.google_api_key else '未配置'}")
    print(f"   - Bing API配置: {'已配置' if settings.search_api.bing_api_key else '未配置'}")
    print(f"   - 最大结果数: {settings.search_api.max_results_per_source}")
    print()
    
    # 演示数学内容检测
    print("2. 数学内容检测演示:")
    test_texts = [
        "这是关于微积分和导数的内容",
        "Linear algebra with matrices and vectors",
        "The equation $x^2 + y^2 = 1$ represents a circle",
        "这只是普通的文本内容",
        "Regular text without math content"
    ]
    
    for text in test_texts:
        is_math = manager._detect_math_content(text)
        print(f"   '{text}' -> {'包含数学内容' if is_math else '不包含数学内容'}")
    print()


def demo_search_results_combination():
    """演示搜索结果合并功能"""
    print("=== 搜索结果合并演示 ===\n")
    
    settings = create_demo_settings()
    manager = SearchManager(settings)
    
    # 获取模拟搜索结果
    mock_results = create_mock_search_results()
    
    print("1. 各搜索源结果:")
    for i, results in enumerate(mock_results):
        source_names = ["Google", "学术搜索", "Bing"]
        print(f"   {source_names[i]}搜索结果 ({len(results)}个):")
        for result in results:
            print(f"     - {result.title} (相关度: {result.relevance_score:.2f})")
    print()
    
    # 合并结果
    combined = manager.combine_results(mock_results)
    
    print("2. 合并后的结果 (按相关度排序):")
    for i, result in enumerate(combined, 1):
        print(f"   {i}. {result.title}")
        print(f"      来源: {result.source} | 相关度: {result.relevance_score:.2f}")
        print(f"      URL: {result.url}")
        print(f"      摘要: {result.snippet[:50]}...")
        print()


def demo_search_workflow():
    """演示完整搜索工作流"""
    print("=== 完整搜索工作流演示 ===\n")
    
    settings = create_demo_settings()
    manager = SearchManager(settings)
    
    # 模拟搜索关键词
    keywords = ["微积分", "导数", "积分"]
    print(f"搜索关键词: {', '.join(keywords)}")
    print()
    
    # 注意：这里使用模拟数据，因为没有真实的API密钥
    print("注意: 由于没有真实的API密钥，以下演示使用模拟数据\n")
    
    # 模拟网页搜索
    print("1. 网页搜索结果:")
    try:
        # 在实际环境中，这会调用真实的API
        # web_results = manager.search_web(keywords)
        web_results = create_mock_search_results()[0]  # 使用模拟数据
        
        for result in web_results:
            print(f"   - {result.title} ({result.source})")
            print(f"     相关度: {result.relevance_score:.2f} | 数学内容: {'是' if result.math_content_detected else '否'}")
    except Exception as e:
        print(f"   网页搜索失败: {e}")
    print()
    
    # 模拟学术搜索
    print("2. 学术搜索结果:")
    try:
        # academic_results = manager.search_academic(keywords)
        academic_results = create_mock_search_results()[1]  # 使用模拟数据
        
        for result in academic_results:
            print(f"   - {result.title} ({result.source})")
            print(f"     相关度: {result.relevance_score:.2f}")
    except Exception as e:
        print(f"   学术搜索失败: {e}")
    print()
    
    # 合并结果
    print("3. 合并所有搜索结果:")
    all_results = [web_results, academic_results]
    combined = manager.combine_results(all_results)
    
    print(f"   总共找到 {len(combined)} 个结果")
    print("   前3个最相关的结果:")
    for i, result in enumerate(combined[:3], 1):
        print(f"   {i}. {result.title} (相关度: {result.relevance_score:.2f})")


def demo_error_handling():
    """演示错误处理"""
    print("=== 错误处理演示 ===\n")
    
    # 创建没有API密钥的设置
    settings = Settings()
    settings.search_api = SearchAPIConfig()  # 空配置
    
    manager = SearchManager(settings)
    
    print("1. 无API密钥配置的搜索:")
    results = manager.search_web(["test"])
    print(f"   结果数量: {len(results)} (应该为0，因为没有API密钥)")
    print()
    
    print("2. 空关键词搜索:")
    results = manager.search_web([])
    print(f"   空关键词结果: {len(results)} (应该为0)")
    
    results = manager.search_web([""])
    print(f"   空字符串关键词结果: {len(results)} (应该为0)")
    print()
    
    print("3. 结果去重演示:")
    duplicate_result = SearchResult(
        title="重复结果",
        url="https://example.com/same",
        snippet="相同的URL",
        source="Test",
        relevance_score=0.8,
        timestamp=datetime.now(),
        math_content_detected=True
    )
    
    # 创建包含重复结果的列表
    results_with_duplicates = [[duplicate_result], [duplicate_result]]
    combined = manager.combine_results(results_with_duplicates)
    
    print(f"   原始结果数: 2 (重复)")
    print(f"   去重后结果数: {len(combined)} (应该为1)")


def main():
    """主函数"""
    print("搜索管理器功能演示")
    print("=" * 50)
    print()
    
    try:
        demo_search_manager_basic()
        print("\n" + "=" * 50 + "\n")
        
        demo_search_results_combination()
        print("\n" + "=" * 50 + "\n")
        
        demo_search_workflow()
        print("\n" + "=" * 50 + "\n")
        
        demo_error_handling()
        
        print("\n演示完成！")
        print("\n使用说明:")
        print("1. 在实际使用中，需要在.env文件中配置真实的API密钥")
        print("2. 支持的API包括Google Custom Search和Bing Search")
        print("3. 搜索管理器会自动检测数学内容并进行相关度排序")
        print("4. 支持多个搜索源的结果合并和去重")
        
    except Exception as e:
        print(f"演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()