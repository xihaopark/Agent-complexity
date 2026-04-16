---
name: finish-snakemake-workflows-chipseq-bedtools_sort_blacklist
description: Use this skill when orchestrating the retained "bedtools_sort_blacklist" step of the snakemake workflows chipseq finish finish workflow. It keeps the bedtools sort blacklist stage tied to upstream `generate_igenomes_blacklist` and the downstream handoff to `bedtools_complement_blacklist`. It tracks completion via `results/finish/bedtools_sort_blacklist.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: bedtools_sort_blacklist
  step_name: bedtools sort blacklist
---

# Scope
Use this skill only for the `bedtools_sort_blacklist` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `generate_igenomes_blacklist`
- Step file: `finish/chipseq-finish/steps/bedtools_sort_blacklist.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bedtools_sort_blacklist.done`
- Representative outputs: `results/finish/bedtools_sort_blacklist.done`
- Execution targets: `bedtools_sort_blacklist`
- Downstream handoff: `bedtools_complement_blacklist`

## Guardrails
- Treat `results/finish/bedtools_sort_blacklist.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bedtools_sort_blacklist.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bedtools_complement_blacklist` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bedtools_sort_blacklist.done` exists and `bedtools_complement_blacklist` can proceed without re-running bedtools sort blacklist.
