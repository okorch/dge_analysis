# Differential Gene Expression Analysis

With the advent of affordable high-throughput sequencing technologies, transcriptome data has become widely available across biological research. A **transcriptome** represents all mRNA transcripts within a sample and is typically expressed as a **raw count matrix**, where rows are genes, columns are samples, and each entry represents the number of reads mapped to a specific gene.

Despite its accessibility, differential gene expression (DGE) analysis often requires programming expertise, creating a barrier for many biologists. This project introduces a **user-friendly, command-line tool** that enables researchers to perform DGE analysis and explore results through **rich, interactive visualizations**, all without writing a single line of code.


## Description

The tool consists of 2 different parts:

1. **Exploratory Data Analysis**  \
   The first step is to explore the raw count data. The tool performs *normalization* using **CPM** (counts per million). It then conducts dimensionality reduction and visualizes the results using **PCA** and **UMAP** plots to evaluate the similarity or dissimilarity between sample groups (e.g., patients with two different cancer types) as well as provides **correlation heatmap** and **sequencing sizes** for all samples in the data.

2. **Differential Gene Expression Analysis and Results Visualization** \
   The tool supports DGE analysis for datasets both with and without replicates (with a minimum of one sample per group). It utilizes the **pyDESeq2** library to fit a **generalized linear model (GLM)**, perform statistical testing, and calculate both raw and adjusted *p-values* (FDR correction).

   The analysis results are presented through a rich interactive dashboard that includes:

   - **Volcano plots** for visualizing significantly expressed genes
   - **MA plots** (mean expression vs. log2 fold change)
   - **P-Value distribution histograms** 

### User Input

1. **Count matrix file**  
   A CSV or TSV file containing gene count data.

2. **Group mapping file**  
   A CSV or TSV file specifying sample groups and factor levels.

More information about the input formats can be found within the app.

3. Control and treatment groups should be specified when calling tool (see Usage section)

## Project architecture
```text
dge_pipeline/
├── README.md
├── app.py
├── config
│   ├── __init__.py
│   └── config.py
├── dge_pipeline
│   ├── __main__.py
│   ├── dashboard.py
│   ├── dge.py
│   └── main.py
├── eda_pipeline
│   ├── __init__.py
│   ├── __main__.py
│   ├── dashboard.py
│   ├── eda.py
│   ├── main.py
│   └── normalisation.py
├── pages
│   ├── dge.py
│   ├── eda.py
│   ├── main_page.py
│   └── upload.py
└── requirements.txt
```

## Visuals
... in progress ...

## Installation
### Instalation from GitHub
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/dge_pipeline.git
cd dge_pipeline

# Create and activate a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run the application
python app.py

```

### Instalation from Docker
To run this app using Docker, make sure Docker is installed and currently running on your machine. Then follow these steps:
```bash
# Clone the repository
git clone https://github.com/yourname/dge_pipeline.git
cd dge_pipeline

# Build Docker image using provided config files
docker build -t dge_pipeline_app .

# Run image
docker run -it --rm -p 8050:8050 dge_pipeline_app
```

## Support
... in progress ...

## Contributing
... in progress ...

## Authors and Acknowledgments

- **Olesia Korchevaia** – [GitLab Profile](https://gitlab.gwdg.de/o.korchevaia)  
- **Irem Berna Güven** – [GitLab Profile](https://gitlab.gwdg.de/iremberna.gueven)  

---

Special thanks to the open source community.

Resources and tools used in this project:

- [PyDESeq2](https://pydeseq2.readthedocs.io/en/latest/auto_examples/index.html) – Gene expression analysis  
- [Plotly](https://plotly.com/) – Interactive plotting  
- [Dash](https://dash.plotly.com/) – Visual dashboards  
- [ChatGPT](https://chatgpt.com/) – Debugging and help with visual presentation

## Project status
development

## Similar projects 
[Visit BigOmics RNA-Seq Tool](https://bigomics.ch/rna-seq-data-analysis)
