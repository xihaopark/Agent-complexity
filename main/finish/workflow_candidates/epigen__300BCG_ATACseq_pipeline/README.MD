# 300BCG ATAC-seq pipeline

## Part 1. Download and parse references

### Genome
1. Create a references/hg38 subfolder
2. Download and g-unzip the FASTA file from the encode project in the references/hg38 folder (https://www.encodeproject.org/files/GRCh38_no_alt_analysis_set_GCA_000001405.15/@@download/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta.gz)
3. Within the hg38 subfolder create the bowtie2 index: `bowtie2-build GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta GRCh38_no_alt_analysis_set_GCA_000001405.15`
4. Within the references subfolder download and g-unzip the gencode annotations: https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_31/gencode.v31.basic.annotation.gtf.gz

### Chrom sizes
1. In the references folder, create a fai index using `samtools faidx hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta`
2. Extract the chromosome sizes `cut -f1,2 hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta.fai >  hg38.chrom.sizes`

### Obtain the regulatory build files
1. In the references folder, download the regulatory build gff (ftp://ftp.ensembl.org/pub/release-98/regulation/homo_sapiens/homo_sapiens.GRCh38.Regulatory_Build.regulatory_features.20190329.gff.gz)
2. Parse the regulatory build file `python pipeline/parse_reg_build_file.py references/homo_sapiens.GRCh38.Regulatory_Build.regulatory_features.20190329.gff.gz references/hg38.chrom.sizes`


### Other files
1. In the references folder, download and g-unzip the hg38_gencode_tss_unique.bed file from the official ENCODE repository https://storage.googleapis.com/encode-pipeline-genome-data/hg38/ataqc/hg38_gencode_tss_unique.bed.gz
2. In the references folder, download and g-unzip the hg38.blacklist.bed file from the official ENCODE repository https://storage.googleapis.com/encode-pipeline-genome-data/hg38/hg38.blacklist.bed.gz

### Configuration
Edit the paths in the pipeline/atac/atacseq.yaml file to point to the newly created reference files and to the location of the spp script


## Part 2. Setup environment

1. Create the conda environments
```
conda env create python=2.7 -f ./pipeline/env_config/pipeline_env.yml
conda env create -f ./notebooks/notebooks_env.yml
```

2.  On the LUSTRE cluster load the relevant modules and activate the environment
```
source ./pipeline/env_config/activate_env.sh
conda activate bcg_notebooks
```

3. Start Jupyter lab and check the connection string in the jupyterlab.err logfile
```
sbatch notebooks/jupyter_lab.sh
```

## Part 3. Run the pipeline

1. Run the notebooks/0000.01-Prepare_pipeline_input notebook.ipynb to generate the annotations to run the pipeline
2. Activate the pipeline environemnt `conda activate bcg_pipeline`
3. Run the pipeline for all samples `looper run ./pipeline/bcg_pipeline.yaml`
4. Summarize the results for all samples `looper summarize ./pipeline/bcg_pipeline.yaml`


## Part 4. Postprocessing
The notebooks bust be run within jupyter lab launcehd within the "bcg_notebooks" environment.

1. Create the complete_metadata file using the "0001.01-Create_Annotations" notebook
2. Run QC to set the QC flag using the "0001.02-QC.stats" notebook
3. Run Quantification (count matrix), Binary Quantification (binary matrix) and median signal tracks (bigWig) using the 0001.03-Quantification notebook
4. To create the configuration files for the peak annotation software UROPA use the 0001.04.a-Features_analysis notebook
5. Run the peak annotation software jobs: `ls data/quantification/characterization_ALL_V4/*sub|while read script;do sbatch $script;done`
6. To combine the results of peak annotation use the 0001.04.b-Features_analysis notebook
