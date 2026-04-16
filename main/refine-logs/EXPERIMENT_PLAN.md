# Experiment Plan

**Problem**: 缺少一个面向 bioinformatics R workflow 的统一智能体评估框架，难以系统比较 Biomni、DSWizard、STELLA、ToolUniverse、Renzo 等智能体在真实 workflow 执行中的成功率、代价、稳定性与失效模式。  
**Method Thesis**: 先构建一个同时考虑 `evaluable` 与 `process trace` 的 workflow-level agent evaluation framework，再基于 trace tree 与 failure onset localization 识别具体问题点，对 `Biomni` 做诊断信号驱动 replay，并在同一批 R workflow 上做同预算复跑验证改进是否真实有效，最后再进入大规模 workflow 运行。  
**Date**: 2026-04-13

## Claim Map

| Claim | Why It Matters | Minimum Convincing Evidence | Linked Blocks |
|-------|-----------------|-----------------------------|---------------|
| C1: 一个 workflow-level 评估框架可以稳定比较不同 bio agents 的执行表现 | 本工作首先是 benchmark / evaluation framework，而不是单一 agent 系统 | 在同一批 R workflow 上，对多个 agents 产生统一输入、统一输出、统一指标与统一失败归因报告 | B1, B2 |
| C2: 基于评估框架识别问题并定向调整 agent 后，指标可以在同一 workflow 集上真实提升 | 证明 framework 不只是“看分数”，而能驱动 agent 改进 | 至少一个 agent 家族在同一 workflow 集上重跑后，成功率、token 效率、LLM 调用次数、时长中的一个或多个核心指标显著改善，且失败原因更集中、更可解释 | B3, B4 |
| Anti-claim: 改进只是换了 workflow 集、放宽条件或偶然波动 | 需要排除“比较不公平”或“结果不可复现” | 固定 workflow 集、固定输入、固定超时与资源策略，在同等条件下 before/after 对比 | B3, B4 |

## Paper Storyline

- Main paper must prove:
  - workflow-level 评估框架本身是清晰、统一且可复用的；
  - workflow benchmark 不能只看终局分数，必须先区分 `evaluable / not_evaluable`；
  - trace tree 能让 agent 的执行状态、偏航点和错误链可见；
  - failure onset localization 可以把终局失败拆成更早的可归因事件；
  - 多个 bio agents 在同一 R workflow 集上的表现确实存在显著差异；
  - framework 能输出 actionable diagnostics，并指导 `Biomni` 定向 replay；
  - 优化后的 agent 在相同 workflow、相同 budget 上有可验证提升。
- Appendix can support:
  - 更多 workflow 家族与更大规模扩展实验；
  - 更多失败案例与日志片段；
  - 更细粒度的 token / wall-time / env reuse 分析。
- Experiments intentionally cut:
  - 现在不追求“所有 workflow 一次性全跑完”；
  - 现在不追求所有 agent 都做深入重构；
  - 现在不把重点放在 direct baseline，而是聚焦 agent-vs-agent workflow benchmark。

## Proposed Main Workflow Set (v1)

- 目标数量: 20
- 选择原则:
  - 优先从 `release_core` 里选取已通过 dry-run 的 workflow
  - 优先覆盖 `rna / single-cell / epigenomics / variant / spatial / other`
  - 同时覆盖 `small / medium` 难度梯度，避免全是 toy workflows 或全是超大 workflows
  - 保留 `auto` 与 `manual-special` 两类 finish 来源，降低单一路径偏差
  - 暂不把 `release_large` 作为主实验集主体，它们更适合闭环验证后再做扩展
- 家族配比:
  - rna: 4
  - single-cell: 4
  - epigenomics: 5
  - variant: 3
  - spatial: 1
  - other: 3
- 明确不纳入主实验集（当前阶段）:
  - `snakemake-workflow-template-finish`: 更适合作为 infra / protocol sanity，不适合作为 paper 主 benchmark workflow
  - `zarp-finish`: 当前已暴露强 infra/resource 干扰，适合作为 failure case，而非主实验集核心样本
  - `release_large` 中 >40 steps workflows: 保留到大规模扩展阶段

