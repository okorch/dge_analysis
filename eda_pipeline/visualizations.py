import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import numpy as np


def plot_pca(log_counts, design):
    pca = PCA(n_components=2)
    reduced = pca.fit_transform(log_counts.T)
    conditions = design.loc[log_counts.columns, 'condition']

    for cond in conditions.unique():
        idx = conditions == cond
        plt.scatter(reduced[idx, 0], reduced[idx, 1], label=cond)
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("PCA Plot")
    plt.legend()
    plt.savefig("outputs/pca.png")
    plt.close()


def plot_volcano(results):
    plt.scatter(results["log2FC"], -np.log10(results["pvalue"]), alpha=0.5)
    plt.axhline(-np.log10(0.05), color='red', linestyle='--')
    plt.xlabel("log2 Fold Change")
    plt.ylabel("-log10 p-value")
    plt.title("Volcano Plot")
    plt.savefig("outputs/volcano.png")
    plt.close()
