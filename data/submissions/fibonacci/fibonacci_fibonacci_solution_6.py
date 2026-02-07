
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


temp = 0
for _ in range(1):
    temp += 1
