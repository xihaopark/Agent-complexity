---
name: finish-epigen-rnaseq-pipeline-get_genome
description: Use this skill when orchestrating the retained "get_genome" step of the epigen rnaseq_pipeline finish finish workflow. It keeps the get genome stage tied to upstream `annot_export` and the downstream handoff to `get_annotation`. It tracks completion via `results/finish/get_genome.done`.
metadata:
  workflow_id: epigen-rnaseq_pipeline-finish
  workflow_name: epigen rnaseq_pipeline finish
  step_id: get_genome
  step_name: get genome
---

# Scope
Use this skill only for the `get_genome` step in `epigen-rnaseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `annot_export`
- Step file: `finish/epigen-rnaseq_pipeline-finish/steps/get_genome.smk`
- Config file: `finish/epigen-rnaseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_genome.done`
- Representative outputs: `results/finish/get_genome.done`
- Execution targets: `get_genome`
- Downstream handoff: `get_annotation`

## Guardrails
- Treat `results/finish/get_genome.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_genome.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_annotation` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_genome.done` exists and `get_annotation` can proceed without re-running get genome.
