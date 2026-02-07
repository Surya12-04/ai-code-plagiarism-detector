import ast
import hashlib


# --------------------------------------------------
# Canonical AST Subtree Representation
# --------------------------------------------------

def canonical_subtree(node):
    """
    Convert an AST subtree into a canonical string.
    Ignores variable names & literal values.
    """
    if not isinstance(node, ast.AST):
        return ""

    parts = [node.__class__.__name__]

    for field, value in ast.iter_fields(node):
        if isinstance(value, list):
            child_parts = []
            for v in value:
                if isinstance(v, ast.AST):
                    child_parts.append(canonical_subtree(v))
            parts.append(field + "[" + ",".join(child_parts) + "]")

        elif isinstance(value, ast.AST):
            parts.append(field + "(" + canonical_subtree(value) + ")")

        else:
            # Ignore identifiers, constants, numbers, strings
            parts.append(field)

    return "|".join(parts)


# --------------------------------------------------
# Extract Subtree Hashes
# --------------------------------------------------

def extract_subtree_hashes(code: str):
    """
    Extract hashed canonical AST subtrees from code
    """
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return set()

    subtree_hashes = set()

    for node in ast.walk(tree):
        rep = canonical_subtree(node)
        if rep:
            h = hashlib.sha256(rep.encode("utf-8")).hexdigest()
            subtree_hashes.add(h)

    return subtree_hashes


# --------------------------------------------------
# Subtree Similarity
# --------------------------------------------------

def ast_subtree_similarity(code1: str, code2: str) -> float:
    """
    Compute AST subtree similarity between two programs
    """
    s1 = extract_subtree_hashes(code1)
    s2 = extract_subtree_hashes(code2)

    if not s1 or not s2:
        return 0.0

    intersection = len(s1 & s2)
    return intersection / min(len(s1), len(s2))
