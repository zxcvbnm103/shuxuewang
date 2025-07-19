"""
文本处理器测试
Text Processor Tests
"""

import pytest
from math_search.text_processing.text_processor import TextProcessor
from math_search.models.math_term import MathTerm


class TestTextProcessor:
    """文本处理器测试类"""
    
    def setup_method(self):
        """测试前的设置"""
        self.processor = TextProcessor()
    
    def test_extract_selected_text_basic(self):
        """测试基本文本提取功能"""
        content = "这是一个包含数学术语的文本，比如导数和积分。"
        selection_range = (6, 10)  # "数学术语"
        
        result = self.processor.extract_selected_text(content, selection_range)
        assert result == "数学术语"
    
    def test_extract_selected_text_with_whitespace(self):
        """测试包含空白字符的文本提取"""
        content = "  This is a test with spaces  "
        selection_range = (2, 28)
        
        result = self.processor.extract_selected_text(content, selection_range)
        assert result == "This is a test with spaces"
    
    def test_extract_selected_text_empty_selection(self):
        """测试空选择的情况"""
        content = "Some text here"
        selection_range = (5, 5)  # 空选择
        
        result = self.processor.extract_selected_text(content, selection_range)
        assert result == ""
    
    def test_extract_selected_text_invalid_range(self):
        """测试无效范围的错误处理"""
        content = "Short text"
        
        # 测试负数起始位置
        with pytest.raises(ValueError, match="无效的选择范围"):
            self.processor.extract_selected_text(content, (-1, 5))
        
        # 测试超出范围的结束位置
        with pytest.raises(ValueError, match="无效的选择范围"):
            self.processor.extract_selected_text(content, (0, 20))
        
        # 测试起始位置大于结束位置
        with pytest.raises(ValueError, match="无效的选择范围"):
            self.processor.extract_selected_text(content, (8, 3))
    
    def test_identify_math_terms_english(self):
        """测试英文数学术语识别"""
        text = "The derivative of a polynomial function is another polynomial."
        
        terms = self.processor.identify_math_terms(text)
        
        # 检查是否识别出关键术语
        term_names = [term.term for term in terms]
        assert "derivative" in term_names
        assert "polynomial" in term_names
        assert "function" in term_names
        
        # 检查术语分类
        derivative_term = next(term for term in terms if term.term == "derivative")
        assert derivative_term.category == "calculus"
        
        polynomial_term = next(term for term in terms if term.term == "polynomial")
        assert polynomial_term.category == "algebra"
    
    def test_identify_math_terms_chinese(self):
        """测试中文数学术语识别"""
        text = "这个函数的导数可以通过求极限来计算。"
        
        terms = self.processor.identify_math_terms(text)
        
        # 检查是否识别出关键术语
        term_names = [term.term for term in terms]
        assert "函数" in term_names
        assert "导数" in term_names
        assert "极限" in term_names
        
        # 检查术语分类
        derivative_term = next(term for term in terms if term.term == "导数")
        assert derivative_term.category == "calculus"
    
    def test_identify_math_terms_symbols(self):
        """测试数学符号识别"""
        text = "设 α ∈ ℝ，且 ∫f(x)dx = ∞"
        
        terms = self.processor.identify_math_terms(text)
        
        # 检查是否识别出数学符号
        term_names = [term.term for term in terms]
        assert "α" in term_names
        assert "∈" in term_names
        assert "∫" in term_names
        assert "∞" in term_names
    
    def test_identify_math_terms_confidence_scores(self):
        """测试置信度评分"""
        text = "The integral of a function represents the area under the curve."
        
        terms = self.processor.identify_math_terms(text)
        
        # 所有术语的置信度应该在0-1之间
        for term in terms:
            assert 0 <= term.confidence <= 1
        
        # 已知数学术语应该有较高的置信度
        integral_term = next(term for term in terms if term.term == "integral")
        assert integral_term.confidence >= 0.8
    
    def test_identify_math_terms_deduplication(self):
        """测试术语去重功能"""
        text = "A polynomial function is a function where polynomial coefficients are used."
        
        terms = self.processor.identify_math_terms(text)
        
        # 检查是否正确去重
        term_names = [term.term for term in terms]
        assert term_names.count("polynomial") == 1
        assert term_names.count("function") == 1
    
    def test_parse_latex_formulas_inline(self):
        """测试行内LaTeX公式解析"""
        text = "The formula $x^2 + y^2 = r^2$ represents a circle."
        
        formulas = self.processor.parse_latex_formulas(text)
        
        assert len(formulas) == 1
        assert "x^2 + y^2 = r^2" in formulas
    
    def test_parse_latex_formulas_block(self):
        """测试块级LaTeX公式解析"""
        text = "The quadratic formula is: $$x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$$"
        
        formulas = self.processor.parse_latex_formulas(text)
        
        assert len(formulas) == 1
        assert "x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}" in formulas
    
    def test_parse_latex_formulas_environment(self):
        """测试LaTeX环境解析"""
        text = """
        \\begin{equation}
        E = mc^2
        \\end{equation}
        """
        
        formulas = self.processor.parse_latex_formulas(text)
        
        assert len(formulas) == 1
        assert "\\begin{equation}" in formulas[0]
        assert "E = mc^2" in formulas[0]
    
    def test_parse_latex_formulas_multiple(self):
        """测试多个LaTeX公式解析"""
        text = "We have $f(x) = x^2$ and also $$\\int_0^1 f(x) dx = \\frac{1}{3}$$"
        
        formulas = self.processor.parse_latex_formulas(text)
        
        assert len(formulas) == 2
        assert "f(x) = x^2" in formulas
        assert "\\int_0^1 f(x) dx = \\frac{1}{3}" in formulas
    
    def test_parse_latex_formulas_empty(self):
        """测试无LaTeX公式的文本"""
        text = "This is just plain text without any formulas."
        
        formulas = self.processor.parse_latex_formulas(text)
        
        assert len(formulas) == 0
    
    def test_generate_search_keywords_math_terms(self):
        """测试基于数学术语的关键词生成"""
        text = "The derivative of a polynomial function can be calculated using calculus."
        
        keywords = self.processor.generate_search_keywords(text)
        
        # 应该包含数学术语
        assert "derivative" in keywords
        assert "polynomial" in keywords
        assert "function" in keywords
        assert "calculus" in keywords
    
    def test_generate_search_keywords_with_formulas(self):
        """测试包含公式的关键词生成"""
        text = "The area of a circle is $A = \\pi r^2$ where r is the radius."
        
        keywords = self.processor.generate_search_keywords(text)
        
        # 应该包含LaTeX公式
        assert "A = \\pi r^2" in keywords
        # 应该包含数学术语
        assert "circle" in keywords
    
    def test_generate_search_keywords_chinese(self):
        """测试中文文本的关键词生成"""
        text = "这个函数的导数可以用来计算切线的斜率。"
        
        keywords = self.processor.generate_search_keywords(text)
        
        # 应该包含中文数学术语
        assert "函数" in keywords
        assert "导数" in keywords
    
    def test_generate_search_keywords_limit(self):
        """测试关键词数量限制"""
        text = """
        This is a very long text with many mathematical terms including
        derivative, integral, function, polynomial, matrix, vector, calculus,
        algebra, geometry, statistics, probability, distribution, and more terms.
        """
        
        keywords = self.processor.generate_search_keywords(text)
        
        # 关键词数量应该被限制
        assert len(keywords) <= 10
    
    def test_generate_search_keywords_prioritize_math(self):
        """测试数学关键词优先级"""
        text = """
        The mathematical function and its derivative are important concepts
        in calculus, along with other regular words like computer, internet,
        website, programming, software, hardware, network, database.
        """
        
        keywords = self.processor.generate_search_keywords(text)
        
        # 数学术语应该优先出现
        math_keywords = ["function", "derivative", "calculus"]
        for math_kw in math_keywords:
            assert math_kw in keywords
    
    def test_latex_representation_mapping(self):
        """测试LaTeX表示映射"""
        # 测试希腊字母
        terms = self.processor.identify_math_terms("alpha beta gamma")
        alpha_term = next(term for term in terms if term.term == "alpha")
        assert alpha_term.latex_representation == r'\alpha'
        
        # 测试中文术语
        terms = self.processor.identify_math_terms("积分和导数")
        integral_term = next(term for term in terms if term.term == "积分")
        assert integral_term.latex_representation == r'\int'
    
    def test_math_context_detection(self):
        """测试数学上下文检测"""
        # 包含数学符号的上下文应该提高置信度
        text_with_context = "The function f(x) = x² has derivative f'(x) = 2x"
        text_without_context = "The function is working properly in the system"
        
        terms_with_context = self.processor.identify_math_terms(text_with_context)
        terms_without_context = self.processor.identify_math_terms(text_without_context)
        
        # 有数学上下文的术语应该有更高的置信度
        func_with_context = next(term for term in terms_with_context if term.term == "function")
        func_without_context = next(term for term in terms_without_context if term.term == "function")
        
        assert func_with_context.confidence >= func_without_context.confidence
    
    def test_edge_cases(self):
        """测试边界情况"""
        # 空文本
        assert self.processor.identify_math_terms("") == []
        assert self.processor.parse_latex_formulas("") == []
        assert self.processor.generate_search_keywords("") == []
        
        # 只有空格的文本
        assert self.processor.identify_math_terms("   ") == []
        
        # 只有标点符号的文本
        terms = self.processor.identify_math_terms("!@#$%^&*()")
        assert len(terms) == 0
    
    def test_mixed_language_text(self):
        """测试中英文混合文本"""
        text = "The 函数 has a 导数 that can be calculated using derivative methods."
        
        terms = self.processor.identify_math_terms(text)
        term_names = [term.term for term in terms]
        
        # 应该同时识别中英文术语
        assert "函数" in term_names
        assert "导数" in term_names
        assert "derivative" in term_names
    
    def test_special_characters_handling(self):
        """测试特殊字符处理"""
        text = "f(x) = x² + 2x + 1, where x ∈ ℝ"
        
        terms = self.processor.identify_math_terms(text)
        
        # 应该正确处理特殊数学字符
        term_names = [term.term for term in terms]
        assert "∈" in term_names
    
    def test_performance_with_long_text(self):
        """测试长文本的处理性能"""
        # 创建一个较长的文本
        long_text = """
        Calculus is a branch of mathematics that deals with derivatives and integrals.
        A function can have multiple derivatives, and the integral of a function
        represents the area under its curve. Polynomial functions are particularly
        easy to differentiate and integrate. Linear algebra deals with vectors,
        matrices, and linear transformations. Geometry studies shapes, angles,
        and spatial relationships. Statistics involves probability distributions,
        mean, variance, and hypothesis testing.
        """ * 10  # 重复10次
        
        # 这应该能够在合理时间内完成
        terms = self.processor.identify_math_terms(long_text)
        keywords = self.processor.generate_search_keywords(long_text)
        
        # 验证结果的合理性
        assert len(terms) > 0
        assert len(keywords) > 0
        assert len(keywords) <= 10  # 关键词数量限制仍然有效


if __name__ == "__main__":
    pytest.main([__file__])