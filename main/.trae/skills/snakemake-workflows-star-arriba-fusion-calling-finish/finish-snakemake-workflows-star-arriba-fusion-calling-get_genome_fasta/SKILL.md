---
name: finish-snakemake-workflows-star-arriba-fusion-calling-get_genome_fasta
description: Use this skill when orchestrating the retained "get_genome_fasta" step of the snakemake workflows star arriba fusion calling finish finish workflow. It keeps the get genome fasta stage and the downstream handoff to `get_genome_gtf`. It tracks completion via `results/finish/get_genome_fasta.done`.
metadata:
  workflow_id: star-arriba-fusion-calling-finish
  workflow_name: snakemake workflows star arriba fusion calling finish
  step_id: get_genome_fasta
  step_name: get genome fasta
---

# Scope
Use this skill only for the `get_genome_fasta` step in `star-arriba-fusion-calling-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/star-arriba-fusion-calling-finish/steps/get_genome_fasta.smk`
- Config file: `finish/star-arriba-fusion-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_genome_fasta.done`
- Representative outputs: `results/finish/get_genome_fasta.done`
- Execution targets: `get_genome_fasta`
- Downstream handoff: `get_genome_gtf`

## Guardrails
- Treat `results/finish/get_genome_fasta.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_genome_fasta.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_genome_gtf` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_genome_fasta.done` exists and `get_genome_gtf` can proceed without re-running get genome fasta.
