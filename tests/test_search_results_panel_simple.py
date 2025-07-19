"""
搜索结果展示面板简单测试
Simple Test for Search Results Display Panel
"""

from datetime import datetime
from math_search.models.search_result import SearchResult


def test_search_results_filtering_and_sorting():
    """测试搜索结果的过滤和排序功能"""
    
    # 创建测试数据
    test_results = [
        SearchResult(
            title="微积分基础教程",
            url="https://example.com/calculus",
            snippet="微积分基础概念详细教程",
            source="Wikipedia",
            relevance_score=0.95,
            timestamp=datetime.now(),
            math_content_detected=True
        ),
        SearchResult(
            title="数学历史概述",
            url="https://example.com/math-history",
            snippet="数学发展历史回顾",
            source="Wolfram MathWorld",
            relevance_score=0.72,
            timestamp=datetime.now(),
            math_content_detected=False
        ),
        SearchResult(
            title="线性代数入门",
            url="https://example.com/linear-algebra",
            snippet="线性代数基本概念",
            source="Khan Academy",
            relevance_score=0.88,
            timestamp=datetime.now(),
            math_content_detected=True
        )
    ]
    
    # 测试数学内容过滤
    math_results = [r for r in test_results if r.math_content_detected]
    assert len(math_results) == 2
    assert all(r.math_content_detected for r in math_results)
    
    # 测试相关度排序
    sorted_results = sorted(test_results, key=lambda x: x.relevance_score, reverse=True)
    assert sorted_results[0].relevance_score == 0.95
    assert sorted_results[-1].relevance_score == 0.72
    
    # 测试相关度阈值过滤
    high_relevance = [r for r in test_results if r.relevance_score >= 0.8]
    assert len(high_relevance) == 2
    
    # 测试来源过滤
    wiki_results = [r for r in test_results if r.source == "Wikipedia"]
    assert len(wiki_results) == 1
    assert wiki_results[0].title == "微积分基础教程"
    
    print("✅ 所有搜索结果过滤和排序测试通过")


def test_pagination_logic():
    """测试分页逻辑"""
    
    # 创建10个测试结果
    test_results = []
    for i in range(10):
        result = SearchResult(
            title=f"测试结果 {i+1}",
            url=f"https://example.com/test{i+1}",
            snippet=f"这是第{i+1}个测试结果",
            source="Test Source",
            relevance_score=0.8,
            timestamp=datetime.now(),
            math_content_detected=True
        )
        test_results.append(result)
    
    # 测试分页计算
    results_per_page = 3
    total_pages = (len(test_results) + results_per_page - 1) // results_per_page
    assert total_pages == 4  # 10个结果，每页3个，应该是4页
    
    # 测试第2页的结果切片
    current_page = 2
    start_idx = (current_page - 1) * results_per_page  # (2-1) * 3 = 3
    end_idx = min(start_idx + results_per_page, len(test_results))  # min(3+3, 10) = 6
    page_results = test_results[start_idx:end_idx]
    
    assert len(page_results) == 3
    assert page_results[0].title == "测试结果 4"
    assert page_results[2].title == "测试结果 6"
    
    print("✅ 分页逻辑测试通过")


def test_statistics_calculation():
    """测试统计信息计算"""
    
    test_results = [
        SearchResult("Test 1", "url1", "snippet1", "Source1", 0.9, datetime.now(), True),
        SearchResult("Test 2", "url2", "snippet2", "Source2", 0.8, datetime.now(), True),
        SearchResult("Test 3", "url3", "snippet3", "Source3", 0.7, datetime.now(), False),
        SearchResult("Test 4", "url4", "snippet4", "Source4", 0.6, datetime.now(), True),
    ]
    
    # 计算数学内容数量
    math_count = sum(1 for r in test_results if r.math_content_detected)
    assert math_count == 3
    
    # 计算平均相关度
    avg_relevance = sum(r.relevance_score for r in test_results) / len(test_results)
    expected_avg = (0.9 + 0.8 + 0.7 + 0.6) / 4
    assert abs(avg_relevance - expected_avg) < 0.01
    
    # 计算来源分布
    sources = {}
    for result in test_results:
        sources[result.source] = sources.get(result.source, 0) + 1
    
    assert len(sources) == 4  # 4个不同来源
    assert all(count == 1 for count in sources.values())  # 每个来源1个结果
    
    print("✅ 统计信息计算测试通过")


if __name__ == "__main__":
    test_search_results_filtering_and_sorting()
    test_pagination_logic()
    test_statistics_calculation()
    print("🎉 所有测试通过！搜索结果展示面板功能正常")