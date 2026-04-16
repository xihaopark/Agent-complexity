---
name: finish-snakemake-workflows-dna-seq-short-read-circle-map-bwa_index
description: Use this skill when orchestrating the retained "bwa_index" step of the snakemake workflows dna seq short read circle map finish finish workflow. It keeps the bwa index stage tied to upstream `get_genome` and the downstream handoff to `genome_faidx`. It tracks completion via `results/finish/bwa_index.done`.
metadata:
  workflow_id: dna-seq-short-read-circle-map-finish
  workflow_name: snakemake workflows dna seq short read circle map finish
  step_id: bwa_index
  step_name: bwa index
---

# Scope
Use this skill only for the `bwa_index` step in `dna-seq-short-read-circle-map-finish`.

## Orchestration
- Upstream requirements: `get_genome`
- Step file: `finish/dna-seq-short-read-circle-map-finish/steps/bwa_index.smk`
- Config file: `finish/dna-seq-short-read-circle-map-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bwa_index.done`
- Representative outputs: `results/finish/bwa_index.done`
- Execution targets: `bwa_index`
- Downstream handoff: `genome_faidx`

## Guardrails
- Treat `results/finish/bwa_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bwa_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `genome_faidx` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bwa_index.done` exists and `genome_faidx` can proceed without re-running bwa index.
