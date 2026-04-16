---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-get_cdna
description: Use this skill when orchestrating the retained "get_cdna" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the get cdna stage tied to upstream `get_genome` and the downstream handoff to `kallisto_index`. It tracks completion via `results/finish/get_cdna.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: get_cdna
  step_name: get cdna
---

# Scope
Use this skill only for the `get_cdna` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `get_genome`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/get_cdna.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_cdna.done`
- Representative outputs: `results/finish/get_cdna.done`
- Execution targets: `get_cdna`
- Downstream handoff: `kallisto_index`

## Guardrails
- Treat `results/finish/get_cdna.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_cdna.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `kallisto_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_cdna.done` exists and `kallisto_index` can proceed without re-running get cdna.
