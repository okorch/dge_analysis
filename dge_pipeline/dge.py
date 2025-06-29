import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats
from pydeseq2.default_inference import DefaultInference
from config.config import OUTPUT_PATH

def prepare_dge_data(count_matrix, design_matrix):
    try:
        transposed_count_matrix = count_matrix.T
        desired_order = transposed_count_matrix.index
        design_matrix = design_matrix.loc[desired_order]
        return transposed_count_matrix, design_matrix
    except Exception as e:
        print(f"[prepare_dge_data] Error: {e}")
        return None, None

def run_pydeseq2(count_matrix, design_matrix, contrasts, design_formula=None):

    try:
        if design_formula is None:
            design_formula = "~ " + " + ".join(design_matrix.columns)

        if len(contrasts) != 3:
            raise ValueError("Contrasts must be a list like: [variable, level_1, level_2]")

        contrast = contrasts  # [variable, level1, level2]
        contrast_var = contrast[0]

        if contrast_var not in design_matrix.columns:
            raise ValueError(f"Contrast variable '{contrast_var}' not found in design matrix.")

        inference = DefaultInference(n_cpus=8)

        # Ensure categorical
        for col in design_matrix.columns:
            design_matrix[col] = design_matrix[col].astype("category")

        dds = DeseqDataSet(
            counts=count_matrix,
            metadata=design_matrix,
            design=design_formula,
            refit_cooks=True,
            inference=inference,
        )
        dds.deseq2()

        ds = DeseqStats(
            dds,
            contrast=contrast,
            inference=inference,
            cooks_filter=True,
            independent_filter=True,
        )
        ds.summary()
        return ds.results_df

    except Exception as e:
        print(f"[run_pydeseq2] Error: {e}")
        return None

def clean_dge_df(df):
    try:
        df = df.copy()
        df = df.dropna(subset=["log2FoldChange", "pvalue", "padj", "baseMean"])
        df = df.replace([float("inf"), float("-inf")], pd.NA)
        df = df.dropna()
        df["log2FoldChange"] = pd.to_numeric(df["log2FoldChange"], errors="coerce")
        df["padj"] = pd.to_numeric(df["padj"], errors="coerce")
        df["pvalue"] = pd.to_numeric(df["pvalue"], errors="coerce")
        df["baseMean"] = pd.to_numeric(df["baseMean"], errors="coerce")
        return df
    except Exception as e:
        print(f"[clean_dge_df] Error: {e}")
        return None

def save_csv_file(data, file_name):
    try:
        file_path = OUTPUT_PATH / file_name
        data.to_csv(file_path, sep=',')
    except Exception as e:
        print(f"[save_csv_file] Error: {e}")
