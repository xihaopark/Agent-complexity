---
name: finish-snakemake-workflows-chipseq-create_consensus_bed
description: Use this skill when orchestrating the retained "create_consensus_bed" step of the snakemake workflows chipseq finish finish workflow. It keeps the create consensus bed stage tied to upstream `macs2_merged_expand` and the downstream handoff to `create_consensus_saf`. It tracks completion via `results/finish/create_consensus_bed.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: create_consensus_bed
  step_name: create consensus bed
---

# Scope
Use this skill only for the `create_consensus_bed` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `macs2_merged_expand`
- Step file: `finish/chipseq-finish/steps/create_consensus_bed.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/create_consensus_bed.done`
- Representative outputs: `results/finish/create_consensus_bed.done`
- Execution targets: `create_consensus_bed`
- Downstream handoff: `create_consensus_saf`

## Guardrails
- Treat `results/finish/create_consensus_bed.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/create_consensus_bed.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `create_consensus_saf` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/create_consensus_bed.done` exists and `create_consensus_saf` can proceed without re-running create consensus bed.
