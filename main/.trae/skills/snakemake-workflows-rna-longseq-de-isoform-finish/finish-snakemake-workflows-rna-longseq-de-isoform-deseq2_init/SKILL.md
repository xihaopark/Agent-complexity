---
name: finish-snakemake-workflows-rna-longseq-de-isoform-deseq2_init
description: Use this skill when orchestrating the retained "deseq2_init" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the deseq2 init stage tied to upstream `transcriptid_to_gene` and the downstream handoff to `deseq2`. It tracks completion via `results/finish/deseq2_init.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: deseq2_init
  step_name: deseq2 init
---

# Scope
Use this skill only for the `deseq2_init` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `transcriptid_to_gene`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/deseq2_init.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/deseq2_init.done`
- Representative outputs: `results/finish/deseq2_init.done`
- Execution targets: `deseq2_init`
- Downstream handoff: `deseq2`

## Guardrails
- Treat `results/finish/deseq2_init.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/deseq2_init.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `deseq2` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/deseq2_init.done` exists and `deseq2` can proceed without re-running deseq2 init.
