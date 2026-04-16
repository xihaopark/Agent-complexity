---
name: finish-tgirke-systempiperdata-varseq-preprocessing
description: Use this skill when orchestrating the retained "preprocessing" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the preprocessing stage tied to upstream `trimmomatic` and the downstream handoff to `bwa_index`. It tracks completion via `results/finish/preprocessing.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: preprocessing
  step_name: preprocessing
---

# Scope
Use this skill only for the `preprocessing` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `trimmomatic`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/preprocessing.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/preprocessing.done`
- Representative outputs: `results/finish/preprocessing.done`
- Execution targets: `preprocessing`
- Downstream handoff: `bwa_index`

## Guardrails
- Treat `results/finish/preprocessing.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/preprocessing.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bwa_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/preprocessing.done` exists and `bwa_index` can proceed without re-running preprocessing.
