---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-cds_polya_t_removal
description: Use this skill when orchestrating the retained "cds_polyA_T_removal" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the cds polyA T removal stage tied to upstream `get_spia_db` and the downstream handoff to `get_main_transcripts_fasta`. It tracks completion via `results/finish/cds_polyA_T_removal.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: cds_polyA_T_removal
  step_name: cds polyA T removal
---

# Scope
Use this skill only for the `cds_polyA_T_removal` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `get_spia_db`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/cds_polyA_T_removal.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/cds_polyA_T_removal.done`
- Representative outputs: `results/finish/cds_polyA_T_removal.done`
- Execution targets: `cds_polyA_T_removal`
- Downstream handoff: `get_main_transcripts_fasta`

## Guardrails
- Treat `results/finish/cds_polyA_T_removal.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/cds_polyA_T_removal.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_main_transcripts_fasta` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/cds_polyA_T_removal.done` exists and `get_main_transcripts_fasta` can proceed without re-running cds polyA T removal.
