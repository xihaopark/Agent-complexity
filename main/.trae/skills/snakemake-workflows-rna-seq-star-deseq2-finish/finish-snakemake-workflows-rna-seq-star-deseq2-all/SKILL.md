---
name: finish-snakemake-workflows-rna-seq-star-deseq2-all
description: Use this skill when orchestrating the retained "all" step of the snakemake workflows rna seq star deseq2 finish finish workflow. It keeps the all stage tied to upstream `deseq2`. It tracks completion via `results/finish/all.done`.
metadata:
  workflow_id: rna-seq-star-deseq2-finish
  workflow_name: snakemake workflows rna seq star deseq2 finish
  step_id: all
  step_name: all
---

# Scope
Use this skill only for the `all` step in `rna-seq-star-deseq2-finish`.

## Orchestration
- Upstream requirements: `deseq2`
- Step file: `finish/rna-seq-star-deseq2-finish/steps/all.smk`
- Config file: `finish/rna-seq-star-deseq2-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/all.done`
- Representative outputs: `results/finish/all.done`
- Execution targets: `all`
- Downstream handoff: none

## Guardrails
- Treat `results/finish/all.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/all.smk` so the step remains separable and replayable inside the finish workflow.

## Done Criteria
Mark this step complete only when `results/finish/all.done` exists and matches the intended step boundary.
