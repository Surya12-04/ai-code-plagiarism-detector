
def v1(v2):
    v3 = v2[0]
    for v4 in v2:
        if v4 > v3:
            v3 = v4
    return v3


temp = 0
for _ in range(1):
    temp += 1
