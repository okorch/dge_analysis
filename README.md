# Differential Gene Expression Analysis

With the advent of affordable high-throughput sequencing technologies, transcriptome data has become widely available across biological research. A **transcriptome** represents all mRNA transcripts within a sample and is typically expressed as a **raw count matrix**, where rows are genes, columns are samples, and each entry represents the number of reads mapped to a specific gene.

Despite its accessibility, differential gene expression (DGE) analysis often requires programming expertise, creating a barrier for many biologists. This project introduces a **user-friendly, command-line tool** that enables researchers to perform DGE analysis and explore results through **rich, interactive visualizations**, all without writing a single line of code.


## Description

The tool consists of 2 different parts:

1. **Exploratory Data Analysis**  \
   The first step is to explore the raw count data. The tool performs *normalization* using **CPM** (counts per million). It then conducts dimensionality reduction and visualizes the results using **PCA** and **UMAP** plots to evaluate the similarity or dissimilarity between sample groups (e.g., patients with two different cancer types).

2. **Differential Gene Expression Analysis and Results Visualization** \
   The tool supports DGE analysis for datasets both with and without replicates (with a minimum of one sample per group). It utilizes the **pyDESeq2** library to fit a **generalized linear model (GLM)**, perform statistical testing, and calculate both raw and adjusted *p-values* (FDR correction).

   The analysis results are presented through a rich interactive dashboard that includes:

   - **Volcano plots** for visualizing significantly expressed genes (with and without labels for the top 10 upregulated and downregulated genes)
   - **Heatmaps** for significantly up- and downregulated genes (based on raw counts)
   - **Gene interaction networks** for genes with more than 2-fold change and significant p-values
   - **MA plots** (mean expression vs. log2 fold change)
   - **Venn diagrams** for comparing DEGs across multiple groups
   - **Cluster dendrograms** to show sample similarity
   - **Interactive tables** for filtering and exploring DEGs

### User Input

1. **Count matrix file**: A CSV or TSV file with sample names as columns and gene IDs as rows.  
2. **Group mapping file**: A CSV file without headers containing two columns:

```
sample_name_1,control
sample_name_2,treatment
...
```

3. Control and treatment froup shuold be spesified when calling tool (see Usage section)

## Project architecture
```text
dge_pipeline/
│
├── data/                          # Input data (counts, design matrix)
│   ├── example_counts.csv
│   └── group_mapping.csv
│
├── results/                       # Output folder (plots, reports, tables)
│   └── (generated at runtime)
|
├── eda_pipeline/                 # Preparation and normalisation of the data
│   ├── __init__.py
│   ├── main.py                   # CLI entry point
│   ├── io.py                     # Data loading and saving
│   ├── normalisation.py          # data normalisation
│   ├── dimensionality.py         # PCA, UMAP
│   ├── visualizations.py         # Plotting (PCA, UMAP etc.)
│   ├── dashboard.py              # Dash interactive app
│   ├── utils.py                  # Helper functions
│   └── config.py                 # Default parameters, constants
│
├── dge_pipeline/                 # Core Python package
│   ├── __init__.py
│   ├── main.py                   # CLI entry point
│   ├── io.py                     # Data loading and saving
│   ├── eda.py                    # exploritary data analysis + data normalisation
│   ├── differential.py           # pyDESeq2 interface and stats
│   ├── visualizations.py         # Plotting (heatmap, volcano, MA, etc.)
│   ├── dashboard.py              # Dash interactive app
│   ├── utils.py                  # Helper functions if needed
│   └── config.py                 # Default parameters, constants
│
├── docker/                       # Docker-related files
│   └── Dockerfile
│
├── notebooks/                    # Example and exploratory notebooks
│   └── example_analysis.ipynb
│
├── tests/                        # Unit tests ( maybe )
│   └── test_differential.py
│
├── .gitignore
├── README.md
├── LICENSE
├── requirements.txt              # All necessary pip packages
├── setup.py                      # If packaging as installable module
└── gea_deseq.py                  # Wrapper script to call_

## Visuals
... in progress ...

## Installation
... in progress ...

## Usage
Preprosessing
``` linux
eda.py [path to the data file] [path to the file with groups mapping] [type of normalisation]
```

``` linux
gea_deseq.py [path to the data file] [path to the file with groups mapping] [name for control group] [name for reference group]
```

## Support
... in progress ...

## Contributing
... in progress ...

## Authors and acknowledgment
... in progress ...


## Project status
development