---
name: finish-snakemake-workflows-cyrcular-calling-all
description: Use this skill when orchestrating the retained "all" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the all stage tied to upstream `datavzrd_circle_calls`. It tracks completion via `results/finish/all.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: all
  step_name: all
---

# Scope
Use this skill only for the `all` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `datavzrd_circle_calls`
- Step file: `finish/cyrcular-calling-finish/steps/all.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
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
