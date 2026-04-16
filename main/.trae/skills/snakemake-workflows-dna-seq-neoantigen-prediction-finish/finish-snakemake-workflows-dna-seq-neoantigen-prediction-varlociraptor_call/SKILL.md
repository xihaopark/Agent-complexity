---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-varlociraptor_call
description: Use this skill when orchestrating the retained "varlociraptor_call" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the varlociraptor call stage tied to upstream `varlociraptor_preprocess` and the downstream handoff to `sort_calls`. It tracks completion via `results/finish/varlociraptor_call.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: varlociraptor_call
  step_name: varlociraptor call
---

# Scope
Use this skill only for the `varlociraptor_call` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `varlociraptor_preprocess`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/varlociraptor_call.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/varlociraptor_call.done`
- Representative outputs: `results/finish/varlociraptor_call.done`
- Execution targets: `varlociraptor_call`
- Downstream handoff: `sort_calls`

## Guardrails
- Treat `results/finish/varlociraptor_call.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/varlociraptor_call.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `sort_calls` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/varlociraptor_call.done` exists and `sort_calls` can proceed without re-running varlociraptor call.
