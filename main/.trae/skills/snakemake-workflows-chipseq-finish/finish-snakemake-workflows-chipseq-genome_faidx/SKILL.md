---
name: finish-snakemake-workflows-chipseq-genome_faidx
description: Use this skill when orchestrating the retained "genome_faidx" step of the snakemake workflows chipseq finish finish workflow. It keeps the genome faidx stage tied to upstream `gtf2bed` and the downstream handoff to `bwa_index`. It tracks completion via `results/finish/genome_faidx.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: genome_faidx
  step_name: genome faidx
---

# Scope
Use this skill only for the `genome_faidx` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `gtf2bed`
- Step file: `finish/chipseq-finish/steps/genome_faidx.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/genome_faidx.done`
- Representative outputs: `results/finish/genome_faidx.done`
- Execution targets: `genome_faidx`
- Downstream handoff: `bwa_index`

## Guardrails
- Treat `results/finish/genome_faidx.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/genome_faidx.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bwa_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/genome_faidx.done` exists and `bwa_index` can proceed without re-running genome faidx.
