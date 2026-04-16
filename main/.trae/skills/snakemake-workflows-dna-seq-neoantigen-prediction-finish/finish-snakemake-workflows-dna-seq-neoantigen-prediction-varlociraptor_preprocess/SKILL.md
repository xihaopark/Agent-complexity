---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-varlociraptor_preprocess
description: Use this skill when orchestrating the retained "varlociraptor_preprocess" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the varlociraptor preprocess stage tied to upstream `render_scenario` and the downstream handoff to `varlociraptor_call`. It tracks completion via `results/finish/varlociraptor_preprocess.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: varlociraptor_preprocess
  step_name: varlociraptor preprocess
---

# Scope
Use this skill only for the `varlociraptor_preprocess` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `render_scenario`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/varlociraptor_preprocess.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/varlociraptor_preprocess.done`
- Representative outputs: `results/finish/varlociraptor_preprocess.done`
- Execution targets: `varlociraptor_preprocess`
- Downstream handoff: `varlociraptor_call`

## Guardrails
- Treat `results/finish/varlociraptor_preprocess.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/varlociraptor_preprocess.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `varlociraptor_call` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/varlociraptor_preprocess.done` exists and `varlociraptor_call` can proceed without re-running varlociraptor preprocess.
