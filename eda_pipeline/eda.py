import pandas as pd
import umap.umap_ as umap
from sklearn.decomposition import PCA
from config.config import OUTPUT_PATH
from .normalisation import log_cpm

def check_data_dimensions(data):
    '''

    Args:
        data: count matrix

    Returns:
        data if correct dimension (genes x samples)
        transposed data if dimensions reversed

    '''
    n_genes = data.shape[0]
    n_samples = data.shape[1]

    if n_genes > n_samples:
        return data
    else:
        return data.T



def clear_not_numerical(data):
    '''

    Args:
        data: count matrix

    Returns:
        count matrix with only count columns.
        Drops all non-numerical columns for example Gene ID.
        Genes will be named later as index column was specified.

    '''

    only_numerical_columns = data.select_dtypes(exclude=['number']).columns
    clear_data = data.drop(only_numerical_columns, axis=1)

    return clear_data


def clear_nan(data):
    '''

    Args:
        data: count matrix

    Returns:
        clear_data: data without not-annotated genes. Some gene indexes may be nan values instead of names.
        Therefore, we keep only annotated genes.
        message: How many genes were annotated from all possible.

    '''

    data_copy = data.copy()
    n_all_genes = data_copy.index.size
    idx_nan = data_copy.index.notnull()
    n_of_nan = data_copy.index.isnull().sum()
    message = f'From all genes ({n_all_genes}), there are {n_of_nan} not-annotated genes in the data. They are going to be removed.'
    clear_data = data_copy[idx_nan]
    return clear_data, message


def select_unique_genes(data, keep='first'):
    '''
    Sometimes if user chooses gene name as a reference column for naming there might be issues when
    one gene has 2 splice variants with different gene ids but whey have the same gene name. That is
    why for some cases we might obtain not unique gene labels.

    Args:
        data: count matrix
        keep: 'first' will keep first entry of row met twice, 'second' will keep second entry

    Returns:
        deduped_data: cleared data with all gene labels unique

    '''

    data_copy = data.copy()
    unique_genes = data_copy.index.unique()

    n_unique_genes = unique_genes.size
    n_all_genes = data_copy.index.size

    message = f'From all annotated ({n_all_genes}), found {n_unique_genes} unique gene labels. Using only {keep} occurrence.'

    deduped_data = data_copy[~data_copy.index.duplicated(keep=keep)]
    return deduped_data, message



def check_compatibility(data, design_matrix):

    data_samples = set(data.columns) # can contain more samples that design matrix
    design_samples = set(design_matrix.index)

    if len(design_samples - data_samples) != 0: # If there are samples in design matrix but not in the data.
        samples = list(design_samples - data_samples)
        message = f"Design matrix contains samples not found in the data matrix: {samples}. Please ensure all samples in the design exist in the data."
        return False, None, message

    elif len(data_samples - design_samples) != 0:
        samples_to_delete = data_samples - design_samples
        message = f"The following samples are not specified in the design matrix and will be removed from further analysis: {samples_to_delete}."
        clean_data = delete_samples(data, samples_to_delete)

        return True, clean_data, message

    else:
        message = "Sample names in data and design matrix are compatible."
        return True, data, message

def delete_samples(data, samples_names):
    data_copy = data.copy()
    data_copy = data_copy.drop(columns=samples_names, errors='ignore')
    return data_copy


def perform_pca(data, design_matrix=None):
    '''
    Performs PCA dimensionality reduction on log-CPM normalized data.
    Optionally concatenates the result with a design matrix
    Args:
        data: count matrix unnormalised. Normalisation will be applied later.
        design_matrix:

    Returns:
        PCA plot

    '''

    # Log normalize the data
    log_cpm_data = log_cpm(data)

    # Transpose: rows = samples, columns = genes
    log_cpm_transposed = log_cpm_data.T

    # Perform PCA
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(log_cpm_transposed)

    pca_df = pd.DataFrame(pca_result, columns=['PC1', 'PC2'], index=log_cpm_transposed.index)

    # Optionally merge with design matrix
    if design_matrix is not None and not design_matrix.empty:
        shared_index = design_matrix.index.intersection(pca_df.index)
        if shared_index.empty:
            raise ValueError("No shared sample names between PCA result and design matrix.")
        design_matrix_aligned = design_matrix.loc[shared_index]
        result = pd.concat([pca_df.loc[shared_index], design_matrix_aligned], axis=1)
    else:
        result = pca_df

    return result

def perform_umap(data, design_matrix=None):
    '''
    Performs UMAP dimensionality reduction on log-CPM normalized data.
    Optionally concatenates the result with a design matrix.

    Args:
        data: count matrix unnormalised. Normalisation will be applied later.
        design_matrix:

    Returns:
        UMAP plot

    '''

    log_cpm_data = log_cpm(data)
    log_cpm_transposed = log_cpm_data.T

    # Fit UMAP
    umap_model = umap.UMAP(n_neighbors=15, min_dist=0.1, random_state=42)
    umap_result = umap_model.fit_transform(log_cpm_transposed)

    umap_df = pd.DataFrame(umap_result, columns=['UMAP1', 'UMAP2'], index=log_cpm_transposed.index)

    # Merge with design matrix if provided
    if design_matrix is not None and not design_matrix.empty:
        shared_index = design_matrix.index.intersection(umap_df.index)
        if shared_index.empty:
            raise ValueError("No shared sample names between UMAP result and design matrix.")
        design_matrix_aligned = design_matrix.loc[shared_index]
        result = pd.concat([umap_df.loc[shared_index], design_matrix_aligned], axis=1)
    else:
        result = umap_df

    return result


def calculate_library_sizes(count_matrix, design_matrix):
    '''

    Args:
        count_matrix:
        design_matrix:

    Returns:

    '''
    lib_sizes = count_matrix.sum(axis=0).sort_values(ascending=False)
    lib_df = pd.DataFrame({"Sample": lib_sizes.index, "Library Size": lib_sizes.values}, index=lib_sizes.index)
    lib_df = pd.concat([lib_df, design_matrix], axis=1)

    return lib_df


def save_csv_file(data, file_name):
    try:
        file_path = OUTPUT_PATH / file_name
        data.to_csv(file_path, sep=',')

    except Exception as e:
        message = f"[save_csv_file] Error occurred: {str(e)}"
        print(message)
        return None
