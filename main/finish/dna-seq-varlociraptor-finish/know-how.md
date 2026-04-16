# DNA-seq Varlociraptor finish workflow

## 审计结论

- 已核对 `steps/*.smk`、workflow 内 `run_workflow.py` 与统一入口 `finish/run_finish_workflow.py`
- 保留步骤共 10 个：`validate_config` → `inspect_inputs` → `prepare_references` → `prepare_reads` → `mapping` → `candidate_calling` → `evidence_build` → `calling` → `annotation_filtering` → `delivery_report`
- Renzo 发现别名：`varlociraptor`、`dna-seq-varlociraptor`、`variant-calling`
- workflow 关注肿瘤/对照输入准备、证据构建、最终变异输出与交付报告

## 执行契约

- 工作目录固定为 `/lab_workspace/projects/Agent-complexity/main/finish/dna-seq-varlociraptor-finish`
- 共享执行环境：`conda run -n snakemake python -m snakemake`
- 按依赖顺序单步执行；任何失败都应先定位最近一步的输入完整性
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

- 目标：验证样本、对照配对和资源配置
- 成功信号：配置检查通过且关键路径可解析
- 失败优先排查：tumor/normal 样本映射、参考文件声明、可选模块开关

### inspect_inputs

- 目标：确认 FASTQ/BAM 输入是否完整、配对是否合理
- 依赖：`validate_config`
- 成功信号：输入盘点信息生成且无缺失样本
- 失败优先排查：文件命名、lane 合并策略、压缩文件损坏

### prepare_references

- 目标：准备参考 genome、索引和注释 bundle
- 依赖：`inspect_inputs`
- 成功信号：参考 bundle 可被 mapping/calling 重用
- 失败优先排查：参考版本是否一致、索引构建是否中断

### prepare_reads

- 目标：把原始测序输入整理成 mapping 友好的布局
- 依赖：`prepare_references`
- 成功信号：`results/prepared_reads/*` 可用
- 失败优先排查：样本标签、read group 信息、文件权限

### mapping

- 目标：生成比对 BAM 及其索引
- 依赖：`prepare_reads`
- 成功信号：`results/alignment/*.bam` 与 `.bai`
- 失败优先排查：参考索引、线程/内存、磁盘空间

### candidate_calling

- 目标：从比对结果生成候选变异集合
- 依赖：`mapping`
- 成功信号：`results/candidates/*.bcf`
- 失败优先排查：BAM 索引、样本配对、调用器参数

### evidence_build

- 目标：为最终 calling 汇总覆盖度、证据与中间统计
- 依赖：`candidate_calling`
- 成功信号：`results/evidence/*` 已生成
- 失败优先排查：候选位点是否为空、上游中间文件是否缺失

### calling

- 目标：执行最终 varlociraptor calling 并生成高可信结果
- 依赖：`evidence_build`
- 成功信号：`results/final/*.bcf`
- 失败优先排查：证据目录、过滤参数、参考与样本一致性

### annotation_filtering

- 目标：对最终 calling 结果做注释、过滤和交付前整理
- 依赖：`calling`
- 成功信号：注释目录与 MAF/表格结果已生成
- 失败优先排查：注释数据库、过滤阈值、结果字段兼容性

### delivery_report

- 目标：把最终 BCF、注释表和报告资产收敛成用户交付物
- 依赖：`annotation_filtering`
- 成功信号：`results/reports/datavzrd/index.html` 与 MAF 表存在
- 失败优先排查：交付清单、datavzrd 索引文件、上游产物路径
