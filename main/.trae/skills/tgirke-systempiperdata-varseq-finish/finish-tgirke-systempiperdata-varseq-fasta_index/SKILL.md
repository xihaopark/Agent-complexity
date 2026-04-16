---
name: finish-tgirke-systempiperdata-varseq-fasta_index
description: Use this skill when orchestrating the retained "fasta_index" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the fasta index stage tied to upstream `bwa_index` and the downstream handoff to `faidx_index`. It tracks completion via `results/finish/fasta_index.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: fasta_index
  step_name: fasta index
---

# Scope
Use this skill only for the `fasta_index` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `bwa_index`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/fasta_index.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/fasta_index.done`
- Representative outputs: `results/finish/fasta_index.done`
- Execution targets: `fasta_index`
- Downstream handoff: `faidx_index`

## Guardrails
- Treat `results/finish/fasta_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/fasta_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `faidx_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/fasta_index.done` exists and `faidx_index` can proceed without re-running fasta index.
