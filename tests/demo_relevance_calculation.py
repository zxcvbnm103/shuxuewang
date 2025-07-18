"""
相关度计算和排序演示
Relevance Calculation and Sorting Demo
"""

from datetime import datetime
from math_search.relevance_calculation import RelevanceCalculator
from math_search.models import SearchResult


def create_demo_results():
    """创建演示用的搜索结果"""
    return [
        SearchResult(
            title="Introduction to Linear Algebra",
            url="https://khanacademy.org/math/linear-algebra",
            snippet="Learn basic linear algebra concepts including vectors and matrices",
            source="Khan Academy",
            relevance_score=0.0,  # 将被计算器更新
            timestamp=datetime.now(),
            math_content_detected=True
        ),
        SearchResult(
            title="Advanced Manifold Theory and Topology",
            url="https://arxiv.org/abs/2023.12345",
            snippet="Research paper on manifold topology, homomorphism, and differential geometry",
            source="arXiv",
            relevance_score=0.0,
            timestamp=datetime.now(),
            math_content_detected=True
        ),
        SearchResult(
            title="Linear Algebra Course - MIT OpenCourseWare",
            url="https://mit.edu/courses/18-06-linear-algebra",
            snippet="Graduate level course covering eigenvalues, eigenvectors, and matrix theory",
            source="MIT",
            relevance_score=0.0,
            timestamp=datetime.now(),
            math_content_detected=True
        ),
        SearchResult(
            title="Cooking Recipes for Beginners",
            url="https://example.com/cooking",
            snippet="Simple cooking recipes and kitchen tips for beginners",
            source="Example Site",
            relevance_score=0.0,
            timestamp=datetime.now(),
            math_content_detected=False
        ),
        SearchResult(
            title="Journal of Mathematical Analysis",
            url="https://elsevier.com/journal/jmaa",
            snippet="Research articles on functional analysis, differential equations, and theorem proofs",
            source="Elsevier",
            relevance_score=0.0,
            timestamp=datetime.now(),
            math_content_detected=True
        )
    ]


def demo_relevance_calculation():
    """演示相关度计算功能"""
    print("=" * 60)
    print("相关度计算和排序演示")
    print("Relevance Calculation and Sorting Demo")
    print("=" * 60)
    
    # 初始化计算器
    calculator = RelevanceCalculator()
    
    # 创建演示数据
    results = create_demo_results()
    query = "linear algebra eigenvalues"
    
    print(f"\n查询: {query}")
    print(f"Query: {query}")
    print("-" * 40)
    
    # 计算相关度
    print("\n1. 计算基础相关度评分...")
    for result in results:
        score = calculator.calculate_relevance(query, result)
        result.relevance_score = score
        print(f"   {result.title[:40]:<40} | 评分: {score:.3f}")
    
    # 应用数学领域权重提升
    print("\n2. 应用数学领域权重提升...")
    boosted_results = calculator.apply_math_domain_boost(results)
    
    for result in boosted_results:
        print(f"   {result.title[:40]:<40} | 提升后: {result.relevance_score:.3f}")
    
    # 排序结果
    print("\n3. 按相关度排序...")
    sorted_results = calculator.rank_results(boosted_results)
    
    print("\n最终排序结果:")
    print("Final Sorted Results:")
    print("-" * 80)
    
    for i, result in enumerate(sorted_results, 1):
        math_indicator = "🧮" if result.math_content_detected else "📄"
        print(f"{i}. {math_indicator} {result.title}")
        print(f"   URL: {result.url}")
        print(f"   评分: {result.relevance_score:.3f} | 来源: {result.source}")
        print(f"   摘要: {result.snippet[:60]}...")
        print()
    
    # 显示详细指标
    print("\n4. 详细排序指标分析:")
    print("Detailed Sorting Metrics Analysis:")
    print("-" * 80)
    
    metrics = calculator.get_advanced_sorting_metrics(results)
    
    for i, metric in enumerate(metrics, 1):
        print(f"{i}. {metric['title']}")
        print(f"   基础相关度: {metric['base_relevance']:.3f}")
        print(f"   来源权重: {metric['source_boost']:.2f}")
        print(f"   数学术语权重: {metric['math_terms_boost']:.2f}")
        print(f"   领域深度权重: {metric['domain_depth_boost']:.2f}")
        print(f"   学术级别权重: {metric['academic_level_boost']:.2f}")
        print(f"   总权重提升: {metric['total_boost']:.2f}")
        print(f"   最终评分: {metric['final_score']:.3f}")
        print()


def demo_different_queries():
    """演示不同查询的相关度计算"""
    print("\n" + "=" * 60)
    print("不同查询的相关度对比")
    print("Relevance Comparison for Different Queries")
    print("=" * 60)
    
    calculator = RelevanceCalculator()
    results = create_demo_results()
    
    queries = [
        "linear algebra",
        "manifold topology",
        "cooking recipes",
        "differential equations",
        "eigenvalues eigenvectors"
    ]
    
    for query in queries:
        print(f"\n查询: '{query}'")
        print("-" * 30)
        
        # 计算相关度并排序
        for result in results:
            score = calculator.calculate_relevance(query, result)
            result.relevance_score = score
        
        boosted_results = calculator.apply_math_domain_boost(results)
        sorted_results = calculator.rank_results(boosted_results)
        
        # 显示前3个结果
        for i, result in enumerate(sorted_results[:3], 1):
            print(f"  {i}. {result.title[:50]:<50} | {result.relevance_score:.3f}")


if __name__ == "__main__":
    demo_relevance_calculation()
    demo_different_queries()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("Demo completed!")
    print("=" * 60)