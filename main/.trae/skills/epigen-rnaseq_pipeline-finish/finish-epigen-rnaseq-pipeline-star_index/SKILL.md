---
name: finish-epigen-rnaseq-pipeline-star_index
description: Use this skill when orchestrating the retained "star_index" step of the epigen rnaseq_pipeline finish finish workflow. It keeps the star index stage tied to upstream `bwa_index` and the downstream handoff to `rseqc_gtf2bed`. It tracks completion via `results/finish/star_index.done`.
metadata:
  workflow_id: epigen-rnaseq_pipeline-finish
  workflow_name: epigen rnaseq_pipeline finish
  step_id: star_index
  step_name: star index
---

# Scope
Use this skill only for the `star_index` step in `epigen-rnaseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `bwa_index`
- Step file: `finish/epigen-rnaseq_pipeline-finish/steps/star_index.smk`
- Config file: `finish/epigen-rnaseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/star_index.done`
- Representative outputs: `results/finish/star_index.done`
- Execution targets: `star_index`
- Downstream handoff: `rseqc_gtf2bed`

## Guardrails
- Treat `results/finish/star_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/star_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `rseqc_gtf2bed` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/star_index.done` exists and `rseqc_gtf2bed` can proceed without re-running star index.
