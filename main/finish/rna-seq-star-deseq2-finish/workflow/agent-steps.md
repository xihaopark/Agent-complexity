# rna-seq-star-deseq2 LLM Execution Spec

## Purpose

- Use this file as a prompt-oriented execution contract for the `rna-seq-star-deseq2` workflow.
- Treat `workflow/Snakefile` as the source of truth for actual execution.
- Treat this file as the control layer that tells an LLM what to do, what not to do, and how to decide that a step is complete.

## Operating Rules

- Run steps in numeric order.
- Do not start the next step before the current step passes validation.
- Write one manifest per completed step.
- If a step fails validation, stop and report the failure point instead of improvising the next step.
- Do not silently change config values, sample metadata, or DESeq2 design terms.
- Use sample-unit fanout only where explicitly allowed.
- Use contrast fanout only where explicitly allowed.

## Shared Terms

- Run scope: one `config.yaml`, one `samples.tsv`, and one `units.tsv`
- Sample-unit: execution grain for reads, alignment, and QC
- Sample: execution grain for count aggregation and sample-level metadata
- Contrast: execution grain for DESeq2 result generation

## Manifest Mapping

- Step 1 → `analysis_manifest`
- Step 2 → `reads_manifest`
- Step 3 → `reference_manifest`
- Step 4 → `prepared_reads_manifest`
- Step 5 → `alignment_manifest`
- Step 6 → `qc_manifest`
- Step 7 → `count_matrix_manifest`
- Step 8 → `deseq2_init_manifest`
- Step 9 → `deseq2_results_manifest`
- Step 10 → `delivery_manifest`

## Common Manifest Requirements

- Every manifest must satisfy `agent-orchestration/manifest-schema.yaml`.
- Every manifest must set `workflow_id` to `rna-seq-star-deseq2`.
- Every manifest must set `step_id` to the current step identifier.
- Every manifest must include `summary`, `artifacts`, `validations`, and `errors`.
- Every successful step must record at least one produced or verified artifact.

## Step 1

- **Step ID:** `step-1-parse-config`
- **Manifest type:** `analysis_manifest`
- **Name:** Parse analysis configuration
- **Objective:** load workflow configuration and normalize all run-level metadata
- **Inputs:** `config/config.yaml`, `config/samples.tsv`, `config/units.tsv`
- **Allowed actions:** parse reference settings, trimming toggle, PCA toggle, variables of interest, batch effects, contrasts, and sample-unit mapping
- **Forbidden actions:** download references, inspect reads, run alignment
- **Expected outputs:** `analysis_manifest.json`
- **Manifest must record:** run context, contrasts, design variables, trimming and PCA settings
- **Validation checks:** all referenced columns exist; all samples in `units.tsv` exist in `samples.tsv`; every contrast is resolvable
- **On failure:** stop the run and report the inconsistent metadata field
- **Completion signal:** `analysis_manifest.json` exists and lists all contrasts
- **Next step:** Step 2

## Step 2

- **Step ID:** `step-2-resolve-reads`
- **Manifest type:** `reads_manifest`
- **Name:** Resolve raw read sources
- **Objective:** determine the concrete raw input source for each `sample-unit`
- **Inputs:** `analysis_manifest.json`
- **Allowed actions:** classify each unit as local FASTQ or SRA source; determine single-end or paired-end; capture strandedness and fastp parameters
- **Forbidden actions:** download references, run trimming, run alignment
- **Expected outputs:** `reads_manifest.json`
- **Manifest must record:** one entry per sample-unit, source type, pairedness, strandedness, trimming parameters
- **Validation checks:** every unit resolves to exactly one legal source; paired-end units provide both mates
- **Parallelism:** by `sample-unit`
- **On failure:** retry transient source inspection once, then stop
- **Completion signal:** `reads_manifest.json` covers all sample-units
- **Next step:** Step 3

## Step 3

