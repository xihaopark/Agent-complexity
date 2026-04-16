---
name: finish-snakemake-workflows-chipseq-generate_igenomes_blacklist
description: Use this skill when orchestrating the retained "generate_igenomes_blacklist" step of the snakemake workflows chipseq finish finish workflow. It keeps the generate igenomes blacklist stage tied to upstream `generate_igenomes` and the downstream handoff to `bedtools_sort_blacklist`. It tracks completion via `results/finish/generate_igenomes_blacklist.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: generate_igenomes_blacklist
  step_name: generate igenomes blacklist
---

# Scope
Use this skill only for the `generate_igenomes_blacklist` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `generate_igenomes`
- Step file: `finish/chipseq-finish/steps/generate_igenomes_blacklist.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/generate_igenomes_blacklist.done`
- Representative outputs: `results/finish/generate_igenomes_blacklist.done`
- Execution targets: `generate_igenomes_blacklist`
- Downstream handoff: `bedtools_sort_blacklist`

## Guardrails
- Treat `results/finish/generate_igenomes_blacklist.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/generate_igenomes_blacklist.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bedtools_sort_blacklist` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/generate_igenomes_blacklist.done` exists and `bedtools_sort_blacklist` can proceed without re-running generate igenomes blacklist.
