# Sandbox Preparation Plan

更新日期: 2026-04-10

## 目标

- 在正式 benchmark 前，把 workflow 运行依赖提前准备好。
- 避免运行过程中临时装包、环境污染、以及不同 workflow 间的依赖冲突。
- 参考 `RBioBench` 的做法，采用“统一宿主 + workflow 专用隔离环境 + 预热”的模式。

## 总体策略

### 1. 宿主 Snakemake 环境

- 统一使用 `snakemake` conda 环境作为宿主执行层。
- 用于：
- 调用 `python -m snakemake`
- 管理 `--use-conda`
- 预热 Snakemake rule 级环境

对应环境文件:
- `finish/sandbox/env_specs/snakemake-host.yaml`

### 2. 特殊 workflow 独立环境

对于不完全依赖 Snakemake rule env、而是直接通过 `command` 执行脚本的 workflow，
统一使用 `command_conda_env` 做隔离，避免依赖冲突。

当前已定义:

- `renzo-wf-systempiper`
- `renzo-wf-gammon-rnaseq`
- `renzo-wf-saidmlonji-rnaseq`
- `renzo-wf-signac-atacseq`
- `renzo-wf-astro`
- `renzo-wf-st-pipeline`
- `renzo-wf-300bcg`

对应环境文件位于:
- `finish/sandbox/env_specs/*.yaml`

### 3. Snakemake rule env 预热

对于 source workflow 自带 `envs/*.yaml` 的 finish workflows：

- 不再等正式实验时首次建 DAG 才现场建环境
- 而是在正式实验前先执行：
- `--use-conda --conda-create-envs-only`

这样可提前暴露：
- 缺失频道
- 求解冲突
- 特定 env yaml 失效

## 冲突隔离原则

### A. R / Bioconductor 大栈

- `systemPipeR` 系列单独放在 `renzo-wf-systempiper`
- 避免与 Seurat / Signac / 其他 R workflow 混装

### B. Signac / Seurat ATAC

- `mohammedemamkhattabunipd-atacseq-finish`
- 单独放 `renzo-wf-signac-atacseq`

### C. 传统 bulk RNA 下游 R 分析

- `gammon-bio-rnaseq_pipeline-finish`
- `saidmlonji-rnaseq_pipeline-finish`
- 分别独立 env，避免 Bioconductor 版本冲突

### D. 旧版 Python legacy pipeline

- `epigen-300bcg-atacseq_pipeline-finish`
- 单独用 `renzo-wf-300bcg`
- 当前按 Python 2 legacy 栈隔离

### E. 纯 Python / CLI spatial pipelines

- `gersteinlab-astro-finish`
- `jfnavarro-st_pipeline-finish`
- 分别放进独立 Python env，避免 `pysam/HTSeq/taggd` 等包冲突

## 审计文件

- 全量依赖审计:
- `finish/WORKFLOW_ENV_AUDIT.md`
- `finish/WORKFLOW_ENV_AUDIT.json`

## 预配置脚本

- `finish/tools/prepare_sandbox_envs.py`

默认行为:

1. 创建/更新宿主 `snakemake` 环境
2. 创建/更新 special workflows 的 `command_conda_env`
3. 对所有 finish workflows 做 Snakemake env 预热

## 推荐执行方式

### 全量预配置

```bash
python3 finish/tools/prepare_sandbox_envs.py
```

### 只准备 special workflow 环境

```bash
python3 finish/tools/prepare_sandbox_envs.py --skip-snakemake-prewarm
```

### 只准备指定 workflows

```bash
python3 finish/tools/prepare_sandbox_envs.py \
  --only tgirke-systempiperdata-rnaseq-finish \
         rna-seq-star-deseq2-finish
```

## 当前已完成的运行时改造

- `finish_step_runtime.py` 现在支持 `command_conda_env`
- `manual_finishify_specials.py` 已为 special workflows 写入隔离环境名
- `systempiper_step_runner.R` 已改成支持本地 R library 自举

## 当前已知剩余风险

- 某些 source workflow 本身需要真实输入数据，单纯预热环境无法替代输入物料
- 某些上游仓库可能存在语法或配置错误，预热只能提前暴露，不能自动修正
- 少数 legacy workflow 可能仍需要更细的系统级依赖（例如外部二进制）
