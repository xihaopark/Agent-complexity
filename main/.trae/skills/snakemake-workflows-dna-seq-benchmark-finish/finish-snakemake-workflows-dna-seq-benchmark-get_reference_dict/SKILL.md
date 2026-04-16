---
name: finish-snakemake-workflows-dna-seq-benchmark-get_reference_dict
description: Use this skill when orchestrating the retained "get_reference_dict" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the get reference dict stage tied to upstream `stratify_regions` and the downstream handoff to `merge_callsets`. It tracks completion via `results/finish/get_reference_dict.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: get_reference_dict
  step_name: get reference dict
---

# Scope
Use this skill only for the `get_reference_dict` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `stratify_regions`
- Step file: `finish/dna-seq-benchmark-finish/steps/get_reference_dict.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_reference_dict.done`
- Representative outputs: `results/finish/get_reference_dict.done`
- Execution targets: `get_reference_dict`
- Downstream handoff: `merge_callsets`

## Guardrails
- Treat `results/finish/get_reference_dict.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_reference_dict.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merge_callsets` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_reference_dict.done` exists and `merge_callsets` can proceed without re-running get reference dict.
