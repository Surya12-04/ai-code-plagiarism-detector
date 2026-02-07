
    def max_element(arr):
        m = arr[0]
        for x in arr:
            if x > m:
                m = x
        return m