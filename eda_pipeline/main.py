import sys

from eda_pipeline.dashboard import run_dashboard


def main():

    args = sys.argv

    if len(args[1:]) < 3:
        print("Usage: python eda_pipeline.py <design_matrix_path> <gene_names_col>")
        sys.exit(1)

    file_path = args[1]
    design_matrix_path = args[2]
    gene_names_col = args[3]

    print(f"Running with design matrix: {design_matrix_path}")
    print(f"Gene name column: {gene_names_col}")

    # ================= Perform EDA =================
    count_matrix = None
    design_matrix = None
    info_messages = [
        f'File name: {file_path}',
        f"Running with design matrix: {design_matrix_path}",
        f"Gene name column: {gene_names_col}",
        #message1,
        #message2 ...
    ]
    # ================= Save results =================
    # ================= Run dashboard =================
    run_dashboard(count_matrix, design_matrix, info_messages)