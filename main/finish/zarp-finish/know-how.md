# Zarp finish workflow

## 审计结论

- 已核对 `steps/*.smk`、workflow 内 `run_workflow.py` 与统一入口 `finish/run_finish_workflow.py`
- 保留步骤共 6 个：`validate_config` → `stage_inputs` → `trimming` → `alignment` → `quantification` → `finish_target`
- Renzo 发现别名：`zarp`、`rna-zarp`、`zarp-rnaseq`
- workflow 聚焦输入整理、核心 RNA-seq 处理链路和最终 finish 交付集合

## 执行契约

- 工作目录固定为 `/lab_workspace/projects/Agent-complexity/main/finish/zarp-finish`
- 使用共享环境：`conda run -n snakemake python -m snakemake`
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

- 目标：验证 Zarp 所需配置项、样本定义和参考路径
- 成功信号：配置检查通过
- 失败优先排查：样本表字段、参考资源声明、输出目录设置

### stage_inputs

- 目标：把原始 reads 和元数据整理到 workflow 统一输入布局
- 依赖：`validate_config`
- 成功信号：`output/staged_inputs/*` 可用
- 失败优先排查：输入路径、样本命名和 staging 目录权限

### trimming

- 目标：对 staged reads 做修剪和基础清洗
- 依赖：`stage_inputs`
- 成功信号：`output/trimmed/*`
- 失败优先排查：reads 配对关系、trimming 参数和中间磁盘空间

### alignment

- 目标：对修剪后的 reads 进行比对
- 依赖：`trimming`
- 成功信号：`output/alignment/*` 中出现主要比对产物
- 失败优先排查：参考索引、比对器参数、样本 ID 映射

### quantification

- 目标：从比对结果生成表达量或覆盖度相关结果
- 依赖：`alignment`
- 成功信号：`output/quantification/*`
- 失败优先排查：上游 BAM 是否完整、注释文件和参考版本

### finish_target

- 目标：收敛所有必需交付物，生成 finish workflow 最终输出集合
- 依赖：`quantification`
- 成功信号：`output/multiqc_report.html` 与样本级 `.bigWig` 输出存在
- 失败优先排查：交付清单、MultiQC 输入源、必需产物是否齐备
