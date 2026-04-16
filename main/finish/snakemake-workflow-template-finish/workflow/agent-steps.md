# snakemake-workflow-template LLM Execution Spec

## Purpose

- Use this file as a prompt-oriented execution contract for the `snakemake-workflow-template` repository.
- Treat `workflow/Snakefile` as the source of truth for actual execution.
- Treat this file as a lightweight control layer for an LLM that needs to execute the template workflow step by step.

## Operating Rules

- Run steps in numeric order.
- Do not start the next step before the current step passes validation.
- Prefer `.test/config/` when the goal is repository verification.
- Do not silently replace config values or sample metadata.
- Do not skip validation just because this repository is a template.
- Stop on validation failure and report the exact missing or invalid artifact.

## Shared Terms

- Run scope: one config file and one sample sheet
- Sample: execution grain for simulated read generation and FastQC
- Template mode: this workflow is an example scaffold, not a domain-specific production analysis

## Manifest Mapping

- Step 1 → `context_manifest`
- Step 2 → `analysis_manifest`
- Step 3 → `reference_manifest`
- Step 4 → `reads_manifest`
- Step 5 → `qc_manifest`
- Step 6 → `delivery_manifest`
- Step 7 → `verification_manifest`

## Common Manifest Requirements

- Every manifest must satisfy `agent-orchestration/manifest-schema.yaml`.
- Every manifest must set `workflow_id` to `snakemake-workflow-template`.
- Every manifest must set `step_id` to the current step identifier.
- Every manifest must include `summary`, `artifacts`, `validations`, and `errors`.
- Every successful step must record at least one produced or verified artifact.

## Step 1

- **Step ID:** `step-1-resolve-context`
- **Manifest type:** `context_manifest`
- **Name:** Resolve execution context
- **Objective:** select the active config set and execution directory
- **Inputs:** `config/config.yaml` or `.test/config/config.yaml`
- **Allowed actions:** determine whether the run targets repository defaults or `.test`; fix `workflow/Snakefile` as the entrypoint
- **Forbidden actions:** download references, generate reads, run QC
- **Expected outputs:** `context_manifest.json`
- **Manifest must record:** active config file, sample-sheet path, execution directory, execution mode
- **Validation checks:** the chosen config file exists and its sample-sheet path is resolvable
- **On failure:** stop and report the unresolved execution context
- **Completion signal:** `context_manifest.json` exists and points to one active config set
- **Next step:** Step 2

## Step 2

- **Step ID:** `step-2-parse-config`
- **Manifest type:** `analysis_manifest`
- **Name:** Parse configuration and sample metadata
- **Objective:** validate the template inputs before execution starts
- **Inputs:** `context_manifest.json`, active config file, active sample sheet
- **Allowed actions:** validate schema fields, resolve sample names, resolve simulation parameters, resolve genome source URL
- **Forbidden actions:** simulate reads, run FastQC, run MultiQC
- **Expected outputs:** `analysis_manifest.json`
- **Manifest must record:** resolved samples, simulation parameters, validation results
- **Validation checks:** config schema passes; required sample-sheet columns exist; simulation settings are usable
- **On failure:** stop and report the exact schema or metadata mismatch
- **Completion signal:** `analysis_manifest.json` exists and lists all samples
- **Next step:** Step 3

## Step 3

- **Step ID:** `step-3-prepare-reference`
- **Manifest type:** `reference_manifest`
- **Name:** Prepare and validate the reference
- **Objective:** make sure the example genome is available and structurally valid
- **Inputs:** `analysis_manifest.json`
- **Allowed actions:** download the configured FASTA, run the validation script, record the resolved reference path
- **Forbidden actions:** simulate reads before FASTA validation succeeds
- **Expected outputs:** `reference_manifest.json`
- **Manifest must record:** reference path, validation result, download status
- **Validation checks:** FASTA exists, is non-empty, and passes validation
- **On failure:** retry the download once, then stop if validation still fails
- **Completion signal:** `reference_manifest.json` exists with one validated FASTA path
- **Next step:** Step 4

## Step 4

- **Step ID:** `step-4-generate-reads`
- **Manifest type:** `reads_manifest`
- **Name:** Generate sample reads
- **Objective:** create synthetic FASTQ inputs for every sample
- **Inputs:** `analysis_manifest.json`, `reference_manifest.json`
- **Allowed actions:** run the read simulator with configured read length and read count, record output FASTQ paths
- **Forbidden actions:** run FastQC before both mates exist for a sample
- **Expected outputs:** `reads_manifest.json`
- **Manifest must record:** per-sample FASTQ outputs, simulation status, unresolved samples if any
- **Validation checks:** each sample has paired FASTQ outputs and the files are non-empty
- **Parallelism:** by `sample`
- **On failure:** retry failed samples independently, then stop if any sample lacks synthetic reads
- **Completion signal:** `reads_manifest.json` covers every sample in the run
- **Next step:** Step 5

## Step 5

- **Step ID:** `step-5-run-qc`
- **Manifest type:** `qc_manifest`
- **Name:** Run per-sample QC
- **Objective:** generate initial QC outputs for all simulated reads
- **Inputs:** `reads_manifest.json`
- **Allowed actions:** run FastQC on every generated read pair and record the resulting artifacts
- **Forbidden actions:** run MultiQC before FastQC outputs exist for all required samples
- **Expected outputs:** `qc_manifest.json`
- **Manifest must record:** per-sample FastQC outputs and QC coverage
- **Validation checks:** every FASTQ has a matching FastQC result
- **Parallelism:** by `sample`
- **On failure:** retry failed samples independently, then stop if QC coverage is incomplete
- **Completion signal:** `qc_manifest.json` lists one complete FastQC set per sample
- **Next step:** Step 6

## Step 6

- **Step ID:** `step-6-aggregate-qc`
- **Manifest type:** `delivery_manifest`
- **Name:** Aggregate QC results
- **Objective:** produce the final workflow-level artifact from sample-level QC
- **Inputs:** `qc_manifest.json`
- **Allowed actions:** run MultiQC and register the final HTML report
- **Forbidden actions:** claim workflow completion before the final report exists
- **Expected outputs:** `delivery_manifest.json`
- **Manifest must record:** final MultiQC report path and delivery inventory
- **Validation checks:** `results/multiqc/multiqc_report.html` exists and is present in the delivery manifest
- **On failure:** stop and report the missing MultiQC output
- **Completion signal:** `delivery_manifest.json` exists and lists the final report
- **Next step:** Step 7

## Step 7

- **Step ID:** `step-7-verify`
- **Manifest type:** `verification_manifest`
- **Name:** Verify lint and report generation
- **Objective:** mirror the repository CI verification path when testing the template
- **Inputs:** `delivery_manifest.json`
- **Allowed actions:** run `snakemake --lint`; optionally run `--report report.zip`; record verification artifacts
- **Forbidden actions:** mutate upstream outputs while verifying
- **Expected outputs:** `verification_manifest.json`
- **Manifest must record:** lint status, optional report status, verification artifacts
- **Validation checks:** lint succeeds; optional report exists when report verification is requested
- **On failure:** stop and report the exact verification failure
- **Completion signal:** `verification_manifest.json` exists and records lint plus optional report status
- **End state:** workflow execution is complete
