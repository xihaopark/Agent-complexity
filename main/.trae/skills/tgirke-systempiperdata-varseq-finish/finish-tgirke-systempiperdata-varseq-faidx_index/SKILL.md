---
name: finish-tgirke-systempiperdata-varseq-faidx_index
description: Use this skill when orchestrating the retained "faidx_index" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the faidx index stage tied to upstream `fasta_index` and the downstream handoff to `bwa_alignment`. It tracks completion via `results/finish/faidx_index.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: faidx_index
  step_name: faidx index
---

# Scope
Use this skill only for the `faidx_index` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `fasta_index`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/faidx_index.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/faidx_index.done`
- Representative outputs: `results/finish/faidx_index.done`
- Execution targets: `faidx_index`
- Downstream handoff: `bwa_alignment`

## Guardrails
- Treat `results/finish/faidx_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/faidx_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bwa_alignment` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/faidx_index.done` exists and `bwa_alignment` can proceed without re-running faidx index.
