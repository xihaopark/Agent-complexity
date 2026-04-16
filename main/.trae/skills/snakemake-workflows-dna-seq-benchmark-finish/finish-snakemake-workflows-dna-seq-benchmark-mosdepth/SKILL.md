---
name: finish-snakemake-workflows-dna-seq-benchmark-mosdepth
description: Use this skill when orchestrating the retained "mosdepth" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the mosdepth stage tied to upstream `samtools_index` and the downstream handoff to `stratify_regions`. It tracks completion via `results/finish/mosdepth.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: mosdepth
  step_name: mosdepth
---

# Scope
Use this skill only for the `mosdepth` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `samtools_index`
- Step file: `finish/dna-seq-benchmark-finish/steps/mosdepth.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/mosdepth.done`
- Representative outputs: `results/finish/mosdepth.done`
- Execution targets: `mosdepth`
- Downstream handoff: `stratify_regions`

## Guardrails
- Treat `results/finish/mosdepth.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/mosdepth.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `stratify_regions` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/mosdepth.done` exists and `stratify_regions` can proceed without re-running mosdepth.
