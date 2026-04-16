---
name: finish-snakemake-workflows-cyrcular-calling-varlociraptor_call
description: Use this skill when orchestrating the retained "varlociraptor_call" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the varlociraptor call stage tied to upstream `bcftools_sort` and the downstream handoff to `varlociraptor_alignment_properties`. It tracks completion via `results/finish/varlociraptor_call.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: varlociraptor_call
  step_name: varlociraptor call
---

# Scope
Use this skill only for the `varlociraptor_call` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `bcftools_sort`
- Step file: `finish/cyrcular-calling-finish/steps/varlociraptor_call.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/varlociraptor_call.done`
- Representative outputs: `results/finish/varlociraptor_call.done`
- Execution targets: `varlociraptor_call`
- Downstream handoff: `varlociraptor_alignment_properties`

## Guardrails
- Treat `results/finish/varlociraptor_call.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/varlociraptor_call.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `varlociraptor_alignment_properties` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/varlociraptor_call.done` exists and `varlociraptor_alignment_properties` can proceed without re-running varlociraptor call.
