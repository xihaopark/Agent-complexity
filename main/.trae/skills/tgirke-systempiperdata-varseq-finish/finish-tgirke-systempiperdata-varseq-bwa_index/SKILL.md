---
name: finish-tgirke-systempiperdata-varseq-bwa_index
description: Use this skill when orchestrating the retained "bwa_index" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the bwa index stage tied to upstream `preprocessing` and the downstream handoff to `fasta_index`. It tracks completion via `results/finish/bwa_index.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: bwa_index
  step_name: bwa index
---

# Scope
Use this skill only for the `bwa_index` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `preprocessing`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/bwa_index.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bwa_index.done`
- Representative outputs: `results/finish/bwa_index.done`
- Execution targets: `bwa_index`
- Downstream handoff: `fasta_index`

## Guardrails
- Treat `results/finish/bwa_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bwa_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `fasta_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bwa_index.done` exists and `fasta_index` can proceed without re-running bwa index.
