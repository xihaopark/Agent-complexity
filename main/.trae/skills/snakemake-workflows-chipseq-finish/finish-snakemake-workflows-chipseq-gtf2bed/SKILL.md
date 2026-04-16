---
name: finish-snakemake-workflows-chipseq-gtf2bed
description: Use this skill when orchestrating the retained "gtf2bed" step of the snakemake workflows chipseq finish finish workflow. It keeps the gtf2bed stage tied to upstream `sra_get_fastq_se` and the downstream handoff to `genome_faidx`. It tracks completion via `results/finish/gtf2bed.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: gtf2bed
  step_name: gtf2bed
---

# Scope
Use this skill only for the `gtf2bed` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `sra_get_fastq_se`
- Step file: `finish/chipseq-finish/steps/gtf2bed.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/gtf2bed.done`
- Representative outputs: `results/finish/gtf2bed.done`
- Execution targets: `gtf2bed`
- Downstream handoff: `genome_faidx`

## Guardrails
- Treat `results/finish/gtf2bed.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/gtf2bed.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `genome_faidx` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/gtf2bed.done` exists and `genome_faidx` can proceed without re-running gtf2bed.
