---
name: finish-zarp-finish-target
description: Use this skill when orchestrating the retained "finish_target" step of the Zarp finish workflow. It captures the terminal aggregation stage that collects final QC and bigWig outputs for delivery.
metadata:
  workflow_id: zarp-finish
  workflow_name: Zarp Finish Workflow
  step_id: finish_target
  step_name: Assemble final finish outputs
---

# Scope
Use this skill only for the `finish_target` step in `zarp-finish`.

## Orchestration
- Upstream requirements: `quantification`
- Step file: `finish/zarp-finish/steps/finish_target.smk`
- Config file: `finish/zarp-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/finish_target.done`
- Representative outputs: `results/{organism}/multiqc_summary`, `results/{organism}/summary_salmon/quantmerge/genes_tpm.tsv`, `results/{organism}/summary_kallisto/genes_tpm.tsv`, `results/{organism}/samples/{sample}/bigWig/UniqueMappers/{sample}_UniqueMappers_plus.bw`, `results/{organism}/samples/{sample}/bigWig/MultimappersIncluded/{sample}_MultimappersIncluded_plus.bw`
- Execution targets: `results/{organism}/multiqc_summary`
- Downstream handoff: none

## Guardrails
- Treat `results/finish/finish_target.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage packaging-oriented: aggregate final reports and coverage tracks without rerunning upstream quantification.

## Done Criteria
Mark this step complete only when the final MultiQC summary, merged quantification tables, and exported bigWig tracks exist. Do not require auxiliary TIN outputs to block this wrapped finish step.
