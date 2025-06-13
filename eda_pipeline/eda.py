import pandas as pd
import umap.umap_ as umap
from sklearn.decomposition import PCA

from config import DATA_PATH, OUTPUT_PATH
from normalisation import log_cpm



def read_count_matrix(file_name, gene_names_col):
    try:
        file_path = DATA_PATH / file_name

        if file_path.suffix == ".tsv":
            separator = '\t'
        else:
            separator = ','

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        df = pd.read_csv(file_path, sep=separator)
        df.set_index(df.columns[gene_names_col], inplace=True)
        df = df.drop(df.columns[gene_names_col], axis=1)
        return df

    except Exception as e:
        message = f"[read_count_matrix] Error occurred: {str(e)}"
        print(message)
        return None


def read_design_matrix(file_name):
    try:
        file_path = DATA_PATH / file_name

        if not file_path.exists():
            raise FileNotFoundError(f"Design matrix file not found: {file_path}")

        design_matrix = pd.read_csv(
            file_path,
            header=None,
            names=['condition'],
            index_col=0
        )
        return design_matrix
    except Exception as e:
        message = f"[read_design_matrix] Error occurred: {str(e)}"
        print(message)
        return None


def check_data_dimensions(data):
    try:
        n_genes = data.shape[0]
        n_samples = data.shape[1]

        if n_genes > n_samples:
            return data
        else:
            return data.T
    except Exception as e:
        message = f"[check_data_dimensions] Error occurred: {str(e)}"
        print(message)
        return None


def clear_not_numerical(data):
    try:
        only_numerical_columns = data.select_dtypes(exclude=['number']).columns
        clear_data = data.drop(only_numerical_columns, axis=1)
        return clear_data
    except Exception as e:
        message = f"[clear_not_numerical] Error occurred: {str(e)}"
        print(message)
        return None

def clear_nan(data):
    try:
        data_copy = data.copy()
        idx_nan = data_copy.index.notnull()
        n_of_nan = data_copy.index.isnull().sum()
        message = f'There are {n_of_nan} unannotated genes in the data.'
        clear_data = data_copy[idx_nan]
        return clear_data, message
    except Exception as e:
        message = f"[clear_nan] Error occurred: {str(e)}"
        print(message)
        return None, message

def select_unique_genes(data, keep='first'):
    try:
        '''
        keep = ('first', 'last')
        '''
        data_copy = data.copy()
        unique_genes = data_copy.index.unique()

        n_unique_genes = unique_genes.size
        n_all_genes = data_copy.index.size

        message = f'From all genes ({n_all_genes}), found {n_unique_genes} unique genes. Using only {keep} occurrence.'

        deduped_data = data_copy[~data_copy.index.duplicated(keep=keep)]
        return deduped_data, message

    except Exception as e:
        message = f"[select_unique_genes] Error occurred: {str(e)}"
        print(message)
        return None, message


def check_compatibility(data, design_matrix):
    try:
        data_samples = set(data.columns)
        design_samples = set(design_matrix.index)

        if not data_samples == design_samples:
            missing_in_design = data_samples - design_samples
            missing_in_data = design_samples - data_samples

            message_parts = []
            if missing_in_design:
                message_parts.append(f"Samples in data but not in design: {missing_in_design}")
            if missing_in_data:
                message_parts.append(f"Samples in design but not in data: {missing_in_data}")

            full_message = "Incompatible sample names:\n" + "\n".join(message_parts)
            raise ValueError(full_message)

        message = "Sample names in data and design matrix are compatible."
        return True, message

    except Exception as e:
        message = f"[check_compatibility] Error occurred: {str(e)}"
        print(message)
        return False, message


def delete_samples(data, design_matrix, samples_names):
    try:
        data_copy = data.copy()
        design_matrix_copy = design_matrix.copy()

        data_copy = data_copy.drop(columns=samples_names, errors='ignore')
        design_matrix_copy = design_matrix_copy.drop(index=samples_names, errors='ignore')

        message = f"Deleted {len(samples_names)} samples from data and design matrix (ignored missing)."
        return data_copy, design_matrix_copy, message

    except Exception as e:
        message = f"[delete_samples] Error occurred: {str(e)}"
        print(message)
        return None, None, message

def perform_pca(data, design_matrix=None):
    try:
        # Log normalize the data
        log_cpm_data = log_cpm(data)

        # Transpose: rows = samples, columns = genes
        log_cpm_transposed = log_cpm_data.T

        # Perform PCA
        pca = PCA(n_components=2)
        pca_result = pca.fit_transform(log_cpm_transposed)

        # Create DataFrame for PCA results
        pca_df = pd.DataFrame(pca_result, columns=['PC1', 'PC2'], index=log_cpm_transposed.index)

        # Optionally merge with design matrix
        if design_matrix is not None and not design_matrix.empty:
            # Align indices before merging
            shared_index = design_matrix.index.intersection(pca_df.index)
            if shared_index.empty:
                raise ValueError("No shared sample names between PCA result and design matrix.")
            design_matrix_aligned = design_matrix.loc[shared_index]
            result = pd.concat([pca_df.loc[shared_index], design_matrix_aligned], axis=1)
        else:
            result = pca_df

        return result

    except Exception as e:
        message = f"[perform_pca] Error occurred: {str(e)}"
        print(message)
        return None


def perform_umap(data, design_matrix=None):
    try:
        """
        Performs UMAP dimensionality reduction on log-CPM normalized data.
        Optionally concatenates the result with a design matrix.
        """
        log_cpm_data = log_cpm(data)
        log_cpm_transposed = log_cpm_data.T

        # Fit UMAP
        umap_model = umap.UMAP(n_neighbors=15, min_dist=0.1, random_state=42)
        umap_result = umap_model.fit_transform(log_cpm_transposed)

        # Create DataFrame
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

    except Exception as e:
        message = f"[perform_umap] Error occurred: {str(e)}"
        print(message)
        return None


def save_csv_file(data, file_name):
    try:
        file_path = OUTPUT_PATH / file_name
        data.to_csv(file_path, sep=',')


    except Exception as e:
        message = f"[save_csv_file] Error occurred: {str(e)}"
        print(message)
        return None
