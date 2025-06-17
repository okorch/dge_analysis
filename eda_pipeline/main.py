from eda import perform_pca, perform_umap, check_data_dimensions, clear_not_numerical, clear_nan, select_unique_genes, check_compatibility
import os
from config import DATA_PATH, OUTPUT_PATH

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



    pca_result = perform_pca(count_matrix, design_matrix)
    umap_result = perform_umap(count_matrix, design_matrix)


    if len(info_messages) == 0:
        count_matrix_path = os.path.join(OUTPUT_PATH, "processed_count_matrix.csv")
        design_matrix_path = os.path.join(OUTPUT_PATH, "processed_design_matrix.csv")
        pca_path = os.path.join(OUTPUT_PATH, "pca_result.csv")
        umap_path = os.path.join(OUTPUT_PATH, "umap_result.csv")


        count_matrix.to_csv(count_matrix_path)
        design_matrix.to_csv(design_matrix_path)


        if pca_result is not None:
            pca_result.to_csv(pca_path)
        if umap_result is not None:
            umap_result.to_csv(umap_path)

        info_messages.append(
            f"Processed count matrix and design matrix saved to {count_matrix_path} and {design_matrix_path}")
        info_messages.append(f"PCA results saved to {pca_path}")
        info_messages.append(f"UMAP results saved to {umap_path}")

    return count_matrix, design_matrix, pca_result, umap_result, info_messages

