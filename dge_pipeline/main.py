from .dge import *



def main(count_matrix, design_matrix, contrast=None, output_name="dge_results.csv", design_formula=None):
    try:
        print(" Preparing data...")
        count_matrix_t, design_matrix_prepped = prepare_dge_data(count_matrix, design_matrix)
        if count_matrix_t is None or design_matrix_prepped is None:
            raise ValueError(" Data preparation failed.")

        # automatic contrast
        for col in design_matrix_prepped.columns:
            design_matrix_prepped[col] = design_matrix_prepped[col].astype("category")

        # Auto-generate design formula if not provided
        if design_formula is None:
            design_formula = "~ " + " + ".join(design_matrix_prepped.columns)
            print(f"Auto design formula: {design_formula}")

        if contrast is None:
            main_var = design_matrix_prepped.columns[0]
            levels = design_matrix_prepped[main_var].cat.categories.tolist()
            if len(levels) == 2:
                contrast = [main_var, levels[1], levels[0]]
                print(f"Auto contrast: {contrast[1]} vs {contrast[2]} on '{main_var}'")
            else:
                raise ValueError(f"Multiple levels found in '{main_var}': {levels}. Please specify contrast explicitly.")

        # DGE analysis
        print(" Running PyDESeq2...")
        dge_result = run_pydeseq2(count_matrix_t, design_matrix_prepped, contrast, design_formula=design_formula)
        if dge_result is None:
            raise ValueError(" PyDESeq2 failed.")

        # Cleaning
        print(" Cleaning results...")
        dge_result_clean = clean_dge_df(dge_result)
        if dge_result_clean is None or dge_result_clean.empty:
            raise ValueError(" DGE result is empty after cleaning.")

        # Saving
        print(" Saving results...")
        save_csv_file(dge_result_clean, output_name)

        print(" DGE analysis complete.")
        return dge_result_clean

    except Exception as e:
        print(f"[main] Error: {e}")
        return None


