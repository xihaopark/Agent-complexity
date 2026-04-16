---
name: finish-snakemake-workflows-chipseq-fastqc
description: Use this skill when orchestrating the retained "fastqc" step of the snakemake workflows chipseq finish finish workflow. It keeps the fastqc stage tied to upstream `get_gsize` and the downstream handoff to `multiqc`. It tracks completion via `results/finish/fastqc.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: fastqc
  step_name: fastqc
---

# Scope
Use this skill only for the `fastqc` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `get_gsize`
- Step file: `finish/chipseq-finish/steps/fastqc.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/fastqc.done`
- Representative outputs: `results/finish/fastqc.done`
- Execution targets: `fastqc`
- Downstream handoff: `multiqc`

## Guardrails
- Treat `results/finish/fastqc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/fastqc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `multiqc` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/fastqc.done` exists and `multiqc` can proceed without re-running fastqc.
