---
name: finish-snakemake-workflows-chipseq-bedgraphtobigwig
description: Use this skill when orchestrating the retained "bedGraphToBigWig" step of the snakemake workflows chipseq finish finish workflow. It keeps the bedGraphToBigWig stage tied to upstream `sort_genomecov` and the downstream handoff to `create_igv_bigwig`. It tracks completion via `results/finish/bedGraphToBigWig.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: bedGraphToBigWig
  step_name: bedGraphToBigWig
---

# Scope
Use this skill only for the `bedGraphToBigWig` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `sort_genomecov`
- Step file: `finish/chipseq-finish/steps/bedGraphToBigWig.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bedGraphToBigWig.done`
- Representative outputs: `results/finish/bedGraphToBigWig.done`
- Execution targets: `bedGraphToBigWig`
- Downstream handoff: `create_igv_bigwig`

## Guardrails
- Treat `results/finish/bedGraphToBigWig.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bedGraphToBigWig.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `create_igv_bigwig` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bedGraphToBigWig.done` exists and `create_igv_bigwig` can proceed without re-running bedGraphToBigWig.
