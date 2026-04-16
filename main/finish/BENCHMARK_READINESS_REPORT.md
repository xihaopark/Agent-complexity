# Benchmark Readiness Report

更新日期: 2026-04-10

## 核心结论

- 新增生成的 finish workflows 已经不只是目录级产物，而是已经进入现有 benchmark 的统一发现路径。
- 根目录 `run_finish_workflow.py` 能自动扫描 `*/manifest.json` 并识别这些 workflow。
- `Renzo_DA_Agent` 的 workflow registry 也能统一发现这些 workflow。

## 发现验证结果

- `run_finish_workflow.py` 可扫描到的 `-finish` workflows 数量: 57
- `Renzo_DA_Agent` registry 可发现的 `-finish` workflows 数量: 57
- 其中:
- 原始已存在 finish workflows: 5
- 本轮新增 finish workflows: 52

## 验证方式

### 1. 根目录运行入口

- 文件: `finish/run_finish_workflow.py`
- 结论: 使用 `ROOT.glob("*/manifest.json")` 自动扫描 workflow 目录，不依赖硬编码列表。

### 2. Renzo workflow registry

- 文件: `finish/Renzo_DA_Agent/app/workflows/registry.py`
- 结论: `discover_workflows()` 会把 `finish/` 作为 discovery root，并解析其中的 `manifest.json`。

### 3. Dry-run 验证

- 自动转化 workflows: `finish/GENERATED_FINISH_VALIDATION.md`
- 特殊转化 workflows: `finish/MANUAL_FINISH_VALIDATION.md`
- 当前所有已纳入的新增 workflow 均已通过 `run_workflow.py --dry-run`。

## 代表性发现样例

以下 workflow 已确认能被统一发现:

- `epigen-300bcg-atacseq_pipeline-finish`
- `tgirke-systempiperdata-rnaseq-finish`
- `tgirke-systempiperdata-chipseq-finish`
- `tgirke-systempiperdata-riboseq-finish`
- `tgirke-systempiperdata-varseq-finish`
- `tgirke-systempiperdata-spscrna-finish`
- `lwang-genomics-ngs_pipeline_sn-rna_seq-finish`
- `lwang-genomics-ngs_pipeline_sn-chip_seq-finish`
- `lwang-genomics-ngs_pipeline_sn-atac_seq-finish`

## 当前剩余阻塞

- `snakemake-workflows__oncology`
- 原因: 上游仓库当前只有一份 README，没有任何可执行 workflow 资产，因此无法有意义地 finish 化。

## 当前可直接使用的统一脚本

- 总入口: `finish/tools/finishify_workflows.py`
- 自动 Snakemake 转化: `finish/tools/auto_finishify_candidates.py`
- 特殊 workflow 转化: `finish/tools/manual_finishify_specials.py`
- systemPipeR step runner: `finish/tools/systempiper_step_runner.R`
- release 清单生成: `finish/tools/build_benchmark_release_candidates.py`
- smoke test 脚本: `finish/tools/smoke_test_finish_workflows.py`
- 首批运行计划生成: `finish/tools/build_benchmark_run_plan.py`
- 正式批量对比运行器: `finish/tools/run_release_comparisons.py`

## 当前 release 产物

- 首批 benchmark release 清单: `finish/BENCHMARK_RELEASE_CANDIDATES.md`
- 首批 benchmark release JSON: `finish/BENCHMARK_RELEASE_CANDIDATES.json`
- 首批 benchmark 运行计划: `finish/BENCHMARK_RUN_PLAN.md`
- smoke test 结果: `finish/SMOKE_TEST_RESULTS.md`
- 批量运行指南: `finish/BENCHMARK_RUN_GUIDE.md`

## 建议的下一步

- 可以开始按你们的 benchmark 需求挑选一批 workflow 进入正式运行对比。
- 下一阶段建议做:
- 批量 smoke test 若干新增 workflow 的真实运行入口
- 统计每个 workflow 的 step 数、配置依赖和运行代价
- 形成 benchmark release 清单，而不是继续做转换基础设施
