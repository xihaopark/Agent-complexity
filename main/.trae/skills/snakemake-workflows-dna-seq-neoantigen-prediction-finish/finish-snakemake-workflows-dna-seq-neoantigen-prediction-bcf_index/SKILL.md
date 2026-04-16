---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-bcf_index
description: Use this skill when orchestrating the retained "bcf_index" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the bcf index stage and the downstream handoff to `bam_index`. It tracks completion via `results/finish/bcf_index.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: bcf_index
  step_name: bcf index
---

# Scope
Use this skill only for the `bcf_index` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/bcf_index.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bcf_index.done`
- Representative outputs: `results/finish/bcf_index.done`
- Execution targets: `bcf_index`
- Downstream handoff: `bam_index`

## Guardrails
- Treat `results/finish/bcf_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bcf_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bam_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bcf_index.done` exists and `bam_index` can proceed without re-running bcf index.
