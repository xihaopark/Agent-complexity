# Benchmark Run Guide

更新日期: 2026-04-10

## 目标

- 基于已经转换成功并通过 dry-run 的 `-finish` workflows，
- 生成首批正式 benchmark 运行计划，
- 然后批量执行 `Renzor vs peers` 对比，
- 最后自动汇总为 `summary_flat.json/csv`。

## Step 1: 生成首批运行计划

```bash
python3 finish/tools/build_benchmark_run_plan.py
```

输出:
- `finish/BENCHMARK_RUN_PLAN.json`
- `finish/BENCHMARK_RUN_PLAN.md`

默认策略:
- 从 `release_core` 中选取 12 个 workflow
- 每个 family 最多 3 个
- 优先选择 steps 数适中的 workflow

可选参数:

```bash
python3 finish/tools/build_benchmark_run_plan.py --max-total 16 --max-per-family 4
python3 finish/tools/build_benchmark_run_plan.py --include-large
```

## Step 2: 批量运行正式对比

在正式运行前，先准备沙箱环境:

```bash
python3 finish/tools/prepare_sandbox_envs.py \
  --exclude-command-envs renzo-wf-300bcg
```

说明:
- 正式实验阶段不建议现场求解 conda 环境。
- `run_release_comparisons.py` 现在默认要求 `SANDBOX_ENV_STATUS.json` 中对应 workflow 标记为 ready。
- 如需绕过此检查，可显式传 `--ignore-env-readiness`，但不建议在正式实验中使用。

环境就绪后，再运行正式对比:

```bash
python3 finish/tools/run_release_comparisons.py
```

默认行为:
- 读取 `finish/BENCHMARK_RUN_PLAN.json`
- 检查 `finish/SANDBOX_ENV_STATUS.json` 中的环境就绪状态
- 对每个选中的 workflow 调用
- `finish/Renzo_DA_Agent/scripts/run_finish_workflow_comparison.py`
- 完成后自动调用
- `finish/Renzo_DA_Agent/scripts/summarize_formal_peer_runs.py`

默认输出目录:
- `finish/Renzo_DA_Agent/data/release_runs/<timestamp>/`

## 常用运行示例

### 先小跑 3 个 workflow

```bash
python3 finish/tools/run_release_comparisons.py --limit 3
```

### 显式指定 agents

```bash
python3 finish/tools/run_release_comparisons.py \
  --agents renzo,biomni,stella,tooluniverse
```

### 使用并行 agent 运行

```bash
python3 finish/tools/run_release_comparisons.py --parallel-runs
```

### 强制 manifest 严格模式

```bash
python3 finish/tools/run_release_comparisons.py --strict-agent-manifest
```

### 指定输出目录

```bash
python3 finish/tools/run_release_comparisons.py \
  --output-root finish/Renzo_DA_Agent/data/release_runs/first_release
```

### 仅在调试时忽略环境就绪检查

```bash
python3 finish/tools/run_release_comparisons.py --ignore-env-readiness
```

## Step 3: 查看结果

每次运行结束后，输出目录下会自动生成:

- `*/artifacts/comparison-summary.json`
- `summary_flat.json`
- `summary_flat.csv`

可以进一步配合现有脚本做导出:

- `finish/Renzo_DA_Agent/scripts/export_finish_step_tables.py`
- `finish/Renzo_DA_Agent/scripts/summarize_formal_peer_runs.py`

## 相关文件

- release 候选: `finish/BENCHMARK_RELEASE_CANDIDATES.md`
- 首批运行计划: `finish/BENCHMARK_RUN_PLAN.md`
- 沙箱环境状态: `finish/SANDBOX_ENV_STATUS.md`
- 批量运行器: `finish/tools/run_release_comparisons.py`
- 运行计划生成器: `finish/tools/build_benchmark_run_plan.py`
