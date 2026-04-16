---
name: finish-snakemake-workflows-chipseq-sra_get_fastq_se
description: Use this skill when orchestrating the retained "sra_get_fastq_se" step of the snakemake workflows chipseq finish finish workflow. It keeps the sra get fastq se stage tied to upstream `sra_get_fastq_pe` and the downstream handoff to `gtf2bed`. It tracks completion via `results/finish/sra_get_fastq_se.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: sra_get_fastq_se
  step_name: sra get fastq se
---

# Scope
Use this skill only for the `sra_get_fastq_se` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `sra_get_fastq_pe`
- Step file: `finish/chipseq-finish/steps/sra_get_fastq_se.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/sra_get_fastq_se.done`
- Representative outputs: `results/finish/sra_get_fastq_se.done`
- Execution targets: `sra_get_fastq_se`
- Downstream handoff: `gtf2bed`

## Guardrails
- Treat `results/finish/sra_get_fastq_se.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/sra_get_fastq_se.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `gtf2bed` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/sra_get_fastq_se.done` exists and `gtf2bed` can proceed without re-running sra get fastq se.
