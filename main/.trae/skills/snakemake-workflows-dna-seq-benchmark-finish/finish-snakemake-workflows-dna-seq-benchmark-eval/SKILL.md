---
name: finish-snakemake-workflows-dna-seq-benchmark-eval
description: Use this skill when orchestrating the retained "eval" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the eval stage and the downstream handoff to `norm_vcf`. It tracks completion via `results/finish/eval.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: eval
  step_name: eval
---

# Scope
Use this skill only for the `eval` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/dna-seq-benchmark-finish/steps/eval.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/eval.done`
- Representative outputs: `results/finish/eval.done`
- Execution targets: `eval`
- Downstream handoff: `norm_vcf`

## Guardrails
- Treat `results/finish/eval.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/eval.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `norm_vcf` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/eval.done` exists and `norm_vcf` can proceed without re-running eval.
