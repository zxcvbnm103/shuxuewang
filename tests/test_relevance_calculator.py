"""
相关度计算器测试
Relevance Calculator Tests
"""

import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock

from math_search.relevance_calculation import RelevanceCalculator
from math_search.models import SearchResult


class TestRelevanceCalculator:
    """相关度计算器测试类"""
    
    def setup_method(self):
        """测试前设置"""
        self.calculator = RelevanceCalculator()
        
        # 创建测试用的搜索结果
        self.sample_results = [
            SearchResult(
                title="Linear Algebra Fundamentals",
                url="https://mathworld.wolfram.com/LinearAlgebra.html",
                snippet="Linear algebra is the branch of mathematics concerning linear equations and linear functions",
                source="Wolfram MathWorld",
                relevance_score=0.0,  # 将被计算器更新
                timestamp=datetime.now(),
                math_content_detected=True
            ),
            SearchResult(
                title="Introduction to Calculus",
                url="https://mit.edu/calculus/intro",
                snippet="Calculus is the mathematical study of continuous change",
                source="MIT OpenCourseWare",
                relevance_score=0.0,
                timestamp=datetime.now(),
                math_content_detected=True
            ),
            SearchResult(
                title="Basic Programming Tutorial",
                url="https://example.com/programming",
                snippet="Learn programming basics with simple examples",
                source="Example Site",
                relevance_score=0.0,
                timestamp=datetime.now(),
                math_content_detected=False
            )
        ]
    
    def test_calculate_relevance_basic(self):
        """测试基础相关度计算"""
        query = "linear algebra"
        result = self.sample_results[0]
        
        score = self.calculator.calculate_relevance(query, result)
        
        assert 0.0 <= score <= 1.0
        assert score > 0.5  # 应该有较高的相关度
    
    def test_calculate_relevance_math_content_boost(self):
        """测试数学内容检测加成"""
        query = "mathematics"
        
        # 有数学内容的结果
        math_result = self.sample_results[0]
        math_score = self.calculator.calculate_relevance(query, math_result)
        
        # 无数学内容的结果
        non_math_result = self.sample_results[2]
        non_math_score = self.calculator.calculate_relevance(query, non_math_result)
        
        # 数学内容应该有更高的评分
        assert math_score > non_math_score
    
    def test_calculate_relevance_title_boost(self):
        """测试标题匹配加成"""
        query = "linear algebra"
        result = self.sample_results[0]  # 标题包含"Linear Algebra"
        
        score = self.calculator.calculate_relevance(query, result)
        
        # 标题匹配应该提供加成
        assert score > 0.6
    
    def test_calculate_relevance_empty_query(self):
        """测试空查询"""
        query = ""
        result = self.sample_results[0]
        
        score = self.calculator.calculate_relevance(query, result)
        
        assert score >= 0.0
        assert score <= 1.0
    
    def test_calculate_relevance_no_match(self):
        """测试完全不匹配的查询"""
        query = "cooking recipes"
        result = self.sample_results[0]  # 数学相关内容
        
        score = self.calculator.calculate_relevance(query, result)
        
        assert 0.0 <= score <= 1.0
        assert score < 0.5  # 应该有较低的相关度
    
    def test_keyword_matching_math_terms(self):
        """测试数学术语关键词匹配"""
        query = "calculus derivative integral"
        result = SearchResult(
            title="Calculus: Derivatives and Integrals",
            url="https://example.com/calculus",
            snippet="Learn about derivatives and integrals in calculus",
            source="Math Site",
            relevance_score=0.0,
            timestamp=datetime.now(),
            math_content_detected=True
        )
        
        score = self.calculator.calculate_relevance(query, result)
        
        # 多个数学术语匹配应该有较高分
        assert score > 0.5
    
    def test_rank_results(self):
        """测试结果排序"""
        # 设置不同的相关度评分
        results = [
            SearchResult(
                title="Low relevance",
                url="https://example.com/low",
                snippet="Not very relevant content",
                source="Example",
                relevance_score=0.3,
                timestamp=datetime.now(),
                math_content_detected=False
            ),
            SearchResult(
                title="High relevance",
                url="https://example.com/high",
                snippet="Very relevant content",
                source="Example",
                relevance_score=0.9,
                timestamp=datetime.now(),
                math_content_detected=True
            ),
            SearchResult(
                title="Medium relevance",
                url="https://example.com/medium",
                snippet="Somewhat relevant content",
                source="Example",
                relevance_score=0.6,
                timestamp=datetime.now(),
                math_content_detected=False
            )
        ]
        
        ranked_results = self.calculator.rank_results(results)
        
        # 检查排序是否正确（降序）
        assert ranked_results[0].relevance_score == 0.9
        assert ranked_results[1].relevance_score == 0.6
        assert ranked_results[2].relevance_score == 0.3
    
    def test_apply_math_domain_boost_academic_sources(self):
        """测试学术来源权重提升"""
        results = [
            SearchResult(
                title="Math Paper",
                url="https://arxiv.org/abs/1234.5678",
                snippet="Mathematical research paper",
                source="arXiv",
                relevance_score=0.5,
                timestamp=datetime.now(),
                math_content_detected=True
            ),
            SearchResult(
                title="Regular Article",
                url="https://example.com/article",
                snippet="Regular article about math",
                source="Example",
                relevance_score=0.5,
                timestamp=datetime.now(),
                math_content_detected=True
            )
        ]
        
        boosted_results = self.calculator.apply_math_domain_boost(results)
        
        # arXiv来源应该有更高的评分
        arxiv_result = next(r for r in boosted_results if 'arxiv.org' in r.url)
        regular_result = next(r for r in boosted_results if 'example.com' in r.url)
        
        assert arxiv_result.relevance_score > regular_result.relevance_score
    
    def test_apply_math_domain_boost_math_content(self):
        """测试数学内容检测权重提升"""
        results = [
            SearchResult(
                title="Math Content",
                url="https://example.com/math",
                snippet="Mathematical content with formulas",
                source="Example",
                relevance_score=0.5,
                timestamp=datetime.now(),
                math_content_detected=True
            ),
            SearchResult(
                title="Non-Math Content",
                url="https://example.com/other",
                snippet="Regular content without math",
                source="Example",
                relevance_score=0.5,
                timestamp=datetime.now(),
                math_content_detected=False
            )
        ]
        
        boosted_results = self.calculator.apply_math_domain_boost(results)
        
        # 数学内容应该有更高的评分
        math_result = next(r for r in boosted_results if r.math_content_detected)
        non_math_result = next(r for r in boosted_results if not r.math_content_detected)
        
        assert math_result.relevance_score > non_math_result.relevance_score
    
    def test_apply_math_domain_boost_math_terms(self):
        """测试数学术语权重提升"""
        results = [
            SearchResult(
                title="Algebra and Calculus",
                url="https://example.com/math",
                snippet="Learn algebra, calculus, and geometry theorems",
                source="Example",
                relevance_score=0.5,
                timestamp=datetime.now(),
                math_content_detected=True
            ),
            SearchResult(
                title="General Topic",
                url="https://example.com/general",
                snippet="General discussion about topics",
                source="Example",
                relevance_score=0.5,
                timestamp=datetime.now(),
                math_content_detected=False
            )
        ]
        
        boosted_results = self.calculator.apply_math_domain_boost(results)
        
        # 包含数学术语的结果应该有更高的评分
        math_terms_result = boosted_results[0]
        general_result = boosted_results[1]
        
        assert math_terms_result.relevance_score > general_result.relevance_score
    
    def test_tokenize_text(self):
        """测试文本分词"""
        text = "Hello, world! This is a test."
        tokens = self.calculator._tokenize_text(text)
        
        expected_tokens = ["Hello", "world", "This", "is", "a", "test"]
        assert tokens == expected_tokens
    
    def test_tokenize_text_with_math_symbols(self):
        """测试包含数学符号的文本分词"""
        text = "f(x) = x^2 + 2x - 1"
        tokens = self.calculator._tokenize_text(text)
        
        # 应该正确处理数学符号
        assert "f" in tokens
        assert "x" in tokens
        assert "2x" in tokens
    
    def test_word_overlap_calculation(self):
        """测试词汇重叠计算"""
        text1 = "linear algebra mathematics"
        text2 = "algebra and linear equations"
        
        overlap = self.calculator._calculate_word_overlap(text1, text2)
        
        assert 0.0 <= overlap <= 1.0
        assert overlap > 0  # 应该有重叠
    
    def test_word_overlap_no_overlap(self):
        """测试无重叠的词汇"""
        text1 = "cooking recipes"
        text2 = "mathematics algebra"
        
        overlap = self.calculator._calculate_word_overlap(text1, text2)
        
        assert overlap == 0.0
    
    def test_word_overlap_empty_text(self):
        """测试空文本的词汇重叠"""
        text1 = ""
        text2 = "mathematics algebra"
        
        overlap = self.calculator._calculate_word_overlap(text1, text2)
        
        assert overlap == 0.0
    
    def test_source_boost_recognition(self):
        """测试来源权重识别"""
        # 测试已知学术来源
        arxiv_boost = self.calculator._get_source_boost("https://arxiv.org/abs/1234.5678")
        assert arxiv_boost > 1.0
        
        mit_boost = self.calculator._get_source_boost("https://mit.edu/course/math")
        assert mit_boost > 1.0
        
        # 测试未知来源
        unknown_boost = self.calculator._get_source_boost("https://unknown-site.com/article")
        assert unknown_boost == 1.0
    
    def test_math_terms_boost_recognition(self):
        """测试数学术语权重识别"""
        # 包含多个数学术语的文本
        math_text = "This algebra theorem involves calculus and geometry"
        boost = self.calculator._get_math_terms_boost(math_text)
        assert boost > 1.0
        
        # 不包含数学术语的文本
        regular_text = "This is a regular article about cooking"
        boost = self.calculator._get_math_terms_boost(regular_text)
        assert boost == 1.0
    
    def test_custom_tfidf_similarity(self):
        """测试自定义TF-IDF相似度计算"""
        text1 = "linear algebra mathematics"
        text2 = "algebra and linear equations in mathematics"
        
        similarity = self.calculator._custom_tfidf_similarity(text1, text2)
        
        assert 0.0 <= similarity <= 1.0
        assert similarity > 0  # 应该有相似度
    
    def test_cosine_similarity(self):
        """测试余弦相似度计算"""
        vec1 = {'word1': 0.5, 'word2': 0.3, 'word3': 0.0}
        vec2 = {'word1': 0.4, 'word2': 0.0, 'word3': 0.6}
        words = {'word1', 'word2', 'word3'}
        
        similarity = self.calculator._cosine_similarity(vec1, vec2, words)
        
        assert 0.0 <= similarity <= 1.0
    
    def test_relevance_score_bounds(self):
        """测试相关度评分边界"""
        query = "test query"
        result = self.sample_results[0]
        
        score = self.calculator.calculate_relevance(query, result)
        
        # 确保评分在有效范围内
        assert 0.0 <= score <= 1.0
    
    def test_boost_application_bounds(self):
        """测试权重提升的边界"""
        # 创建一个高评分的结果
        high_score_result = SearchResult(
            title="High Score Result",
            url="https://arxiv.org/test",
            snippet="algebra calculus geometry theorem",
            source="arXiv",
            relevance_score=0.9,
            timestamp=datetime.now(),
            math_content_detected=True
        )
        
        boosted_results = self.calculator.apply_math_domain_boost([high_score_result])
        
        # 即使应用了权重提升，评分也不应超过1.0
        assert boosted_results[0].relevance_score <= 1.0


if __name__ == "__main__":
    pytest.main([__file__])