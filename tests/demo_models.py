"""
数据模型演示脚本
Data Models Demo Script
"""

from datetime import datetime
from math_search.models import SearchResult, SearchHistory, MathTerm


def demo_search_result():
    """演示 SearchResult 模型"""
    print("=== SearchResult 演示 ===")
    
    # 创建搜索结果
    result = SearchResult(
        title="线性代数基础教程",
        url="https://example.com/linear-algebra",
        snippet="线性代数是数学的一个重要分支，研究向量空间和线性映射...",
        source="教育网站",
        relevance_score=0.92,
        timestamp=datetime.now(),
        math_content_detected=True
    )
    
    print(f"标题: {result.title}")
    print(f"URL: {result.url}")
    print(f"相关度: {result.relevance_score}")
    print(f"包含数学内容: {result.math_content_detected}")
    
    # 序列化和反序列化
    result_dict = result.to_dict()
    print(f"序列化后的时间戳: {result_dict['timestamp']}")
    
    reconstructed = SearchResult.from_dict(result_dict)
    print(f"重构后的标题: {reconstructed.title}")
    print()


def demo_search_history():
    """演示 SearchHistory 模型"""
    print("=== SearchHistory 演示 ===")
    
    # 创建搜索历史
    history = SearchHistory(
        id=1,
        query_text="矩阵乘法运算规则",
        search_keywords=["矩阵", "乘法", "运算", "线性代数"],
        timestamp=datetime.now(),
        results_count=25,
        top_result_url="https://example.com/matrix-multiplication"
    )
    
    print(f"查询ID: {history.id}")
    print(f"查询文本: {history.query_text}")
    print(f"关键词: {', '.join(history.search_keywords)}")
    print(f"结果数量: {history.results_count}")
    print(f"摘要: {history.get_summary()}")
    print()


def demo_math_term():
    """演示 MathTerm 模型"""
    print("=== MathTerm 演示 ===")
    
    # 创建数学术语
    term = MathTerm(
        term="导数",
        latex_representation=r"\frac{d}{dx}f(x)",
        category="calculus",
        confidence=0.95
    )
    
    print(f"术语: {term.term}")
    print(f"LaTeX表示: {term.latex_representation}")
    print(f"类别: {term.category}")
    print(f"置信度: {term.confidence}")
    print(f"是否高置信度: {term.is_high_confidence()}")
    
    # 测试不同类别
    categories = ["algebra", "geometry", "statistics"]
    for cat in categories:
        test_term = MathTerm("测试术语", "x", cat, 0.8)
        print(f"类别 {cat} 创建成功")
    print()


def demo_serialization():
    """演示序列化功能"""
    print("=== 序列化演示 ===")
    
    # 创建所有三种模型的实例
    result = SearchResult(
        title="微积分入门",
        url="https://example.com/calculus",
        snippet="微积分是研究变化率的数学分支...",
        source="学术网站",
        relevance_score=0.88,
        timestamp=datetime.now(),
        math_content_detected=True
    )
    
    history = SearchHistory(
        id=2,
        query_text="积分计算方法",
        search_keywords=["积分", "计算", "微积分"],
        timestamp=datetime.now(),
        results_count=18,
        top_result_url="https://example.com/integration"
    )
    
    term = MathTerm(
        term="积分",
        latex_representation=r"\int f(x) dx",
        category="calculus",
        confidence=0.9
    )
    
    # 序列化所有模型
    models_data = {
        'search_result': result.to_dict(),
        'search_history': history.to_dict(),
        'math_term': term.to_dict()
    }
    
    print("所有模型序列化成功:")
    for model_type, data in models_data.items():
        print(f"  {model_type}: {len(str(data))} 字符")
    
    # 反序列化验证
    reconstructed_result = SearchResult.from_dict(models_data['search_result'])
    reconstructed_history = SearchHistory.from_dict(models_data['search_history'])
    reconstructed_term = MathTerm.from_dict(models_data['math_term'])
    
    print("所有模型反序列化成功:")
    print(f"  SearchResult: {reconstructed_result.title}")
    print(f"  SearchHistory: {reconstructed_history.query_text}")
    print(f"  MathTerm: {reconstructed_term.term}")


if __name__ == "__main__":
    demo_search_result()
    demo_search_history()
    demo_math_term()
    demo_serialization()