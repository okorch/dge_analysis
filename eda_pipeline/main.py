from config.config import OUTPUT_PATH

def main(count_matrix, design_matrix):

    # Check dimensions of count matrix
    # Clear not numerical columns in count matrix, indexed should be already set to Gene Names
    # Clear NaN in count matrix
    # Select only unique genes in count matrix

    # Check dimensions of design matrix
    # Check that design matrix align with count matrix

    info_messages = None # info about how many genes were not identified or met twice


    # Save files to OUTPUT_PATH

    return count_matrix, design_matrix, info_messages
