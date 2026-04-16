# dna-seq-varlociraptor Agent Step Spec

## Workflow Summary

- Workflow entrypoint: `dna-seq-varlociraptor/workflow/Snakefile`
- Upstream method: DNA-seq alignment, candidate discovery, varlociraptor evidence modeling, annotation, filtering, and reporting
- Statistical core: varlociraptor
- Dominant execution shape: staged pipeline with sample-unit fanout and scatter-gather calling
- Best orchestration model: serial stages with explicit manifests and heavy compute checkpoints

## Global Assumptions

- One run is scoped by one `config.yaml`, one `samples.tsv`, one `units.tsv`, and one `scenario.yaml`.
- A `sample-unit` is the execution grain for read preparation and alignment.
- A `group` is the execution grain for scenario rendering and downstream calling.
- The calling stage uses scatter-gather and should be treated as a separate orchestration checkpoint.
- Optional modules such as fusion, population, mutational burden, and mutational signatures are config-driven.

## Step 1: Parse Configuration and Resolve Analysis Modes

- Goal: load all run-level metadata and determine enabled calling and reporting branches.
- Inputs: `config/config.yaml`, `config/samples.tsv`, `config/units.tsv`, optional scenario and target-region files
- Actions: parse groups, calling types, reference settings, annotations, tables, report toggles, and optional modules.
- Outputs: `analysis_manifest.json`
- Validation: all referenced samples and units are resolvable; aliases are legal; group definitions and scenario inputs are consistent.
- Parallelism: none
- Failure handling: stop if any structural metadata is incomplete or contradictory.

## Step 2: Resolve Input Sources and Sample Preconditions

- Goal: determine per-sample raw data sources and sample-specific preprocessing requirements.
- Inputs: `analysis_manifest.json`
- Actions: classify each sample-unit as local FASTQ or SRA source; determine whether primers, UMI handling, consensus reads, or pangenome branches are needed.
- Outputs: `input_manifest.json`
- Validation: every sample-unit resolves to one legal source and all sample-specific prerequisites are recorded.
- Parallelism: by `sample-unit`
- Failure handling: retry transient source inspection once, then stop.

## Step 3: Prepare Shared Reference Assets

- Goal: materialize all reference resources required by mapping, calling, annotation, and reporting.
- Inputs: `analysis_manifest.json`
- Actions: prepare genome, annotations, known variants, VEP cache and plugins, optional pangenome resources, and optional population or benchmarking assets.
- Outputs: `reference_manifest.json`
- Validation: all mandatory resources exist and optional resources are indexed according to enabled modules.
- Parallelism: by resource family
- Failure handling: retry downloads, then stop if a required reference asset is missing.

## Step 4: Prepare Reads

- Goal: transform raw inputs into mapping-ready reads.
- Inputs: `input_manifest.json`
- Actions: download SRA data when needed, run read trimming, and produce effective FASTQ payloads with basic QC context.
- Outputs: `prepared_reads_manifest.json`
- Validation: every sample-unit has a resolved read payload and required preprocessing outputs exist.
- Parallelism: by `sample-unit`
- Failure handling: retry failed units independently and stop before mapping if any required unit remains unresolved.

## Step 5: Align Reads and Standardize BAMs

- Goal: generate analysis-ready BAM files for downstream calling.
- Inputs: `prepared_reads_manifest.json`, `reference_manifest.json`
- Actions: run BWA or VG mapping, sort and index BAMs, add read groups, apply optional UMI and consensus logic, and perform optional BQSR.
- Outputs: `alignment_manifest.json`
- Validation: each processed sample yields an analysis-ready BAM and index with all required metadata.
- Parallelism: by `sample`
- Failure handling: retry failed samples independently and stop the pipeline if any required alignment artifact is missing.

## Step 6: Discover Candidate Events

- Goal: propose small variants, structural variants, and optional fusions for evidence-based calling.
- Inputs: `alignment_manifest.json`, `reference_manifest.json`, `analysis_manifest.json`
- Actions: run candidate discovery tools, normalize candidate event sets, and scatter calling inputs into configured partitions.
- Outputs: `candidate_manifest.json`
- Validation: every enabled candidate branch produces expected BCF or fusion candidate outputs and scatter partitions are complete.
- Parallelism: by `sample` and scatter partition
- Failure handling: retry failed candidate branches independently and stop if scatter partitions are incomplete.

## Step 7: Build Calling Evidence

- Goal: convert candidates and alignments into varlociraptor-ready evidence objects.
- Inputs: `candidate_manifest.json`, `alignment_manifest.json`, `analysis_manifest.json`
- Actions: render scenario files, estimate alignment properties, preprocess observations, and prepare per-group calling payloads.
- Outputs: `evidence_manifest.json`
- Validation: every enabled group has scenario, alignment property, and observation artifacts for all required partitions.
- Parallelism: by `group` and scatter partition
- Failure handling: stop if evidence objects are incomplete for any required group.

## Step 8: Execute varlociraptor Calling

- Goal: produce formal variant calls from the assembled evidence.
- Inputs: `evidence_manifest.json`, `analysis_manifest.json`
- Actions: run `varlociraptor call variants`, perform optional genotyping, and gather scattered results into call sets.
- Outputs: `calling_manifest.json`
- Validation: each required group produces gathered call outputs and all scatter partitions are consumed.
- Parallelism: by `group` and scatter partition
- Failure handling: retry failed partitions independently and stop if gather cannot complete.

## Step 9: Annotate and Filter Calls

- Goal: convert raw calls into finalized, interpretable result sets.
- Inputs: `calling_manifest.json`, `reference_manifest.json`, `analysis_manifest.json`
- Actions: run VEP and external annotations, apply annotation filters, posterior-odds thresholds, FDR control, and merge final calls.
- Outputs: `final_calls_manifest.json`
- Validation: final calls, annotated calls, and filtered call sets exist for every required group.
- Parallelism: by `group`
- Failure handling: retry failed annotation or filtering branches independently and stop before reporting if final calls are incomplete.

## Step 10: Build Reports and Downstream Deliverables

- Goal: produce human-consumable outputs from finalized calls.
- Inputs: `final_calls_manifest.json`, `analysis_manifest.json`
- Actions: export tables, MAF, datavzrd reports, MultiQC outputs, oncoprints, and optional mutational burden or mutational signature summaries.
- Outputs: `delivery_manifest.json`
- Validation: final delivery inventory covers all enabled report and table families.
- Parallelism: by report family and optional module
- Failure handling: retry report-generation tasks and stop if required deliverables remain incomplete.
