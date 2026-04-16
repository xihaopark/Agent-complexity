---
name: finish-snakemake-workflows-dna-seq-benchmark-get_reference
description: Use this skill when orchestrating the retained "get_reference" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the get reference stage tied to upstream `postprocess_target_bed` and the downstream handoff to `get_liftover_chain`. It tracks completion via `results/finish/get_reference.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: get_reference
  step_name: get reference
---

# Scope
Use this skill only for the `get_reference` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `postprocess_target_bed`
- Step file: `finish/dna-seq-benchmark-finish/steps/get_reference.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_reference.done`
- Representative outputs: `results/finish/get_reference.done`
- Execution targets: `get_reference`
- Downstream handoff: `get_liftover_chain`

## Guardrails
- Treat `results/finish/get_reference.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_reference.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_liftover_chain` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_reference.done` exists and `get_liftover_chain` can proceed without re-running get reference.
