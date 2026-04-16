# Smoke Run Report (2026-04-14)

## Goal

在启动 30-workflow 正式实验前，先用 3 个 workflow 做 smoke benchmark，验证：

- 多 agent 运行链路是否稳定
- 真实框架（biomni / stella）是否可正常接入
- 共享 env / shared conda cache 是否不再引发基础 infra 问题
- workflow 本身是否具备进入正式 benchmark 的“可运行性”

## Smoke Attempt 1

### Workflow

- `dwheelerau-snakemake-rnaseq-counts-finish`

### Result

- 5 个 agents 全部失败

### Root Cause

- 失败发生在最早的 `project_setup` 步骤
- 原始 `Snakefile` 中命令生成为 `None`
- Snakemake 报错：
  - `Shell command: None`
  - `SyntaxError: Command must be given as string after the shell keyword`

### Interpretation

- 这是 workflow 本身 / finish step generation 的协议问题
- 不是 agent 编排差异，也不是共享 env / 磁盘缓存问题
- 该 workflow 不适合作为当前主实验集样本，已从 smoke/core 候选中移除

## Smoke Attempt 2

### Workflow

- `rna-seq-star-deseq2-finish`

### Result

- 5 个 agents 全部失败

### Root Cause

- 失败发生在最早的 `get_genome` 链路
- 深层报错是 workflow DAG 构建阶段的 `MissingInputException`
- 缺失输入：
  - `A.1.fq.gz`
  - `A.2.fq.gz`

### Interpretation

- 当前 workflow candidate / staged input setup 不完整
- 这是 workflow readiness / input provisioning 问题
- 同样不是 agent 之间的能力差异

## Conclusion

当前 smoke benchmark **不符合进入 30-workflow 正式实验的预期**。

原因不是共享 env 或真实框架接入失败，而是：

1. 部分 workflow candidate 自身存在协议 / step generation 问题
2. 部分 workflow candidate 依赖的输入数据尚未在当前 finish 运行上下文中正确准备

因此，**现在不应直接启动 30-workflow 正式实验**。

## Immediate Recommendation

下一步应该先做 `workflow readiness gate`，至少覆盖：

- `project_setup` 是否能生成合法 Snakemake step
- config 是否指向可用输入
- required FASTQ / reference / metadata 是否可见
- smoke workflow 是否能至少在 Renzo baseline 上完成首个关键 step

只有 readiness gate 通过后，再继续：

- 3-workflow smoke rerun
- 30-workflow 正式 benchmark
