---
name: finish-snakemake-workflows-star-arriba-fusion-calling-get_genome_gtf
description: Use this skill when orchestrating the retained "get_genome_gtf" step of the snakemake workflows star arriba fusion calling finish finish workflow. It keeps the get genome gtf stage tied to upstream `get_genome_fasta` and the downstream handoff to `star_index`. It tracks completion via `results/finish/get_genome_gtf.done`.
metadata:
  workflow_id: star-arriba-fusion-calling-finish
  workflow_name: snakemake workflows star arriba fusion calling finish
  step_id: get_genome_gtf
  step_name: get genome gtf
---

# Scope
Use this skill only for the `get_genome_gtf` step in `star-arriba-fusion-calling-finish`.

## Orchestration
- Upstream requirements: `get_genome_fasta`
- Step file: `finish/star-arriba-fusion-calling-finish/steps/get_genome_gtf.smk`
- Config file: `finish/star-arriba-fusion-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_genome_gtf.done`
- Representative outputs: `results/finish/get_genome_gtf.done`
- Execution targets: `get_genome_gtf`
- Downstream handoff: `star_index`

## Guardrails
- Treat `results/finish/get_genome_gtf.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_genome_gtf.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `star_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_genome_gtf.done` exists and `star_index` can proceed without re-running get genome gtf.
