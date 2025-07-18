#!/usr/bin/env python3
"""
增强数学领域排序演示
Enhanced Math Domain Sorting Demonstration
"""

from datetime import datetime
from math_search.relevance_calculation import RelevanceCalculator
from math_search.models import SearchResult


def main():
    """演示增强的数学领域排序功能"""
    print("=== 增强数学领域排序演示 ===")
    print("Enhanced Math Domain Sorting Demonstration")
    print()
    
    # 创建相关度计算器
    calculator = RelevanceCalculator()
    
    # 创建测试搜索结果
    test_results = [
        # 高级数学研究论文
        SearchResult(
            title="Category Theory and Homomorphism in Manifold Topology",
            url="https://arxiv.org/abs/2023.advanced-math",
            snippet="This research paper explores category theory, homomorphism, manifold topology, and functional analysis with rigorous theorem proofs",
            source="arXiv",
            relevance_score=0.6,
            timestamp=datetime.now(),
            math_content_detected=True
        ),
        
        # 基础教程
        SearchResult(
            title="Introduction to Basic Algebra",
            url="https://khanacademy.org/math/algebra-basics",
            snippet="Learn elementary algebra concepts with simple examples and basic tutorials for beginners",
            source="Khan Academy",
            relevance_score=0.7,
            timestamp=datetime.now(),
            math_content_detected=True
        ),
        
        # 大学课程
        SearchResult(
            title="Linear Algebra and Matrix Theory - MIT Course",
            url="https://mit.edu/courses/mathematics/linear-algebra",
            snippet="Graduate level course on linear algebra, eigenvalues, eigenvectors, and advanced matrix theory",
            source="MIT",
            relevance_score=0.65,
            timestamp=datetime.now(),
            math_content_detected=True
        ),
        
        # 学术期刊
        SearchResult(
            title="Journal of Mathematical Analysis: Differential Equations Research",
            url="https://elsevier.com/journal/mathematical-analysis/differential-equations",
            snippet="Research paper on differential equations, real analysis, and measure theory applications",
            source="Elsevier",
            relevance_score=0.55,
            timestamp=datetime.now(),
            math_content_detected=True
        ),
        
        # 非数学内容
        SearchResult(
            title="Programming Tutorial for Beginners",
            url="https://example.com/programming-tutorial",
            snippet="Learn programming basics with simple coding examples and software development",
            source="Example",
            relevance_score=0.8,
            timestamp=datetime.now(),
            math_content_detected=False
        )
    ]
    
    print("原始搜索结果:")
    print("Original Search Results:")
    print("-" * 60)
    for i, result in enumerate(test_results, 1):
        print(f"{i}. {result.title}")
        print(f"   来源: {result.source}")
        print(f"   原始评分: {result.relevance_score:.3f}")
        print(f"   数学内容: {'是' if result.math_content_detected else '否'}")
        print()
    
    # 应用数学领域权重提升
    print("应用数学领域权重提升...")
    print("Applying math domain boost...")
    boosted_results = calculator.apply_math_domain_boost(test_results.copy())
    
    # 执行排序
    print("执行智能排序...")
    print("Performing intelligent sorting...")
    sorted_results = calculator.rank_results(boosted_results)
    
    print("\n增强排序后的结果:")
    print("Enhanced Sorted Results:")
    print("=" * 60)
    for i, result in enumerate(sorted_results, 1):
        print(f"{i}. {result.title}")
        print(f"   来源: {result.source}")
        print(f"   最终评分: {result.relevance_score:.3f}")
        print(f"   数学内容: {'是' if result.math_content_detected else '否'}")
        print()
    
    # 显示详细的排序指标
    print("详细排序指标分析:")
    print("Detailed Sorting Metrics Analysis:")
    print("=" * 60)
    
    metrics = calculator.get_advanced_sorting_metrics(test_results)
    
    for i, (result, metric) in enumerate(zip(sorted_results, metrics), 1):
        print(f"{i}. {metric['title']}")
        print(f"   基础相关度: {metric['base_relevance']:.3f}")
        print(f"   来源权重: {metric['source_boost']:.3f}")
        print(f"   数学术语权重: {metric['math_terms_boost']:.3f}")
        print(f"   领域深度权重: {metric['domain_depth_boost']:.3f}")
        print(f"   复杂度权重: {metric['complexity_boost']:.3f}")
        print(f"   学术级别权重: {metric['academic_level_boost']:.3f}")
        print(f"   总权重提升: {metric['total_boost']:.3f}")
        print(f"   最终评分: {metric['final_score']:.3f}")
        print()
    
    # 演示特定功能
    print("特定功能演示:")
    print("Specific Feature Demonstrations:")
    print("=" * 60)
    
    # 数学术语密度测试
    high_density_text = "manifold topology homomorphism category theory functional analysis theorem proof"
    density_boost = calculator._calculate_math_term_density(high_density_text)
    print(f"高密度数学术语文本权重: {density_boost:.3f}")
    print(f"High-density math terms boost: {density_boost:.3f}")
    
    # 数学术语共现测试
    cooccurrence_boost = calculator._calculate_math_term_cooccurrence(high_density_text)
    print(f"数学术语共现权重: {cooccurrence_boost:.3f}")
    print(f"Math terms co-occurrence boost: {cooccurrence_boost:.3f}")
    
    # 数学复杂度测试
    complexity_score = calculator._calculate_mathematical_complexity_score(high_density_text)
    print(f"数学复杂度评分: {complexity_score:.3f}")
    print(f"Mathematical complexity score: {complexity_score:.3f}")
    
    print("\n=== 演示完成 ===")
    print("=== Demonstration Complete ===")


if __name__ == "__main__":
    main()