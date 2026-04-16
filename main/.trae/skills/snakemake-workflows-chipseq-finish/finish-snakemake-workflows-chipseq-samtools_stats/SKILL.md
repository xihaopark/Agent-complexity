---
name: finish-snakemake-workflows-chipseq-samtools_stats
description: Use this skill when orchestrating the retained "samtools_stats" step of the snakemake workflows chipseq finish finish workflow. It keeps the samtools stats stage tied to upstream `samtools_idxstats` and the downstream handoff to `samtools_index`. It tracks completion via `results/finish/samtools_stats.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: samtools_stats
  step_name: samtools stats
---

# Scope
Use this skill only for the `samtools_stats` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `samtools_idxstats`
- Step file: `finish/chipseq-finish/steps/samtools_stats.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/samtools_stats.done`
- Representative outputs: `results/finish/samtools_stats.done`
- Execution targets: `samtools_stats`
- Downstream handoff: `samtools_index`

## Guardrails
- Treat `results/finish/samtools_stats.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/samtools_stats.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `samtools_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/samtools_stats.done` exists and `samtools_index` can proceed without re-running samtools stats.
