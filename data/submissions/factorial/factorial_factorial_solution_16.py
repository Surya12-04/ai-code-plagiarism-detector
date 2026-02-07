
def v1(v2):
    if v2 == 0:
        return 1
    return v2 * v1(v2 - 1)
