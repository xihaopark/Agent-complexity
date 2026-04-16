---
name: finish-joncahn-epigeneticbutton-deduplicate_srna_nextflexv3
description: Use this skill when orchestrating the retained "deduplicate_srna_nextflexv3" step of the joncahn epigeneticbutton finish finish workflow. It keeps the deduplicate srna nextflexv3 stage tied to upstream `convert_bedmethyl_to_cx_report` and the downstream handoff to `make_bt2_indices_for_structural_RNAs`. It tracks completion via `results/finish/deduplicate_srna_nextflexv3.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: deduplicate_srna_nextflexv3
  step_name: deduplicate srna nextflexv3
---

# Scope
Use this skill only for the `deduplicate_srna_nextflexv3` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `convert_bedmethyl_to_cx_report`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/deduplicate_srna_nextflexv3.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/deduplicate_srna_nextflexv3.done`
- Representative outputs: `results/finish/deduplicate_srna_nextflexv3.done`
- Execution targets: `deduplicate_srna_nextflexv3`
- Downstream handoff: `make_bt2_indices_for_structural_RNAs`

## Guardrails
- Treat `results/finish/deduplicate_srna_nextflexv3.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/deduplicate_srna_nextflexv3.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `make_bt2_indices_for_structural_RNAs` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/deduplicate_srna_nextflexv3.done` exists and `make_bt2_indices_for_structural_RNAs` can proceed without re-running deduplicate srna nextflexv3.
