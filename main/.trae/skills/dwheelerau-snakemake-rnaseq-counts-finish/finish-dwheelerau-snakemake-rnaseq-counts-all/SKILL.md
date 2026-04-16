---
name: finish-dwheelerau-snakemake-rnaseq-counts-all
description: Use this skill when orchestrating the retained "all" step of the dwheelerau snakemake rnaseq counts finish finish workflow. It keeps the all stage tied to upstream `clean`. It tracks completion via `results/finish/all.done`.
metadata:
  workflow_id: dwheelerau-snakemake-rnaseq-counts-finish
  workflow_name: dwheelerau snakemake rnaseq counts finish
  step_id: all
  step_name: all
---

# Scope
Use this skill only for the `all` step in `dwheelerau-snakemake-rnaseq-counts-finish`.

## Orchestration
- Upstream requirements: `clean`
- Step file: `finish/dwheelerau-snakemake-rnaseq-counts-finish/steps/all.smk`
- Config file: `finish/dwheelerau-snakemake-rnaseq-counts-finish/config_basic/config.yaml`
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
