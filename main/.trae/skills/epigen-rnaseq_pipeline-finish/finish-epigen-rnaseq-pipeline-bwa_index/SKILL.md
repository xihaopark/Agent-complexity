---
name: finish-epigen-rnaseq-pipeline-bwa_index
description: Use this skill when orchestrating the retained "bwa_index" step of the epigen rnaseq_pipeline finish finish workflow. It keeps the bwa index stage tied to upstream `genome_faidx` and the downstream handoff to `star_index`. It tracks completion via `results/finish/bwa_index.done`.
metadata:
  workflow_id: epigen-rnaseq_pipeline-finish
  workflow_name: epigen rnaseq_pipeline finish
  step_id: bwa_index
  step_name: bwa index
---

# Scope
Use this skill only for the `bwa_index` step in `epigen-rnaseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `genome_faidx`
- Step file: `finish/epigen-rnaseq_pipeline-finish/steps/bwa_index.smk`
- Config file: `finish/epigen-rnaseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bwa_index.done`
- Representative outputs: `results/finish/bwa_index.done`
- Execution targets: `bwa_index`
- Downstream handoff: `star_index`

## Guardrails
- Treat `results/finish/bwa_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bwa_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `star_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bwa_index.done` exists and `star_index` can proceed without re-running bwa index.
