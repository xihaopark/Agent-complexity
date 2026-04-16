---
name: finish-dwheelerau-snakemake-rnaseq-counts-project_setup
description: Use this skill when orchestrating the retained "project_setup" step of the dwheelerau snakemake rnaseq counts finish finish workflow. It keeps the project setup stage and the downstream handoff to `make_index`. It tracks completion via `results/finish/project_setup.done`.
metadata:
  workflow_id: dwheelerau-snakemake-rnaseq-counts-finish
  workflow_name: dwheelerau snakemake rnaseq counts finish
  step_id: project_setup
  step_name: project setup
---

# Scope
Use this skill only for the `project_setup` step in `dwheelerau-snakemake-rnaseq-counts-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/dwheelerau-snakemake-rnaseq-counts-finish/steps/project_setup.smk`
- Config file: `finish/dwheelerau-snakemake-rnaseq-counts-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/project_setup.done`
- Representative outputs: `results/finish/project_setup.done`
- Execution targets: `project_setup`
- Downstream handoff: `make_index`

## Guardrails
- Treat `results/finish/project_setup.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/project_setup.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `make_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/project_setup.done` exists and `make_index` can proceed without re-running project setup.
