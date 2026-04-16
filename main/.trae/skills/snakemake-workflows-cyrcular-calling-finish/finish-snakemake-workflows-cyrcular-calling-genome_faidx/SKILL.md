---
name: finish-snakemake-workflows-cyrcular-calling-genome_faidx
description: Use this skill when orchestrating the retained "genome_faidx" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the genome faidx stage tied to upstream `get_genome` and the downstream handoff to `minimap2_index`. It tracks completion via `results/finish/genome_faidx.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: genome_faidx
  step_name: genome faidx
---

# Scope
Use this skill only for the `genome_faidx` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `get_genome`
- Step file: `finish/cyrcular-calling-finish/steps/genome_faidx.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/genome_faidx.done`
- Representative outputs: `results/finish/genome_faidx.done`
- Execution targets: `genome_faidx`
- Downstream handoff: `minimap2_index`

## Guardrails
- Treat `results/finish/genome_faidx.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/genome_faidx.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `minimap2_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/genome_faidx.done` exists and `minimap2_index` can proceed without re-running genome faidx.
