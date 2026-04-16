---
name: finish-snakemake-workflows-dna-seq-benchmark-stratify_regions
description: Use this skill when orchestrating the retained "stratify_regions" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the stratify regions stage tied to upstream `mosdepth` and the downstream handoff to `get_reference_dict`. It tracks completion via `results/finish/stratify_regions.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: stratify_regions
  step_name: stratify regions
---

# Scope
Use this skill only for the `stratify_regions` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `mosdepth`
- Step file: `finish/dna-seq-benchmark-finish/steps/stratify_regions.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/stratify_regions.done`
- Representative outputs: `results/finish/stratify_regions.done`
- Execution targets: `stratify_regions`
- Downstream handoff: `get_reference_dict`

## Guardrails
- Treat `results/finish/stratify_regions.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/stratify_regions.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_reference_dict` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/stratify_regions.done` exists and `get_reference_dict` can proceed without re-running stratify regions.
