---
name: finish-snakemake-workflows-read-alignment-pangenome-build_primer_regions
description: Use this skill when orchestrating the retained "build_primer_regions" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the build primer regions stage tied to upstream `primer_to_bed` and the downstream handoff to `all`. It tracks completion via `results/finish/build_primer_regions.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: build_primer_regions
  step_name: build primer regions
---

# Scope
Use this skill only for the `build_primer_regions` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `primer_to_bed`
- Step file: `finish/read-alignment-pangenome-finish/steps/build_primer_regions.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/build_primer_regions.done`
- Representative outputs: `results/finish/build_primer_regions.done`
- Execution targets: `build_primer_regions`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/build_primer_regions.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/build_primer_regions.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/build_primer_regions.done` exists and `all` can proceed without re-running build primer regions.
