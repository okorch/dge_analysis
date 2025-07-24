from .eda import *

def main(count_matrix, design_matrix, contrast_column):
    info_messages = []
    # Check if data not empty
    if count_matrix.empty or design_matrix.empty:
        info_messages.append('Count or design matrix was provided as an empty dataset. Please check your data before loading.')
        return count_matrix, design_matrix, None, None, None, None, info_messages

    # Check data dimensions, transform if necessary
    count_matrix = check_data_dimensions(count_matrix)

    # Delete non-numerical columns
    count_matrix = clear_not_numerical(count_matrix)
    if count_matrix is None:
        info_messages.append("Error: Count matrix contains only non-numerical columns.")

    # Clean unannotated genes
    count_matrix, message_nan = clear_nan(count_matrix)
    info_messages.append(message_nan)

    # Select unique gene names / id
    count_matrix, message_genes = select_unique_genes(count_matrix)
    info_messages.append(message_genes)

    # Check if samples names in design and count matrix align
    compatibility, count_matrix, compatibility_message = check_compatibility(count_matrix, design_matrix)
    info_messages.append(compatibility_message)

    # If there are samples specified in the design matrix but not in count matrix stop the analysis
    if not compatibility:
        return count_matrix, design_matrix, None, None, None, None, info_messages
    else:

        design_matrix_plotting = design_matrix[[contrast_column]].rename(columns={contrast_column: "condition"})

        # ============ for visualisation =====================
        lib_df = calculate_library_sizes(count_matrix, design_matrix_plotting)
        pca_result = perform_pca(count_matrix, design_matrix_plotting)
        umap_result = perform_umap(count_matrix, design_matrix_plotting)
        log_data = log_cpm(count_matrix)
        corr_matrix = log_data.corr()

        # ============ saving files =====================
        files_to_save = [
                (count_matrix, "processed_count_matrix.csv"),
                (design_matrix, "processed_design_matrix.csv"),
                (pca_result, "pca_result.csv"),
                (umap_result, "umap_result.csv")
            ]

        for data, file_name in files_to_save:
            if data is not None:
                save_csv_file(data, file_name)

        return count_matrix, design_matrix, lib_df, pca_result, umap_result, corr_matrix, info_messages

