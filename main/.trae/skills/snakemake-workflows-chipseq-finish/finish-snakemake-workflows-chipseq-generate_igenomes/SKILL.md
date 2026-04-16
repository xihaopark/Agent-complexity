---
name: finish-snakemake-workflows-chipseq-generate_igenomes
description: Use this skill when orchestrating the retained "generate_igenomes" step of the snakemake workflows chipseq finish finish workflow. It keeps the generate igenomes stage tied to upstream `chromosome_size` and the downstream handoff to `generate_igenomes_blacklist`. It tracks completion via `results/finish/generate_igenomes.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: generate_igenomes
  step_name: generate igenomes
---

# Scope
Use this skill only for the `generate_igenomes` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `chromosome_size`
- Step file: `finish/chipseq-finish/steps/generate_igenomes.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/generate_igenomes.done`
- Representative outputs: `results/finish/generate_igenomes.done`
- Execution targets: `generate_igenomes`
- Downstream handoff: `generate_igenomes_blacklist`

## Guardrails
- Treat `results/finish/generate_igenomes.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/generate_igenomes.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `generate_igenomes_blacklist` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/generate_igenomes.done` exists and `generate_igenomes_blacklist` can proceed without re-running generate igenomes.
