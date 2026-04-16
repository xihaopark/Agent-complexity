---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-get_callregions
description: Use this skill when orchestrating the retained "get_callregions" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the get callregions stage tied to upstream `genome_dict` and the downstream handoff to `get_known_variants`. It tracks completion via `results/finish/get_callregions.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: get_callregions
  step_name: get callregions
---

# Scope
Use this skill only for the `get_callregions` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `genome_dict`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/get_callregions.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_callregions.done`
- Representative outputs: `results/finish/get_callregions.done`
- Execution targets: `get_callregions`
- Downstream handoff: `get_known_variants`

## Guardrails
- Treat `results/finish/get_callregions.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_callregions.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_known_variants` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_callregions.done` exists and `get_known_variants` can proceed without re-running get callregions.
