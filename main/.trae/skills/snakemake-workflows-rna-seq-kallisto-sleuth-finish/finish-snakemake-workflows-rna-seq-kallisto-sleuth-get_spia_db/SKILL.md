---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-get_spia_db
description: Use this skill when orchestrating the retained "get_spia_db" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the get spia db stage tied to upstream `calculate_cpat_logit_model` and the downstream handoff to `cds_polyA_T_removal`. It tracks completion via `results/finish/get_spia_db.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: get_spia_db
  step_name: get spia db
---

# Scope
Use this skill only for the `get_spia_db` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `calculate_cpat_logit_model`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/get_spia_db.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_spia_db.done`
- Representative outputs: `results/finish/get_spia_db.done`
- Execution targets: `get_spia_db`
- Downstream handoff: `cds_polyA_T_removal`

## Guardrails
- Treat `results/finish/get_spia_db.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_spia_db.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `cds_polyA_T_removal` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_spia_db.done` exists and `cds_polyA_T_removal` can proceed without re-running get spia db.
