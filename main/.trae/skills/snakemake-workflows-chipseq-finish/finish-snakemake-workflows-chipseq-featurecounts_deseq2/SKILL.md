---
name: finish-snakemake-workflows-chipseq-featurecounts_deseq2
description: Use this skill when orchestrating the retained "featurecounts_deseq2" step of the snakemake workflows chipseq finish finish workflow. It keeps the featurecounts deseq2 stage tied to upstream `featurecounts_modified_colnames` and the downstream handoff to `create_deseq2_igv`. It tracks completion via `results/finish/featurecounts_deseq2.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: featurecounts_deseq2
  step_name: featurecounts deseq2
---

# Scope
Use this skill only for the `featurecounts_deseq2` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `featurecounts_modified_colnames`
- Step file: `finish/chipseq-finish/steps/featurecounts_deseq2.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/featurecounts_deseq2.done`
- Representative outputs: `results/finish/featurecounts_deseq2.done`
- Execution targets: `featurecounts_deseq2`
- Downstream handoff: `create_deseq2_igv`

## Guardrails
- Treat `results/finish/featurecounts_deseq2.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/featurecounts_deseq2.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `create_deseq2_igv` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/featurecounts_deseq2.done` exists and `create_deseq2_igv` can proceed without re-running featurecounts deseq2.
