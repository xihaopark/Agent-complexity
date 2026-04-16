---
name: finish-snakemake-workflows-chipseq-chromosome_size
description: Use this skill when orchestrating the retained "chromosome_size" step of the snakemake workflows chipseq finish finish workflow. It keeps the chromosome size stage tied to upstream `bwa_index` and the downstream handoff to `generate_igenomes`. It tracks completion via `results/finish/chromosome_size.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: chromosome_size
  step_name: chromosome size
---

# Scope
Use this skill only for the `chromosome_size` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `bwa_index`
- Step file: `finish/chipseq-finish/steps/chromosome_size.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/chromosome_size.done`
- Representative outputs: `results/finish/chromosome_size.done`
- Execution targets: `chromosome_size`
- Downstream handoff: `generate_igenomes`

## Guardrails
- Treat `results/finish/chromosome_size.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/chromosome_size.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `generate_igenomes` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/chromosome_size.done` exists and `generate_igenomes` can proceed without re-running chromosome size.
