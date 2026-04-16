---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-spia
description: Use this skill when orchestrating the retained "spia" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the spia stage tied to upstream `annotate_isoform_switch` and the downstream handoff to `fgsea`. It tracks completion via `results/finish/spia.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: spia
  step_name: spia
---

# Scope
Use this skill only for the `spia` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `annotate_isoform_switch`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/spia.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/spia.done`
- Representative outputs: `results/finish/spia.done`
- Execution targets: `spia`
- Downstream handoff: `fgsea`

## Guardrails
- Treat `results/finish/spia.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/spia.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `fgsea` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/spia.done` exists and `fgsea` can proceed without re-running spia.
