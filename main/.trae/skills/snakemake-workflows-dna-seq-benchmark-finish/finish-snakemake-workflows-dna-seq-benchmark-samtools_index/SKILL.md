---
name: finish-snakemake-workflows-dna-seq-benchmark-samtools_index
description: Use this skill when orchestrating the retained "samtools_index" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the samtools index stage tied to upstream `mark_duplicates` and the downstream handoff to `mosdepth`. It tracks completion via `results/finish/samtools_index.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: samtools_index
  step_name: samtools index
---

# Scope
Use this skill only for the `samtools_index` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `mark_duplicates`
- Step file: `finish/dna-seq-benchmark-finish/steps/samtools_index.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/samtools_index.done`
- Representative outputs: `results/finish/samtools_index.done`
- Execution targets: `samtools_index`
- Downstream handoff: `mosdepth`

## Guardrails
- Treat `results/finish/samtools_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/samtools_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `mosdepth` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/samtools_index.done` exists and `mosdepth` can proceed without re-running samtools index.
