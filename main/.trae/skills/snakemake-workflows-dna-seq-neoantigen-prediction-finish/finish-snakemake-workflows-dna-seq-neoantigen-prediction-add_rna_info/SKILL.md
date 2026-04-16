---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-add_rna_info
description: Use this skill when orchestrating the retained "add_RNA_info" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the add RNA info stage tied to upstream `mhc_csv_table` and the downstream handoff to `kallisto_quant`. It tracks completion via `results/finish/add_RNA_info.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: add_RNA_info
  step_name: add RNA info
---

# Scope
Use this skill only for the `add_RNA_info` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `mhc_csv_table`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/add_RNA_info.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/add_RNA_info.done`
- Representative outputs: `results/finish/add_RNA_info.done`
- Execution targets: `add_RNA_info`
- Downstream handoff: `kallisto_quant`

## Guardrails
- Treat `results/finish/add_RNA_info.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/add_RNA_info.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `kallisto_quant` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/add_RNA_info.done` exists and `kallisto_quant` can proceed without re-running add RNA info.
