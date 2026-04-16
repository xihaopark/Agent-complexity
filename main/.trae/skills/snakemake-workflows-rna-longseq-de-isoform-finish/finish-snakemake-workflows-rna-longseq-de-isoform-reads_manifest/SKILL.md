---
name: finish-snakemake-workflows-rna-longseq-de-isoform-reads_manifest
description: Use this skill when orchestrating the retained "reads_manifest" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the reads manifest stage tied to upstream `pca` and the downstream handoff to `gff_to_gtf`. It tracks completion via `results/finish/reads_manifest.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: reads_manifest
  step_name: reads manifest
---

# Scope
Use this skill only for the `reads_manifest` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `pca`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/reads_manifest.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/reads_manifest.done`
- Representative outputs: `results/finish/reads_manifest.done`
- Execution targets: `reads_manifest`
- Downstream handoff: `gff_to_gtf`

## Guardrails
- Treat `results/finish/reads_manifest.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/reads_manifest.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `gff_to_gtf` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/reads_manifest.done` exists and `gff_to_gtf` can proceed without re-running reads manifest.
