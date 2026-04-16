---
name: finish-snakemake-workflows-chipseq-multiqc
description: Use this skill when orchestrating the retained "multiqc" step of the snakemake workflows chipseq finish finish workflow. It keeps the multiqc stage tied to upstream `fastqc` and the downstream handoff to `cutadapt_pe`. It tracks completion via `results/finish/multiqc.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: multiqc
  step_name: multiqc
---

# Scope
Use this skill only for the `multiqc` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `fastqc`
- Step file: `finish/chipseq-finish/steps/multiqc.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/multiqc.done`
- Representative outputs: `results/finish/multiqc.done`
- Execution targets: `multiqc`
- Downstream handoff: `cutadapt_pe`

## Guardrails
- Treat `results/finish/multiqc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/multiqc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `cutadapt_pe` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/multiqc.done` exists and `cutadapt_pe` can proceed without re-running multiqc.
