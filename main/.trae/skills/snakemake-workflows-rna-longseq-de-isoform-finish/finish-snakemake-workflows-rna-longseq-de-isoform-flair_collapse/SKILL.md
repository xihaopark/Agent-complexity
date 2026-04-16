---
name: finish-snakemake-workflows-rna-longseq-de-isoform-flair_collapse
description: Use this skill when orchestrating the retained "flair_collapse" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the flair collapse stage tied to upstream `flair_correct` and the downstream handoff to `flair_quantify`. It tracks completion via `results/finish/flair_collapse.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: flair_collapse
  step_name: flair collapse
---

# Scope
Use this skill only for the `flair_collapse` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `flair_correct`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/flair_collapse.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/flair_collapse.done`
- Representative outputs: `results/finish/flair_collapse.done`
- Execution targets: `flair_collapse`
- Downstream handoff: `flair_quantify`

## Guardrails
- Treat `results/finish/flair_collapse.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/flair_collapse.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `flair_quantify` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/flair_collapse.done` exists and `flair_quantify` can proceed without re-running flair collapse.
