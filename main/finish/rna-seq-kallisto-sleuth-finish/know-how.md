# RNA-seq Kallisto Sleuth finish workflow

## 审计结论

- 已核对 `steps/*.smk`、目录内 `run_workflow.py` 与统一入口 `finish/run_finish_workflow.py`
- 保留步骤共 9 个：`validate_config` → `normalize_inputs` → `prepare_references` → `prepare_reads` → `quantify` → `init_sleuth` → `differential_expression` → `optional_modules` → `delivery_report`
- Renzo 发现别名：`kallisto`、`rna-seq-kallisto`、`sleuth`
- workflow 面向本地配置、参考数据、测试 reads 和最终交付报告

## 执行契约

- 始终在当前 workflow 根目录执行：`/lab_workspace/projects/Agent-complexity/main/finish/rna-seq-kallisto-sleuth-finish`
- 优先使用共享环境：`conda run -n snakemake python -m snakemake`
- 单步执行，不跨步并行，不跳过显式依赖
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

- 目标：确认配置、样本表和单位表满足后续量化要求
- 成功信号：配置检查规则完成且无 schema/路径错误
- 失败优先排查：配置键名、样本 ID、读长与路径格式

### normalize_inputs

- 目标：把样本元数据和输入命名规整为后续步骤统一格式
- 依赖：`validate_config`
- 成功信号：标准化输入目录或中间表已生成
- 失败优先排查：样本命名冲突、分组字段缺失

### prepare_references

- 目标：准备 transcriptome/reference 索引供 kallisto 使用
- 依赖：`normalize_inputs`
- 成功信号：参考索引文件存在于本地资源目录
- 失败优先排查：参考 fasta/gtf 是否匹配、索引是否完整

### prepare_reads

- 目标：把 reads 整理成量化步骤可直接消费的布局
- 依赖：`prepare_references`
- 成功信号：`results/prepared_reads/*` 可用
- 失败优先排查：read pair 配对关系、压缩文件是否损坏

### quantify

- 目标：运行 kallisto 生成样本级 abundance 结果
- 依赖：`prepare_reads`
- 成功信号：`results/kallisto/*/abundance.tsv`
- 失败优先排查：索引路径、样本表、线程/内存配置

### init_sleuth

- 目标：把 abundance 结果组织为 sleuth 模型输入
- 依赖：`quantify`
- 成功信号：sleuth 中间对象或输入目录已生成
- 失败优先排查：样本条件列、量化目录结构、bioconductor 依赖

### differential_expression

- 目标：运行 sleuth 差异表达分析并导出统计结果
- 依赖：`init_sleuth`
- 成功信号：`results/diffexp/*/*.tsv` 与差异图表已生成
- 失败优先排查：对比设计、重复数、模型公式

### optional_modules

- 目标：执行可选比较或增强模块并补充交付材料
- 依赖：`differential_expression`
- 成功信号：可选模块目录下出现新结果
- 失败优先排查：可选开关是否开启、上游 diffexp 结果是否齐全

### delivery_report

- 目标：汇总核心与可选模块结果，生成最终交付视图
- 依赖：`optional_modules`
- 成功信号：`results/datavzrd/*/index.html` 和交付表格存在
- 失败优先排查：交付清单拼装逻辑、datavzrd 输入目录、必需报告是否缺失
