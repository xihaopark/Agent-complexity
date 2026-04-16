---
name: finish-epigen-rnaseq-pipeline-get_annotation
description: Use this skill when orchestrating the retained "get_annotation" step of the epigen rnaseq_pipeline finish finish workflow. It keeps the get annotation stage tied to upstream `get_genome` and the downstream handoff to `genome_faidx`. It tracks completion via `results/finish/get_annotation.done`.
metadata:
  workflow_id: epigen-rnaseq_pipeline-finish
  workflow_name: epigen rnaseq_pipeline finish
  step_id: get_annotation
  step_name: get annotation
---

# Scope
Use this skill only for the `get_annotation` step in `epigen-rnaseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `get_genome`
- Step file: `finish/epigen-rnaseq_pipeline-finish/steps/get_annotation.smk`
- Config file: `finish/epigen-rnaseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_annotation.done`
- Representative outputs: `results/finish/get_annotation.done`
- Execution targets: `get_annotation`
- Downstream handoff: `genome_faidx`

## Guardrails
- Treat `results/finish/get_annotation.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_annotation.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `genome_faidx` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_annotation.done` exists and `genome_faidx` can proceed without re-running get annotation.
