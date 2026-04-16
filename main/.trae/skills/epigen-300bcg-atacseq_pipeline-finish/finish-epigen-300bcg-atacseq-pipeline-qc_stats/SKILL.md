---
name: finish-epigen-300bcg-atacseq-pipeline-qc_stats
description: Use this skill when orchestrating the retained "qc_stats" step of the epigen 300bcg atacseq_pipeline finish finish workflow. It keeps the QC Stats stage tied to upstream `create_annotations` and the downstream handoff to `quantification`. It tracks completion via `results/finish/qc_stats.done`.
metadata:
  workflow_id: epigen-300bcg-atacseq_pipeline-finish
  workflow_name: epigen 300bcg atacseq_pipeline finish
  step_id: qc_stats
  step_name: QC Stats
---

# Scope
Use this skill only for the `qc_stats` step in `epigen-300bcg-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `create_annotations`
- Step file: `finish/epigen-300bcg-atacseq_pipeline-finish/steps/qc_stats.smk`
- Config file: `finish/epigen-300bcg-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/qc_stats.done`
- Representative outputs: `results/finish/qc_stats.done`
- Execution targets: `qc_stats`
- Downstream handoff: `quantification`

## Guardrails
- Treat `results/finish/qc_stats.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/qc_stats.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `quantification` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/qc_stats.done` exists and `quantification` can proceed without re-running QC Stats.
