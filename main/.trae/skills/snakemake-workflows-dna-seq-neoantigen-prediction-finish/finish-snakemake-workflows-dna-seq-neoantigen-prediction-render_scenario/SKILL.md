---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-render_scenario
description: Use this skill when orchestrating the retained "render_scenario" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the render scenario stage tied to upstream `scatter_candidates` and the downstream handoff to `varlociraptor_preprocess`. It tracks completion via `results/finish/render_scenario.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: render_scenario
  step_name: render scenario
---

# Scope
Use this skill only for the `render_scenario` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `scatter_candidates`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/render_scenario.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/render_scenario.done`
- Representative outputs: `results/finish/render_scenario.done`
- Execution targets: `render_scenario`
- Downstream handoff: `varlociraptor_preprocess`

## Guardrails
- Treat `results/finish/render_scenario.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/render_scenario.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `varlociraptor_preprocess` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/render_scenario.done` exists and `varlociraptor_preprocess` can proceed without re-running render scenario.
