---
name: finish-snakemake-workflows-dna-seq-short-read-circle-map-get_genome
description: Use this skill when orchestrating the retained "get_genome" step of the snakemake workflows dna seq short read circle map finish finish workflow. It keeps the get genome stage tied to upstream `bam_index` and the downstream handoff to `bwa_index`. It tracks completion via `results/finish/get_genome.done`.
metadata:
  workflow_id: dna-seq-short-read-circle-map-finish
  workflow_name: snakemake workflows dna seq short read circle map finish
  step_id: get_genome
  step_name: get genome
---

# Scope
Use this skill only for the `get_genome` step in `dna-seq-short-read-circle-map-finish`.

## Orchestration
- Upstream requirements: `bam_index`
- Step file: `finish/dna-seq-short-read-circle-map-finish/steps/get_genome.smk`
- Config file: `finish/dna-seq-short-read-circle-map-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_genome.done`
- Representative outputs: `results/finish/get_genome.done`
- Execution targets: `get_genome`
- Downstream handoff: `bwa_index`

## Guardrails
- Treat `results/finish/get_genome.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_genome.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bwa_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_genome.done` exists and `bwa_index` can proceed without re-running get genome.
