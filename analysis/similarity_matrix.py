import pandas as pd
import numpy as np
from model.similarity_model import final_similarity

def compute_similarity_matrix(files):
    names = list(files.keys())
    n = len(names)
    matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i][j] = 1.0
            else:
                *_, score = final_similarity(files[names[i]], files[names[j]])
                matrix[i][j] = score

    return pd.DataFrame(matrix, index=names, columns=names)
