import math
import ast
import hashlib
from collections import Counter
import re

# =========================================================
# ---------------- LEXICAL ANALYSIS ----------------
# =========================================================

KEYWORDS = {
    "def", "return", "if", "elif", "else", "while", "for",
    "in", "and", "or", "not", "break", "continue", "class",
    "import", "from", "as", "with", "try", "except", "finally",
    "pass", "raise", "yield", "lambda"
}

def tokenize(code: str):
    return re.findall(
        r"[A-Za-z_][A-Za-z_0-9]*|\d+|==|!=|<=|>=|[+\-*/%<>]",
        code
    )

def normalize_identifiers(tokens):
    mapping = {}
    counter = 0
    normalized = []

    for t in tokens:
        if t.isidentifier() and t not in KEYWORDS:
            if t not in mapping:
                counter += 1
                mapping[t] = f"VAR_{counter}"
            normalized.append(mapping[t])
        else:
            normalized.append(t)

    return normalized

def token_vector(tokens):
    freq = Counter(tokens)
    total = sum(freq.values())
    if total == 0:
        return {}
    return {k: v / total for k, v in freq.items()}

def cosine(v1, v2):
    if not v1 or not v2:
        return 0.0

    common = set(v1) & set(v2)
    num = sum(v1[k] * v2[k] for k in common)
    den = math.sqrt(sum(v ** 2 for v in v1.values())) * \
          math.sqrt(sum(v ** 2 for v in v2.values()))

    return num / den if den else 0.0


# =========================================================
# ---------------- AST GLOBAL ANALYSIS ----------------
# =========================================================

class ASTExtractor(ast.NodeVisitor):
    def __init__(self):
        self.counter = Counter()
        self.depth = 0
        self.max_depth = 0

    def generic_visit(self, node):
        self.depth += 1
        self.max_depth = max(self.max_depth, self.depth)
        self.counter[type(node).__name__] += 1
        super().generic_visit(node)
        self.depth -= 1

def ast_vector(code: str):
    try:
        tree = ast.parse(code)
    except Exception:
        return {}

    extractor = ASTExtractor()
    extractor.visit(tree)
    extractor.counter["MAX_DEPTH"] = extractor.max_depth

    total = sum(extractor.counter.values())
    if total == 0:
        return {}

    return {k: v / total for k, v in extractor.counter.items()}


# =========================================================
# ---------------- AST SUBTREE ANALYSIS ----------------
# =========================================================

def canonical_subtree(node):
    if not isinstance(node, ast.AST):
        return ""

    parts = [node.__class__.__name__]

    for field, value in ast.iter_fields(node):
        if isinstance(value, list):
            parts.append(
                field + "[" + ",".join(
                    canonical_subtree(v)
                    for v in value if isinstance(v, ast.AST)
                ) + "]"
            )
        elif isinstance(value, ast.AST):
            parts.append(field + "(" + canonical_subtree(value) + ")")
        else:
            parts.append(field)

    return "|".join(parts)

def extract_subtree_hashes(code: str):
    try:
        tree = ast.parse(code)
    except Exception:
        return set()

    hashes = set()
    for node in ast.walk(tree):
        rep = canonical_subtree(node)
        h = hashlib.md5(rep.encode("utf-8")).hexdigest()
        hashes.add(h)

    return hashes

def ast_subtree_similarity(code1: str, code2: str):
    s1 = extract_subtree_hashes(code1)
    s2 = extract_subtree_hashes(code2)

    if not s1 or not s2:
        return 0.0

    return len(s1 & s2) / min(len(s1), len(s2))


# =========================================================
# ---------------- STYLE ANALYSIS ----------------
# =========================================================

def indentation_variance(code: str):
    indents = [
        len(line) - len(line.lstrip())
        for line in code.splitlines()
        if line.strip()
    ]

    if not indents:
        return 0.0

    mean = sum(indents) / len(indents)
    return sum((x - mean) ** 2 for x in indents) / len(indents)

def identifier_entropy(code: str):
    words = [w for w in code.split() if w.isidentifier()]
    freq = Counter(words)
    total = sum(freq.values())

    if total == 0:
        return 0.0

    return -sum(
        (c / total) * math.log2(c / total)
        for c in freq.values()
    )

def style_vector(code: str):
    return {
        "indent": indentation_variance(code),
        "entropy": identifier_entropy(code)
    }


# =========================================================
# ---------------- FINAL SIMILARITY (AUC-TUNED) ----------------
# =========================================================

def final_similarity(code1: str, code2: str):
    # ----- Lexical -----
    t1 = normalize_identifiers(tokenize(code1))
    t2 = normalize_identifiers(tokenize(code2))
    lex_sim = cosine(token_vector(t1), token_vector(t2))

    # ----- AST -----
    ast_global = cosine(ast_vector(code1), ast_vector(code2))
    ast_sub = ast_subtree_similarity(code1, code2)

    # AST-dominant hybrid (best for plagiarism)
    ast_hybrid = 0.3 * ast_global + 0.7 * ast_sub

    # ----- Style -----
    s1, s2 = style_vector(code1), style_vector(code2)
    style_sim = 1 / (1 + abs(s1["entropy"] - s2["entropy"]))

    # Final weighted score (ROC/AUC optimized)
    final_score = (
        0.20 * lex_sim +
        0.65 * ast_hybrid +
        0.15 * style_sim
    )

    # Non-linear stretching for better separation
    final_score = min(1.0, max(0.0, final_score ** 1.3))

    return (
        lex_sim,
        ast_global,
        ast_sub,
        ast_hybrid,
        style_sim,
        final_score
    )
