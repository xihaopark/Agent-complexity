---
name: pipeline-read-alignment-pangenome-finish
source_type: pipeline
workflow_id: read-alignment-pangenome-finish
workflow_dir: main/finish/workflow_candidates/snakemake-workflows__read-alignment-pangenome
generated_at: 2026-04-16T16:56:45Z
model: openrouter/openai/gpt-4o
files_used: 19
chars_used: 46391
generator: experiments/skills_pipeline/tools/generate_pipeline_skill.py
---

## Method

The pipeline is designed for aligning sequencing reads to both linear reference genomes and pangenome graphs, specifically using the vg giraffe tool for pangenome alignment. It processes raw sequencing data through several stages: trimming, mapping, and post-processing to produce final BAM and BAI files per sample. The workflow supports both traditional linear alignment using BWA and graph-based alignment using vg giraffe, with the latter being activated when pangenome alignment is specified in the configuration. The pipeline includes steps for primer trimming, UMI annotation, and duplicate removal, with options for calculating consensus reads from PCR duplicates. It is tailored for human genome analysis but can be adapted for other species by modifying the configuration files.

## Parameters

- `samples`: Path to the samples TSV file (e.g., `config/samples.tsv`).
- `units`: Path to the units TSV file (e.g., `config/units.tsv`).
- `ref/species`: Species name for reference genome (default: `homo_sapiens`).
- `ref/release`: Ensembl release version (default: `115`).
- `ref/build`: Genome build version (default: `GRCh38`).
- `ref/pangenome/activate`: Boolean to activate pangenome alignment (default: `true`).
- `ref/pangenome/source`: Pangenome source (default: `hprc`).
- `ref/pangenome/version`: Pangenome version (default: `v1.1`).
- `primers/trimming/primers_fa1`: Path to first primer fasta file (default: `""`).
- `primers/trimming/primers_fa2`: Path to second primer fasta file (default: `""`).
- `primers/trimming/tsv`: Path to primer TSV file (default: `config/primers.tsv`).
- `remove_duplicates/activate`: Boolean to activate duplicate removal (default: `true`).
- `calc_consensus_reads/activate`: Boolean to activate consensus read calculation (default: `false`).
- `params/fastp`: Additional parameters for fastp (default: `""`).
- `params/picard/MarkDuplicates`: Parameters for Picard MarkDuplicates (default: `--VALIDATION_STRINGENCY LENIENT`).
- `params/gatk/BaseRecalibrator`: Parameters for GATK BaseRecalibrator (default: `""`).
- `params/gatk/applyBQSR`: Parameters for GATK applyBQSR (default: `""`).

## Commands / Code Snippets

(No R code snippets visible in the pipeline source.)

## Notes for R-analysis agent

- The pipeline uses `vg giraffe` for pangenome alignment, which requires specific graph files (`.gbz`, `.hapl`) and kmer files (`.kff`). Ensure these resources are correctly configured.
- Primer trimming is conditional based on the presence of primer sequences in the configuration or sample sheet. Check the `primers_fa1`, `primers_fa2`, and `tsv` settings.
- UMI annotation is supported if `umi_read` and `umi_len` columns are present in the samples TSV file.
- The pipeline assumes the presence of a valid reference genome and known variants VCF file for recalibration steps. Verify the paths and formats of these files.
- Duplicate removal and consensus read calculation are optional and controlled via configuration flags. Adjust these settings based on the analysis requirements.
- Ensure the correct sequencing platform is specified in the samples TSV file, as this affects read group assignment during alignment.
