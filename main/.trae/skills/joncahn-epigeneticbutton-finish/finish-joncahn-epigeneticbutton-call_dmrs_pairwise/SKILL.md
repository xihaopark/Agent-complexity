---
name: finish-joncahn-epigeneticbutton-call_dmrs_pairwise
description: Use this skill when orchestrating the retained "call_DMRs_pairwise" step of the joncahn epigeneticbutton finish finish workflow. It keeps the call DMRs pairwise stage tied to upstream `make_mc_bigwig_files` and the downstream handoff to `all_mc`. It tracks completion via `results/finish/call_DMRs_pairwise.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: call_DMRs_pairwise
  step_name: call DMRs pairwise
---

# Scope
Use this skill only for the `call_DMRs_pairwise` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `make_mc_bigwig_files`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/call_DMRs_pairwise.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/call_DMRs_pairwise.done`
- Representative outputs: `results/finish/call_DMRs_pairwise.done`
- Execution targets: `call_DMRs_pairwise`
- Downstream handoff: `all_mc`

## Guardrails
- Treat `results/finish/call_DMRs_pairwise.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/call_DMRs_pairwise.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all_mc` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/call_DMRs_pairwise.done` exists and `all_mc` can proceed without re-running call DMRs pairwise.