## Experiment Blocks

### Block 0: Evaluability Gate

- Claim tested: C1
- Why this block exists: 先剔除 workflow 自身不可评、输入不完整、env 未就绪的样本，避免 benchmark 噪声污染主表
- Dataset / split / task:
  - 对第一批 R workflows 运行 `WORKFLOW_EVALUABILITY_STATUS.json` 检查
- Metrics:
  - evaluable count
  - not_evaluable count
  - workflow_protocol_failure / input_or_env_failure 分布
- Success criterion:
  - 主 benchmark workflow 集全部带有 evaluability 标签
  - `not_evaluable` 样本被移入附录与 fix-then-retry 清单
- Priority: MUST-RUN

### Block 1: Trace Protocol Freeze

- Claim tested: C1
- Why this block exists: 先把 benchmark 本身做成稳定协议，否则后续 trace/onset/replay 结果都不可信
- Dataset / split / task:
  - 以一批代表性的 R workflow 为核心测试集
  - 按 workflow family 做覆盖：rna / single-cell / epigenomics / variant / other
  - 首轮使用中小规模 curated set，避免直接上全量
- Compared systems:
  - Renzo
  - Biomni
  - DSWizard
  - STELLA
  - ToolUniverse
- Metrics:
  - 主指标：workflow success rate
  - 次指标：step completion ratio、declared output coverage、wall-clock runtime、LLM call count、total tokens、cost
  - 诊断指标：failure class、failure onset、terminal symptom、error chain、summary faithfulness
- Setup details:
  - 固定 workflow 输入接口：`workflow_dir / finish_root / data_root / timeout_per_step`
  - 固定输出接口：`agent-<name>-run.json` + `comparison-summary.json`
  - `agent-<name>-run.json` 必须带 `trace_tree / failure_onset / diagnostic_replay_hint`
  - 默认共享 Snakemake conda prefix 与 conda package cache，避免重复建环境导致资源偏差
  - biomni / stella 使用真实框架路径，禁止降级为纯 prompt mock
- Success criterion:
  - 同一 workflow 在不同 agents 上都能产出统一格式结果
  - 指标统计与失败归因可自动汇总成报告
- Failure interpretation:
  - 如果结果 JSON 不稳定或字段不齐，说明 benchmark protocol 还没冻结
  - 如果 framework-native 调用无法记录 usage，说明 token/cost 统计链条仍不完整
- Table / figure target:
  - 主表 T1: agent × workflow 成功率矩阵
  - 主表 T2: runtime / llm_calls / token / cost 汇总
  - 图 F1: evaluability + failure taxonomy
- Priority: MUST-RUN

### Block 2: Baseline Trace Benchmark

- Claim tested: C1
- Why this block exists: 形成第一版正式 benchmark report，明确“谁在哪类 workflow 上强/弱，问题出在哪”
- Dataset / split / task:
  - 固定第一批 benchmark workflows
  - 每个 workflow 至少跑一次所有 agents
- Compared systems:
  - Renzo vs Biomni vs DSWizard vs STELLA vs ToolUniverse
- Metrics:
  - success rate
  - completed_step_count / step_count
  - wall-clock runtime
  - llm_call_count
  - total_tokens / cost
  - failure onset category distribution
  - onset stage distribution
  - error chain length
- Setup details:
  - 统一 timeout、统一 cache / env policy、统一真实框架约束
  - 对 infra failure 单独打标，不和 planning failure 混淆
- Success criterion:
  - 产出 benchmark report，能回答：
    - 哪些 agents 在哪些 workflow 上成功
    - 哪些 workflow 不可评
    - 哪些失败来自 step selection / execution / validation / summary
    - 哪些终局失败其实来自更早 onset
- Failure interpretation:
  - 如果绝大多数失败都是环境问题，则当前评测更多反映 infra，不足以支持“agent 能力差异”
- Table / figure target:
  - 主图 F2: success/failure heatmap
  - 主图 F3: duration & llm call comparison
  - 图 F4: onset taxonomy / stage distribution
  - 附录 A1: trace-backed failure cases
