---
name: finish-epigen-rnaseq-pipeline-rseqc_junction_saturation
description: Use this skill when orchestrating the retained "rseqc_junction_saturation" step of the epigen rnaseq_pipeline finish finish workflow. It keeps the rseqc junction saturation stage tied to upstream `rseqc_junction_annotation` and the downstream handoff to `rseqc_stat`. It tracks completion via `results/finish/rseqc_junction_saturation.done`.
metadata:
  workflow_id: epigen-rnaseq_pipeline-finish
  workflow_name: epigen rnaseq_pipeline finish
  step_id: rseqc_junction_saturation
  step_name: rseqc junction saturation
---

# Scope
Use this skill only for the `rseqc_junction_saturation` step in `epigen-rnaseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `rseqc_junction_annotation`
- Step file: `finish/epigen-rnaseq_pipeline-finish/steps/rseqc_junction_saturation.smk`
- Config file: `finish/epigen-rnaseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/rseqc_junction_saturation.done`
- Representative outputs: `results/finish/rseqc_junction_saturation.done`
- Execution targets: `rseqc_junction_saturation`
- Downstream handoff: `rseqc_stat`

## Guardrails
- Treat `results/finish/rseqc_junction_saturation.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/rseqc_junction_saturation.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `rseqc_stat` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/rseqc_junction_saturation.done` exists and `rseqc_stat` can proceed without re-running rseqc junction saturation.
