---
name: finish-snakemake-workflows-dna-seq-benchmark-get_reads
description: Use this skill when orchestrating the retained "get_reads" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the get reads stage tied to upstream `sort_vcf` and the downstream handoff to `get_archive`. It tracks completion via `results/finish/get_reads.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: get_reads
  step_name: get reads
---

# Scope
Use this skill only for the `get_reads` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `sort_vcf`
- Step file: `finish/dna-seq-benchmark-finish/steps/get_reads.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_reads.done`
- Representative outputs: `results/finish/get_reads.done`
- Execution targets: `get_reads`
- Downstream handoff: `get_archive`

## Guardrails
- Treat `results/finish/get_reads.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_reads.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_archive` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_reads.done` exists and `get_archive` can proceed without re-running get reads.
