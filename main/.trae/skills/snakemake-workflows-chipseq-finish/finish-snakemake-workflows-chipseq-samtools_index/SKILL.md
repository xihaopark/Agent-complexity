---
name: finish-snakemake-workflows-chipseq-samtools_index
description: Use this skill when orchestrating the retained "samtools_index" step of the snakemake workflows chipseq finish finish workflow. It keeps the samtools index stage tied to upstream `samtools_stats` and the downstream handoff to `preseq_lc_extrap`. It tracks completion via `results/finish/samtools_index.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: samtools_index
  step_name: samtools index
---

# Scope
Use this skill only for the `samtools_index` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `samtools_stats`
- Step file: `finish/chipseq-finish/steps/samtools_index.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/samtools_index.done`
- Representative outputs: `results/finish/samtools_index.done`
- Execution targets: `samtools_index`
- Downstream handoff: `preseq_lc_extrap`

## Guardrails
- Treat `results/finish/samtools_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/samtools_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `preseq_lc_extrap` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/samtools_index.done` exists and `preseq_lc_extrap` can proceed without re-running samtools index.
