---
name: finish-snakemake-workflows-dna-seq-benchmark-annotate_shared_fn
description: Use this skill when orchestrating the retained "annotate_shared_fn" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the annotate shared fn stage tied to upstream `tabix_revel_scores` and the downstream handoff to `annotate_unique_fp_fn`. It tracks completion via `results/finish/annotate_shared_fn.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: annotate_shared_fn
  step_name: annotate shared fn
---

# Scope
Use this skill only for the `annotate_shared_fn` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `tabix_revel_scores`
- Step file: `finish/dna-seq-benchmark-finish/steps/annotate_shared_fn.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/annotate_shared_fn.done`
- Representative outputs: `results/finish/annotate_shared_fn.done`
- Execution targets: `annotate_shared_fn`
- Downstream handoff: `annotate_unique_fp_fn`

## Guardrails
- Treat `results/finish/annotate_shared_fn.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/annotate_shared_fn.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `annotate_unique_fp_fn` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/annotate_shared_fn.done` exists and `annotate_unique_fp_fn` can proceed without re-running annotate shared fn.
