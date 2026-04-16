---
name: finish-mckellardw-slide-snake-ilmn_4a_kbpython_std_remove_suffix
description: Use this skill when orchestrating the retained "ilmn_4a_kbpython_std_remove_suffix" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 4a kbpython std remove suffix stage tied to upstream `ilmn_4a_kbpython_std` and the downstream handoff to `ilmn_4a_kbpython_std_compress_outs`. It tracks completion via `results/finish/ilmn_4a_kbpython_std_remove_suffix.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_4a_kbpython_std_remove_suffix
  step_name: ilmn 4a kbpython std remove suffix
---

# Scope
Use this skill only for the `ilmn_4a_kbpython_std_remove_suffix` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_4a_kbpython_std`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_4a_kbpython_std_remove_suffix.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_4a_kbpython_std_remove_suffix.done`
- Representative outputs: `results/finish/ilmn_4a_kbpython_std_remove_suffix.done`
- Execution targets: `ilmn_4a_kbpython_std_remove_suffix`
- Downstream handoff: `ilmn_4a_kbpython_std_compress_outs`

## Guardrails
- Treat `results/finish/ilmn_4a_kbpython_std_remove_suffix.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_4a_kbpython_std_remove_suffix.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_4a_kbpython_std_compress_outs` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_4a_kbpython_std_remove_suffix.done` exists and `ilmn_4a_kbpython_std_compress_outs` can proceed without re-running ilmn 4a kbpython std remove suffix.
