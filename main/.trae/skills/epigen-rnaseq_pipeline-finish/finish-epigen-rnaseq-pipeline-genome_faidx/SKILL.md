---
name: finish-epigen-rnaseq-pipeline-genome_faidx
description: Use this skill when orchestrating the retained "genome_faidx" step of the epigen rnaseq_pipeline finish finish workflow. It keeps the genome faidx stage tied to upstream `get_annotation` and the downstream handoff to `bwa_index`. It tracks completion via `results/finish/genome_faidx.done`.
metadata:
  workflow_id: epigen-rnaseq_pipeline-finish
  workflow_name: epigen rnaseq_pipeline finish
  step_id: genome_faidx
  step_name: genome faidx
---

# Scope
Use this skill only for the `genome_faidx` step in `epigen-rnaseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `get_annotation`
- Step file: `finish/epigen-rnaseq_pipeline-finish/steps/genome_faidx.smk`
- Config file: `finish/epigen-rnaseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/genome_faidx.done`
- Representative outputs: `results/finish/genome_faidx.done`
- Execution targets: `genome_faidx`
- Downstream handoff: `bwa_index`

## Guardrails
- Treat `results/finish/genome_faidx.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/genome_faidx.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bwa_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/genome_faidx.done` exists and `bwa_index` can proceed without re-running genome faidx.
