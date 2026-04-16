---
name: finish-snakemake-workflows-cyrcular-calling-varlociraptor_alignment_properties
description: Use this skill when orchestrating the retained "varlociraptor_alignment_properties" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the varlociraptor alignment properties stage tied to upstream `varlociraptor_call` and the downstream handoff to `varlociraptor_preprocess`. It tracks completion via `results/finish/varlociraptor_alignment_properties.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: varlociraptor_alignment_properties
  step_name: varlociraptor alignment properties
---

# Scope
Use this skill only for the `varlociraptor_alignment_properties` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `varlociraptor_call`
- Step file: `finish/cyrcular-calling-finish/steps/varlociraptor_alignment_properties.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/varlociraptor_alignment_properties.done`
- Representative outputs: `results/finish/varlociraptor_alignment_properties.done`
- Execution targets: `varlociraptor_alignment_properties`
- Downstream handoff: `varlociraptor_preprocess`

## Guardrails
- Treat `results/finish/varlociraptor_alignment_properties.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/varlociraptor_alignment_properties.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `varlociraptor_preprocess` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/varlociraptor_alignment_properties.done` exists and `varlociraptor_preprocess` can proceed without re-running varlociraptor alignment properties.
