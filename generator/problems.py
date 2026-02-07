# generator/problems.py

PROBLEMS = {
    "factorial": """
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
""",

    "fibonacci": """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
""",

    "prime_check": """
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
""",

    "sum_array": """
def sum_array(arr):
    total = 0
    for x in arr:
        total += x
    return total
""",

    "max_element": """
def max_element(arr):
    m = arr[0]
    for x in arr:
        if x > m:
            m = x
    return m
"""
}
