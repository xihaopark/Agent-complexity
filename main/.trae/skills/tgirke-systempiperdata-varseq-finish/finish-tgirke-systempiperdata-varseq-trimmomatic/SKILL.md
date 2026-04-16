---
name: finish-tgirke-systempiperdata-varseq-trimmomatic
description: Use this skill when orchestrating the retained "trimmomatic" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the trimmomatic stage tied to upstream `fastq_report` and the downstream handoff to `preprocessing`. It tracks completion via `results/finish/trimmomatic.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: trimmomatic
  step_name: trimmomatic
---

# Scope
Use this skill only for the `trimmomatic` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `fastq_report`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/trimmomatic.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/trimmomatic.done`
- Representative outputs: `results/finish/trimmomatic.done`
- Execution targets: `trimmomatic`
- Downstream handoff: `preprocessing`

## Guardrails
- Treat `results/finish/trimmomatic.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/trimmomatic.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `preprocessing` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/trimmomatic.done` exists and `preprocessing` can proceed without re-running trimmomatic.
