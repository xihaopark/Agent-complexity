---
name: finish-snakemake-workflows-read-alignment-pangenome-get_genome
description: Use this skill when orchestrating the retained "get_genome" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the get genome stage tied to upstream `tabix_known_variants` and the downstream handoff to `genome_faidx`. It tracks completion via `results/finish/get_genome.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: get_genome
  step_name: get genome
---

# Scope
Use this skill only for the `get_genome` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `tabix_known_variants`
- Step file: `finish/read-alignment-pangenome-finish/steps/get_genome.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_genome.done`
- Representative outputs: `results/finish/get_genome.done`
- Execution targets: `get_genome`
- Downstream handoff: `genome_faidx`

## Guardrails
- Treat `results/finish/get_genome.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_genome.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `genome_faidx` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_genome.done` exists and `genome_faidx` can proceed without re-running get genome.
