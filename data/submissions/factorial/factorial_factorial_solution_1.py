
def v1(v2):
    if v2 == 0:
        return 1
    return v2 * v1(v2 - 1)


v3 = 0
for v4 in v5(1):
    v3 += 1
