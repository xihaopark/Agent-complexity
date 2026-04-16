---
name: finish-tgirke-systempiperdata-varseq-pathenrich
description: Use this skill when orchestrating the retained "pathenrich" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the pathenrich stage tied to upstream `non_syn_vars` and the downstream handoff to `drug_target`. It tracks completion via `results/finish/pathenrich.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: pathenrich
  step_name: pathenrich
---

# Scope
Use this skill only for the `pathenrich` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `non_syn_vars`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/pathenrich.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/pathenrich.done`
- Representative outputs: `results/finish/pathenrich.done`
- Execution targets: `pathenrich`
- Downstream handoff: `drug_target`

## Guardrails
- Treat `results/finish/pathenrich.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/pathenrich.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `drug_target` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/pathenrich.done` exists and `drug_target` can proceed without re-running pathenrich.
