# Finish workflow commands

`-finish` 目录下的 workflow 可以直接运行，不依赖 `agent-orchestration`。
每个 finish workflow 目录都包含：

- 本地 `workflow/` 副本
- 本地输入与资源目录
- 本地 `run_workflow.py`

单步命令统一为：

`python3 -m snakemake -s steps/<step>.smk --configfile config_basic/config.yaml --cores 8`

从 `-finish` 根目录统一顺序执行某个 finish workflow 的全部步骤：

`python3 run_finish_workflow.py --workflow <star|kallisto|varlociraptor|template|zarp> --cores 8`

从 `-finish` 根目录只执行部分步骤：

`python3 run_finish_workflow.py --workflow template --from-step validate_config --to-step fastqc --cores 8`

## rna-seq-star-deseq2-finish

- 目录内运行脚本：`python3 run_workflow.py --cores 8`
- trimming.smk
- alignment.smk
- rseqc_qc.smk
- multiqc_report.smk
- count_matrix.smk
- differential_expression.smk
- pca_plot.smk

## rna-seq-kallisto-sleuth-finish

- 目录内运行脚本：`python3 run_workflow.py --cores 8`
- validate_config.smk
- normalize_inputs.smk
- prepare_references.smk
- prepare_reads.smk
- quantify.smk
- init_sleuth.smk
- differential_expression.smk
- optional_modules.smk
- delivery_report.smk

## dna-seq-varlociraptor-finish

- 目录内运行脚本：`python3 run_workflow.py --cores 8`
- validate_config.smk
- inspect_inputs.smk
- prepare_references.smk
- prepare_reads.smk
- mapping.smk
- candidate_calling.smk
- evidence_build.smk
- calling.smk
- annotation_filtering.smk
- delivery_report.smk

## zarp-finish

- 目录内运行脚本：`python3 run_workflow.py --cores 8`
- validate_config.smk
- stage_inputs.smk
- trimming.smk
- alignment.smk
- quantification.smk
- finish_target.smk

## snakemake-workflow-template-finish

- 目录内运行脚本：`python3 run_workflow.py --cores 8`
- validate_config.smk
- prepare_reference.smk
- simulate_reads.smk
- fastqc.smk
- multiqc_report.smk