- Priority: MUST-RUN

### Block 3: Failure Onset Review

- Claim tested: C2
- Why this block exists: 自动 onset localization 需要少量人工抽查，才能支撑 “failure onset” 这条主张
- Dataset / split / task:
  - 使用 Block 2 中代表性的失败 `Biomni` runs
- Metrics:
  - gold onset vs auto onset 一致性
  - onset stage accuracy
  - onset step accuracy
- Setup details:
  - 使用 `BIOMNI_ONSET_REVIEW.{md,json}` 做人工记录
- Success criterion:
  - 自动 onset localization 与人工结论大体一致
- Failure interpretation:
  - 若 onset 大量对不上，说明 trace/onset 规则还没冻结，不能进入 replay
- Table / figure target:
  - 附录 A2: onset review examples
- Priority: MUST-RUN

### Block 4: Biomni Diagnostic Replay

- Claim tested: C2, Anti-claim
- Why this block exists: 验证诊断信号本身是否有操作价值，而不是只会做离线解释
- Dataset / split / task:
  - 与 Block 2 完全相同的 workflow 集
- Compared systems:
  - `Biomni` baseline
  - `Biomni` + diagnostic replay
- Metrics:
  - workflow-level paired comparison
  - success flips
  - paired runtime delta
  - paired llm call delta
  - paired token delta
- Setup details:
  - 固定 timeout、env policy、workflow inputs、max turns
  - replay 只允许注入 `failure_onset / error_chain / allowed_recovery_advice`
- Success criterion:
  - 同 budget 下至少一个核心指标改善
- Failure interpretation:
  - 若提升只出现在个别 workflow 且伴随高代价，需要弱化 claim
- Table / figure target:
  - 主图 F5: Biomni replay before/after comparison
- Priority: MUST-RUN

### Block 5: Same-Set Re-run Validation

- Claim tested: C2, Anti-claim
- Why this block exists: 排除“换 workflow / 换条件才变好”的伪提升
- Dataset / split / task:
  - 与 Block 2 完全相同的 workflow 集
- Compared systems:
  - `Biomni` baseline vs `Biomni` replay
- Metrics:
  - workflow-level paired comparison
  - success flips
  - paired runtime delta
  - paired llm call delta
  - paired token delta
- Setup details:
  - 固定 timeout、env policy、workflow inputs、max turns
  - 保持 infra policy 一致，仅 replay 信号不同
- Success criterion:
  - paired comparison 下 improvement 仍成立
- Table / figure target:
  - 主图 F6: paired before/after comparison
- Priority: MUST-RUN

### Block 6: Large-Scale R Workflow Expansion

- Claim tested: supporting extension
- Why this block exists: 在完成闭环验证后，才有资格进入规模化 benchmark
- Dataset / split / task:
  - 扩展到更大规模 R workflow 池
  - 保持 family coverage 与 step-complexity coverage
- Compared systems:
  - 优先跑 benchmark 中表现较好且已完成定向优化的 agents
- Metrics:
  - 大规模 success rate
  - resource-normalized runtime
  - token / cost per successful workflow
  - failure taxonomy stability
- Setup details:
  - 必须在共享 env / shared cache / cleaned infra 前提下运行
  - 先小批次，再分阶段扩容
- Success criterion:
  - 指标趋势与小规模阶段一致
- Failure interpretation:
  - 若规模化后 failure taxon 改变显著，说明此前 benchmark 集代表性不足
- Table / figure target:
  - 主图 F6: scaling curves
- Priority: NICE-TO-HAVE（只有前四块完成后才启动）

## Run Order and Milestones

