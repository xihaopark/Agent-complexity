---
name: finish-snakemake-workflows-read-alignment-pangenome-primer_to_bed
description: Use this skill when orchestrating the retained "primer_to_bed" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the primer to bed stage tied to upstream `filter_unmapped_primers` and the downstream handoff to `build_primer_regions`. It tracks completion via `results/finish/primer_to_bed.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: primer_to_bed
  step_name: primer to bed
---

# Scope
Use this skill only for the `primer_to_bed` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `filter_unmapped_primers`
- Step file: `finish/read-alignment-pangenome-finish/steps/primer_to_bed.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/primer_to_bed.done`
- Representative outputs: `results/finish/primer_to_bed.done`
- Execution targets: `primer_to_bed`
- Downstream handoff: `build_primer_regions`

## Guardrails
- Treat `results/finish/primer_to_bed.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/primer_to_bed.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `build_primer_regions` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/primer_to_bed.done` exists and `build_primer_regions` can proceed without re-running primer to bed.
