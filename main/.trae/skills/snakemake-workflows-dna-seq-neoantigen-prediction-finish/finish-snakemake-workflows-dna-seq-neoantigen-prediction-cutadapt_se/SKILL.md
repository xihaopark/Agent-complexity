---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-cutadapt_se
description: Use this skill when orchestrating the retained "cutadapt_se" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the cutadapt se stage tied to upstream `cutadapt_pe` and the downstream handoff to `merge_fastqs`. It tracks completion via `results/finish/cutadapt_se.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: cutadapt_se
  step_name: cutadapt se
---

# Scope
Use this skill only for the `cutadapt_se` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `cutadapt_pe`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/cutadapt_se.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/cutadapt_se.done`
- Representative outputs: `results/finish/cutadapt_se.done`
- Execution targets: `cutadapt_se`
- Downstream handoff: `merge_fastqs`

## Guardrails
- Treat `results/finish/cutadapt_se.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/cutadapt_se.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merge_fastqs` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/cutadapt_se.done` exists and `merge_fastqs` can proceed without re-running cutadapt se.
