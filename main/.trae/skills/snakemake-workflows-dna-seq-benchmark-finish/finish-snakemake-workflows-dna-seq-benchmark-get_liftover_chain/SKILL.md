---
name: finish-snakemake-workflows-dna-seq-benchmark-get_liftover_chain
description: Use this skill when orchestrating the retained "get_liftover_chain" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the get liftover chain stage tied to upstream `get_reference` and the downstream handoff to `samtools_faidx`. It tracks completion via `results/finish/get_liftover_chain.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: get_liftover_chain
  step_name: get liftover chain
---

# Scope
Use this skill only for the `get_liftover_chain` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `get_reference`
- Step file: `finish/dna-seq-benchmark-finish/steps/get_liftover_chain.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_liftover_chain.done`
- Representative outputs: `results/finish/get_liftover_chain.done`
- Execution targets: `get_liftover_chain`
- Downstream handoff: `samtools_faidx`

## Guardrails
- Treat `results/finish/get_liftover_chain.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_liftover_chain.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `samtools_faidx` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_liftover_chain.done` exists and `samtools_faidx` can proceed without re-running get liftover chain.
