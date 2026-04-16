---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-get_tumor_from_somatic
description: Use this skill when orchestrating the retained "get_tumor_from_somatic" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the get tumor from somatic stage tied to upstream `concat_somatic` and the downstream handoff to `reheader_germline`. It tracks completion via `results/finish/get_tumor_from_somatic.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: get_tumor_from_somatic
  step_name: get tumor from somatic
---

# Scope
Use this skill only for the `get_tumor_from_somatic` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `concat_somatic`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/get_tumor_from_somatic.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_tumor_from_somatic.done`
- Representative outputs: `results/finish/get_tumor_from_somatic.done`
- Execution targets: `get_tumor_from_somatic`
- Downstream handoff: `reheader_germline`

## Guardrails
- Treat `results/finish/get_tumor_from_somatic.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_tumor_from_somatic.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `reheader_germline` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_tumor_from_somatic.done` exists and `reheader_germline` can proceed without re-running get tumor from somatic.
