import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix


def evaluate_system(sim_scores, ground_truth_path, threshold):
    """
    Fast evaluation using cached similarity scores
    """

    gt = pd.read_csv(ground_truth_path)

    y_true = []
    y_pred = []

    for _, row in gt.iterrows():
        key = tuple(sorted([row["file1"], row["file2"]]))

        if key not in sim_scores:
            continue

        y_true.append(int(row["label"]))
        y_pred.append(1 if sim_scores[key] >= threshold else 0)

    if len(y_true) == 0:
        return {
            "Precision": 0.0,
            "Recall": 0.0,
            "F1-score": 0.0,
            "Confusion Matrix": [[0, 0], [0, 0]]
        }

    return {
        "Precision": round(precision_score(y_true, y_pred, zero_division=0), 3),
        "Recall": round(recall_score(y_true, y_pred, zero_division=0), 3),
        "F1-score": round(f1_score(y_true, y_pred, zero_division=0), 3),
        "Confusion Matrix": confusion_matrix(y_true, y_pred).tolist()
    }
