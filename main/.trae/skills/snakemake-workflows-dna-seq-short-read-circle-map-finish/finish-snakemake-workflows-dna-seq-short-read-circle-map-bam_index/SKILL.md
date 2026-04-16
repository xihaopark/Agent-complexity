---
name: finish-snakemake-workflows-dna-seq-short-read-circle-map-bam_index
description: Use this skill when orchestrating the retained "bam_index" step of the snakemake workflows dna seq short read circle map finish finish workflow. It keeps the bam index stage and the downstream handoff to `get_genome`. It tracks completion via `results/finish/bam_index.done`.
metadata:
  workflow_id: dna-seq-short-read-circle-map-finish
  workflow_name: snakemake workflows dna seq short read circle map finish
  step_id: bam_index
  step_name: bam index
---

# Scope
Use this skill only for the `bam_index` step in `dna-seq-short-read-circle-map-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/dna-seq-short-read-circle-map-finish/steps/bam_index.smk`
- Config file: `finish/dna-seq-short-read-circle-map-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bam_index.done`
- Representative outputs: `results/finish/bam_index.done`
- Execution targets: `bam_index`
- Downstream handoff: `get_genome`

## Guardrails
- Treat `results/finish/bam_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bam_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_genome` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bam_index.done` exists and `get_genome` can proceed without re-running bam index.
