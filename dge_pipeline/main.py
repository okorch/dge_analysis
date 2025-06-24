from config.config import OUTPUT_PATH
import pandas as pd
from .dge import *



def main(count_matrix, design_matrix, contrast=None, output_name="dge_results.csv"):
    try:
        print(" Preparing data...")
        count_matrix_t, design_matrix_prepped = prepare_dge_data(count_matrix, design_matrix)
        if count_matrix_t is None or design_matrix_prepped is None:
            raise ValueError(" Data preparation failed.")

        # automatic contrast
        conditions = design_matrix_prepped['condition'].unique().tolist()
        print(f" Detected groups: {conditions}")

        if contrast is None:
            if len(conditions) == 2:
                contrast = (conditions[1], conditions[0])  # varsayılan olarak sonuncu - ilk
                print(f"⚙️ Auto contrast: {contrast[0]} vs {contrast[1]}")
            else:
                raise ValueError(f" Multiple condition levels found: {conditions}. Please specify `contrast`.")

        elif contrast[0] not in conditions or contrast[1] not in conditions:
            raise ValueError(f" Invalid contrast: {contrast}. Available groups: {conditions}")

        # DGE analysis
        print(" Running PyDESeq2...")
        dge_result = run_pydeseq2(count_matrix_t, design_matrix_prepped, list(contrast))
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



#def main(count_matrix, design_matrix, tested_level, control_level):

    #contrasts = [tested_level, control_level]

    # Run DGE and clean result from NaN

    # save files to OUTPUT_PATH


    #clear_summary_df = None

   # return clear_summary_df


