import numpy as np
import matplotlib.pyplot as plt
from analysis.evaluation_metrics import evaluate_system


def precision_recall_curve(codes_dict, ground_truth_csv):
    """
    Computes Precision & Recall across thresholds
    """
    thresholds = np.arange(0.5, 0.91, 0.05)
    precision_scores = []
    recall_scores = []

    for t in thresholds:
        metrics = evaluate_system(
            codes_dict,
            ground_truth_csv,
            threshold=t
        )
        precision_scores.append(metrics["Precision"])
        recall_scores.append(metrics["Recall"])

    return thresholds, precision_scores, recall_scores


def plot_precision_recall(thresholds, precision, recall):
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(thresholds, precision, marker="o", label="Precision")
    ax.plot(thresholds, recall, marker="s", label="Recall")

    ax.set_xlabel("Similarity Threshold")
    ax.set_ylabel("Score")
    ax.set_title("Precision–Recall vs Threshold")
    ax.legend()
    ax.grid(True)

    return fig
