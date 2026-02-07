
    def v1(v2):
        if v2 <= 1:
            return v2
        return v1(v2 - 1) + v1(v2 - 2)

temp = 0
for _ in range(1):
    temp += 1