- **Step ID:** `step-3-prepare-reference`
- **Manifest type:** `reference_manifest`
- **Name:** Prepare reference resources
- **Objective:** materialize shared reference assets required by alignment and QC
- **Inputs:** `analysis_manifest.json`
- **Allowed actions:** download genome FASTA, download GTF annotation, build STAR index
- **Forbidden actions:** process reads, run alignment, build count matrices
- **Expected outputs:** `reference_manifest.json`
- **Manifest must record:** genome path, annotation path, STAR index path, species-release-build tuple
- **Validation checks:** reference files exist; STAR index directory is complete; species-release-build tuple matches requested config
- **On failure:** retry failed downloads, then stop if index build is incomplete
- **Completion signal:** `reference_manifest.json` lists all resolved reference paths
- **Next step:** Step 4

## Step 4

- **Step ID:** `step-4-prepare-reads`
- **Manifest type:** `prepared_reads_manifest`
- **Name:** Prepare reads
- **Objective:** transform raw read sources into alignment-ready FASTQ inputs
- **Inputs:** `reads_manifest.json`, `reference_manifest.json`
- **Allowed actions:** download SRA data when needed; run fastp when trimming is enabled; otherwise register raw FASTQ as effective input
- **Forbidden actions:** run STAR, run QC, run DESeq2
- **Expected outputs:** `prepared_reads_manifest.json`
- **Manifest must record:** effective FASTQ paths, per-unit preprocessing status, raw-versus-trimmed source decision
- **Validation checks:** every sample-unit has one resolved effective FASTQ payload; trimming outputs are non-empty when trimming is enabled
- **Parallelism:** by `sample-unit`
- **On failure:** retry per unit and stop before alignment if any required unit remains unresolved
- **Completion signal:** `prepared_reads_manifest.json` exists and matches the expected inventory
- **Next step:** Step 5

## Step 5

- **Step ID:** `step-5-align`
- **Manifest type:** `alignment_manifest`
- **Name:** Run STAR alignment
- **Objective:** align every prepared unit to the reference genome and collect alignment-side outputs
- **Inputs:** `prepared_reads_manifest.json`, `reference_manifest.json`
- **Allowed actions:** run STAR per sample-unit and capture BAM, gene counts, and alignment logs
- **Forbidden actions:** aggregate counts across samples, run DESeq2
- **Expected outputs:** `alignment_manifest.json`
- **Manifest must record:** per-unit BAM path, gene-count path, STAR logs, alignment completion status
- **Validation checks:** every unit produces BAM, `ReadsPerGene.out.tab`, and STAR logs; sample-unit count matches the prepared read manifest
- **Parallelism:** by `sample-unit`
- **On failure:** retry failed units and stop if any required unit remains missing
- **Completion signal:** `alignment_manifest.json` lists all aligned units
- **Next step:** Step 6

## Step 6

- **Step ID:** `step-6-run-qc`
- **Manifest type:** `qc_manifest`
- **Name:** Run RNA-seq QC
- **Objective:** compute post-alignment QC and aggregate it into a release gate
- **Inputs:** `alignment_manifest.json`, `reference_manifest.json`
- **Allowed actions:** run RSeQC tasks on each aligned unit and generate a MultiQC report
- **Forbidden actions:** aggregate counts before QC release passes
- **Expected outputs:** `qc_manifest.json`
- **Manifest must record:** per-unit QC outputs, MultiQC path, QC coverage summary
- **Validation checks:** each unit has expected QC artifacts; `multiqc_report.html` exists; QC summary table covers all aligned units
- **Parallelism:** by `sample-unit` with a final fan-in for MultiQC
- **On failure:** allow unit-level retries, but stop before count aggregation if MultiQC cannot be produced
- **Completion signal:** `qc_manifest.json` exists and includes the final MultiQC report
- **Next step:** Step 7

## Step 7

