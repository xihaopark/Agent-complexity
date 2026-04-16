# rna-seq-kallisto-sleuth LLM Execution Spec

## Purpose

- Use this file as a prompt-oriented execution contract for the `rna-seq-kallisto-sleuth` workflow.
- Treat `workflow/Snakefile` as the source of truth for actual execution.
- Treat this file as the control layer that tells an LLM what to do, what not to do, and how to decide that a step is complete.

## Operating Rules

- Run steps in numeric order.
- Do not start the next step before the current step passes validation.
- Write one manifest per completed step.
- If a step fails validation, stop and report the failure point instead of improvising the next step.
- Do not silently change workflow mode, enrichment toggles, or model definitions.
- Use sample-unit fanout only where explicitly allowed.
- Use model-level or module-level fanout only where explicitly allowed.

## Shared Terms

- Run scope: one `config.yaml`, one `samples.tsv`, and one `units.tsv`
- Sample-unit: execution grain for input normalization and quantification
- Model: execution grain for sleuth initialization and diffexp
- Module: execution grain for optional analytics
- Workflow mode: `short_read`, `3prime`, or `long_read`

## Manifest Mapping

- Step 1 → `analysis_manifest`
- Step 2 → `reads_manifest`
- Step 3 → `reference_manifest`
- Step 4 → `prepared_reads_manifest`
- Step 5 → `quant_manifest`
- Step 6 → `sleuth_init_manifest`
- Step 7 → `diffexp_manifest`
- Step 8 → `optional_modules_manifest`
- Step 9 → `delivery_manifest`

## Common Manifest Requirements

- Every manifest must satisfy `agent-orchestration/manifest-schema.yaml`.
- Every manifest must set `workflow_id` to `rna-seq-kallisto-sleuth`.
- Every manifest must set `step_id` to the current step identifier.
- Every manifest must include `summary`, `artifacts`, `validations`, and `errors`.
- Every successful step must record at least one produced or verified artifact.

## Step 1

- **Step ID:** `step-1-parse-config`
- **Manifest type:** `analysis_manifest`
- **Name:** Parse configuration and resolve workflow mode
- **Objective:** normalize config and determine the execution branch before heavy compute starts
- **Inputs:** `config/config.yaml`, `config/samples.tsv`, `config/units.tsv`
- **Allowed actions:** parse experiment settings, detect `3-prime-rna-seq` mode, detect `long_read` mode, load diffexp models, collect optional analysis toggles
- **Forbidden actions:** fetch references, transform reads, start quantification
- **Expected outputs:** `analysis_manifest.json`
- **Manifest must record:** workflow mode, diffexp models, enabled optional modules, branch-specific settings
- **Validation checks:** mode resolves to exactly one branch; all configured models are parseable; sample and unit metadata are consistent
- **On failure:** stop if the mode is ambiguous or if required metadata is missing
- **Completion signal:** `analysis_manifest.json` exists and lists the chosen mode
- **Next step:** Step 2

## Step 2

- **Step ID:** `step-2-normalize-inputs`
- **Manifest type:** `reads_manifest`
- **Name:** Normalize input sources
- **Objective:** turn heterogeneous raw inputs into one consistent read-source inventory
- **Inputs:** `analysis_manifest.json`
- **Allowed actions:** detect FASTQ or BAM input per sample-unit; determine single-end or paired-end; capture fragment length settings for single-end quantification
- **Forbidden actions:** fetch references, run fastp, run quantification
- **Expected outputs:** `reads_manifest.json`
- **Manifest must record:** sample-unit source type, pairedness, fragment statistics, unresolved items if any
- **Validation checks:** every unit resolves to one valid source; single-end units have the required fragment statistics when applicable
- **Parallelism:** by `sample-unit`
- **On failure:** retry source inspection once, then stop the run
- **Completion signal:** `reads_manifest.json` covers all sample-units in the run
- **Next step:** Step 3

## Step 3

- **Step ID:** `step-3-prepare-references`
- **Manifest type:** `reference_manifest`
- **Name:** Prepare shared and optional reference resources
- **Objective:** materialize all reference assets required by the selected branch and optional modules
- **Inputs:** `analysis_manifest.json`
- **Allowed actions:** download transcriptome, GTF, transcript annotations, shared resources, Pfam and CPAT assets, GO and SPIA assets, and 3prime derivatives when enabled
- **Forbidden actions:** run quantification or initialize sleuth before reference validation succeeds
- **Expected outputs:** `reference_manifest.json`
- **Manifest must record:** shared references, optional references, branch-specific references, resolved paths
- **Validation checks:** all resources required by the chosen branch and enabled modules exist and are indexed in the manifest
- **Parallelism:** by resource family where safe
- **On failure:** retry remote downloads, then stop if a required branch asset is missing
- **Completion signal:** `reference_manifest.json` lists all resolved resource paths
- **Next step:** Step 4

## Step 4

- **Step ID:** `step-4-prepare-reads`
- **Manifest type:** `prepared_reads_manifest`
- **Name:** Prepare effective reads
- **Objective:** produce cleaned FASTQ inputs for downstream quantification
- **Inputs:** `reads_manifest.json`
- **Allowed actions:** convert BAM to FASTQ when needed; run fastp; compute supporting read statistics needed by downstream QC
- **Forbidden actions:** start kallisto, bustools, or BWA before prepared read validation succeeds
- **Expected outputs:** `prepared_reads_manifest.json`
- **Manifest must record:** per-unit prepared read paths, conversion status, cleaning status
- **Validation checks:** every sample-unit has a usable cleaned input payload; converted BAM-derived reads are non-empty
- **Parallelism:** by `sample-unit`
- **On failure:** retry failed units independently and stop before quantification if any required unit remains unresolved
- **Completion signal:** `prepared_reads_manifest.json` exists and matches the sample-unit inventory
- **Next step:** Step 5

