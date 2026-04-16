---
name: finish-snakemake-workflows-chipseq-samtools_idxstats
description: Use this skill when orchestrating the retained "samtools_idxstats" step of the snakemake workflows chipseq finish finish workflow. It keeps the samtools idxstats stage tied to upstream `samtools_flagstat` and the downstream handoff to `samtools_stats`. It tracks completion via `results/finish/samtools_idxstats.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: samtools_idxstats
  step_name: samtools idxstats
---

# Scope
Use this skill only for the `samtools_idxstats` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `samtools_flagstat`
- Step file: `finish/chipseq-finish/steps/samtools_idxstats.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/samtools_idxstats.done`
- Representative outputs: `results/finish/samtools_idxstats.done`
- Execution targets: `samtools_idxstats`
- Downstream handoff: `samtools_stats`

## Guardrails
- Treat `results/finish/samtools_idxstats.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/samtools_idxstats.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `samtools_stats` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/samtools_idxstats.done` exists and `samtools_stats` can proceed without re-running samtools idxstats.
