---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-get_sra
description: Use this skill when orchestrating the retained "get_sra" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the get sra stage tied to upstream `tsv_to_excel` and the downstream handoff to `cutadapt_pipe`. It tracks completion via `results/finish/get_sra.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: get_sra
  step_name: get sra
---

# Scope
Use this skill only for the `get_sra` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `tsv_to_excel`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/get_sra.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_sra.done`
- Representative outputs: `results/finish/get_sra.done`
- Execution targets: `get_sra`
- Downstream handoff: `cutadapt_pipe`

## Guardrails
- Treat `results/finish/get_sra.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_sra.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `cutadapt_pipe` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_sra.done` exists and `cutadapt_pipe` can proceed without re-running get sra.
