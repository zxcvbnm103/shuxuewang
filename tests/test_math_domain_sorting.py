"""
数学领域特定排序优化测试
Math Domain-Specific Sorting Optimization Tests
"""

import pytest
from datetime import datetime
from math_search.relevance_calculation import RelevanceCalculator
from math_search.models import SearchResult


class TestMathDomainSorting:
    """数学领域排序优化测试类"""
    
    def setup_method(self):
        """测试前设置"""
        self.calculator = RelevanceCalculator()
        
        # 创建不同类型的测试搜索结果
        self.test_results = [
            # 高级数学研究论文 (arXiv)
            SearchResult(
                title="Manifold Learning and Topology in High-Dimensional Analysis",
                url="https://arxiv.org/abs/2023.12345",
                snippet="This paper presents novel research on manifold topology and homomorphism in functional analysis",
                source="arXiv",
                relevance_score=0.6,
                timestamp=datetime.now(),
                math_content_detected=True
            ),
            
            # 基础教程 (Khan Academy)
            SearchResult(
                title="Introduction to Basic Algebra",
                url="https://khanacademy.org/math/algebra-basics",
                snippet="Learn elementary algebra concepts with simple examples and tutorials",
                source="Khan Academy",
                relevance_score=0.7,
                timestamp=datetime.now(),
                math_content_detected=True
            ),
            
            # 大学课程 (MIT)
            SearchResult(
                title="Linear Algebra Course - MIT OpenCourseWare",
                url="https://mit.edu/courses/mathematics/linear-algebra",
                snippet="Graduate level course on linear algebra, eigenvalues, and matrix theory",
                source="MIT",
                relevance_score=0.65,
                timestamp=datetime.now(),
                math_content_detected=True
            ),
            
            # 学术期刊论文
            SearchResult(
                title="Journal of Mathematical Analysis: Differential Equations",
                url="https://elsevier.com/journal/mathematical-analysis",
                snippet="Research paper on differential equations and their applications in analysis",
                source="Elsevier",
                relevance_score=0.55,
                timestamp=datetime.now(),
                math_content_detected=True
            ),
            
            # 非数学内容
            SearchResult(
                title="Programming Tutorial",
                url="https://example.com/programming",
                snippet="Learn programming basics with simple coding examples",
                source="Example",
                relevance_score=0.8,
                timestamp=datetime.now(),
                math_content_detected=False
            )
        ]
    
    def test_math_domain_depth_boost_advanced_concepts(self):
        """测试高级数学概念的深度权重提升"""
        # 包含高级概念的文本
        advanced_text = "manifold topology homomorphism functional analysis"
        boost = self.calculator._get_math_domain_depth_boost(advanced_text)
        
        assert boost > 1.0
        assert boost <= 1.8
        
        # 基础概念的文本
        basic_text = "basic algebra introduction"
        basic_boost = self.calculator._get_math_domain_depth_boost(basic_text)
        
        assert boost > basic_boost
    
    def test_math_domain_depth_boost_research_keywords(self):
        """测试研究级关键词的深度权重提升"""
        research_text = "theorem proof lemma research paper journal publication"
        boost = self.calculator._get_math_domain_depth_boost(research_text)
        
        assert boost > 1.0
        
        # 非研究级文本
        tutorial_text = "tutorial introduction basic examples"
        tutorial_boost = self.calculator._get_math_domain_depth_boost(tutorial_text)
        
        assert boost > tutorial_boost
    
    def test_math_domain_depth_boost_math_symbols(self):
        """测试数学符号检测的权重提升"""
        symbol_text = "∫ f(x)dx = ∑ a_n where ∂f/∂x ≤ ∞"
        boost = self.calculator._get_math_domain_depth_boost(symbol_text)
        
        assert boost > 1.0
        
        # 无符号文本
        no_symbol_text = "regular text without math symbols"
        no_symbol_boost = self.calculator._get_math_domain_depth_boost(no_symbol_text)
        
        assert boost > no_symbol_boost
    
    def test_math_domain_depth_boost_latex_detection(self):
        """测试LaTeX检测的权重提升"""
        latex_text = "The formula is $x^2 + y^2 = z^2$ and \\int_0^1 f(x) dx"
        boost = self.calculator._get_math_domain_depth_boost(latex_text)
        
        assert boost > 1.0
        
        # 无LaTeX文本
        no_latex_text = "regular text without latex"
        no_latex_boost = self.calculator._get_math_domain_depth_boost(no_latex_text)
        
        assert boost > no_latex_boost
    
    def test_academic_level_boost_high_level(self):
        """测试高级学术指标的权重提升"""
        high_level_result = SearchResult(
            title="PhD Research on Advanced Mathematics",
            url="https://university.edu/research",
            snippet="Professor's research paper published in journal proceedings",
            source="University",
            relevance_score=0.5,
            timestamp=datetime.now(),
            math_content_detected=True
        )
        
        boost = self.calculator._get_academic_level_boost(high_level_result)
        assert boost > 1.0
    
    def test_academic_level_boost_basic_level(self):
        """测试基础学术指标的权重影响"""
        basic_result = SearchResult(
            title="Elementary Introduction to Basic Math",
            url="https://example.com/basic",
            snippet="Basic tutorial for elementary students",
            source="Example",
            relevance_score=0.5,
            timestamp=datetime.now(),
            math_content_detected=True
        )
        
        boost = self.calculator._get_academic_level_boost(basic_result)
        assert boost < 1.0  # 基础内容应该有较低的权重
    
    def test_academic_level_boost_edu_domain(self):
        """测试教育域名的权重提升"""
        edu_result = SearchResult(
            title="Mathematics Course",
            url="https://university.edu/math/course",
            snippet="University mathematics course content",
            source="University",
            relevance_score=0.5,
            timestamp=datetime.now(),
            math_content_detected=True
        )
        
        boost = self.calculator._get_academic_level_boost(edu_result)
        assert boost > 1.0
    
    def test_enhanced_academic_sources_weights(self):
        """测试增强的学术来源权重"""
        # 测试顶级来源
        arxiv_boost = self.calculator._get_source_boost("https://arxiv.org/abs/1234.5678")
        assert arxiv_boost >= 1.9
        
        mit_boost = self.calculator._get_source_boost("https://mit.edu/course")
        assert mit_boost >= 1.8
        
        # 测试中级来源
        wiki_boost = self.calculator._get_source_boost("https://wikipedia.org/article")
        assert wiki_boost >= 1.3
        
        # 测试未知来源
        unknown_boost = self.calculator._get_source_boost("https://unknown-site.com")
        assert unknown_boost == 1.0
        
        # 验证权重层次
        assert arxiv_boost > mit_boost > wiki_boost > unknown_boost
    
    def test_enhanced_math_terms_weights(self):
        """测试增强的数学术语权重"""
        # 测试高级概念
        advanced_text = "manifold homomorphism topology"
        advanced_boost = self.calculator._get_math_terms_boost(advanced_text)
        
        # 测试基础概念
        basic_text = "algebra calculus"
        basic_boost = self.calculator._get_math_terms_boost(basic_text)
        
        # 测试非数学文本
        non_math_text = "cooking recipe tutorial"
        non_math_boost = self.calculator._get_math_terms_boost(non_math_text)
        
        assert advanced_boost > basic_boost > non_math_boost
        assert non_math_boost == 1.0
    
    def test_multi_layer_sorting(self):
        """测试多层排序策略"""
        # 应用权重提升
        boosted_results = self.calculator.apply_math_domain_boost(self.test_results)
        
        # 执行排序
        sorted_results = self.calculator.rank_results(boosted_results)
        
        # 验证排序结果
        assert len(sorted_results) == len(self.test_results)
        
        # 检查是否按相关度降序排列
        for i in range(len(sorted_results) - 1):
            assert sorted_results[i].relevance_score >= sorted_results[i + 1].relevance_score
    
    def test_comprehensive_domain_boost_application(self):
        """测试综合领域权重提升应用"""
        original_results = self.test_results.copy()
        boosted_results = self.calculator.apply_math_domain_boost(original_results)
        
        # 验证所有结果都被处理
        assert len(boosted_results) == len(original_results)
        
        # 验证数学内容的结果得到了提升
        for i, (original, boosted) in enumerate(zip(original_results, boosted_results)):
            if original.math_content_detected:
                # 数学内容应该得到权重提升
                assert boosted.relevance_score >= original.relevance_score
            
            # 验证评分仍在有效范围内
            assert 0.0 <= boosted.relevance_score <= 1.0
    
    def test_advanced_sorting_metrics(self):
        """测试高级排序指标获取"""
        metrics = self.calculator.get_advanced_sorting_metrics(self.test_results)
        
        assert len(metrics) == len(self.test_results)
        
        for metric in metrics:
            # 验证所有必要的指标都存在
            required_keys = [
                'base_relevance', 'source_boost', 'math_terms_boost',
                'domain_depth_boost', 'academic_level_boost', 
                'math_content_detected', 'url', 'title',
                'total_boost', 'final_score'
            ]
            
            for key in required_keys:
                assert key in metric
            
            # 验证数值范围
            assert 0.0 <= metric['base_relevance'] <= 1.0
            assert metric['source_boost'] >= 1.0
            assert metric['math_terms_boost'] >= 1.0
            assert metric['domain_depth_boost'] >= 1.0
            assert metric['academic_level_boost'] >= 0.8
            assert 0.0 <= metric['final_score'] <= 1.0
    
    def test_sorting_preserves_original_data(self):
        """测试排序过程保持原始数据完整性"""
        original_results = self.test_results.copy()
        boosted_results = self.calculator.apply_math_domain_boost(original_results)
        sorted_results = self.calculator.rank_results(boosted_results)
        
        # 验证结果数量不变
        assert len(sorted_results) == len(original_results)
        
        # 创建URL到原始结果的映射
        original_by_url = {result.url: result for result in original_results}
        
        # 验证所有原始字段都被保留（除了relevance_score）
        for sorted_result in sorted_results:
            original = original_by_url[sorted_result.url]
            assert sorted_result.title == original.title
            assert sorted_result.url == original.url
            assert sorted_result.snippet == original.snippet
            assert sorted_result.source == original.source
            assert sorted_result.timestamp == original.timestamp
            assert sorted_result.math_content_detected == original.math_content_detected
    
    def test_boost_bounds_enforcement(self):
        """测试权重提升边界强制执行"""
        # 创建一个高评分结果，测试是否会超过1.0
        high_score_result = SearchResult(
            title="Advanced Manifold Topology Research Paper",
            url="https://arxiv.org/abs/advanced-math",
            snippet="PhD research on homomorphism, eigenvalues, fourier analysis, theorem proof",
            source="arXiv",
            relevance_score=0.95,
            timestamp=datetime.now(),
            math_content_detected=True
        )
        
        boosted_results = self.calculator.apply_math_domain_boost([high_score_result])
        
        # 即使应用了多重权重提升，评分也不应超过1.0
        assert boosted_results[0].relevance_score <= 1.0
    
    def test_empty_results_handling(self):
        """测试空结果列表的处理"""
        empty_results = []
        
        boosted_results = self.calculator.apply_math_domain_boost(empty_results)
        sorted_results = self.calculator.rank_results(boosted_results)
        metrics = self.calculator.get_advanced_sorting_metrics(empty_results)
        
        assert boosted_results == []
        assert sorted_results == []
        assert metrics == []
    
    def test_single_result_handling(self):
        """测试单个结果的处理"""
        single_result = [self.test_results[0]]
        
        boosted_results = self.calculator.apply_math_domain_boost(single_result)
        sorted_results = self.calculator.rank_results(boosted_results)
        metrics = self.calculator.get_advanced_sorting_metrics(single_result)
        
        assert len(boosted_results) == 1
        assert len(sorted_results) == 1
        assert len(metrics) == 1
    
    def test_math_term_density_calculation(self):
        """测试数学术语密度计算"""
        # 高密度数学术语文本
        high_density_text = "algebra calculus geometry topology analysis theorem proof"
        high_density_boost = self.calculator._calculate_math_term_density(high_density_text)
        
        # 低密度数学术语文本
        low_density_text = "this is a long text with only one algebra term in it"
        low_density_boost = self.calculator._calculate_math_term_density(low_density_text)
        
        # 无数学术语文本
        no_math_text = "this is regular text without any mathematical content"
        no_math_boost = self.calculator._calculate_math_term_density(no_math_text)
        
        assert high_density_boost > low_density_boost > no_math_boost
        assert no_math_boost == 1.0
    
    def test_math_term_cooccurrence_calculation(self):
        """测试数学术语共现计算"""
        # 多个高级术语共现
        multi_advanced_text = "manifold topology homomorphism functional analysis"
        multi_boost = self.calculator._calculate_math_term_cooccurrence(multi_advanced_text)
        
        # 两个高级术语共现
        dual_advanced_text = "category theory measure theory"
        dual_boost = self.calculator._calculate_math_term_cooccurrence(dual_advanced_text)
        
        # 单个高级术语
        single_advanced_text = "abstract algebra concepts"
        single_boost = self.calculator._calculate_math_term_cooccurrence(single_advanced_text)
        
        # 无高级术语
        no_advanced_text = "basic algebra and simple calculus"
        no_boost = self.calculator._calculate_math_term_cooccurrence(no_advanced_text)
        
        assert multi_boost > dual_boost > single_boost > no_boost
        assert no_boost == 1.0
    
    def test_mathematical_complexity_score_calculation(self):
        """测试数学复杂度评分计算"""
        # 高复杂度文本
        high_complexity_text = "category theory homomorphism manifold topology proof theorem"
        high_score = self.calculator._calculate_mathematical_complexity_score(high_complexity_text)
        
        # 中等复杂度文本
        medium_complexity_text = "differential equations analysis theorem"
        medium_score = self.calculator._calculate_mathematical_complexity_score(medium_complexity_text)
        
        # 低复杂度文本
        low_complexity_text = "basic algebra and simple geometry"
        low_score = self.calculator._calculate_mathematical_complexity_score(low_complexity_text)
        
        # 无数学内容文本
        no_math_text = "regular text without mathematical content"
        no_math_score = self.calculator._calculate_mathematical_complexity_score(no_math_text)
        
        assert high_score > medium_score > low_score
        assert no_math_score == 1.0
        assert high_score <= 2.0  # 确保不超过最大值
    
    def test_enhanced_math_terms_boost_with_new_features(self):
        """测试增强的数学术语权重提升（包含新功能）"""
        # 包含高密度和共现术语的文本
        enhanced_text = "manifold topology homomorphism category theory functional analysis theorem proof"
        enhanced_boost = self.calculator._get_math_terms_boost(enhanced_text)
        
        # 基础数学术语文本
        basic_text = "algebra calculus"
        basic_boost = self.calculator._get_math_terms_boost(basic_text)
        
        # 验证增强版本有更高的权重
        assert enhanced_boost > basic_boost
        assert enhanced_boost <= 2.5  # 确保不超过最大值
    
    def test_comprehensive_boost_integration(self):
        """测试综合权重提升集成"""
        # 创建一个包含多种数学特征的结果
        comprehensive_result = SearchResult(
            title="Advanced Category Theory and Homomorphism in Manifold Topology",
            url="https://arxiv.org/abs/advanced-math-research",
            snippet="PhD research paper on category theory, homomorphism, manifold topology, functional analysis, theorem proof, and measure theory",
            source="arXiv",
            relevance_score=0.6,
            timestamp=datetime.now(),
            math_content_detected=True
        )
        
        # 应用综合权重提升
        boosted_results = self.calculator.apply_math_domain_boost([comprehensive_result])
        boosted_result = boosted_results[0]
        
        # 验证权重提升效果
        assert boosted_result.relevance_score > comprehensive_result.relevance_score
        assert boosted_result.relevance_score <= 1.0
        
        # 获取详细指标
        metrics = self.calculator.get_advanced_sorting_metrics([comprehensive_result])
        metric = metrics[0]
        
        # 验证所有新指标都存在
        assert 'complexity_boost' in metric
        assert metric['complexity_boost'] > 1.0
        assert metric['math_terms_boost'] > 1.0
        assert metric['domain_depth_boost'] > 1.0
    
    def test_enhanced_academic_sources_coverage(self):
        """测试增强的学术来源覆盖"""
        # 测试新增的数学术语权重
        new_terms = [
            'abstract algebra', 'real analysis', 'complex analysis',
            'functional analysis', 'algebraic geometry', 'differential geometry',
            'group theory', 'ring theory', 'field theory', 'category theory',
            'measure theory', 'operator theory', 'mathematical modeling',
            'mathematical physics', 'set theory', 'mathematical logic'
        ]
        
        for term in new_terms:
            assert term in self.calculator.math_terms_weights
            assert self.calculator.math_terms_weights[term] > 1.0
    
    def test_sorting_stability_with_enhancements(self):
        """测试增强功能的排序稳定性"""
        # 创建多个相似评分的结果，测试排序稳定性
        similar_results = []
        for i in range(5):
            result = SearchResult(
                title=f"Mathematical Research Paper {i}",
                url=f"https://example{i}.com/math",
                snippet="algebra calculus geometry analysis theorem",
                source="Example",
                relevance_score=0.5,
                timestamp=datetime.now(),
                math_content_detected=True
            )
            similar_results.append(result)
        
        # 多次排序，验证结果一致性
        boosted_results1 = self.calculator.apply_math_domain_boost(similar_results.copy())
        sorted_results1 = self.calculator.rank_results(boosted_results1)
        
        boosted_results2 = self.calculator.apply_math_domain_boost(similar_results.copy())
        sorted_results2 = self.calculator.rank_results(boosted_results2)
        
        # 验证排序结果一致
        for r1, r2 in zip(sorted_results1, sorted_results2):
            assert r1.url == r2.url
            assert abs(r1.relevance_score - r2.relevance_score) < 1e-10


if __name__ == "__main__":
    pytest.main([__file__])