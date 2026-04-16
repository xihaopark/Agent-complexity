# Snakemake workflow template finish workflow

## 审计结论

- 已核对 `steps/*.smk`、workflow 内 `run_workflow.py` 与统一入口 `finish/run_finish_workflow.py`
- 保留步骤共 5 个：`validate_config` → `prepare_reference` → `simulate_reads` → `fastqc` → `multiqc_report`
- Renzo 发现别名：`template`、`snakemake-template`、`workflow-template`
- 该 workflow 是最小可运行模板，适合作为新 finish workflow 的结构参考

## 执行契约

- 工作目录固定为 `/lab_workspace/projects/Agent-complexity/main/finish/snakemake-workflow-template-finish`
- 使用共享环境：`conda run -n snakemake python -m snakemake`
- 所有步骤都以 `config_basic/config.yaml` 为唯一配置入口
- 标准命令模板：

```bash
conda run -n snakemake python -m snakemake \
  --snakefile steps/<step>.smk \
  --configfile config_basic/config.yaml \
  --cores 1 \
  --directory .
```

## 标准步骤技能

### validate_config

- 目标：确认模板 workflow 的配置项完整且可执行
- 成功信号：配置验证通过且必需资源路径存在
- 失败优先排查：配置键值、参考路径、输出目录权限

### prepare_reference

- 目标：准备下游模拟和 QC 所需参考资源
- 依赖：`validate_config`
- 成功信号：参考资源文件可被后续规则复用
- 失败优先排查：参考文件缺失、索引准备是否完整

### simulate_reads

- 目标：生成模板样例 reads，验证 workflow 主体逻辑
- 依赖：`prepare_reference`
- 成功信号：`results/simulated_reads/*` 已生成
- 失败优先排查：模拟参数、参考长度、输出目录空间

### fastqc

- 目标：对样例 reads 执行基础质量控制
- 依赖：`simulate_reads`
- 成功信号：`results/fastqc/*` 出现 HTML 和 zip 报告
- 失败优先排查：reads 是否存在、FastQC 依赖、文件格式

### multiqc_report

- 目标：汇总 FastQC 结果并生成 workflow 级最终 HTML 报告
- 依赖：`fastqc`
- 成功信号：`results/multiqc/multiqc_report.html`
- 失败优先排查：MultiQC 输入目录、FastQC 产物命名、报告模板
