from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests
import pandas as pd


def differential_expression(log_counts, design):
    group1 = design[design['condition'] == 'control'].index
    group2 = design[design['condition'] == 'treated'].index

    pvals, log2fc = [], []
    for gene in log_counts.index:
        x = log_counts.loc[gene, group1]
        y = log_counts.loc[gene, group2]
        pvals.append(ttest_ind(x, y).pvalue)
        log2fc.append(y.mean() - x.mean())

    df = pd.DataFrame({'gene': log_counts.index, 'pvalue': pvals, 'log2FC': log2fc})
    df['adj_pval'] = multipletests(df['pvalue'], method='fdr_bh')[1]
    return df
