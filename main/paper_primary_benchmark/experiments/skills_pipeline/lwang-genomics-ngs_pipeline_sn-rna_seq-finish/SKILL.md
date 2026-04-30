---
name: pipeline-lwang-genomics-ngs_pipeline_sn-rna_seq-finish
source_type: pipeline
workflow_id: lwang-genomics-ngs_pipeline_sn-rna_seq-finish
workflow_dir: main/finish/workflow_candidates/lwang-genomics__NGS_pipeline_sn
generated_at: 2026-04-16T16:55:58Z
model: openrouter/openai/gpt-4o
files_used: 5
chars_used: 28339
generator: experiments/skills_pipeline/tools/generate_pipeline_skill.py
---

## Method
The pipeline is designed for the analysis of RNA-seq, ChIP-seq, and ATAC-seq data, providing a comprehensive workflow for each type of sequencing data. It supports both single-end and paired-end reads and integrates standard NGS processing steps such as trimming, alignment, filtering, quantification, peak calling, and quality control. For RNA-seq, the pipeline offers both traditional alignment-based quantification using STAR and pseudo-alignment using Salmon. ChIP-seq and ATAC-seq analyses involve alignment with BWA, followed by peak calling with MACS2, and generation of normalized signal tracks with deepTools. The pipeline is highly configurable via a centralized `config.yaml` file, allowing for flexibility in experimental design and computational resources.

## Parameters
- `genome.name`: Default is `hg38`; specifies the genome version.
- `genome.bwa_index`: Path to BWA index for genome alignment.
- `genome.star_index`: Path to STAR index for RNA-seq alignment.
- `genome.salmon_index`: Path to Salmon index for RNA-seq pseudo-alignment.
- `genome.chrom_sizes`: Path to chromosome sizes file.
- `genome.gtf`: Path to gene annotation GTF file.
- `peaktype`: Default is `narrow`; specifies peak type for ChIP-seq and ATAC-seq.
- `threads`: Default is `4`; number of threads to use per rule.
- `mapq`: Default is `5`; minimum mapping quality for filtering aligned reads.
- `keep_intermediate`: Default is `false`; whether to retain intermediate files.
- `skip_trimming`: Default is `false`; whether to skip the trimming step.
- `read_type`: Default is `paired`; specifies if reads are paired-end or single-end.
- `strandness`: Default is `forward`; strand-specific quantification for RNA-seq.
- `pseudo`: Default is `false`; flag to choose between STAR and Salmon for RNA-seq.

## Commands / Code Snippets
(No R code snippets visible in the pipeline source.)

## Notes for R-analysis agent
- The pipeline uses STAR for traditional RNA-seq alignment and Salmon for pseudo-alignment. Ensure the correct index paths are set in `config.yaml`.
- For RNA-seq, the pipeline generates BAM files, gene-level counts, and BigWig files. Ensure that the `strandness` parameter is correctly set to match the library preparation.
- ChIP-seq and ATAC-seq analyses involve peak calling with MACS2. The `peaktype` parameter should be set according to the experimental design (narrow or broad peaks).
- The pipeline requires several external tools, including FastQC, Trimmomatic, SAMtools, MultiQC, and others. Verify that these are installed and accessible.
- The `config.yaml` file centralizes configuration, making it crucial to verify paths and parameters before running the pipeline.
