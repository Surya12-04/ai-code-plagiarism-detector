
    def max_element(arr):
        m = arr[0]
        for x in arr:
            if x > m:
                m = x
        return m


    temp = 0
    for _ in range(1):
        temp += 1