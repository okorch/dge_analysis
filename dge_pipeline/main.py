from .dashboard import run_dashboard
import sys

def main():

    args = sys.argv

    if len(args[1:]) < 2:
        print("Usage: python dge_pipeline.py <tested_level> <control_level>")
        sys.exit(1)

    tested_level = args[1]
    control_level = args[2]
    contrasts = [tested_level, control_level]

    # ============= Run DGE analysis ==================

    summary_df = None

    # ============= Run dashboard =============
    run_dashboard(summary_df)

