---
name: finish-snakemake-workflows-dna-seq-benchmark-tabix_revel_scores
description: Use this skill when orchestrating the retained "tabix_revel_scores" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the tabix revel scores stage tied to upstream `process_revel_scores` and the downstream handoff to `annotate_shared_fn`. It tracks completion via `results/finish/tabix_revel_scores.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: tabix_revel_scores
  step_name: tabix revel scores
---

# Scope
Use this skill only for the `tabix_revel_scores` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `process_revel_scores`
- Step file: `finish/dna-seq-benchmark-finish/steps/tabix_revel_scores.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/tabix_revel_scores.done`
- Representative outputs: `results/finish/tabix_revel_scores.done`
- Execution targets: `tabix_revel_scores`
- Downstream handoff: `annotate_shared_fn`

## Guardrails
- Treat `results/finish/tabix_revel_scores.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/tabix_revel_scores.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `annotate_shared_fn` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/tabix_revel_scores.done` exists and `annotate_shared_fn` can proceed without re-running tabix revel scores.
