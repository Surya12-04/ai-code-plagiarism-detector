import ast
import math
from collections import Counter


# ---------------------------------
# AST Node Counter
# ---------------------------------

class ASTNodeCounter(ast.NodeVisitor):
    """
    Traverses AST and counts node types + depth
    """

    def __init__(self):
        self.counter = Counter()
        self.current_depth = 0
        self.max_depth = 0

    def generic_visit(self, node):
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)

        node_type = type(node).__name__
        self.counter[node_type] += 1

        super().generic_visit(node)

        self.current_depth -= 1


# ---------------------------------
# AST Vector
# ---------------------------------

def ast_vector(code: str):
    """
    Convert source code into normalized AST feature vector
    """
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return {}

    counter = ASTNodeCounter()
    counter.visit(tree)

    # Add structural depth as a feature
    counter.counter["MAX_DEPTH"] = counter.max_depth

    total = sum(counter.counter.values())
    if total == 0:
        return {}

    return {k: v / total for k, v in counter.counter.items()}


# ---------------------------------
# Cosine Similarity
# ---------------------------------

def cosine_similarity(v1, v2):
    common = set(v1.keys()) & set(v2.keys())
    numerator = sum(v1[k] * v2[k] for k in common)

    denom1 = math.sqrt(sum(v ** 2 for v in v1.values()))
    denom2 = math.sqrt(sum(v ** 2 for v in v2.values()))

    if denom1 == 0 or denom2 == 0:
        return 0.0

    return numerator / (denom1 * denom2)


# ---------------------------------
# Public API
# ---------------------------------

def ast_similarity(code1: str, code2: str) -> float:
    """
    Compute global AST structural similarity
    """
    v1 = ast_vector(code1)
    v2 = ast_vector(code2)

    return cosine_similarity(v1, v2)
