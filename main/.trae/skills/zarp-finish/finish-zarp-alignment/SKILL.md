---
name: finish-zarp-alignment
description: Use this skill when orchestrating the retained "alignment" step of the Zarp finish workflow. It connects trimmed reads to transcriptome or genome alignment outputs and prepares quantification.
metadata:
  workflow_id: zarp-finish
  workflow_name: Zarp Finish Workflow
  step_id: alignment
  step_name: Align reads to the transcriptome or genome
---

# Scope
Use this skill only for the `alignment` step in `zarp-finish`.

## Orchestration
- Upstream requirements: `trimming`
- Step file: `finish/zarp-finish/steps/alignment.smk`
- Config file: `finish/zarp-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/alignment.done`
- Representative outputs: `output/alignment/*`
- Execution targets: `alignment_ready`
- Downstream handoff: `quantification`

## Guardrails
- Treat `results/finish/alignment.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage scoped to alignment products that quantification can reuse directly.

## Done Criteria
Mark this step complete only when alignment outputs are present and the quantification stage can start without revisiting trimming.
