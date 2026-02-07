import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc


def roc_curve_data(sim_scores, ground_truth_path):
    """
    Fast ROC computation using cached similarity scores
    """

    gt = pd.read_csv(ground_truth_path)

    y_true = []
    y_scores = []

    for _, row in gt.iterrows():
        key = tuple(sorted([row["file1"], row["file2"]]))

        if key not in sim_scores:
            continue

        y_true.append(int(row["label"]))
        y_scores.append(sim_scores[key])

    if len(y_true) == 0:
        return None, None, None

    return roc_curve(y_true, y_scores)


def plot_roc_curve(fpr, tpr):
    auc_score = auc(fpr, tpr)

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(fpr, tpr, linewidth=2, label=f"AUC = {auc_score:.3f}")
    ax.plot([0, 1], [0, 1], linestyle="--", color="gray")

    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curve")
    ax.legend(loc="lower right")
    ax.grid(True)

    return fig, auc_score
