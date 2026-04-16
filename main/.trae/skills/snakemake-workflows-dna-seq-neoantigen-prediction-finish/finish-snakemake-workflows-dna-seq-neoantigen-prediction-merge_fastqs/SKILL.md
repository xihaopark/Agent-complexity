---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-merge_fastqs
description: Use this skill when orchestrating the retained "merge_fastqs" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the merge fastqs stage tied to upstream `cutadapt_se` and the downstream handoff to `get_genome`. It tracks completion via `results/finish/merge_fastqs.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: merge_fastqs
  step_name: merge fastqs
---

# Scope
Use this skill only for the `merge_fastqs` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `cutadapt_se`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/merge_fastqs.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merge_fastqs.done`
- Representative outputs: `results/finish/merge_fastqs.done`
- Execution targets: `merge_fastqs`
- Downstream handoff: `get_genome`

## Guardrails
- Treat `results/finish/merge_fastqs.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merge_fastqs.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_genome` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merge_fastqs.done` exists and `get_genome` can proceed without re-running merge fastqs.
