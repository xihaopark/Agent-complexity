---
name: finish-snakemake-workflows-chipseq-bwa_mem
description: Use this skill when orchestrating the retained "bwa_mem" step of the snakemake workflows chipseq finish finish workflow. It keeps the bwa mem stage tied to upstream `cutadapt_se` and the downstream handoff to `merge_bams`. It tracks completion via `results/finish/bwa_mem.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: bwa_mem
  step_name: bwa mem
---

# Scope
Use this skill only for the `bwa_mem` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `cutadapt_se`
- Step file: `finish/chipseq-finish/steps/bwa_mem.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bwa_mem.done`
- Representative outputs: `results/finish/bwa_mem.done`
- Execution targets: `bwa_mem`
- Downstream handoff: `merge_bams`

## Guardrails
- Treat `results/finish/bwa_mem.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bwa_mem.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merge_bams` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bwa_mem.done` exists and `merge_bams` can proceed without re-running bwa mem.
