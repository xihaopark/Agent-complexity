---
name: finish-kallisto-sleuth-init-sleuth
description: Use this skill when orchestrating the retained "init_sleuth" step of the RNA-seq Kallisto Sleuth finish workflow. It connects quantification outputs to sleuth model initialization and sets up the downstream differential-expression analysis.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: RNA-seq Kallisto Sleuth Finish Workflow
  step_id: init_sleuth
  step_name: Initialize sleuth model inputs
---

# Scope
Use this skill only for the `init_sleuth` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `quantify`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/init_sleuth.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/init_sleuth.done`
- Representative outputs: `results/sleuth/model_X.samples.tsv`, `results/sleuth/model_X.rds`, `results/sleuth/model_X.designmatrix.rds`
- Execution targets: `results/sleuth/model_X.samples.tsv`, `results/sleuth/model_X.rds`, `results/sleuth/model_X.designmatrix.rds`
- Downstream handoff: `differential_expression`

## Guardrails
- Treat `results/finish/init_sleuth.done` as the authoritative completion signal for the wrapped finish step.
- Do not invoke this stage via `all --until compose_sample_sheet sleuth_init`; use the explicit sleuth sample-sheet and sleuth object targets instead.
- Preserve the atomic contract of this step: only initialize sleuth inputs needed for downstream diffexp.

## Done Criteria
Mark this step complete only when sleuth-ready model inputs exist and the differential-expression step can start from initialized analysis state.
