"""
文本处理器实现
Text Processor Implementation
"""

import re
import sympy as sp
from sympy.parsing.latex import parse_latex
from sympy.parsing.sympy_parser import parse_expr
from typing import List, Tuple, Dict, Set, Optional, Union
from ..interfaces.text_processor import ITextProcessor
from ..models.math_term import MathTerm


class TextProcessor(ITextProcessor):
    """文本处理器实现类"""
    
    def __init__(self):
        """初始化文本处理器"""
        self._init_math_patterns()
        self._init_math_terms_dict()
    
    def _init_math_patterns(self):
        """初始化数学术语识别的正则表达式模式"""
        
        # LaTeX公式模式
        self.latex_patterns = [
            r'\$\$[^$]+\$\$',  # 块级公式 $$...$$
            r'\$[^$]+\$',      # 行内公式 $...$
            r'\\begin\{[^}]+\}.*?\\end\{[^}]+\}',  # LaTeX环境
        ]
        
        # 数学符号和运算符模式
        self.math_symbol_patterns = [
            r'[∀∃∈∉⊂⊃⊆⊇∪∩∅]',  # 集合论符号
            r'[∫∮∑∏∂∇∆]',        # 微积分符号
            r'[≤≥≠≈≡∞]',          # 比较和特殊符号
            r'[αβγδεζηθικλμνξοπρστυφχψω]',  # 希腊字母
            r'[ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ]',  # 大写希腊字母
            r'[±×÷√∛∜]',          # 基本运算符号
        ]
        
        # 数学术语模式（英文）
        self.english_math_terms = [
            # 代数
            r'\b(?:polynomial|equation|variable|coefficient|constant|expression|function|domain|range|inverse|composition)\b',
            r'\b(?:linear|quadratic|cubic|exponential|logarithmic|trigonometric)\b',
            r'\b(?:matrix|determinant|eigenvalue|eigenvector|vector|scalar)\b',
            r'\b(?:alpha|beta|gamma|delta|epsilon|theta|lambda|mu|pi|sigma|phi|omega)\b',  # 希腊字母英文名
            
            # 微积分
            r'\b(?:derivative|integral|limit|continuity|differentiable|antiderivative)\b',
            r'\b(?:partial|gradient|divergence|curl|laplacian)\b',
            
            # 几何
            r'\b(?:triangle|circle|ellipse|parabola|hyperbola|polygon|angle|perpendicular|parallel)\b',
            r'\b(?:theorem|proof|lemma|corollary|axiom|postulate)\b',
            
            # 统计
            r'\b(?:probability|distribution|mean|median|mode|variance|deviation|correlation)\b',
            r'\b(?:normal|binomial|poisson|chi-square|t-test|hypothesis)\b',
            
            # 其他
            r'\b(?:calculus|algebra|geometry|statistics|analysis)\b',
        ]
        
        # 数学术语模式（中文）
        self.chinese_math_terms = [
            # 代数
            r'(?:多项式|方程|变量|系数|常数|表达式|函数|定义域|值域|反函数|复合函数)',
            r'(?:线性|二次|三次|指数|对数|三角函数)',
            r'(?:矩阵|行列式|特征值|特征向量|向量|标量)',
            
            # 微积分
            r'(?:导数|积分|极限|连续性|可微|原函数)',
            r'(?:偏导数|梯度|散度|旋度|拉普拉斯)',
            
            # 几何
            r'(?:三角形|圆|椭圆|抛物线|双曲线|多边形|角|垂直|平行)',
            r'(?:定理|证明|引理|推论|公理|公设)',
            
            # 统计
            r'(?:概率|分布|均值|中位数|众数|方差|标准差|相关性)',
            r'(?:正态分布|二项分布|泊松分布|卡方|t检验|假设检验)',
        ]
        
        # 数学数字和表达式模式
        self.number_patterns = [
            r'\b\d+\.\d+\b',      # 小数
            r'\b\d+/\d+\b',       # 分数
            r'\b\d+\^\d+\b',      # 指数
            r'\b\d+!\b',          # 阶乘
            r'\b\d+%\b',          # 百分比
        ]
    
    def _init_math_terms_dict(self):
        """初始化数学术语分类字典"""
        self.math_categories = {
            # 代数相关
            'algebra': {
                'polynomial', 'equation', 'variable', 'coefficient', 'constant', 'expression',
                'function', 'domain', 'range', 'inverse', 'composition', 'linear', 'quadratic',
                'cubic', 'matrix', 'determinant', 'eigenvalue', 'eigenvector', 'vector', 'scalar',
                'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'theta', 'lambda', 'mu',
                'pi', 'sigma', 'phi', 'omega', 'algebra',
                '多项式', '方程', '变量', '系数', '常数', '表达式', '函数', '定义域', '值域',
                '反函数', '复合函数', '线性', '二次', '三次', '矩阵', '行列式', '特征值', '特征向量',
                '向量', '标量'
            },
            
            # 微积分相关
            'calculus': {
                'derivative', 'integral', 'limit', 'continuity', 'differentiable', 'antiderivative',
                'partial', 'gradient', 'divergence', 'curl', 'laplacian', 'calculus',
                '导数', '积分', '极限', '连续性', '可微', '原函数', '偏导数', '梯度', '散度', '旋度',
                '拉普拉斯'
            },
            
            # 几何相关
            'geometry': {
                'triangle', 'circle', 'ellipse', 'parabola', 'hyperbola', 'polygon', 'angle',
                'perpendicular', 'parallel', 'theorem', 'proof', 'lemma', 'corollary', 'axiom',
                'postulate', 'geometry',
                '三角形', '圆', '椭圆', '抛物线', '双曲线', '多边形', '角', '垂直',
                '平行', '定理', '证明', '引理', '推论', '公理', '公设'
            },
            
            # 统计相关
            'statistics': {
                'probability', 'distribution', 'mean', 'median', 'mode', 'variance', 'deviation',
                'correlation', 'normal', 'binomial', 'poisson', 'chi-square', 't-test', 'hypothesis',
                'statistics',
                '概率', '分布', '均值', '中位数', '众数', '方差', '标准差', '相关性', '正态分布',
                '二项分布', '泊松分布', '卡方', 't检验', '假设检验'
            },
            
            # 其他数学分支
            'analysis': {
                'exponential', 'logarithmic', 'trigonometric', 'analysis',
                '指数', '对数', '三角函数'
            }
        }
    
    def extract_selected_text(self, content: str, selection_range: Tuple[int, int]) -> str:
        """
        提取选中的文本
        
        Args:
            content: 完整文本内容
            selection_range: 选择范围 (start, end)
            
        Returns:
            选中的文本
        """
        start, end = selection_range
        
        # 验证范围
        if start < 0 or end > len(content) or start > end:
            raise ValueError("无效的选择范围")
        
        selected_text = content[start:end].strip()
        
        # 如果选中的文本为空，返回空字符串
        if not selected_text:
            return ""
        
        return selected_text
    
    def identify_math_terms(self, text: str) -> List[MathTerm]:
        """
        识别数学术语
        
        Args:
            text: 输入文本
            
        Returns:
            识别出的数学术语列表
        """
        math_terms = []
        text_lower = text.lower()
        
        # 识别英文数学术语
        for pattern in self.english_math_terms:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                term = match.group().lower()
                category = self._get_term_category(term)
                confidence = self._calculate_confidence(term, text)
                latex_repr = self._get_latex_representation(term)
                
                math_terms.append(MathTerm(
                    term=term,
                    latex_representation=latex_repr,
                    category=category,
                    confidence=confidence
                ))
        
        # 识别中文数学术语
        for pattern in self.chinese_math_terms:
            matches = re.finditer(pattern, text)
            for match in matches:
                term = match.group()
                category = self._get_term_category(term)
                confidence = self._calculate_confidence(term, text)
                latex_repr = self._get_latex_representation(term)
                
                math_terms.append(MathTerm(
                    term=term,
                    latex_representation=latex_repr,
                    category=category,
                    confidence=confidence
                ))
        
        # 识别数学符号
        for pattern in self.math_symbol_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                symbol = match.group()
                math_terms.append(MathTerm(
                    term=symbol,
                    latex_representation=symbol,
                    category='other',
                    confidence=0.9
                ))
        
        # 去重并按置信度排序
        unique_terms = self._deduplicate_terms(math_terms)
        return sorted(unique_terms, key=lambda x: x.confidence, reverse=True)
    
    def parse_latex_formulas(self, text: str) -> List[str]:
        """
        解析LaTeX公式
        
        Args:
            text: 包含LaTeX公式的文本
            
        Returns:
            解析出的LaTeX公式列表
        """
        formulas = []
        
        # 按优先级顺序处理，避免重复匹配
        # 先处理块级公式
        block_matches = re.findall(r'\$\$([^$]+)\$\$', text, re.DOTALL)
        for match in block_matches:
            formulas.append(match.strip())
        
        # 移除已匹配的块级公式，避免重复
        text_without_blocks = re.sub(r'\$\$[^$]+\$\$', '', text, flags=re.DOTALL)
        
        # 处理行内公式
        inline_matches = re.findall(r'\$([^$]+)\$', text_without_blocks)
        for match in inline_matches:
            formulas.append(match.strip())
        
        # 处理LaTeX环境
        env_matches = re.findall(r'(\\begin\{[^}]+\}.*?\\end\{[^}]+\})', text, re.DOTALL)
        for match in env_matches:
            formulas.append(match.strip())
        
        # 去重并过滤空公式
        unique_formulas = []
        seen = set()
        for formula in formulas:
            if formula and formula not in seen:
                seen.add(formula)
                unique_formulas.append(formula)
        
        return unique_formulas
    
    def generate_search_keywords(self, text: str) -> List[str]:
        """
        生成搜索关键词
        
        Args:
            text: 输入文本
            
        Returns:
            生成的搜索关键词列表
        """
        keywords = set()
        
        # 添加识别出的数学术语
        math_terms = self.identify_math_terms(text)
        for term in math_terms:
            if term.confidence >= 0.6:  # 只添加高置信度的术语
                keywords.add(term.term)
        
        # 添加LaTeX公式
        formulas = self.parse_latex_formulas(text)
        keywords.update(formulas)
        
        # 添加重要的普通词汇（去除停用词）
        words = re.findall(r'\b[a-zA-Z\u4e00-\u9fff]{3,}\b', text)
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'are', 'important', 'concepts', 'along', 'other', 'regular', 'words', 'like'}
        for word in words:
            if word.lower() not in stop_words and len(word) >= 3:
                keywords.add(word)
        
        # 限制关键词数量，优先选择数学相关的
        keywords_list = list(keywords)
        math_keywords = [kw for kw in keywords_list if self._is_math_related(kw)]
        other_keywords = [kw for kw in keywords_list if not self._is_math_related(kw)]
        
        # 优先返回数学关键词，然后是其他关键词
        result = math_keywords[:8] + other_keywords[:4]
        return result[:10]  # 最多返回10个关键词
    
    def parse_latex_to_sympy(self, latex_formula: str) -> Optional[sp.Basic]:
        """
        将LaTeX公式解析为SymPy表达式
        
        Args:
            latex_formula: LaTeX公式字符串
            
        Returns:
            SymPy表达式对象，解析失败时返回None
        """
        try:
            # 清理LaTeX公式，移除外层的$符号
            cleaned_formula = latex_formula.strip()
            if cleaned_formula.startswith('$$') and cleaned_formula.endswith('$$'):
                cleaned_formula = cleaned_formula[2:-2].strip()
            elif cleaned_formula.startswith('$') and cleaned_formula.endswith('$'):
                cleaned_formula = cleaned_formula[1:-1].strip()
            
            # 尝试使用SymPy的LaTeX解析器
            try:
                # 抑制SymPy的警告
                import warnings
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    sympy_expr = parse_latex(cleaned_formula)
                return sympy_expr
            except Exception:
                # 如果LaTeX解析失败，尝试直接解析为SymPy表达式
                try:
                    # 预处理一些常见的LaTeX命令
                    processed_formula = self._preprocess_latex_for_sympy(cleaned_formula)
                    sympy_expr = parse_expr(processed_formula)
                    return sympy_expr
                except Exception:
                    return None
                    
        except Exception:
            return None
    
    def _preprocess_latex_for_sympy(self, latex_str: str) -> str:
        """
        预处理LaTeX字符串以便SymPy解析
        
        Args:
            latex_str: LaTeX字符串
            
        Returns:
            处理后的字符串
        """
        # 替换常见的LaTeX命令为SymPy可识别的格式
        replacements = {
            r'\\frac\{([^}]+)\}\{([^}]+)\}': r'(\1)/(\2)',  # 分数
            r'\\sqrt\{([^}]+)\}': r'sqrt(\1)',              # 平方根
            r'\\sqrt\[([^]]+)\]\{([^}]+)\}': r'(\2)**(1/\1)', # n次根
            r'\\int': 'integrate',                           # 积分
            r'\\sum': 'Sum',                                # 求和
            r'\\prod': 'Product',                           # 乘积
            r'\\lim': 'limit',                              # 极限
            r'\\sin\{([^}]+)\}': r'sin(\1)',               # 三角函数
            r'\\cos\{([^}]+)\}': r'cos(\1)',
            r'\\tan\{([^}]+)\}': r'tan(\1)',
            r'\\sin': 'sin',                                # 简单三角函数
            r'\\cos': 'cos',
            r'\\tan': 'tan',
            r'\\log': 'log',
            r'\\ln': 'ln',
            r'\\exp': 'exp',
            r'\\pi': 'pi',
            r'\\infty': 'oo',                               # 无穷大
            r'\^': '**',                                    # 指数
            r'\\alpha': 'alpha',                            # 希腊字母
            r'\\beta': 'beta',
            r'\\gamma': 'gamma',
            r'\\delta': 'delta',
            r'\\epsilon': 'epsilon',
            r'\\theta': 'theta',
            r'\\lambda': 'lambda',
            r'\\mu': 'mu',
            r'\\sigma': 'sigma',
            r'\\phi': 'phi',
            r'\\omega': 'omega',
        }
        
        result = latex_str
        for pattern, replacement in replacements.items():
            result = re.sub(pattern, replacement, result)
        
        return result
    
    def analyze_mathematical_expression(self, expression: Union[str, sp.Basic]) -> Dict[str, any]:
        """
        分析数学表达式的属性和特征
        
        Args:
            expression: 数学表达式（字符串或SymPy对象）
            
        Returns:
            包含表达式分析结果的字典
        """
        try:
            # 如果输入是字符串，先尝试解析
            if isinstance(expression, str):
                # 尝试LaTeX解析
                sympy_expr = self.parse_latex_to_sympy(expression)
                if sympy_expr is None:
                    # 尝试直接解析
                    try:
                        sympy_expr = parse_expr(expression)
                    except Exception:
                        return {'error': '无法解析表达式'}
            else:
                sympy_expr = expression
            
            analysis = {
                'original': str(expression),
                'sympy_form': str(sympy_expr),
                'latex_form': sp.latex(sympy_expr),
                'variables': [str(var) for var in sympy_expr.free_symbols],
                'is_polynomial': sympy_expr.is_polynomial() if hasattr(sympy_expr, 'is_polynomial') else False,
                'is_rational': sympy_expr.is_rational if hasattr(sympy_expr, 'is_rational') else None,
                'complexity': len(str(sympy_expr)),  # 简单的复杂度度量
            }
            
            # 尝试获取更多属性
            try:
                analysis['expanded'] = str(sp.expand(sympy_expr))
                analysis['simplified'] = str(sp.simplify(sympy_expr))
                analysis['factored'] = str(sp.factor(sympy_expr))
            except Exception:
                pass
            
            # 分析表达式类型
            expr_type = self._classify_expression_type(sympy_expr)
            analysis['expression_type'] = expr_type
            
            return analysis
            
        except Exception as e:
            return {'error': f'分析失败: {str(e)}'}
    
    def _classify_expression_type(self, expr: sp.Basic) -> str:
        """
        分类数学表达式的类型
        
        Args:
            expr: SymPy表达式
            
        Returns:
            表达式类型字符串
        """
        try:
            # 检查是否为多项式
            if expr.is_polynomial():
                degree = sp.degree(expr)
                if degree == 1:
                    return 'linear'
                elif degree == 2:
                    return 'quadratic'
                elif degree == 3:
                    return 'cubic'
                else:
                    return f'polynomial_degree_{degree}'
            
            # 检查是否包含三角函数
            if any(func in str(expr) for func in ['sin', 'cos', 'tan', 'sec', 'csc', 'cot']):
                return 'trigonometric'
            
            # 检查是否包含指数或对数
            if any(func in str(expr) for func in ['exp', 'log', 'ln']):
                return 'exponential_logarithmic'
            
            # 检查是否为有理函数
            if expr.is_rational_function():
                return 'rational'
            
            # 检查是否包含积分或导数
            if any(func in str(type(expr)) for func in ['Integral', 'Derivative']):
                return 'calculus'
            
            # 检查是否为方程
            if hasattr(expr, 'lhs') and hasattr(expr, 'rhs'):
                return 'equation'
            
            return 'general'
            
        except Exception:
            return 'unknown'
    
    def extract_mathematical_concepts(self, text: str) -> Dict[str, List[str]]:
        """
        从文本中提取数学概念和公式
        
        Args:
            text: 输入文本
            
        Returns:
            包含各类数学概念的字典
        """
        concepts = {
            'formulas': [],
            'equations': [],
            'symbols': [],
            'terms': [],
            'expressions': []
        }
        
        # 提取LaTeX公式
        formulas = self.parse_latex_formulas(text)
        concepts['formulas'] = formulas
        
        # 分析每个公式
        for formula in formulas:
            analysis = self.analyze_mathematical_expression(formula)
            if 'error' not in analysis:
                if analysis.get('expression_type') in ['linear', 'quadratic', 'cubic']:
                    concepts['equations'].append(formula)
                else:
                    concepts['expressions'].append(formula)
        
        # 提取数学术语
        math_terms = self.identify_math_terms(text)
        concepts['terms'] = [term.term for term in math_terms]
        
        # 提取数学符号
        for pattern in self.math_symbol_patterns:
            matches = re.findall(pattern, text)
            concepts['symbols'].extend(matches)
        
        # 去重
        for key in concepts:
            concepts[key] = list(set(concepts[key]))
        
        return concepts
    
    def validate_latex_syntax(self, latex_str: str) -> Dict[str, any]:
        """
        验证LaTeX语法的正确性
        
        Args:
            latex_str: LaTeX字符串
            
        Returns:
            验证结果字典
        """
        result = {
            'is_valid': False,
            'errors': [],
            'warnings': [],
            'parsed_expression': None
        }
        
        try:
            # 尝试解析LaTeX
            parsed = self.parse_latex_to_sympy(latex_str)
            
            if parsed is not None:
                result['is_valid'] = True
                result['parsed_expression'] = str(parsed)
            else:
                result['errors'].append('无法解析LaTeX表达式')
            
            # 检查常见的语法问题
            syntax_issues = self._check_latex_syntax_issues(latex_str)
            result['warnings'].extend(syntax_issues)
            
        except Exception as e:
            result['errors'].append(f'解析错误: {str(e)}')
        
        return result
    
    def _check_latex_syntax_issues(self, latex_str: str) -> List[str]:
        """
        检查LaTeX语法问题
        
        Args:
            latex_str: LaTeX字符串
            
        Returns:
            问题列表
        """
        issues = []
        
        # 检查括号匹配
        if latex_str.count('{') != latex_str.count('}'):
            issues.append('花括号不匹配')
        
        if latex_str.count('[') != latex_str.count(']'):
            issues.append('方括号不匹配')
        
        if latex_str.count('(') != latex_str.count(')'):
            issues.append('圆括号不匹配')
        
        # 检查常见的LaTeX命令
        common_commands = [r'\\frac', r'\\sqrt', r'\\int', r'\\sum', r'\\lim']
        for cmd in common_commands:
            if re.search(cmd + r'(?!\{)', latex_str):
                issues.append(f'命令 {cmd} 可能缺少参数')
        
        return issues
    
    def _get_term_category(self, term: str) -> str:
        """获取术语的数学分类"""
        term_lower = term.lower()
        
        for category, terms in self.math_categories.items():
            if term_lower in terms or term in terms:
                return category
        
        return 'other'
    
    def _calculate_confidence(self, term: str, context: str) -> float:
        """计算术语识别的置信度"""
        base_confidence = 0.7
        
        # 如果术语在已知的数学术语字典中，提高置信度
        if self._is_known_math_term(term):
            base_confidence += 0.2
        
        # 如果周围有数学符号或公式，提高置信度
        if self._has_math_context(term, context):
            base_confidence += 0.1
        
        # 如果术语长度较长且包含数学特征，提高置信度
        if len(term) > 6 and any(char in term for char in 'αβγδεζηθικλμνξοπρστυφχψω'):
            base_confidence += 0.1
        
        return min(base_confidence, 1.0)
    
    def _get_latex_representation(self, term: str) -> str:
        """获取术语的LaTeX表示"""
        latex_mappings = {
            'alpha': r'\alpha', 'beta': r'\beta', 'gamma': r'\gamma', 'delta': r'\delta',
            'epsilon': r'\epsilon', 'theta': r'\theta', 'lambda': r'\lambda', 'mu': r'\mu',
            'pi': r'\pi', 'sigma': r'\sigma', 'phi': r'\phi', 'omega': r'\omega',
            'integral': r'\int', 'derivative': r'\frac{d}{dx}', 'limit': r'\lim',
            'infinity': r'\infty', 'sum': r'\sum', 'product': r'\prod',
            '积分': r'\int', '导数': r'\frac{d}{dx}', '极限': r'\lim',
            '无穷': r'\infty', '求和': r'\sum', '乘积': r'\prod',
        }
        
        return latex_mappings.get(term.lower(), term)
    
    def _deduplicate_terms(self, terms: List[MathTerm]) -> List[MathTerm]:
        """去除重复的数学术语"""
        seen = set()
        unique_terms = []
        
        for term in terms:
            key = (term.term.lower(), term.category)
            if key not in seen:
                seen.add(key)
                unique_terms.append(term)
        
        return unique_terms
    
    def _is_math_related(self, word: str) -> bool:
        """判断词汇是否与数学相关"""
        word_lower = word.lower()
        
        # 检查是否在数学术语字典中
        for terms in self.math_categories.values():
            if word_lower in terms or word in terms:
                return True
        
        # 检查是否包含数学符号
        for pattern in self.math_symbol_patterns:
            if re.search(pattern, word):
                return True
        
        return False
    
    def _is_known_math_term(self, term: str) -> bool:
        """检查是否为已知的数学术语"""
        term_lower = term.lower()
        
        for terms in self.math_categories.values():
            if term_lower in terms or term in terms:
                return True
        
        return False
    
    def _has_math_context(self, term: str, context: str) -> bool:
        """检查术语周围是否有数学上下文"""
        # 查找术语在文本中的位置
        term_pos = context.lower().find(term.lower())
        if term_pos == -1:
            return False
        
        # 检查前后50个字符的上下文
        start = max(0, term_pos - 50)
        end = min(len(context), term_pos + len(term) + 50)
        surrounding_text = context[start:end]
        
        # 检查是否包含数学符号或公式
        for pattern in self.math_symbol_patterns:
            if re.search(pattern, surrounding_text):
                return True
        
        # 检查是否包含数学相关词汇
        math_context_words = ['equation', 'formula', 'calculate', 'solve', 'proof', '公式', '计算', '求解', '证明']
        for word in math_context_words:
            if word in surrounding_text.lower():
                return True
        
        return False