## Step 5

- **Step ID:** `step-5-quantify`
- **Manifest type:** `quant_manifest`
- **Name:** Run branch-specific quantification
- **Objective:** execute exactly one quantification branch and converge it into a shared quantification interface
- **Inputs:** `prepared_reads_manifest.json`, `reference_manifest.json`, `analysis_manifest.json`
- **Allowed actions:** run short-read kallisto quant when mode is `short_read`; run BWA plus 3prime read selection plus kallisto 3prime quant when mode is `3prime`; run long-read kallisto and bustools when mode is `long_read`
- **Forbidden actions:** initialize sleuth before branch convergence is complete
- **Expected outputs:** `quant_manifest.json`
- **Manifest must record:** branch mode, per-unit quant outputs, shared `kallisto_output` path, branch-specific intermediate status
- **Validation checks:** each processed unit emits one branch-appropriate quantification output; the manifest exposes one normalized `kallisto_output` path per unit
- **Parallelism:** by `sample-unit`
- **On failure:** retry failed units within the active branch and stop if convergence to the shared quantification interface is incomplete
- **Completion signal:** `quant_manifest.json` exists and covers all required sample-units
- **Next step:** Step 6

## Step 6

- **Step ID:** `step-6-init-sleuth`
- **Manifest type:** `sleuth_init_manifest`
- **Name:** Build sleuth inputs and initialize models
- **Objective:** transform quantification outputs into sleuth-ready model state
- **Inputs:** `quant_manifest.json`, `analysis_manifest.json`
- **Allowed actions:** compose sleuth sample sheets; initialize sleuth objects for each configured model; initialize the shared `all` model used by global visualizations
- **Forbidden actions:** run diffexp before all required model initializations pass validation
- **Expected outputs:** `sleuth_init_manifest.json`
- **Manifest must record:** per-model sample sheet paths, `.rds` paths, shared `all` model status
- **Validation checks:** every configured model has a sample sheet and `.rds`; the `all` model exists when required by enabled plots
- **Parallelism:** by `model`
- **On failure:** retry failed models independently and stop if any required model cannot be initialized
- **Completion signal:** `sleuth_init_manifest.json` exists and lists all required models
- **Next step:** Step 7

## Step 7

- **Step ID:** `step-7-run-diffexp`
- **Manifest type:** `diffexp_manifest`
- **Name:** Run differential expression and core visualizations
- **Objective:** generate the main diffexp outputs that define the analytical backbone of the workflow
- **Inputs:** `sleuth_init_manifest.json`, `analysis_manifest.json`
- **Allowed actions:** run sleuth diffexp for each explicit model; emit transcript, aggregated gene, and representative gene outputs; generate core plots such as volcano, MA, QQ, bootstrap, matrices, heatmaps, and PCA-related outputs
- **Forbidden actions:** run optional modules or final reports before required model results are complete
- **Expected outputs:** `diffexp_manifest.json`
- **Manifest must record:** per-model result tables, core plot artifacts, aggregated outputs
- **Validation checks:** every required model produces a complete diffexp result set and the expected core visualization inventory
- **Parallelism:** by `model`
- **On failure:** retry failed models independently and stop final reporting until all required models succeed
- **Completion signal:** `diffexp_manifest.json` exists and lists all required model outputs
- **Next step:** Step 8

## Step 8

- **Step ID:** `step-8-run-optional-modules`
- **Manifest type:** `optional_modules_manifest`
- **Name:** Run optional analytical modules
- **Objective:** attach branch-specific and config-driven optional analyses without mutating the core diffexp contract
- **Inputs:** `diffexp_manifest.json`, `analysis_manifest.json`, `reference_manifest.json`
- **Allowed actions:** run diffsplice when enabled; run GO, FGSEA, and SPIA when enabled; run 3prime QC when active; collect optional module outputs into one manifest
- **Forbidden actions:** mark disabled modules as failures; skip enabled required modules without recording an error
- **Expected outputs:** `optional_modules_manifest.json`
- **Manifest must record:** one entry per optional module, enabled or disabled state, produced artifacts, skipped reasons
- **Validation checks:** enabled modules produce their declared artifacts; disabled modules are recorded as skipped rather than failed
- **Parallelism:** by `module` and then by `model` where applicable
- **On failure:** stop on failure of an enabled required module and skip only modules that are explicitly disabled
- **Completion signal:** `optional_modules_manifest.json` exists and records all optional module states
- **Next step:** Step 9

## Step 9

- **Step ID:** `step-9-build-delivery`
- **Manifest type:** `delivery_manifest`
- **Name:** Build reports and meta comparisons
- **Objective:** assemble final human-consumable outputs from core and optional analysis artifacts
- **Inputs:** `diffexp_manifest.json`, `optional_modules_manifest.json`, `analysis_manifest.json`
- **Allowed actions:** postprocess diffexp and enrichment outputs; generate datavzrd reports; run meta comparisons when enabled; assemble final delivery inventory
- **Forbidden actions:** claim workflow completion before all required reports and tables are present
- **Expected outputs:** `delivery_manifest.json`
- **Manifest must record:** reports, tables, plots, meta-comparison outputs, final delivery inventory
- **Validation checks:** final manifest lists all required reports, tables, and plots for the chosen branch and enabled modules
- **Parallelism:** by report family
- **On failure:** retry report-generation tasks and stop if required delivery assets remain incomplete
- **Completion signal:** `delivery_manifest.json` exists and enumerates the final deliverables
- **End state:** workflow execution is complete
