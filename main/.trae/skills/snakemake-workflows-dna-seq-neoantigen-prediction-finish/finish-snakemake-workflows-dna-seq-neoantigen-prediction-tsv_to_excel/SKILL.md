---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-tsv_to_excel
description: Use this skill when orchestrating the retained "tsv_to_excel" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the tsv to excel stage tied to upstream `gzip_fastq` and the downstream handoff to `get_sra`. It tracks completion via `results/finish/tsv_to_excel.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: tsv_to_excel
  step_name: tsv to excel
---

# Scope
Use this skill only for the `tsv_to_excel` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `gzip_fastq`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/tsv_to_excel.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/tsv_to_excel.done`
- Representative outputs: `results/finish/tsv_to_excel.done`
- Execution targets: `tsv_to_excel`
- Downstream handoff: `get_sra`

## Guardrails
- Treat `results/finish/tsv_to_excel.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/tsv_to_excel.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_sra` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/tsv_to_excel.done` exists and `get_sra` can proceed without re-running tsv to excel.
