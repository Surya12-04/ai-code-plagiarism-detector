import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from model.similarity_model import final_similarity
from analysis.clustering_analysis import perform_clustering
from analysis.evaluation_metrics import evaluate_system
from analysis.roc_analysis import roc_curve_data, plot_roc_curve


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="AI Code Similarity & Plagiarism Detection",
    layout="wide"
)

# =========================================================
# HEADER
# =========================================================
st.title("AI-Based Code Similarity & Plagiarism Detection System")
st.markdown("""
Hybrid plagiarism detection using  
**Lexical + AST (Global & Subtree) + Stylistic Features**
""")

# =========================================================
# SESSION STATE
# =========================================================
if "codes_dict" not in st.session_state:
    st.session_state.codes_dict = None

if "sim_df" not in st.session_state:
    st.session_state.sim_df = None

if "sim_scores" not in st.session_state:
    st.session_state.sim_scores = None


# =========================================================
# PAIRWISE COMPARISON
# =========================================================
st.header("🔍 Pairwise Code Comparison")

pair_files = st.file_uploader(
    "Upload exactly TWO Python (.py) files",
    type=["py"],
    accept_multiple_files=True
)

if pair_files and len(pair_files) == 2:
    code1 = pair_files[0].read().decode("utf-8", errors="ignore")
    code2 = pair_files[1].read().decode("utf-8", errors="ignore")

    if st.button("Compare Files"):
        lex, ast_g, ast_s, ast_h, style, score = final_similarity(code1, code2)

        c1, c2, c3 = st.columns(3)
        c1.metric("Lexical", round(lex, 3))
        c2.metric("AST Global", round(ast_g, 3))
        c3.metric("AST Subtree", round(ast_s, 3))

        c1.metric("AST Hybrid", round(ast_h, 3))
        c2.metric("Style", round(style, 3))
        c3.metric("Final Score", round(score, 3))


# =========================================================
# MULTI FILE ANALYSIS
# =========================================================
st.divider()
st.header("📊 Multi-File Plagiarism Analysis")

multi_files = st.file_uploader(
    "Upload TWO OR MORE Python (.py) files",
    type=["py"],
    accept_multiple_files=True
)

if multi_files and len(multi_files) >= 2:
    if st.button("Generate Similarity Matrix"):

        st.session_state.codes_dict = {
            f.name: f.read().decode("utf-8", errors="ignore")
            for f in multi_files
        }

        files = list(st.session_state.codes_dict.keys())
        codes = list(st.session_state.codes_dict.values())
        n = len(files)

        sim_matrix = np.zeros((n, n))
        scores = {}

        with st.spinner("Computing similarity scores (one-time)..."):
            for i in range(n):
                for j in range(i + 1, n):
                    sim = final_similarity(codes[i], codes[j])[-1]

                    key = tuple(sorted([files[i], files[j]]))
                    scores[key] = sim

                    sim_matrix[i][j] = sim
                    sim_matrix[j][i] = sim

                sim_matrix[i][i] = 1.0

        st.session_state.sim_df = pd.DataFrame(
            sim_matrix, index=files, columns=files
        )

        st.session_state.sim_scores = scores


# =========================================================
# DISPLAY RESULTS
# =========================================================
if st.session_state.sim_df is not None:

    df = st.session_state.sim_df

    st.subheader("Similarity Matrix")
    st.dataframe(df.round(3), width="stretch")

    st.subheader("Heatmap")
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(df, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    st.pyplot(fig)

    # ---------------- CLUSTERING ----------------
    st.subheader("🧬 Clustering")

    cluster_threshold = st.slider(
        "Clustering Distance Threshold",
        0.05, 0.6, 0.3, 0.05
    )

    clusters, dendro_fig = perform_clustering(df, cluster_threshold)

    for cid, members in clusters.items():
        if len(members) > 1:
            st.warning(f"Cluster {cid}: {', '.join(members)}")

    st.pyplot(dendro_fig)

    # =================================================
    # EVALUATION METRICS (FAST)
    # =================================================
    st.divider()
    st.header("📈 Evaluation Metrics")

    eval_threshold = st.slider(
        "Similarity Threshold",
        0.1, 0.9, 0.4, 0.05
    )

    if st.button("Evaluate System"):
        metrics = evaluate_system(
            st.session_state.sim_scores,
            "data/ground_truth.csv",
            eval_threshold
        )

        c1, c2, c3 = st.columns(3)
        c1.metric("Precision", metrics["Precision"])
        c2.metric("Recall", metrics["Recall"])
        c3.metric("F1-score", metrics["F1-score"])

        st.subheader("Confusion Matrix")
        st.json(metrics["Confusion Matrix"])

    # =================================================
    # ROC + AUC (FAST)
    # =================================================
    st.divider()
    st.header("📉 ROC Curve & AUC")

    if st.button("Generate ROC Curve"):
        fpr, tpr, _ = roc_curve_data(
            st.session_state.sim_scores,
            "data/ground_truth.csv"
        )

        if fpr is None:
            st.error("No matching file pairs found in ground_truth.csv")
        else:
            roc_fig, auc_score = plot_roc_curve(fpr, tpr)
            st.pyplot(roc_fig)
            st.metric("AUC Score", round(auc_score, 3))
