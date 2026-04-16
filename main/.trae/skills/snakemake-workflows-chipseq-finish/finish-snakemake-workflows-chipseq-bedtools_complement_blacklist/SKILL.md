---
name: finish-snakemake-workflows-chipseq-bedtools_complement_blacklist
description: Use this skill when orchestrating the retained "bedtools_complement_blacklist" step of the snakemake workflows chipseq finish finish workflow. It keeps the bedtools complement blacklist stage tied to upstream `bedtools_sort_blacklist` and the downstream handoff to `get_gsize`. It tracks completion via `results/finish/bedtools_complement_blacklist.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: bedtools_complement_blacklist
  step_name: bedtools complement blacklist
---

# Scope
Use this skill only for the `bedtools_complement_blacklist` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `bedtools_sort_blacklist`
- Step file: `finish/chipseq-finish/steps/bedtools_complement_blacklist.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bedtools_complement_blacklist.done`
- Representative outputs: `results/finish/bedtools_complement_blacklist.done`
- Execution targets: `bedtools_complement_blacklist`
- Downstream handoff: `get_gsize`

## Guardrails
- Treat `results/finish/bedtools_complement_blacklist.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bedtools_complement_blacklist.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_gsize` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bedtools_complement_blacklist.done` exists and `get_gsize` can proceed without re-running bedtools complement blacklist.
