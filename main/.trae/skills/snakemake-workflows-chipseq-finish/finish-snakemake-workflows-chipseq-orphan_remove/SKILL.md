---
name: finish-snakemake-workflows-chipseq-orphan_remove
description: Use this skill when orchestrating the retained "orphan_remove" step of the snakemake workflows chipseq finish finish workflow. It keeps the orphan remove stage tied to upstream `samtools_sort` and the downstream handoff to `samtools_sort_pe`. It tracks completion via `results/finish/orphan_remove.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: orphan_remove
  step_name: orphan remove
---

# Scope
Use this skill only for the `orphan_remove` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `samtools_sort`
- Step file: `finish/chipseq-finish/steps/orphan_remove.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/orphan_remove.done`
- Representative outputs: `results/finish/orphan_remove.done`
- Execution targets: `orphan_remove`
- Downstream handoff: `samtools_sort_pe`

## Guardrails
- Treat `results/finish/orphan_remove.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/orphan_remove.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `samtools_sort_pe` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/orphan_remove.done` exists and `samtools_sort_pe` can proceed without re-running orphan remove.
