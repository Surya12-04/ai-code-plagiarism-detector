# generator/transformations.py

import random
import re

def rename_variables(code):
    mapping = {}
    var_id = 1

    def repl(match):
        nonlocal var_id
        name = match.group(0)
        if name in {"def", "return", "for", "if", "else", "while", "in"}:
            return name
        if name not in mapping:
            mapping[name] = f"v{var_id}"
            var_id += 1
        return mapping[name]

    return re.sub(r"\b[a-zA-Z_]\w*\b", repl, code)


def add_dummy_code(code):
    dummy = """
temp = 0
for _ in range(1):
    temp += 1
"""
    return code + "\n" + dummy


def change_loop_style(code):
    return code.replace("for", "while", 1) if "for" in code else code


def change_whitespace(code):
    lines = code.splitlines()
    return "\n".join("    " + line if line.strip() else line for line in lines)


TRANSFORMATIONS = [
    rename_variables,
    add_dummy_code,
    change_whitespace
]


def apply_random_transformations(code, k=2):
    code = code
    funcs = random.sample(TRANSFORMATIONS, k)
    for f in funcs:
        code = f(code)
    return code
