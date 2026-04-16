# zarp LLM Execution Spec

## Purpose

- Use this file as a prompt-oriented execution contract for the `zarp` workflow.
- Treat `workflow/Snakefile` as the source of truth for actual execution.
- Treat this file as the control layer that tells an LLM what to do, what not to do, and how to decide that a step is complete.

## Operating Rules

- Run steps in numeric order.
- Do not start the next step before the current step passes validation.
- Write one manifest per completed step.
- If a step fails validation, stop and report the failure point instead of improvising the next step.
- Do not silently switch execution profile, sample metadata, or indexing strategy.
- Treat SRA download and HTSinfer as optional pre-main workflow stages.
- Use sample fanout only where explicitly allowed.

## Shared Terms

- Run scope: one config file, one sample sheet, and one selected execution profile
- Sample: execution grain for trimming, alignment, quantification, and QC
- Mode: single-end or paired-end processing path
- Profile: local-conda, local-apptainer, slurm-conda, or slurm-apptainer

## Manifest Mapping

- Step 1 → `context_manifest`
- Step 2 → `analysis_manifest`
- Step 3 → `reference_manifest`
- Step 4 → `input_manifest`
- Step 5 → `prepared_reads_manifest`
- Step 6 → `alignment_manifest`
- Step 7 → `quant_manifest`
- Step 8 → `qc_manifest`
- Step 9 → `delivery_manifest`
- Step 10 → `verification_manifest`

## Common Manifest Requirements

- Every manifest must satisfy `agent-orchestration/manifest-schema.yaml`.
- Every manifest must set `workflow_id` to `zarp`.
- Every manifest must set `step_id` to the current step identifier.
- Every manifest must include `summary`, `artifacts`, `validations`, and `errors`.
- Every successful step must record at least one produced or verified artifact.

## Step 1

- **Step ID:** `step-1-resolve-context`
- **Manifest type:** `context_manifest`
- **Name:** Resolve execution context
- **Objective:** determine profile, config source, and execution mode before workflow expansion
- **Inputs:** `config.yaml`, selected profile config, optional `rule_config.yaml`
- **Allowed actions:** resolve active profile, output directory, log directory, rule overrides, and selected execution environment
- **Forbidden actions:** build indexes, copy reads, run alignment
- **Expected outputs:** `context_manifest.json`
- **Manifest must record:** profile, active config, log directory, output directory, optional rule override status
- **Validation checks:** profile exists; config file exists; required global output and log paths are resolvable
- **On failure:** stop and report the unresolved profile or config path
- **Completion signal:** `context_manifest.json` exists and identifies one active execution context
- **Next step:** Step 2

## Step 2

- **Step ID:** `step-2-parse-samples`
- **Manifest type:** `analysis_manifest`
- **Name:** Parse configuration and sample metadata
- **Objective:** build the run-level biological and technical inventory
- **Inputs:** `context_manifest.json`, config file, samples table
- **Allowed actions:** validate config schema, validate sample-sheet columns, resolve organism, seqmode, lanes, and enabled tools
- **Forbidden actions:** create indexes, preprocess reads, run quantification
- **Expected outputs:** `analysis_manifest.json`
- **Manifest must record:** all samples, seqmode, organism, enabled analysis branches, lane-merging expectations
- **Validation checks:** config schema passes; required sample-sheet columns exist; seqmode is legal for each sample
- **On failure:** stop and report the exact config or sample-sheet mismatch
- **Completion signal:** `analysis_manifest.json` exists and lists all samples with execution modes
- **Next step:** Step 3

## Step 3

- **Step ID:** `step-3-build-indexes`
- **Manifest type:** `reference_manifest`
- **Name:** Build public and derived reference indexes
- **Objective:** prepare shared reference assets for STAR, Salmon, Kallisto, and ALFA
- **Inputs:** `analysis_manifest.json`
- **Allowed actions:** sort GTF, extract transcriptome, concatenate transcriptome and genome, and build STAR, Salmon, Kallisto, and ALFA indexes
- **Forbidden actions:** process FASTQ reads before mandatory index validation succeeds
- **Expected outputs:** `reference_manifest.json`
- **Manifest must record:** index paths, annotation paths, transcriptome derivation paths, enabled index families
- **Validation checks:** all required indexes exist and are consistent with the selected organism and annotation set
- **On failure:** retry failed index builds and stop if mandatory index families remain incomplete
- **Completion signal:** `reference_manifest.json` exists and lists all resolved index artifacts
- **Next step:** Step 4

## Step 4

- **Step ID:** `step-4-stage-inputs`
- **Manifest type:** `input_manifest`
- **Name:** Stage raw input reads
- **Objective:** normalize input files into the workflow-owned directory structure
- **Inputs:** `analysis_manifest.json`
- **Allowed actions:** execute `start`, copy or relink reads, register lane grouping, and standardize naming
- **Forbidden actions:** trim, align, or quantify before staged inputs are validated
- **Expected outputs:** `input_manifest.json`
- **Manifest must record:** per-sample staged raw inputs, lane mapping, mode-specific input structure
- **Validation checks:** all declared input reads are staged and every sample has the expected mode-specific file layout
- **Parallelism:** by `sample`
- **On failure:** retry failed sample staging independently and stop if any required sample remains unstaged
- **Completion signal:** `input_manifest.json` exists and covers all samples
- **Next step:** Step 5

## Step 5

