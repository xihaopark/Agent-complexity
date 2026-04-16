---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-sleuth_init
description: Use this skill when orchestrating the retained "sleuth_init" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the sleuth init stage tied to upstream `compose_sample_sheet` and the downstream handoff to `sleuth_diffexp`. It tracks completion via `results/finish/sleuth_init.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: sleuth_init
  step_name: sleuth init
---

# Scope
Use this skill only for the `sleuth_init` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `compose_sample_sheet`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/sleuth_init.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/sleuth_init.done`
- Representative outputs: `results/finish/sleuth_init.done`
- Execution targets: `sleuth_init`
- Downstream handoff: `sleuth_diffexp`

## Guardrails
- Treat `results/finish/sleuth_init.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/sleuth_init.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `sleuth_diffexp` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/sleuth_init.done` exists and `sleuth_diffexp` can proceed without re-running sleuth init.
