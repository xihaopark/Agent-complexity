# R-task stub: `rna-seq-kallisto-sleuth-finish` / `setup_config_and_inputs`

> **Status:** stub — evaluation inputs, metrics, and gold outputs are **not** filled in yet.
> Pipeline overlay comes from `paper_primary_benchmark/task_definitions/rna-seq-kallisto-sleuth-finish.json`.

## Stage

- **Label:** 配置校验与输入规范化
- **Order:** 1
- **Finish manifest (reference):** `finish/rna-seq-kallisto-sleuth-finish/manifest.json`

## Snakemake steps in this stage

- `validate_config`
- `normalize_inputs`

## Summary (from task_definitions metadata)

Validate YAML/samples/units and normalize metadata paths.

### Declared inputs (path hints)
- **workflow_config** — `config_basic/config.yaml` — Finish step-split config driving Snakemake.
- **samplesheet** — `config_basic/samples.tsv`
- **units** — `config_basic/units.tsv`

### Declared outputs (path hints)
- **checkpoint** — `results/finish/normalize_inputs.done` — (from steps: normalize_inputs)

## TODO — fill before marking `status: ready` in registry

1. **Data:** Place minimal inputs under `input/` (or document symlinks/capsules). Do not commit large raw data without LFS or external URLs.
2. **Objective:** Replace this stub text with precise success criteria (files, metrics, thresholds).
3. **Gold / baseline:** Optional path to expected artifacts or a Snakemake/finish command used to produce reference outputs.
4. **Environment:** Note R/Bioconductor/conda requirements if different from the default pilot.

## Default env hint

`RTaskEvalEnv` expects a success artifact (see registry `success_artifact_glob`, default `output/result.txt`) before `submit_done(success=true)` with reward.
