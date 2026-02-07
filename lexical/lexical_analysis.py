import math
import re
from collections import Counter

# ---------------------------------
# Tokenization
# ---------------------------------

def tokenize(code: str):
    """
    Split code into identifiers, numbers, and operators
    """
    pattern = r"[A-Za-z_][A-Za-z_0-9]*|\d+|==|!=|<=|>=|[+\-*/%<>]"
    return re.findall(pattern, code)


# ---------------------------------
# Identifier Normalization
# ---------------------------------

def normalize_identifiers(tokens):
    """
    Replace variable names with generic placeholders
    """
    keywords = {
        "def", "return", "if", "elif", "else", "while", "for",
        "in", "and", "or", "not", "break", "continue", "class"
    }

    mapping = {}
    normalized = []
    counter = 0

    for token in tokens:
        if token.isidentifier() and token not in keywords:
            if token not in mapping:
                counter += 1
                mapping[token] = f"VAR_{counter}"
            normalized.append(mapping[token])
        else:
            normalized.append(token)

    return normalized


# ---------------------------------
# Vectorization
# ---------------------------------

def token_vector(tokens):
    freq = Counter(tokens)
    total = sum(freq.values())

    if total == 0:
        return {}

    return {k: v / total for k, v in freq.items()}


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

def lexical_similarity(code1: str, code2: str) -> float:
    """
    Compute lexical similarity between two code strings
    """
    t1 = normalize_identifiers(tokenize(code1))
    t2 = normalize_identifiers(tokenize(code2))

    v1 = token_vector(t1)
    v2 = token_vector(t2)

    return cosine_similarity(v1, v2)
