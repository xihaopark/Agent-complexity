---
name: finish-snakemake-workflows-chipseq-bwa_index
description: Use this skill when orchestrating the retained "bwa_index" step of the snakemake workflows chipseq finish finish workflow. It keeps the bwa index stage tied to upstream `genome_faidx` and the downstream handoff to `chromosome_size`. It tracks completion via `results/finish/bwa_index.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: bwa_index
  step_name: bwa index
---

# Scope
Use this skill only for the `bwa_index` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `genome_faidx`
- Step file: `finish/chipseq-finish/steps/bwa_index.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bwa_index.done`
- Representative outputs: `results/finish/bwa_index.done`
- Execution targets: `bwa_index`
- Downstream handoff: `chromosome_size`

## Guardrails
- Treat `results/finish/bwa_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bwa_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `chromosome_size` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bwa_index.done` exists and `chromosome_size` can proceed without re-running bwa index.
