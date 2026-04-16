---
name: finish-snakemake-workflows-chipseq-sra_get_fastq_pe
description: Use this skill when orchestrating the retained "sra_get_fastq_pe" step of the snakemake workflows chipseq finish finish workflow. It keeps the sra get fastq pe stage tied to upstream `get_annotation` and the downstream handoff to `sra_get_fastq_se`. It tracks completion via `results/finish/sra_get_fastq_pe.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: sra_get_fastq_pe
  step_name: sra get fastq pe
---

# Scope
Use this skill only for the `sra_get_fastq_pe` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `get_annotation`
- Step file: `finish/chipseq-finish/steps/sra_get_fastq_pe.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/sra_get_fastq_pe.done`
- Representative outputs: `results/finish/sra_get_fastq_pe.done`
- Execution targets: `sra_get_fastq_pe`
- Downstream handoff: `sra_get_fastq_se`

## Guardrails
- Treat `results/finish/sra_get_fastq_pe.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/sra_get_fastq_pe.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `sra_get_fastq_se` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/sra_get_fastq_pe.done` exists and `sra_get_fastq_se` can proceed without re-running sra get fastq pe.
