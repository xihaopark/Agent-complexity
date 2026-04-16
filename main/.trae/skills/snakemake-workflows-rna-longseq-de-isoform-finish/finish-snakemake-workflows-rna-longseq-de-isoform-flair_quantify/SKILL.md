---
name: finish-snakemake-workflows-rna-longseq-de-isoform-flair_quantify
description: Use this skill when orchestrating the retained "flair_quantify" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the flair quantify stage tied to upstream `flair_collapse` and the downstream handoff to `flair_diffexp`. It tracks completion via `results/finish/flair_quantify.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: flair_quantify
  step_name: flair quantify
---

# Scope
Use this skill only for the `flair_quantify` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `flair_collapse`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/flair_quantify.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/flair_quantify.done`
- Representative outputs: `results/finish/flair_quantify.done`
- Execution targets: `flair_quantify`
- Downstream handoff: `flair_diffexp`

## Guardrails
- Treat `results/finish/flair_quantify.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/flair_quantify.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `flair_diffexp` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/flair_quantify.done` exists and `flair_diffexp` can proceed without re-running flair quantify.
