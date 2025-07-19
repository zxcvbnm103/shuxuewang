"""
LaTeX和SymPy集成功能演示
Demo for LaTeX and SymPy Integration
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from math_search.text_processing.text_processor import TextProcessor
import json


def print_section(title):
    """打印章节标题"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")


def print_subsection(title):
    """打印子章节标题"""
    print(f"\n{'-'*40}")
    print(f" {title}")
    print(f"{'-'*40}")


def demo_latex_parsing():
    """演示LaTeX解析功能"""
    print_section("LaTeX公式解析演示")
    
    processor = TextProcessor()
    
    # 测试文本
    test_text = """
    这是一个包含多种数学公式的文本：
    
    1. 行内公式：爱因斯坦质能方程 $E = mc^2$
    2. 块级公式：高斯积分
    $$\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}$$
    
    3. 分数：$\\frac{a+b}{c+d}$
    4. 根式：$\\sqrt{x^2 + y^2}$
    5. 三角函数：$\\sin(\\theta) + \\cos(\\theta) = \\sqrt{2}\\sin(\\theta + \\frac{\\pi}{4})$
    6. 希腊字母：$\\alpha, \\beta, \\gamma, \\delta, \\pi, \\omega$
    
    7. LaTeX环境：
    \\begin{equation}
    \\sum_{n=1}^{\\infty} \\frac{1}{n^2} = \\frac{\\pi^2}{6}
    \\end{equation}
    """
    
    print("原始文本：")
    print(test_text)
    
    print_subsection("提取的LaTeX公式")
    formulas = processor.parse_latex_formulas(test_text)
    for i, formula in enumerate(formulas, 1):
        print(f"{i}. {formula}")
    
    print_subsection("数学概念提取")
    concepts = processor.extract_mathematical_concepts(test_text)
    for concept_type, items in concepts.items():
        if items:
            print(f"{concept_type.upper()}: {items}")


def demo_sympy_integration():
    """演示SymPy集成功能"""
    print_section("SymPy集成演示")
    
    processor = TextProcessor()
    
    # 测试各种LaTeX表达式
    test_expressions = [
        r"x^2 + 2*x + 1",
        r"$\frac{x+1}{x-1}$",
        r"$$\sqrt{x^2 + y^2}$$",
        r"\sin(x) + \cos(x)",
        r"\int x dx",
        r"\frac{d}{dx}(x^2)",
        r"e^{i\pi} + 1",
        r"\sum_{n=1}^{\infty} \frac{1}{n^2}",
    ]
    
    for expr in test_expressions:
        print_subsection(f"分析表达式: {expr}")
        
        # 解析为SymPy
        sympy_expr = processor.parse_latex_to_sympy(expr)
        if sympy_expr:
            print(f"SymPy形式: {sympy_expr}")
        else:
            print("无法解析为SymPy表达式")
        
        # 完整分析
        analysis = processor.analyze_mathematical_expression(expr)
        if 'error' not in analysis:
            print("分析结果：")
            for key, value in analysis.items():
                if key not in ['original']:  # 跳过原始表达式，已经显示过了
                    print(f"  {key}: {value}")
        else:
            print(f"分析错误: {analysis['error']}")


def demo_latex_validation():
    """演示LaTeX语法验证功能"""
    print_section("LaTeX语法验证演示")
    
    processor = TextProcessor()
    
    # 测试有效和无效的LaTeX
    test_cases = [
        (r"\frac{1}{2}", "有效的分数"),
        (r"\sqrt{x}", "有效的平方根"),
        (r"\frac{1{2}", "无效的分数（缺少括号）"),
        (r"\sqrt[3{x}", "无效的根式（括号不匹配）"),
        (r"\sin(x) + \cos(x)", "有效的三角函数"),
        (r"\unknown_command{x}", "未知命令"),
        ("", "空字符串"),
        ("x + 1", "简单表达式"),
    ]
    
    for latex_expr, description in test_cases:
        print_subsection(f"{description}: {latex_expr}")
        
        validation = processor.validate_latex_syntax(latex_expr)
        
        print(f"是否有效: {validation['is_valid']}")
        
        if validation['errors']:
            print("错误:")
            for error in validation['errors']:
                print(f"  - {error}")
        
        if validation['warnings']:
            print("警告:")
            for warning in validation['warnings']:
                print(f"  - {warning}")
        
        if validation['parsed_expression']:
            print(f"解析结果: {validation['parsed_expression']}")


def demo_mathematical_term_enhancement():
    """演示数学术语识别的增强功能"""
    print_section("增强的数学术语识别演示")
    
    processor = TextProcessor()
    
    test_text = """
    在微积分中，derivative（导数）是函数变化率的度量。
    对于函数f(x) = x^2，其derivative为f'(x) = 2x。
    相反地，integral（积分）是导数的逆运算。
    ∫2x dx = x^2 + C，其中C是积分常数。
    
    在代数中，我们经常处理polynomial（多项式），如quadratic equation（二次方程）。
    一个典型的quadratic equation是ax^2 + bx + c = 0。
    
    几何学中包含triangle（三角形）、circle（圆）等图形。
    三角函数sin、cos、tan在解决角度问题时很有用。
    """
    
    print("原始文本：")
    print(test_text)
    
    print_subsection("识别的数学术语")
    math_terms = processor.identify_math_terms(test_text)
    
    for term in math_terms:
        print(f"术语: {term.term}")
        print(f"  分类: {term.category}")
        print(f"  LaTeX表示: {term.latex_representation}")
        print(f"  置信度: {term.confidence:.2f}")
        print()


def demo_preprocessing():
    """演示LaTeX预处理功能"""
    print_section("LaTeX预处理演示")
    
    processor = TextProcessor()
    
    # 测试各种LaTeX命令的预处理
    test_cases = [
        r"\frac{1}{2}",
        r"\sqrt{x}",
        r"\sqrt[3]{x}",
        r"x^2",
        r"\sin(x)",
        r"\cos(x)",
        r"\pi",
        r"\alpha + \beta",
        r"\int f(x) dx",
        r"\sum_{i=1}^n i",
        r"\lim_{x \to 0} \frac{\sin x}{x}",
    ]
    
    for latex_expr in test_cases:
        processed = processor._preprocess_latex_for_sympy(latex_expr)
        print(f"原始: {latex_expr}")
        print(f"预处理: {processed}")
        print()


def main():
    """主函数"""
    print("LaTeX和SymPy集成功能演示")
    print("=" * 60)
    
    try:
        # 运行各个演示
        demo_latex_parsing()
        demo_sympy_integration()
        demo_latex_validation()
        demo_mathematical_term_enhancement()
        demo_preprocessing()
        
        print_section("演示完成")
        print("所有功能演示已完成！")
        
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()