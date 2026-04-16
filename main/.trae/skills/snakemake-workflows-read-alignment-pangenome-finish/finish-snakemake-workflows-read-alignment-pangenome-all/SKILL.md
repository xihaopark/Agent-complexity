---
name: finish-snakemake-workflows-read-alignment-pangenome-all
description: Use this skill when orchestrating the retained "all" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the all stage tied to upstream `build_primer_regions`. It tracks completion via `results/finish/all.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: all
  step_name: all
---

# Scope
Use this skill only for the `all` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `build_primer_regions`
- Step file: `finish/read-alignment-pangenome-finish/steps/all.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/all.done`
- Representative outputs: `results/finish/all.done`
- Execution targets: `all`
- Downstream handoff: none

## Guardrails
- Treat `results/finish/all.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/all.smk` so the step remains separable and replayable inside the finish workflow.

## Done Criteria
Mark this step complete only when `results/finish/all.done` exists and matches the intended step boundary.
