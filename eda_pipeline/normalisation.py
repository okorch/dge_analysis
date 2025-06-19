import numpy as np

def cpm(counts_df):
    """
    Normalize raw counts to Counts Per Million (CPM).

    Parameters:
        counts_df (pd.DataFrame): Raw count matrix (genes x samples)

    Returns:
        pd.DataFrame: CPM-normalized count matrix (genes x samples)
    """
    library_sizes = counts_df.sum(axis=0)

    # CPM = (counts / library_size) * 1e6
    cpm_df = counts_df.divide(library_sizes, axis=1) * 1e6

    return cpm_df


def log_cpm(counts_df):
    """
    log(CPM + 1)
    """
    cpm_data = cpm(counts_df)
    log_cpm_data = np.log2(cpm_data + 1)

    return log_cpm_data
