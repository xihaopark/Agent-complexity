---
name: finish-joncahn-epigeneticbutton-shortstack_map
description: Use this skill when orchestrating the retained "shortstack_map" step of the joncahn epigeneticbutton finish finish workflow. It keeps the shortstack map stage tied to upstream `make_bowtie1_indices_large` and the downstream handoff to `make_cluster_bedfiles`. It tracks completion via `results/finish/shortstack_map.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: shortstack_map
  step_name: shortstack map
---

# Scope
Use this skill only for the `shortstack_map` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `make_bowtie1_indices_large`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/shortstack_map.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/shortstack_map.done`
- Representative outputs: `results/finish/shortstack_map.done`
- Execution targets: `shortstack_map`
- Downstream handoff: `make_cluster_bedfiles`

## Guardrails
- Treat `results/finish/shortstack_map.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/shortstack_map.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `make_cluster_bedfiles` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/shortstack_map.done` exists and `make_cluster_bedfiles` can proceed without re-running shortstack map.
