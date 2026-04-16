# dna-seq-varlociraptor LLM Execution Spec

## Purpose

- Use this file as a prompt-oriented execution contract for the `dna-seq-varlociraptor` workflow.
- Treat `workflow/Snakefile` as the source of truth for actual execution.
- Treat this file as the control layer that tells an LLM what to do, what not to do, and how to decide that a step is complete.

## Operating Rules

- Run steps in numeric order.
- Do not start the next step before the current step passes validation.
- Write one manifest per completed step.
- If a step fails validation, stop and report the failure point instead of improvising the next step.
- Do not silently change biological assumptions, config values, or sample metadata.
- Use sample-level fanout only where explicitly allowed.
- Use group-level or scatter-level fanout only where explicitly allowed.

## Shared Terms

- Run scope: one `config.yaml`, one `samples.tsv`, one `units.tsv`, and one `scenario.yaml`
- Sample-unit: execution grain for read preparation
- Sample: execution grain for alignment and candidate discovery
- Group: execution grain for scenario rendering, evidence building, calling, and filtering
- Partition: scatter-gather shard used by calling

## Manifest Mapping

- Step 1 → `analysis_manifest`
- Step 2 → `input_manifest`
- Step 3 → `reference_manifest`
- Step 4 → `prepared_reads_manifest`
- Step 5 → `alignment_manifest`
- Step 6 → `candidate_manifest`
- Step 7 → `evidence_manifest`
- Step 8 → `calling_manifest`
- Step 9 → `final_calls_manifest`
- Step 10 → `delivery_manifest`

## Common Manifest Requirements

- Every manifest must satisfy `agent-orchestration/manifest-schema.yaml`.
- Every manifest must set `workflow_id` to `dna-seq-varlociraptor`.
- Every manifest must set `step_id` to the current step identifier.
- Every manifest must include `summary`, `artifacts`, `validations`, and `errors`.
- Every successful step must record at least one produced or verified artifact.

## Step 1

- **Step ID:** `step-1-parse-config`
- **Manifest type:** `analysis_manifest`
- **Name:** Parse configuration and resolve analysis modes
- **Objective:** build the run-level execution context before compute begins
- **Inputs:** `config/config.yaml`, `config/samples.tsv`, `config/units.tsv`, optional target-region and scenario files
- **Allowed actions:** read config files, validate required fields, resolve groups, resolve calling modes, record enabled optional modules
- **Forbidden actions:** download references, touch reads, run mapping, create calls
- **Expected outputs:** `analysis_manifest.json`
- **Manifest must record:** run context, resolved groups, enabled modules, config validation results
- **Validation checks:** all referenced files exist; sample aliases are legal; groups and calling types are internally consistent
- **On failure:** stop immediately and return the exact config inconsistency
- **Completion signal:** `analysis_manifest.json` exists and lists all enabled branches
- **Next step:** Step 2

## Step 2

- **Step ID:** `step-2-resolve-inputs`
- **Manifest type:** `input_manifest`
- **Name:** Resolve input sources and sample preconditions
- **Objective:** determine what raw data exists and what per-sample preprocessing is required
- **Inputs:** `analysis_manifest.json`
- **Allowed actions:** classify each sample-unit as local FASTQ or SRA; detect primer, UMI, consensus, and pangenome requirements; record sample-level prerequisites
- **Forbidden actions:** download references, run trimming, run alignment
- **Expected outputs:** `input_manifest.json`
- **Manifest must record:** all sample-units, source type, preconditions, unresolved items if any
- **Validation checks:** every sample-unit has one legal source; all sample-specific prerequisites are explicitly recorded
- **Parallelism:** by `sample-unit`
- **On failure:** retry one source inspection if the failure is transient, otherwise stop
- **Completion signal:** `input_manifest.json` covers all sample-units in the run
- **Next step:** Step 3

## Step 3

- **Step ID:** `step-3-prepare-reference`
- **Manifest type:** `reference_manifest`
- **Name:** Prepare shared reference assets
- **Objective:** materialize all mandatory and enabled optional references
- **Inputs:** `analysis_manifest.json`
- **Allowed actions:** prepare genome, annotations, known variants, VEP cache, VEP plugins, optional pangenome assets, optional population resources, optional benchmarking resources
- **Forbidden actions:** process reads, run mapping, run calling
- **Expected outputs:** `reference_manifest.json`
- **Manifest must record:** mandatory references, optional references, resolved paths, missing resources if validation fails
- **Validation checks:** all mandatory assets exist; optional assets are present only when their modules are enabled
- **Parallelism:** by resource family
- **On failure:** retry downloads, then stop if any required asset is still missing
- **Completion signal:** `reference_manifest.json` lists all resolved resource paths
- **Next step:** Step 4

## Step 4

- **Step ID:** `step-4-prepare-reads`
- **Manifest type:** `prepared_reads_manifest`
- **Name:** Prepare reads
- **Objective:** transform raw sources into mapping-ready read payloads
- **Inputs:** `input_manifest.json`
- **Allowed actions:** download SRA when needed, run trimming, merge or normalize read outputs, record preprocessing context
- **Forbidden actions:** run alignment, run candidate discovery
- **Expected outputs:** `prepared_reads_manifest.json`
- **Manifest must record:** one entry per sample-unit, prepared read paths, preprocessing status
- **Validation checks:** every sample-unit has a resolved read payload; required preprocessing artifacts exist
- **Parallelism:** by `sample-unit`
- **On failure:** retry failed units independently, then stop before mapping if any required unit is unresolved
- **Completion signal:** `prepared_reads_manifest.json` exists and matches the expected sample-unit inventory
- **Next step:** Step 5

## Step 5

