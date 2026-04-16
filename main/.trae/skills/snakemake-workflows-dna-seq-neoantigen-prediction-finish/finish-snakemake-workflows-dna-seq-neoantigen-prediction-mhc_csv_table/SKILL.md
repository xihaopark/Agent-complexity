---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-mhc_csv_table
description: Use this skill when orchestrating the retained "mhc_csv_table" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the mhc csv table stage tied to upstream `parse_mhc_out` and the downstream handoff to `add_RNA_info`. It tracks completion via `results/finish/mhc_csv_table.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: mhc_csv_table
  step_name: mhc csv table
---

# Scope
Use this skill only for the `mhc_csv_table` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `parse_mhc_out`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/mhc_csv_table.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/mhc_csv_table.done`
- Representative outputs: `results/finish/mhc_csv_table.done`
- Execution targets: `mhc_csv_table`
- Downstream handoff: `add_RNA_info`

## Guardrails
- Treat `results/finish/mhc_csv_table.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/mhc_csv_table.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `add_RNA_info` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/mhc_csv_table.done` exists and `add_RNA_info` can proceed without re-running mhc csv table.
