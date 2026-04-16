---
name: finish-snakemake-workflows-chipseq-samtools_flagstat
description: Use this skill when orchestrating the retained "samtools_flagstat" step of the snakemake workflows chipseq finish finish workflow. It keeps the samtools flagstat stage tied to upstream `merge_se_pe` and the downstream handoff to `samtools_idxstats`. It tracks completion via `results/finish/samtools_flagstat.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: samtools_flagstat
  step_name: samtools flagstat
---

# Scope
Use this skill only for the `samtools_flagstat` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `merge_se_pe`
- Step file: `finish/chipseq-finish/steps/samtools_flagstat.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/samtools_flagstat.done`
- Representative outputs: `results/finish/samtools_flagstat.done`
- Execution targets: `samtools_flagstat`
- Downstream handoff: `samtools_idxstats`

## Guardrails
- Treat `results/finish/samtools_flagstat.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/samtools_flagstat.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `samtools_idxstats` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/samtools_flagstat.done` exists and `samtools_idxstats` can proceed without re-running samtools flagstat.
