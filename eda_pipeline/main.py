from .eda import *
from config.config import  OUTPUT_PATH

def main(count_matrix, design_matrix):
    info_messages = []

    count_matrix = check_data_dimensions(count_matrix)
    if count_matrix is None:
        info_messages.append("Error: Count matrix dimensions are not compatible.")


    count_matrix = clear_not_numerical(count_matrix)
    if count_matrix is None:
        info_messages.append("Error: Count matrix contains non-numerical columns.")


    count_matrix, message_nan = clear_nan(count_matrix)
    info_messages.append(message_nan)


    count_matrix, message_genes = select_unique_genes(count_matrix)
    info_messages.append(message_genes)


    if design_matrix is None or design_matrix.empty:
        info_messages.append("Error: Design matrix is empty or not provided.")


    compatibility, compatibility_message = check_compatibility(count_matrix, design_matrix)
    info_messages.append(compatibility_message)

    if not compatibility:
        info_messages.append("Error: Design matrix is not compatible with count matrix.")

    # ============ for visualisation =====================
    lib_df = calculate_library_sizes(count_matrix, design_matrix)
    pca_result = perform_pca(count_matrix, design_matrix)
    umap_result = perform_umap(count_matrix, design_matrix)
    log_data = log_cpm(count_matrix)
    corr_matrix = log_data.corr()

    # ============ saving files =====================
    if len(info_messages) == 0:
        files_to_save = [
            (count_matrix, "processed_count_matrix.csv"),
            (design_matrix, "processed_design_matrix.csv"),
            (pca_result, "pca_result.csv"),
            (umap_result, "umap_result.csv")
        ]


        for data, file_name in files_to_save:
            if data is not None:
                save_csv_file(data, file_name)

        info_messages.append(f"All results saved to {OUTPUT_PATH}")

    return count_matrix, design_matrix, lib_df, pca_result, umap_result, corr_matrix, info_messages

