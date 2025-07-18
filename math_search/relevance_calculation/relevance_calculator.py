"""
相关度计算器实现
Relevance Calculator Implementation
"""

import re
import math
from typing import List, Dict, Set
from collections import Counter

from ..interfaces.relevance_calculator import IRelevanceCalculator
from ..models import SearchResult


class RelevanceCalculator(IRelevanceCalculator):
    """基础相关度计算器实现"""
    
    def __init__(self):
        """初始化相关度计算器"""
        # 英文停用词列表
        self.stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'the', 'this', 'but', 'they', 'have',
            'had', 'what', 'said', 'each', 'which', 'their', 'time', 'if'
        }
        
        # 数学术语权重映射 - 按重要性和专业性分级
        self.math_terms_weights = {
            # 核心数学分支 (高权重)
            'algebra': 1.6,
            'calculus': 1.6,
            'geometry': 1.6,
            'topology': 1.7,
            'analysis': 1.7,
            'statistics': 1.5,
            'probability': 1.5,
            'combinatorics': 1.6,
            'number theory': 1.7,
            'differential equations': 1.6,
            'linear algebra': 1.6,
            'abstract algebra': 1.7,
            'real analysis': 1.8,
            'complex analysis': 1.8,
            'functional analysis': 1.8,
            'algebraic geometry': 1.8,
            'differential geometry': 1.8,
            
            # 数学概念和结构 (中高权重)
            'theorem': 1.4,
            'lemma': 1.3,
            'corollary': 1.3,
            'proof': 1.3,
            'axiom': 1.4,
            'definition': 1.2,
            'proposition': 1.3,
            'conjecture': 1.5,
            'hypothesis': 1.3,
            
            # 数学对象和运算 (中权重)
            'function': 1.3,
            'derivative': 1.4,
            'integral': 1.4,
            'limit': 1.4,
            'matrix': 1.3,
            'vector': 1.3,
            'polynomial': 1.3,
            'logarithm': 1.3,
            'exponential': 1.3,
            'trigonometry': 1.4,
            'sine': 1.2,
            'cosine': 1.2,
            'tangent': 1.2,
            'series': 1.4,
            'sequence': 1.3,
            'convergence': 1.4,
            'divergence': 1.4,
            
            # 数学方法和技术 (中权重)
            'formula': 1.3,
            'equation': 1.3,
            'inequality': 1.3,
            'optimization': 1.4,
            'algorithm': 1.3,
            'method': 1.2,
            'technique': 1.2,
            'approximation': 1.3,
            'iteration': 1.3,
            
            # 高级数学概念 (高权重)
            'manifold': 1.8,
            'homomorphism': 1.8,
            'isomorphism': 1.8,
            'eigenvalue': 1.5,
            'eigenvector': 1.5,
            'fourier': 1.6,
            'laplace': 1.6,
            'transform': 1.4,
            'group theory': 1.7,
            'ring theory': 1.7,
            'field theory': 1.7,
            'category theory': 1.9,
            'measure theory': 1.8,
            'operator theory': 1.8,
            
            # 应用数学 (中权重)
            'model': 1.2,
            'simulation': 1.3,
            'numerical': 1.4,
            'computational': 1.4,
            'applied': 1.3,
            'mathematical modeling': 1.5,
            'mathematical physics': 1.6,
            'operations research': 1.4,
            
            # 数学逻辑和基础 (高权重)
            'logic': 1.5,
            'set theory': 1.6,
            'mathematical logic': 1.7,
            'foundations': 1.6,
            'axiomatics': 1.6
        }
        
        # 学术来源权重 - 按权威性和专业性分级
        self.academic_sources = {
            # 顶级数学预印本和期刊 (最高权重)
            'arxiv.org': 1.9,
            'mathscinet.ams.org': 1.9,
            'zbmath.org': 1.8,
            
            # 权威数学资源 (高权重)
            'mathworld.wolfram.com': 1.8,
            'planetmath.org': 1.7,
            'mathoverflow.net': 1.7,
            'math.stackexchange.com': 1.6,
            
            # 顶级大学数学系 (高权重)
            'mit.edu': 1.8,
            'stanford.edu': 1.8,
            'harvard.edu': 1.8,
            'princeton.edu': 1.8,
            'caltech.edu': 1.8,
            'berkeley.edu': 1.7,
            'cmu.edu': 1.7,
            'yale.edu': 1.7,
            'columbia.edu': 1.7,
            'uchicago.edu': 1.7,
            
            # 国际知名大学 (中高权重)
            'cambridge.ac.uk': 1.7,
            'ox.ac.uk': 1.7,  # Oxford
            'imperial.ac.uk': 1.6,
            'ethz.ch': 1.7,  # ETH Zurich
            'ens.fr': 1.7,   # École Normale Supérieure
            'u-tokyo.ac.jp': 1.6,
            
            # 学术出版商 (中高权重)
            'springer.com': 1.6,
            'elsevier.com': 1.6,
            'wiley.com': 1.5,
            'cambridge.org': 1.6,
            'jstor.org': 1.7,
            'projecteuclid.org': 1.7,
            'ams.org': 1.8,  # American Mathematical Society
            
            # 在线教育平台 (中权重)
            'khanacademy.org': 1.4,
            'coursera.org': 1.3,
            'edx.org': 1.3,
            'brilliant.org': 1.4,
            
            # 通用学术资源 (中低权重)
            'wikipedia.org': 1.3,
            'scholarpedia.org': 1.4,
            'nist.gov': 1.5,
            
            # 专业数学软件文档 (中权重)
            'wolfram.com': 1.5,
            'mathworks.com': 1.4,  # MATLAB
            'sagemath.org': 1.4,
            'sympy.org': 1.4,
            
            # 数学竞赛和奥数 (中权重)
            'artofproblemsolving.com': 1.4,
            'imo-official.org': 1.5,
            
            # 其他学术机构
            'maa.org': 1.6,  # Mathematical Association of America
            'siam.org': 1.6,  # Society for Industrial and Applied Mathematics
            'ieee.org': 1.5
        }
    
    def calculate_relevance(self, query: str, result: SearchResult) -> float:
        """
        计算相关度评分
        
        Args:
            query: 查询文本
            result: 搜索结果
            
        Returns:
            相关度评分 (0-1)
        """
        # 基础TF-IDF相似度
        tfidf_score = self._calculate_tfidf_similarity(query, result)
        
        # 关键词匹配评分
        keyword_score = self._calculate_keyword_matching(query, result)
        
        # 数学内容检测加成
        math_boost = 1.2 if result.math_content_detected else 1.0
        
        # 标题匹配加成
        title_boost = self._calculate_title_boost(query, result.title)
        
        # 综合评分
        combined_score = (
            tfidf_score * 0.4 +
            keyword_score * 0.4 +
            0.2  # 基础分
        ) * math_boost * title_boost
        
        # 确保评分在0-1范围内
        return min(max(combined_score, 0.0), 1.0)
    
    def _calculate_tfidf_similarity(self, query: str, result: SearchResult) -> float:
        """计算TF-IDF相似度"""
        try:
            # 组合结果文本
            result_text = f"{result.title} {result.snippet}"
            
            # 使用自定义TF-IDF计算
            return self._custom_tfidf_similarity(query, result_text)
        except Exception:
            # 如果TF-IDF计算失败，回退到简单的词汇重叠
            return self._calculate_word_overlap(query, f"{result.title} {result.snippet}")
    
    def _custom_tfidf_similarity(self, text1: str, text2: str) -> float:
        """自定义TF-IDF相似度计算"""
        # 分词并移除停用词
        words1 = [w for w in self._tokenize_text(text1.lower()) if w not in self.stop_words and len(w) > 1]
        words2 = [w for w in self._tokenize_text(text2.lower()) if w not in self.stop_words and len(w) > 1]
        
        if not words1 or not words2:
            return 0.0
        
        # 计算词频
        tf1 = Counter(words1)
        tf2 = Counter(words2)
        
        # 获取所有唯一词汇
        all_words = set(words1 + words2)
        
        if not all_words:
            return 0.0
        
        # 计算TF-IDF向量
        tfidf1 = {}
        tfidf2 = {}
        
        for word in all_words:
            # TF计算（归一化词频）
            tf1_val = tf1.get(word, 0) / len(words1) if len(words1) > 0 else 0
            tf2_val = tf2.get(word, 0) / len(words2) if len(words2) > 0 else 0
            
            # 简化的IDF计算
            # 如果词在两个文档中都出现，IDF较低；如果只在一个文档中出现，IDF较高
            df = (1 if tf1.get(word, 0) > 0 else 0) + (1 if tf2.get(word, 0) > 0 else 0)
            idf = math.log(2 / df) if df > 0 else 0
            
            tfidf1[word] = tf1_val * (1 + idf)  # 加1避免0值
            tfidf2[word] = tf2_val * (1 + idf)
        
        # 计算余弦相似度
        return self._cosine_similarity(tfidf1, tfidf2, all_words)
    
    def _cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float], words: Set[str]) -> float:
        """计算余弦相似度"""
        dot_product = sum(vec1.get(word, 0) * vec2.get(word, 0) for word in words)
        
        norm1 = math.sqrt(sum(vec1.get(word, 0) ** 2 for word in words))
        norm2 = math.sqrt(sum(vec2.get(word, 0) ** 2 for word in words))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def _calculate_keyword_matching(self, query: str, result: SearchResult) -> float:
        """计算关键词匹配评分"""
        query_words = set(self._tokenize_text(query.lower()))
        result_text = f"{result.title} {result.snippet}".lower()
        result_words = set(self._tokenize_text(result_text))
        
        if not query_words:
            return 0.0
        
        # 计算词汇重叠率
        intersection = query_words.intersection(result_words)
        overlap_ratio = len(intersection) / len(query_words)
        
        # 数学术语匹配加成
        math_term_boost = 1.0
        for term in intersection:
            if term in self.math_terms_weights:
                math_term_boost *= self.math_terms_weights[term]
        
        return min(overlap_ratio * math_term_boost, 1.0)
    
    def _calculate_title_boost(self, query: str, title: str) -> float:
        """计算标题匹配加成"""
        query_words = set(self._tokenize_text(query.lower()))
        title_words = set(self._tokenize_text(title.lower()))
        
        if not query_words:
            return 1.0
        
        # 标题中包含查询词的比例
        intersection = query_words.intersection(title_words)
        title_match_ratio = len(intersection) / len(query_words)
        
        # 标题匹配加成：最高1.3倍
        return 1.0 + (title_match_ratio * 0.3)
    
    def _calculate_word_overlap(self, text1: str, text2: str) -> float:
        """计算简单词汇重叠相似度"""
        words1 = set(self._tokenize_text(text1.lower()))
        words2 = set(self._tokenize_text(text2.lower()))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _tokenize_text(self, text: str) -> List[str]:
        """文本分词"""
        # 移除标点符号，保留字母数字
        text = re.sub(r'[^\w\s]', ' ', text)
        # 分割并过滤空字符串
        words = [word.strip() for word in text.split() if word.strip()]
        return words
    
    def rank_results(self, results: List[SearchResult]) -> List[SearchResult]:
        """
        对结果进行排序 - 使用多层排序策略
        
        Args:
            results: 搜索结果列表
            
        Returns:
            按相关度排序的结果列表
        """
        # 多层排序：相关度评分 -> 数学内容检测 -> 学术来源权重 -> 时间戳
        sorted_results = sorted(
            results,
            key=lambda x: (
                x.relevance_score,  # 主要排序：相关度评分
                1 if x.math_content_detected else 0,  # 次要排序：数学内容优先
                self._get_source_boost(x.url),  # 第三排序：学术来源权重
                x.timestamp  # 最后排序：时间戳（较新的优先）
            ),
            reverse=True
        )
        
        return sorted_results
    
    def apply_math_domain_boost(self, results: List[SearchResult]) -> List[SearchResult]:
        """
        应用数学领域权重提升 - 增强版
        
        Args:
            results: 搜索结果列表
            
        Returns:
            应用权重提升后的结果列表
        """
        boosted_results = []
        
        for result in results:
            # 复制结果对象
            boosted_result = SearchResult(
                title=result.title,
                url=result.url,
                snippet=result.snippet,
                source=result.source,
                relevance_score=result.relevance_score,
                timestamp=result.timestamp,
                math_content_detected=result.math_content_detected
            )
            
            # 应用学术来源权重
            source_boost = self._get_source_boost(result.url)
            
            # 应用数学内容检测权重
            math_content_boost = 1.15 if result.math_content_detected else 1.0
            
            # 应用数学术语权重
            math_terms_boost = self._get_math_terms_boost(
                f"{result.title} {result.snippet}"
            )
            
            # 应用数学领域深度权重
            domain_depth_boost = self._get_math_domain_depth_boost(
                f"{result.title} {result.snippet}"
            )
            
            # 应用数学复杂度权重
            complexity_boost = self._calculate_mathematical_complexity_score(
                f"{result.title} {result.snippet}"
            )
            
            # 应用学术级别权重
            academic_level_boost = self._get_academic_level_boost(result)
            
            # 综合权重提升
            total_boost = (
                source_boost * 
                math_content_boost * 
                math_terms_boost * 
                domain_depth_boost * 
                complexity_boost *
                academic_level_boost
            )
            
            # 更新相关度评分
            boosted_result.relevance_score = min(
                result.relevance_score * total_boost,
                1.0
            )
            
            boosted_results.append(boosted_result)
        
        return boosted_results
    
    def _get_source_boost(self, url: str) -> float:
        """获取来源权重加成"""
        url_lower = url.lower()
        
        for domain, weight in self.academic_sources.items():
            if domain in url_lower:
                return weight
        
        return 1.0  # 默认权重
    
    def _get_math_terms_boost(self, text: str) -> float:
        """获取数学术语权重加成 - 增强版"""
        text_lower = text.lower()
        boost = 1.0
        
        # 计算数学术语出现次数和权重
        for term, weight in self.math_terms_weights.items():
            if term in text_lower:
                # 每出现一次数学术语，增加一定权重
                count = text_lower.count(term)
                boost *= (1.0 + (weight - 1.0) * count * 0.1)
        
        # 数学术语密度加成
        math_density_boost = self._calculate_math_term_density(text_lower)
        boost *= math_density_boost
        
        # 数学术语共现加成（多个高级术语同时出现）
        cooccurrence_boost = self._calculate_math_term_cooccurrence(text_lower)
        boost *= cooccurrence_boost
        
        # 限制最大权重提升
        return min(boost, 2.5)
    
    def _get_math_domain_depth_boost(self, text: str) -> float:
        """获取数学领域深度权重加成"""
        text_lower = text.lower()
        
        # 高级数学概念指标
        advanced_concepts = [
            'manifold', 'topology', 'homomorphism', 'isomorphism', 
            'eigenvalue', 'eigenvector', 'fourier', 'laplace',
            'differential equations', 'number theory', 'analysis',
            'abstract algebra', 'real analysis', 'complex analysis',
            'functional analysis', 'measure theory', 'category theory'
        ]
        
        # 研究级关键词
        research_keywords = [
            'theorem', 'proof', 'lemma', 'corollary', 'conjecture',
            'axiom', 'proposition', 'research', 'paper', 'journal',
            'publication', 'study', 'investigation', 'novel', 'new'
        ]
        
        # 计算深度评分
        depth_score = 1.0
        
        # 高级概念加成
        advanced_count = sum(1 for concept in advanced_concepts if concept in text_lower)
        if advanced_count > 0:
            depth_score *= (1.0 + advanced_count * 0.15)
        
        # 研究级关键词加成
        research_count = sum(1 for keyword in research_keywords if keyword in text_lower)
        if research_count > 0:
            depth_score *= (1.0 + research_count * 0.1)
        
        # 数学符号和公式检测（简单启发式）
        if any(symbol in text for symbol in ['∫', '∑', '∂', '∇', '∞', '≤', '≥', '≠', '±']):
            depth_score *= 1.2
        
        # LaTeX数学模式检测
        if '$' in text or '\\' in text:
            depth_score *= 1.15
        
        return min(depth_score, 1.8)
    
    def _get_academic_level_boost(self, result: SearchResult) -> float:
        """获取学术级别权重加成"""
        text = f"{result.title} {result.snippet}".lower()
        
        # 学术级别指标
        academic_indicators = {
            # 高级学术指标
            'phd': 1.4,
            'doctorate': 1.4,
            'professor': 1.3,
            'research': 1.3,
            'university': 1.2,
            'college': 1.1,
            
            # 出版物指标
            'journal': 1.4,
            'paper': 1.3,
            'article': 1.2,
            'publication': 1.3,
            'proceedings': 1.3,
            'conference': 1.2,
            
            # 教育级别指标
            'graduate': 1.3,
            'undergraduate': 1.1,
            'advanced': 1.2,
            'introduction': 1.0,
            'basic': 0.9,
            'elementary': 0.8,
            
            # 课程级别指标
            'course': 1.1,
            'lecture': 1.2,
            'seminar': 1.3,
            'workshop': 1.1,
            'tutorial': 1.0
        }
        
        boost = 1.0
        
        # 应用学术级别权重
        for indicator, weight in academic_indicators.items():
            if indicator in text:
                boost *= weight
        
        # 检查URL中的学术指标
        url_lower = result.url.lower()
        if any(edu_domain in url_lower for edu_domain in ['.edu', '.ac.', 'university', 'college']):
            boost *= 1.2
        
        # 限制权重范围
        return min(max(boost, 0.8), 1.6)
    
    def _calculate_math_term_density(self, text: str) -> float:
        """计算数学术语密度加成"""
        words = self._tokenize_text(text)
        if not words:
            return 1.0
        
        # 计算数学术语数量（考虑多词术语）
        math_term_count = 0
        text_lower = text.lower()
        
        for term in self.math_terms_weights.keys():
            if term in text_lower:
                # 对于多词术语，只计算一次
                if ' ' in term:
                    # 多词术语
                    math_term_count += text_lower.count(term)
                else:
                    # 单词术语，使用词边界匹配
                    import re
                    pattern = r'\b' + re.escape(term) + r'\b'
                    matches = re.findall(pattern, text_lower)
                    math_term_count += len(matches)
        
        # 计算密度（数学术语数量 / 总词数）
        density = math_term_count / len(words) if len(words) > 0 else 0
        
        # 密度加成：密度越高，权重越大
        if density >= 0.4:  # 高密度
            return 1.3
        elif density >= 0.25:  # 中高密度
            return 1.25
        elif density >= 0.15:  # 中密度
            return 1.2
        elif density >= 0.05:  # 低密度
            return 1.1
        else:
            return 1.0
    
    def _calculate_math_term_cooccurrence(self, text: str) -> float:
        """计算数学术语共现加成"""
        # 高级数学术语列表
        advanced_terms = [
            'manifold', 'homomorphism', 'isomorphism', 'topology',
            'category theory', 'measure theory', 'functional analysis',
            'real analysis', 'complex analysis', 'abstract algebra',
            'algebraic geometry', 'differential geometry', 'operator theory'
        ]
        
        # 计算高级术语共现数量
        cooccurring_terms = [term for term in advanced_terms if term in text]
        
        if len(cooccurring_terms) >= 3:
            return 1.4  # 3个或更多高级术语同时出现
        elif len(cooccurring_terms) == 2:
            return 1.2  # 2个高级术语同时出现
        elif len(cooccurring_terms) == 1:
            return 1.1  # 1个高级术语
        else:
            return 1.0  # 无高级术语
    
    def _calculate_mathematical_complexity_score(self, text: str) -> float:
        """计算数学复杂度评分"""
        complexity_indicators = {
            # 高复杂度指标
            'proof': 2.0,
            'theorem': 2.0,
            'lemma': 1.8,
            'corollary': 1.8,
            'conjecture': 2.2,
            
            # 高级数学结构
            'homomorphism': 2.5,
            'isomorphism': 2.5,
            'manifold': 2.3,
            'topology': 2.1,
            'category theory': 2.8,
            'measure theory': 2.4,
            
            # 数学分析
            'functional analysis': 2.6,
            'real analysis': 2.4,
            'complex analysis': 2.4,
            'differential equations': 2.2,
            
            # 代数结构
            'abstract algebra': 2.3,
            'group theory': 2.2,
            'ring theory': 2.2,
            'field theory': 2.2,
            
            # 几何
            'algebraic geometry': 2.7,
            'differential geometry': 2.5,
            
            # 基础概念（较低复杂度）
            'algebra': 1.2,
            'calculus': 1.3,
            'geometry': 1.1,
            'statistics': 1.0,
            'probability': 1.1
        }
        
        text_lower = text.lower()
        total_complexity = 0.0
        term_count = 0
        
        for term, complexity in complexity_indicators.items():
            if term in text_lower:
                total_complexity += complexity
                term_count += 1
        
        if term_count == 0:
            return 1.0
        
        # 平均复杂度
        avg_complexity = total_complexity / term_count
        
        # 转换为权重加成（1.0 - 2.0范围）
        return min(1.0 + (avg_complexity - 1.0) * 0.3, 2.0)
    
    def get_advanced_sorting_metrics(self, results: List[SearchResult]) -> List[Dict[str, float]]:
        """
        获取高级排序指标 - 用于调试和分析
        
        Args:
            results: 搜索结果列表
            
        Returns:
            每个结果的详细指标列表
        """
        metrics = []
        
        for result in results:
            text = f"{result.title} {result.snippet}"
            
            metric = {
                'base_relevance': result.relevance_score,
                'source_boost': self._get_source_boost(result.url),
                'math_terms_boost': self._get_math_terms_boost(text),
                'domain_depth_boost': self._get_math_domain_depth_boost(text),
                'complexity_boost': self._calculate_mathematical_complexity_score(text),
                'academic_level_boost': self._get_academic_level_boost(result),
                'math_content_detected': result.math_content_detected,
                'url': result.url,
                'title': result.title[:50] + '...' if len(result.title) > 50 else result.title
            }
            
            # 计算最终权重
            total_boost = (
                metric['source_boost'] * 
                metric['math_terms_boost'] * 
                metric['domain_depth_boost'] * 
                metric['complexity_boost'] *
                metric['academic_level_boost'] *
                (1.15 if result.math_content_detected else 1.0)
            )
            
            metric['total_boost'] = total_boost
            metric['final_score'] = min(result.relevance_score * total_boost, 1.0)
            
            metrics.append(metric)
        
        return metrics