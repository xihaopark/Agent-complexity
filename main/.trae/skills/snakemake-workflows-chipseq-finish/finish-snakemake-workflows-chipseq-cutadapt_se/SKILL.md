---
name: finish-snakemake-workflows-chipseq-cutadapt_se
description: Use this skill when orchestrating the retained "cutadapt_se" step of the snakemake workflows chipseq finish finish workflow. It keeps the cutadapt se stage tied to upstream `cutadapt_pe` and the downstream handoff to `bwa_mem`. It tracks completion via `results/finish/cutadapt_se.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: cutadapt_se
  step_name: cutadapt se
---

# Scope
Use this skill only for the `cutadapt_se` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `cutadapt_pe`
- Step file: `finish/chipseq-finish/steps/cutadapt_se.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/cutadapt_se.done`
- Representative outputs: `results/finish/cutadapt_se.done`
- Execution targets: `cutadapt_se`
- Downstream handoff: `bwa_mem`

## Guardrails
- Treat `results/finish/cutadapt_se.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/cutadapt_se.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bwa_mem` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/cutadapt_se.done` exists and `bwa_mem` can proceed without re-running cutadapt se.