| Milestone | Goal | Runs | Decision Gate | Cost | Risk |
|-----------|------|------|---------------|------|------|
| M0 | evaluability gate + 协议/schema 冻结 | 1 次小规模 smoke benchmark | 若 evaluability / trace / onset 字段不稳定，则不进入正式评测 | 低 | 指标链条未闭合 |
| M1 | 跑第一批 baseline trace benchmark | 所有 5 agents × 第一批 workflow 集 | 若大多数样本 not_evaluable，则先修 workflow/input；若差异已可见，则进入 onset review | 中 | env / cache / storage 干扰 |
| M2 | 形成 trace benchmark report | 汇总 M1 结果 + onset 分类 | 至少识别出 Biomni 的 2-3 个高频 onset 模式 | 低 | 报告只描述现象，不足以指导 replay |
| M3 | 完成 Biomni onset review | 失败样本人工抽查 | 若 onset 对不上，则不进入 replay | 中 | 自动 onset 规则失真 |
| M4 | 实施 Biomni diagnostic replay | same-set replay rerun | 若改进方向无明确 hypothesis，不开跑 | 中 | 改动过多，难以归因 |
| M5 | 同 workflow 集复跑验证 | paired rerun | 只有 paired improvement 成立，才进入规模化 | 中 | 指标提升不稳 |
| M6 | 大规模 R workflow 扩展 | 优先 agents × 大规模 workflow pool | 只有在 M5 成立后才启动 | 高 | 资源与代表性问题 |

## Must-Run vs Nice-to-Have

- Must-run:
  - Block 0: Evaluability Gate
  - Block 1: Trace Protocol Freeze
  - Block 2: Baseline Trace Benchmark
  - Block 3: Failure Onset Review
  - Block 4: Biomni Diagnostic Replay
  - Block 5: Same-Set Re-run Validation
- Nice-to-have:
  - Block 6: Large-Scale R Workflow Expansion

## Compute and Data Budget

- Total estimated cost structure:
  - M0-M1: 中等，主要花在 workflow env provisioning 与首轮 benchmark
  - M3-M4: 中等，重点是 before/after paired rerun
  - M5: 高，只有前面验证完成后才值得投入
- Data preparation needs:
  - 固定 workflow 集清单
  - family 标注
  - workflow complexity / step count / env count 元数据
- Human evaluation needs:
  - 主要是 Biomni onset review 抽查
  - 不需要大量人工主观评分
- Biggest bottleneck:
  - workflow env provisioning 与存储占用
  - framework-native token/cost telemetry 不完整

## Risks and Mitigations

- Risk: 评测结果被 infra/resource failure 主导，而不是 agent 能力差异  
  - Mitigation: 默认共享 Snakemake conda prefix、共享 conda pkgs cache、清理 runtime cache，并将 infra failure 单独分类

- Risk: biomni / stella 的真实框架 usage 无法完整回传 token/cost  
  - Mitigation: 将 token/cost 作为“available when surfaced”的 secondary metric，同时优先保证 llm_call_count 与 success/failure 可信

- Risk: 改进后提升只来自 prompt 加长、调用次数增加，而非能力增强  
  - Mitigation: before/after paired rerun 中同时报告 success / runtime / calls / tokens / cost

- Risk: workflow 集代表性不足，结论不稳  
  - Mitigation: 第一批使用 curated set，第二阶段再扩 family coverage 与规模

- Risk: 同时改太多 agent，工程复杂度失控  
  - Mitigation: 先挑 1-2 个最值得优化的 agents 做闭环验证

## Immediate Next Actions

1. 冻结第一批 benchmark workflow 集，并先跑 evaluability gate。  
2. 整理第一版 trace benchmark report 模板：success matrix、runtime、llm calls、tokens、cost、onset taxonomy。  
3. 从现有结果中整理 Biomni onset review 清单，并写出 replay 假设。  
4. 完成同 budget 的 Biomni replay 复跑设计，确保复跑 workflow 集完全相同。  
5. 只有在 paired validation 成立后，再启动大规模 R workflow 运行。  

## Final Checklist

- [ ] benchmark 协议与 JSON schema 冻结
- [ ] success / runtime / llm_calls / tokens / cost / onset taxonomy 可统一统计
- [ ] infra failure 与 agent failure 已分离
- [ ] Biomni onset review 与 replay 方案明确
- [ ] before/after 同集复跑计划已定义
- [ ] large-scale run 被放到闭环验证之后
