---
name: finish-epigen-atacseq-pipeline-symlink_stats
description: Use this skill when orchestrating the retained "symlink_stats" step of the epigen atacseq_pipeline finish finish workflow. It keeps the symlink stats stage tied to upstream `aggregate_stats` and the downstream handoff to `multiqc`. It tracks completion via `results/finish/symlink_stats.done`.
metadata:
  workflow_id: epigen-atacseq_pipeline-finish
  workflow_name: epigen atacseq_pipeline finish
  step_id: symlink_stats
  step_name: symlink stats
---

# Scope
Use this skill only for the `symlink_stats` step in `epigen-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `aggregate_stats`
- Step file: `finish/epigen-atacseq_pipeline-finish/steps/symlink_stats.smk`
- Config file: `finish/epigen-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/symlink_stats.done`
- Representative outputs: `results/finish/symlink_stats.done`
- Execution targets: `symlink_stats`
- Downstream handoff: `multiqc`

## Guardrails
- Treat `results/finish/symlink_stats.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/symlink_stats.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `multiqc` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/symlink_stats.done` exists and `multiqc` can proceed without re-running symlink stats.