- **Step ID:** `step-5-trim`
- **Manifest type:** `prepared_reads_manifest`
- **Name:** Trim adapters and polyA sequences
- **Objective:** transform staged reads into cleaned reads for alignment and quantification
- **Inputs:** `input_manifest.json`
- **Allowed actions:** run adapter trimming and polyA trimming according to single-end or paired-end mode
- **Forbidden actions:** align or quantify before trimmed reads are validated
- **Expected outputs:** `prepared_reads_manifest.json`
- **Manifest must record:** per-sample trimmed read paths, trimming status, mode-specific processing path
- **Validation checks:** every sample has cleaned reads and the expected trimmed outputs for its sequencing mode
- **Parallelism:** by `sample`
- **On failure:** retry failed samples independently and stop if any sample lacks cleaned reads
- **Completion signal:** `prepared_reads_manifest.json` exists and lists all cleaned read artifacts
- **Next step:** Step 6

## Step 6

- **Step ID:** `step-6-align`
- **Manifest type:** `alignment_manifest`
- **Name:** Run STAR alignment and alignment post-processing
- **Objective:** produce sorted and indexed alignments for downstream QC and reporting
- **Inputs:** `prepared_reads_manifest.json`, `reference_manifest.json`
- **Allowed actions:** run STAR, sort BAMs, index BAMs, build RPM-normalized coverage, and generate bigWig and bedGraph derivatives
- **Forbidden actions:** aggregate cross-sample quantifications before alignment outputs validate
- **Expected outputs:** `alignment_manifest.json`
- **Manifest must record:** BAM paths, indexes, coverage derivatives, alignment status per sample
- **Validation checks:** each sample has sorted and indexed alignment outputs and required coverage artifacts
- **Parallelism:** by `sample`
- **On failure:** retry failed samples independently and stop if any sample lacks validated alignment outputs
- **Completion signal:** `alignment_manifest.json` exists and lists all alignment artifacts
- **Next step:** Step 7

## Step 7

- **Step ID:** `step-7-quantify`
- **Manifest type:** `quant_manifest`
- **Name:** Run Salmon and Kallisto quantification
- **Objective:** produce transcript-level quantification outputs across all enabled quantifiers
- **Inputs:** `prepared_reads_manifest.json`, `reference_manifest.json`
- **Allowed actions:** run Salmon and Kallisto per sample and aggregate their per-sample result inventory
- **Forbidden actions:** claim sample-level quantification completion before both enabled quantifiers finish
- **Expected outputs:** `quant_manifest.json`
- **Manifest must record:** per-sample Salmon outputs, per-sample Kallisto outputs, enabled quantifier set
- **Validation checks:** every sample produces all required quantification outputs for the enabled tools
- **Parallelism:** by `sample`
- **On failure:** retry failed sample quantification independently and stop if any required quantifier output is missing
- **Completion signal:** `quant_manifest.json` exists and covers all samples
- **Next step:** Step 8

## Step 8

- **Step ID:** `step-8-run-qc`
- **Manifest type:** `qc_manifest`
- **Name:** Run QC and cross-sample summaries
- **Objective:** generate FastQC, ALFA, TIN, PCA, and MultiQC outputs
- **Inputs:** `alignment_manifest.json`, `quant_manifest.json`, `reference_manifest.json`
- **Allowed actions:** run FastQC, compute TIN, generate ALFA outputs, prepare PCA inputs, and build MultiQC
- **Forbidden actions:** finalize delivery before QC aggregation succeeds
- **Expected outputs:** `qc_manifest.json`
- **Manifest must record:** per-sample QC outputs, PCA artifacts, MultiQC path, summary coverage
- **Validation checks:** required QC families exist and the final MultiQC report is present
- **Parallelism:** by `sample` with final fan-in for cross-sample summaries
- **On failure:** retry failed per-sample QC branches and stop if final cross-sample QC artifacts remain incomplete
- **Completion signal:** `qc_manifest.json` exists and includes MultiQC plus cross-sample QC outputs
- **Next step:** Step 9

## Step 9

- **Step ID:** `step-9-deliver`
- **Manifest type:** `delivery_manifest`
- **Name:** Assemble final results and finish targets
- **Objective:** collect workflow outputs into the final delivery inventory
- **Inputs:** `alignment_manifest.json`, `quant_manifest.json`, `qc_manifest.json`
- **Allowed actions:** assemble final bigWig, quantification, QC, and reporting outputs that satisfy the `finish` target
- **Forbidden actions:** silently skip required finish artifacts
- **Expected outputs:** `delivery_manifest.json`
- **Manifest must record:** final result inventory, output directory summary, finish-target artifacts
- **Validation checks:** all required `finish` artifacts exist and are listed in the delivery manifest
- **On failure:** stop if required finish artifacts are incomplete
- **Completion signal:** `delivery_manifest.json` exists and enumerates final outputs
- **Next step:** Step 10

## Step 10

- **Step ID:** `step-10-verify`
- **Manifest type:** `verification_manifest`
- **Name:** Verify reports and optional pre-workflows
- **Objective:** confirm the run is publication-grade and record optional pre-main workflow status
- **Inputs:** `delivery_manifest.json`
- **Allowed actions:** generate report artifacts, record checksum or semantic verification status, and record SRA-download or HTSinfer pre-workflow usage when applicable
- **Forbidden actions:** mutate final delivery artifacts during verification
- **Expected outputs:** `verification_manifest.json`
- **Manifest must record:** report status, verification status, optional pre-workflow status
- **Validation checks:** requested reports exist; optional pre-workflow stages are either completed or explicitly not used
- **On failure:** stop and report the verification gap
- **Completion signal:** `verification_manifest.json` exists and records final verification state
- **End state:** workflow execution is complete
