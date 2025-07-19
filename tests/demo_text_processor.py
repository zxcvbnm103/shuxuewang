"""
文本处理器演示脚本
Text Processor Demo Script
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from math_search.text_processing.text_processor import TextProcessor


def demo_text_extraction():
    """演示文本提取功能"""
    print("=== 文本提取演示 ===")
    processor = TextProcessor()
    
    content = "这是一个包含数学术语的文本，比如导数、积分和函数等概念。"
    
    # 提取"数学术语"
    selection_range = (6, 10)
    selected = processor.extract_selected_text(content, selection_range)
    print(f"原文本: {content}")
    print(f"选择范围: {selection_range}")
    print(f"提取结果: '{selected}'")
    print()


def demo_math_term_identification():
    """演示数学术语识别功能"""
    print("=== 数学术语识别演示 ===")
    processor = TextProcessor()
    
    # 英文数学文本
    english_text = "The derivative of a polynomial function can be calculated using the chain rule in calculus."
    print(f"英文文本: {english_text}")
    
    terms = processor.identify_math_terms(english_text)
    print("识别出的数学术语:")
    for term in terms:
        print(f"  - 术语: {term.term}")
        print(f"    分类: {term.category}")
        print(f"    置信度: {term.confidence:.2f}")
        print(f"    LaTeX: {term.latex_representation}")
        print()
    
    # 中文数学文本
    chinese_text = "这个函数的导数可以通过求极限来计算，积分则表示曲线下的面积。"
    print(f"中文文本: {chinese_text}")
    
    terms = processor.identify_math_terms(chinese_text)
    print("识别出的数学术语:")
    for term in terms:
        print(f"  - 术语: {term.term}")
        print(f"    分类: {term.category}")
        print(f"    置信度: {term.confidence:.2f}")
        print(f"    LaTeX: {term.latex_representation}")
        print()


def demo_latex_parsing():
    """演示LaTeX公式解析功能"""
    print("=== LaTeX公式解析演示 ===")
    processor = TextProcessor()
    
    # 包含多种LaTeX公式的文本
    text_with_latex = """
    The quadratic formula is $x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$.
    
    For integration, we have:
    $$\\int_0^1 x^2 dx = \\frac{1}{3}$$
    
    And the general form:
    \\begin{equation}
    E = mc^2
    \\end{equation}
    """
    
    print("包含LaTeX公式的文本:")
    print(text_with_latex)
    
    formulas = processor.parse_latex_formulas(text_with_latex)
    print("解析出的LaTeX公式:")
    for i, formula in enumerate(formulas, 1):
        print(f"  {i}. {formula}")
    print()


def demo_keyword_generation():
    """演示搜索关键词生成功能"""
    print("=== 搜索关键词生成演示 ===")
    processor = TextProcessor()
    
    # 复杂的数学文本
    complex_text = """
    In linear algebra, we study vector spaces and linear transformations.
    The eigenvalues and eigenvectors of a matrix are fundamental concepts.
    For a given matrix A, if Av = λv for some non-zero vector v, then λ is
    an eigenvalue and v is the corresponding eigenvector. The characteristic
    polynomial det(A - λI) = 0 gives us the eigenvalues.
    """
    
    print("复杂数学文本:")
    print(complex_text)
    
    keywords = processor.generate_search_keywords(complex_text)
    print("生成的搜索关键词:")
    for i, keyword in enumerate(keywords, 1):
        print(f"  {i}. {keyword}")
    print()


def demo_mixed_content():
    """演示混合内容处理"""
    print("=== 混合内容处理演示 ===")
    processor = TextProcessor()
    
    # 包含中英文、LaTeX公式和数学符号的文本
    mixed_text = """
    设函数 f(x) = x² + 2x + 1，其derivative为 f'(x) = 2x + 2。
    当 x ∈ ℝ 时，我们可以计算积分 $\\int_0^1 f(x) dx = \\frac{4}{3}$。
    这个polynomial function在 calculus 中很常见。
    """
    
    print("混合内容文本:")
    print(mixed_text)
    
    # 识别数学术语
    terms = processor.identify_math_terms(mixed_text)
    print("\n识别出的数学术语:")
    for term in terms[:5]:  # 只显示前5个
        print(f"  - {term.term} ({term.category}, 置信度: {term.confidence:.2f})")
    
    # 解析LaTeX公式
    formulas = processor.parse_latex_formulas(mixed_text)
    print(f"\nLaTeX公式: {formulas}")
    
    # 生成关键词
    keywords = processor.generate_search_keywords(mixed_text)
    print(f"\n搜索关键词: {keywords}")
    print()


def demo_edge_cases():
    """演示边界情况处理"""
    print("=== 边界情况处理演示 ===")
    processor = TextProcessor()
    
    test_cases = [
        ("", "空文本"),
        ("   ", "只有空格"),
        ("!@#$%^&*()", "只有标点符号"),
        ("α β γ δ ε", "只有希腊字母"),
        ("123 + 456 = 579", "只有数字和运算符"),
    ]
    
    for text, description in test_cases:
        print(f"{description}: '{text}'")
        terms = processor.identify_math_terms(text)
        keywords = processor.generate_search_keywords(text)
        print(f"  术语数量: {len(terms)}")
        print(f"  关键词数量: {len(keywords)}")
        if terms:
            print(f"  术语: {[term.term for term in terms]}")
        if keywords:
            print(f"  关键词: {keywords}")
        print()


def main():
    """主函数"""
    print("文本处理器功能演示")
    print("=" * 50)
    
    try:
        demo_text_extraction()
        demo_math_term_identification()
        demo_latex_parsing()
        demo_keyword_generation()
        demo_mixed_content()
        demo_edge_cases()
        
        print("演示完成！")
        
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()