---
name: finish-joncahn-epigeneticbutton-all_rna
description: Use this skill when orchestrating the retained "all_rna" step of the joncahn epigeneticbutton finish finish workflow. It keeps the all rna stage tied to upstream `call_rampage_TSS` and the downstream handoff to `make_bismark_indices`. It tracks completion via `results/finish/all_rna.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: all_rna
  step_name: all rna
---

# Scope
Use this skill only for the `all_rna` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `call_rampage_TSS`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/all_rna.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/all_rna.done`
- Representative outputs: `results/finish/all_rna.done`
- Execution targets: `all_rna`
- Downstream handoff: `make_bismark_indices`

## Guardrails
- Treat `results/finish/all_rna.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/all_rna.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `make_bismark_indices` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/all_rna.done` exists and `make_bismark_indices` can proceed without re-running all rna.
