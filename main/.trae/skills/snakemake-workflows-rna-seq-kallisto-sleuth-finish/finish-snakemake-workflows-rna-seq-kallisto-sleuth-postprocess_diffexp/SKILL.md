---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-postprocess_diffexp
description: Use this skill when orchestrating the retained "postprocess_diffexp" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the postprocess diffexp stage tied to upstream `postprocess_go_enrichment` and the downstream handoff to `postprocess_tpm_matrix`. It tracks completion via `results/finish/postprocess_diffexp.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: postprocess_diffexp
  step_name: postprocess diffexp
---

# Scope
Use this skill only for the `postprocess_diffexp` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `postprocess_go_enrichment`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/postprocess_diffexp.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/postprocess_diffexp.done`
- Representative outputs: `results/finish/postprocess_diffexp.done`
- Execution targets: `postprocess_diffexp`
- Downstream handoff: `postprocess_tpm_matrix`

## Guardrails
- Treat `results/finish/postprocess_diffexp.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/postprocess_diffexp.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `postprocess_tpm_matrix` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/postprocess_diffexp.done` exists and `postprocess_tpm_matrix` can proceed without re-running postprocess diffexp.
