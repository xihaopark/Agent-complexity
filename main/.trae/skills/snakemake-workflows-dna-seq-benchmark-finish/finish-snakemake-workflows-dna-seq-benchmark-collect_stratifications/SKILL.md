---
name: finish-snakemake-workflows-dna-seq-benchmark-collect_stratifications
description: Use this skill when orchestrating the retained "collect_stratifications" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the collect stratifications stage tied to upstream `calc_precision_recall` and the downstream handoff to `collect_precision_recall`. It tracks completion via `results/finish/collect_stratifications.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: collect_stratifications
  step_name: collect stratifications
---

# Scope
Use this skill only for the `collect_stratifications` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `calc_precision_recall`
- Step file: `finish/dna-seq-benchmark-finish/steps/collect_stratifications.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/collect_stratifications.done`
- Representative outputs: `results/finish/collect_stratifications.done`
- Execution targets: `collect_stratifications`
- Downstream handoff: `collect_precision_recall`

## Guardrails
- Treat `results/finish/collect_stratifications.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/collect_stratifications.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `collect_precision_recall` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/collect_stratifications.done` exists and `collect_precision_recall` can proceed without re-running collect stratifications.
