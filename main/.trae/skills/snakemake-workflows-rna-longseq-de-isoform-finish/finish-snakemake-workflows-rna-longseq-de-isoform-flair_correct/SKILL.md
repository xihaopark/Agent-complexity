---
name: finish-snakemake-workflows-rna-longseq-de-isoform-flair_correct
description: Use this skill when orchestrating the retained "flair_correct" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the flair correct stage tied to upstream `flair_align` and the downstream handoff to `flair_collapse`. It tracks completion via `results/finish/flair_correct.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: flair_correct
  step_name: flair correct
---

# Scope
Use this skill only for the `flair_correct` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `flair_align`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/flair_correct.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/flair_correct.done`
- Representative outputs: `results/finish/flair_correct.done`
- Execution targets: `flair_correct`
- Downstream handoff: `flair_collapse`

## Guardrails
- Treat `results/finish/flair_correct.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/flair_correct.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `flair_collapse` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/flair_correct.done` exists and `flair_collapse` can proceed without re-running flair correct.
