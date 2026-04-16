---
name: finish-snakemake-workflows-rna-longseq-de-isoform-pca
description: Use this skill when orchestrating the retained "pca" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the pca stage tied to upstream `deseq2` and the downstream handoff to `reads_manifest`. It tracks completion via `results/finish/pca.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: pca
  step_name: pca
---

# Scope
Use this skill only for the `pca` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `deseq2`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/pca.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/pca.done`
- Representative outputs: `results/finish/pca.done`
- Execution targets: `pca`
- Downstream handoff: `reads_manifest`

## Guardrails
- Treat `results/finish/pca.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/pca.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `reads_manifest` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/pca.done` exists and `reads_manifest` can proceed without re-running pca.
