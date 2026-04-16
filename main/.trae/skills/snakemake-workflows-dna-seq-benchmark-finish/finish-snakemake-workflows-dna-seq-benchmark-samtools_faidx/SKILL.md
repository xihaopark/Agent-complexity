---
name: finish-snakemake-workflows-dna-seq-benchmark-samtools_faidx
description: Use this skill when orchestrating the retained "samtools_faidx" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the samtools faidx stage tied to upstream `get_liftover_chain` and the downstream handoff to `bwa_index`. It tracks completion via `results/finish/samtools_faidx.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: samtools_faidx
  step_name: samtools faidx
---

# Scope
Use this skill only for the `samtools_faidx` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `get_liftover_chain`
- Step file: `finish/dna-seq-benchmark-finish/steps/samtools_faidx.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/samtools_faidx.done`
- Representative outputs: `results/finish/samtools_faidx.done`
- Execution targets: `samtools_faidx`
- Downstream handoff: `bwa_index`

## Guardrails
- Treat `results/finish/samtools_faidx.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/samtools_faidx.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bwa_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/samtools_faidx.done` exists and `bwa_index` can proceed without re-running samtools faidx.
