---
name: finish-tgirke-systempiperdata-varseq-non_syn_vars
description: Use this skill when orchestrating the retained "non_syn_vars" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the non syn vars stage tied to upstream `plot_variant` and the downstream handoff to `pathenrich`. It tracks completion via `results/finish/non_syn_vars.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: non_syn_vars
  step_name: non syn vars
---

# Scope
Use this skill only for the `non_syn_vars` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `plot_variant`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/non_syn_vars.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/non_syn_vars.done`
- Representative outputs: `results/finish/non_syn_vars.done`
- Execution targets: `non_syn_vars`
- Downstream handoff: `pathenrich`

## Guardrails
- Treat `results/finish/non_syn_vars.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/non_syn_vars.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `pathenrich` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/non_syn_vars.done` exists and `pathenrich` can proceed without re-running non syn vars.
