---
name: finish-snakemake-workflows-dna-seq-benchmark-mark_duplicates
description: Use this skill when orchestrating the retained "mark_duplicates" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the mark duplicates stage tied to upstream `bwa_mem` and the downstream handoff to `samtools_index`. It tracks completion via `results/finish/mark_duplicates.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: mark_duplicates
  step_name: mark duplicates
---

# Scope
Use this skill only for the `mark_duplicates` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `bwa_mem`
- Step file: `finish/dna-seq-benchmark-finish/steps/mark_duplicates.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/mark_duplicates.done`
- Representative outputs: `results/finish/mark_duplicates.done`
- Execution targets: `mark_duplicates`
- Downstream handoff: `samtools_index`

## Guardrails
- Treat `results/finish/mark_duplicates.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/mark_duplicates.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `samtools_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/mark_duplicates.done` exists and `samtools_index` can proceed without re-running mark duplicates.