- **Step ID:** `step-5-align`
- **Manifest type:** `alignment_manifest`
- **Name:** Align reads and standardize BAMs
- **Objective:** produce analysis-ready BAM or CRAM artifacts for downstream calling
- **Inputs:** `prepared_reads_manifest.json`, `reference_manifest.json`
- **Allowed actions:** run BWA or VG mapping, sort, index, add read groups, apply optional UMI logic, build optional consensus reads, apply optional BQSR
- **Forbidden actions:** call variants, annotate calls, generate reports
- **Expected outputs:** `alignment_manifest.json`
- **Manifest must record:** per-sample alignment outputs, indexes, alignment method, metadata attachment status
- **Validation checks:** each sample yields an analysis-ready alignment artifact and its index; required metadata is attached
- **Parallelism:** by `sample`
- **On failure:** retry failed samples independently, then stop if any required alignment artifact is missing
- **Completion signal:** `alignment_manifest.json` lists all aligned samples
- **Next step:** Step 6

## Step 6

- **Step ID:** `step-6-discover-candidates`
- **Manifest type:** `candidate_manifest`
- **Name:** Discover candidate events
- **Objective:** generate candidate small variants, structural variants, and optional fusions before evidence-based calling
- **Inputs:** `alignment_manifest.json`, `reference_manifest.json`, `analysis_manifest.json`
- **Allowed actions:** run candidate discovery tools, normalize candidate event sets, scatter partitions for downstream calling
- **Forbidden actions:** run final varlociraptor calling, annotate final outputs
- **Expected outputs:** `candidate_manifest.json`
- **Manifest must record:** enabled candidate branches, per-sample candidate outputs, partition inventory
- **Validation checks:** every enabled candidate branch yields expected outputs; all required scatter partitions exist
- **Parallelism:** by `sample` and `partition`
- **On failure:** retry the failed candidate branch or failed partition, then stop if the partition set is incomplete
- **Completion signal:** `candidate_manifest.json` covers all enabled branches and partitions
- **Next step:** Step 7

## Step 7

- **Step ID:** `step-7-build-evidence`
- **Manifest type:** `evidence_manifest`
- **Name:** Build calling evidence
- **Objective:** convert alignments and candidates into group-specific evidence for formal calling
- **Inputs:** `candidate_manifest.json`, `alignment_manifest.json`, `analysis_manifest.json`
- **Allowed actions:** render scenarios, estimate alignment properties, preprocess observations, build per-group evidence payloads
- **Forbidden actions:** produce final gathered calls, build reports
- **Expected outputs:** `evidence_manifest.json`
- **Manifest must record:** per-group evidence artifacts, partition coverage, unresolved evidence gaps if any
- **Validation checks:** every enabled group has scenario, alignment property, and observation artifacts for all required partitions
- **Parallelism:** by `group` and `partition`
- **On failure:** stop as soon as any required group lacks complete evidence
- **Completion signal:** `evidence_manifest.json` is complete for all enabled groups
- **Next step:** Step 8

## Step 8

- **Step ID:** `step-8-call`
- **Manifest type:** `calling_manifest`
- **Name:** Execute varlociraptor calling
- **Objective:** generate formal calls from evidence and gather partition outputs
- **Inputs:** `evidence_manifest.json`, `analysis_manifest.json`
- **Allowed actions:** run `varlociraptor call variants`, run optional genotyping, gather partitions into complete call sets
- **Forbidden actions:** annotate or filter before gather is complete
- **Expected outputs:** `calling_manifest.json`
- **Manifest must record:** per-group gathered calls, per-partition status, genotyping status if enabled
- **Validation checks:** each required group has gathered call outputs; all partitions were consumed
- **Parallelism:** by `group` and `partition`
- **On failure:** retry failed partitions independently, then stop if gather cannot complete
- **Completion signal:** `calling_manifest.json` exists with one gathered call set per required group
- **Next step:** Step 9

## Step 9

- **Step ID:** `step-9-annotate-filter`
- **Manifest type:** `final_calls_manifest`
- **Name:** Annotate and filter calls
- **Objective:** convert raw gathered calls into final biological result sets
- **Inputs:** `calling_manifest.json`, `reference_manifest.json`, `analysis_manifest.json`
- **Allowed actions:** run VEP, apply external annotations, apply annotation filters, posterior-odds thresholds, FDR control, and merge final calls
- **Forbidden actions:** generate final reports before final calls pass validation
- **Expected outputs:** `final_calls_manifest.json`
- **Manifest must record:** per-group annotated outputs, filtered outputs, final merged outputs
- **Validation checks:** final calls, annotated calls, and filtered call sets exist for every required group
- **Parallelism:** by `group`
- **On failure:** retry failed annotation or filtering branches independently, then stop before reporting if final calls are incomplete
- **Completion signal:** `final_calls_manifest.json` exists and lists all final per-group outputs
- **Next step:** Step 10

## Step 10

- **Step ID:** `step-10-build-deliverables`
- **Manifest type:** `delivery_manifest`
- **Name:** Build reports and downstream deliverables
- **Objective:** generate all enabled user-facing outputs from final calls
- **Inputs:** `final_calls_manifest.json`, `analysis_manifest.json`
- **Allowed actions:** export tables, MAF, datavzrd reports, MultiQC outputs, oncoprints, mutational burden, mutational signatures, and other enabled report families
- **Forbidden actions:** mutate upstream calls or silently skip required deliverables
- **Expected outputs:** `delivery_manifest.json`
- **Manifest must record:** final delivery inventory, report families, user-facing tables and reports
- **Validation checks:** every enabled report family is present in the delivery inventory
- **Parallelism:** by report family and optional module
- **On failure:** retry report-generation tasks, then stop if required deliverables remain incomplete
- **Completion signal:** `delivery_manifest.json` exists and enumerates the final deliverables
- **End state:** workflow execution is complete
