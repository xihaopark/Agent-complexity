---
name: finish-snakemake-workflows-chipseq-create_consensus_saf
description: Use this skill when orchestrating the retained "create_consensus_saf" step of the snakemake workflows chipseq finish finish workflow. It keeps the create consensus saf stage tied to upstream `create_consensus_bed` and the downstream handoff to `plot_peak_intersect`. It tracks completion via `results/finish/create_consensus_saf.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: create_consensus_saf
  step_name: create consensus saf
---

# Scope
Use this skill only for the `create_consensus_saf` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `create_consensus_bed`
- Step file: `finish/chipseq-finish/steps/create_consensus_saf.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/create_consensus_saf.done`
- Representative outputs: `results/finish/create_consensus_saf.done`
- Execution targets: `create_consensus_saf`
- Downstream handoff: `plot_peak_intersect`

## Guardrails
- Treat `results/finish/create_consensus_saf.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/create_consensus_saf.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_peak_intersect` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/create_consensus_saf.done` exists and `plot_peak_intersect` can proceed without re-running create consensus saf.
