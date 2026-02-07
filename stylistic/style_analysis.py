import math
from collections import Counter

# -----------------------------------------
# 1. Identifier Entropy
# -----------------------------------------
def identifier_entropy(code):
    """
    Measures diversity of variable/function names
    """
    words = [w for w in code.split() if w.isidentifier()]
    freq = Counter(words)
    total = sum(freq.values())

    if total == 0:
        return 0.0

    return -sum((c / total) * math.log2(c / total) for c in freq.values())


# -----------------------------------------
# 2. Indentation Variance
# -----------------------------------------
def indentation_variance(code):
    """
    Measures consistency of indentation
    """
    indents = [
        len(line) - len(line.lstrip())
        for line in code.splitlines()
        if line.strip()
    ]

    if not indents:
        return 0.0

    mean = sum(indents) / len(indents)
    return sum((x - mean) ** 2 for x in indents) / len(indents)


# -----------------------------------------
# 3. Average Line Length
# -----------------------------------------
def average_line_length(code):
    lines = [line for line in code.splitlines() if line.strip()]
    if not lines:
        return 0.0
    return sum(len(line) for line in lines) / len(lines)


# -----------------------------------------
# 4. Blank Line Ratio
# -----------------------------------------
def blank_line_ratio(code):
    lines = code.splitlines()
    if not lines:
        return 0.0
    blank = sum(1 for l in lines if not l.strip())
    return blank / len(lines)


# -----------------------------------------
# 5. Comment Density
# -----------------------------------------
def comment_density(code):
    lines = code.splitlines()
    if not lines:
        return 0.0
    comments = sum(1 for l in lines if l.strip().startswith("#"))
    return comments / len(lines)


# -----------------------------------------
# Style Vector
# -----------------------------------------
def style_vector(code):
    return {
        "entropy": identifier_entropy(code),
        "indent_var": indentation_variance(code),
        "avg_line_len": average_line_length(code),
        "blank_ratio": blank_line_ratio(code),
        "comment_density": comment_density(code),
    }


# -----------------------------------------
# Style Similarity
# -----------------------------------------
def style_similarity(code1, code2):
    """
    Compute similarity between two coding styles
    """
    v1 = style_vector(code1)
    v2 = style_vector(code2)

    diffs = []
    for key in v1:
        diffs.append(abs(v1[key] - v2[key]))

    # Convert distance to similarity
    avg_diff = sum(diffs) / len(diffs)
    return 1 / (1 + avg_diff)
