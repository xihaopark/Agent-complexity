---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-build_germline_proteome
description: Use this skill when orchestrating the retained "build_germline_proteome" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the build germline proteome stage tied to upstream `concat_proteome` and the downstream handoff to `microphaser_filter`. It tracks completion via `results/finish/build_germline_proteome.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: build_germline_proteome
  step_name: build germline proteome
---

# Scope
Use this skill only for the `build_germline_proteome` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `concat_proteome`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/build_germline_proteome.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/build_germline_proteome.done`
- Representative outputs: `results/finish/build_germline_proteome.done`
- Execution targets: `build_germline_proteome`
- Downstream handoff: `microphaser_filter`

## Guardrails
- Treat `results/finish/build_germline_proteome.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/build_germline_proteome.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `microphaser_filter` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/build_germline_proteome.done` exists and `microphaser_filter` can proceed without re-running build germline proteome.
