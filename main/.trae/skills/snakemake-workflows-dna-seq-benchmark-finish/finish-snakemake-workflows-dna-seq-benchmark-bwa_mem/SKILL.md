---
name: finish-snakemake-workflows-dna-seq-benchmark-bwa_mem
description: Use this skill when orchestrating the retained "bwa_mem" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the bwa mem stage tied to upstream `bwa_index` and the downstream handoff to `mark_duplicates`. It tracks completion via `results/finish/bwa_mem.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: bwa_mem
  step_name: bwa mem
---

# Scope
Use this skill only for the `bwa_mem` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `bwa_index`
- Step file: `finish/dna-seq-benchmark-finish/steps/bwa_mem.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bwa_mem.done`
- Representative outputs: `results/finish/bwa_mem.done`
- Execution targets: `bwa_mem`
- Downstream handoff: `mark_duplicates`

## Guardrails
- Treat `results/finish/bwa_mem.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bwa_mem.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `mark_duplicates` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bwa_mem.done` exists and `mark_duplicates` can proceed without re-running bwa mem.
