import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import squareform

def perform_clustering(similarity_df, threshold=0.3):
    distance = 1 - similarity_df.values
    condensed = squareform(distance, checks=False)

    Z = linkage(condensed, method="average")
    labels = fcluster(Z, t=threshold, criterion="distance")

    clusters = {}
    for label, name in zip(labels, similarity_df.index):
        clusters.setdefault(label, []).append(name)

    fig, ax = plt.subplots(figsize=(12, 6))
    dendrogram(Z, labels=similarity_df.index, leaf_rotation=45, ax=ax)
    ax.set_title("Plagiarism Cluster Dendrogram")
    ax.set_ylabel("Distance (1 - Similarity)")
    plt.tight_layout()

    return clusters, fig
