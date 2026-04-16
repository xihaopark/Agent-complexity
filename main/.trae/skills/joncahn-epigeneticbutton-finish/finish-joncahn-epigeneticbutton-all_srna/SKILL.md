---
name: finish-joncahn-epigeneticbutton-all_srna
description: Use this skill when orchestrating the retained "all_srna" step of the joncahn epigeneticbutton finish finish workflow. It keeps the all srna stage tied to upstream `call_all_differential_srna_clusters` and the downstream handoff to `has_header`. It tracks completion via `results/finish/all_srna.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: all_srna
  step_name: all srna
---

# Scope
Use this skill only for the `all_srna` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `call_all_differential_srna_clusters`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/all_srna.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/all_srna.done`
- Representative outputs: `results/finish/all_srna.done`
- Execution targets: `all_srna`
- Downstream handoff: `has_header`

## Guardrails
- Treat `results/finish/all_srna.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/all_srna.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `has_header` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/all_srna.done` exists and `has_header` can proceed without re-running all srna.
