---
name: finish-snakemake-workflows-cyrcular-calling-varlociraptor_preprocess
description: Use this skill when orchestrating the retained "varlociraptor_preprocess" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the varlociraptor preprocess stage tied to upstream `varlociraptor_alignment_properties` and the downstream handoff to `scatter_candidates`. It tracks completion via `results/finish/varlociraptor_preprocess.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: varlociraptor_preprocess
  step_name: varlociraptor preprocess
---

# Scope
Use this skill only for the `varlociraptor_preprocess` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `varlociraptor_alignment_properties`
- Step file: `finish/cyrcular-calling-finish/steps/varlociraptor_preprocess.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/varlociraptor_preprocess.done`
- Representative outputs: `results/finish/varlociraptor_preprocess.done`
- Execution targets: `varlociraptor_preprocess`
- Downstream handoff: `scatter_candidates`

## Guardrails
- Treat `results/finish/varlociraptor_preprocess.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/varlociraptor_preprocess.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `scatter_candidates` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/varlociraptor_preprocess.done` exists and `scatter_candidates` can proceed without re-running varlociraptor preprocess.
