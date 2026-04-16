---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-reheader_germline
description: Use this skill when orchestrating the retained "reheader_germline" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the reheader germline stage tied to upstream `get_tumor_from_somatic` and the downstream handoff to `concat_variants`. It tracks completion via `results/finish/reheader_germline.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: reheader_germline
  step_name: reheader germline
---

# Scope
Use this skill only for the `reheader_germline` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `get_tumor_from_somatic`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/reheader_germline.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/reheader_germline.done`
- Representative outputs: `results/finish/reheader_germline.done`
- Execution targets: `reheader_germline`
- Downstream handoff: `concat_variants`

## Guardrails
- Treat `results/finish/reheader_germline.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/reheader_germline.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `concat_variants` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/reheader_germline.done` exists and `concat_variants` can proceed without re-running reheader germline.