- **Step ID:** `step-7-build-count-matrix`
- **Manifest type:** `count_matrix_manifest`
- **Name:** Build sample-level count matrix
- **Objective:** convert STAR gene count outputs into one sample-level count matrix
- **Inputs:** `alignment_manifest.json`, `analysis_manifest.json`
- **Allowed actions:** select the correct STAR count column based on strandedness and aggregate technical replicates from unit level to sample level
- **Forbidden actions:** initialize DESeq2 before matrix validation succeeds
- **Expected outputs:** `count_matrix_manifest.json`
- **Manifest must record:** count matrix path, sample columns, strandedness choice, replicate aggregation status
- **Validation checks:** output matrix columns match the expected sample list; row count is non-zero; no sample is missing after technical replicate aggregation
- **On failure:** stop if any required unit count file is absent or if sample columns do not match metadata
- **Completion signal:** `count_matrix_manifest.json` exists and lists the count matrix artifact
- **Next step:** Step 8

## Step 8

- **Step ID:** `step-8-init-deseq2`
- **Manifest type:** `deseq2_init_manifest`
- **Name:** Initialize DESeq2 state
- **Objective:** establish the shared DESeq2 object for all downstream contrasts
- **Inputs:** `count_matrix_manifest.json`, `analysis_manifest.json`
- **Allowed actions:** create `all.rds`, apply batch effects and model design, and generate normalized counts
- **Forbidden actions:** run per-contrast results before shared object validation succeeds
- **Expected outputs:** `deseq2_init_manifest.json`
- **Manifest must record:** `all.rds`, normalized count matrix, design formula, batch-effect usage
- **Validation checks:** `all.rds` exists; normalized count matrix exists; design formula is recorded and references only known metadata columns
- **On failure:** stop if the model cannot be instantiated or if design terms are invalid
- **Completion signal:** `deseq2_init_manifest.json` exists and lists the initialized shared state
- **Next step:** Step 9

## Step 9

- **Step ID:** `step-9-run-statistics`
- **Manifest type:** `deseq2_results_manifest`
- **Name:** Generate statistical results
- **Objective:** produce contrast-level differential expression results and optional PCA outputs
- **Inputs:** `deseq2_init_manifest.json`, `analysis_manifest.json`
- **Allowed actions:** run DESeq2 per contrast; emit differential expression tables and MA plots; emit PCA figures when enabled
- **Forbidden actions:** assemble delivery artifacts before all required contrasts finish
- **Expected outputs:** `deseq2_results_manifest.json`
- **Manifest must record:** one entry per contrast, DE result paths, MA plots, optional PCA outputs
- **Validation checks:** each requested contrast produces a result table; optional PCA outputs match the requested variables
- **Parallelism:** by `contrast`
- **On failure:** retry failed contrasts independently and stop final delivery until all required contrasts succeed
- **Completion signal:** `deseq2_results_manifest.json` lists all required contrasts
- **Next step:** Step 10

## Step 10

- **Step ID:** `step-10-deliver`
- **Manifest type:** `delivery_manifest`
- **Name:** Annotate and deliver final artifacts
- **Objective:** convert technical outputs into delivery-ready result packages
- **Inputs:** `deseq2_results_manifest.json`, `qc_manifest.json`, `count_matrix_manifest.json`
- **Allowed actions:** convert counts, normalized counts, and diffexp outputs to symbol-level tables; assemble final deliverable inventory
- **Forbidden actions:** silently skip required tables or plots
- **Expected outputs:** `delivery_manifest.json`
- **Manifest must record:** diffexp tables, normalized counts, counts, MultiQC report, optional PCA outputs, symbol-level tables
- **Validation checks:** final deliverables include diffexp tables, normalized counts, counts, MultiQC report, and optional PCA plots; symbol-level files exist for every required table
- **Parallelism:** by result table family
- **On failure:** retry annotation tasks and stop if required delivery artifacts remain incomplete
- **Completion signal:** `delivery_manifest.json` exists and enumerates the final deliverables
- **End state:** workflow execution is complete
