# R Workflow 评测框架与 Biomni 闭环计划

## Summary

- 本次计划同时吸收两条灵感线：
  - `BiomniBench / BixBench`：告诉我们为什么生信 agent 不能只看终局正确率，为什么必须区分 `agent 真不懂`、`任务/流程本身有歧义或不可评`、`ground truth / workflow 自身有问题`，以及为什么需要 process-based evaluation。
  - `2604.11641v1 / CodeTracer: Towards Traceable Agent States`：告诉我们具体该怎样把过程做成可研究对象，也就是 `hierarchical trace tree`、`failure onset localization`、`diagnostic replay under matched budgets`。
- 因此，这轮工作的主目标不是在二者之间二选一，而是把它们拼成一条完整方法链：
  - 用 BiomniBench 的视角定义“什么 run 值得评、为什么不能只看终局分数”；
  - 用 CodeTracer 的方法把 run 重建为 trace，并定位最早偏航点；
  - 再把诊断信号回灌给 `Biomni`，做同集、同预算的 before/after 闭环验证。

## Paper-to-Project Mapping

### BiomniBench/BixBench 给我们的评测立场

- `benchmark noise matters`
  - 生信任务里的失败不全是 agent 失败，workflow 本身、输入准备、题目歧义、参考答案问题都可能污染排行榜。
  - 对你们项目的映射是：必须保留 `evaluable / not_evaluable` 区分，并把 `workflow 自己坏掉` 从主表中分离出去。

- `binary scoring is insufficient`
  - 只看最终对错会损失大量诊断信息。
  - 对你们项目的映射是：除了 `workflow success`，还要统计 `step completion`、`declared output coverage`、`failure taxonomy`、`summary faithfulness`。

- `process matters as much as result`
  - 对生信 agent 的信任来自过程，而不只是最终产物。
  - 对你们项目的映射是：R workflow benchmark 不能只保留 flat summary，必须把中间编排、执行、验证过程结构化保留。

### CodeTracer 给我们的具体技术路线

- `hierarchical trace tree`
  - CodeTracer 强调要把异构运行产物重建成分层状态轨迹，而不是依赖零散日志。
  - 对你们项目的映射是：把一个 workflow run 拆成 `workflow -> turn -> step selection -> execution attempt -> validation -> artifact delta` 的层级轨迹。

- `failure onset localization`
  - CodeTracer 的重点不是“最后哪里报错”，而是“最早从哪里开始偏航”。
  - 对你们项目的映射是：区分 `first failed step` 和 `failure onset`。前者可能只是最后爆炸点，后者可能是更早的错误选步、错误恢复、错误成功声明。

- `stage-level + step-level supervision`
  - CodeTracer 的评测不是只有 run 级标签，而是同时有 stage 和 step 级监督。
  - 对你们项目的映射是：R workflow benchmark 不能只存 `success/fail`，还要有至少两级标签：
    - stage 级：输入准备、步骤编排、执行、验证、总结
    - step 级：具体哪个 step 首次偏航

- `replaying diagnostic signals`
  - CodeTracer 显示诊断信号本身可以帮助恢复原本失败的 run。
  - 对你们项目的映射是：对 `Biomni` 不只是分析失败，而是把 `failure onset` 和错误链压缩成可注入的诊断提示，再在相同 workflow、相同 timeout、相同 turns 约束下复跑。

### 二者合起来在你们项目中的角色分工

- `BiomniBench/BixBench` 解决的是：
  - 为什么不能只看终局
  - 为什么要做可评样本筛选
  - 为什么要做 process-aware benchmark

- `CodeTracer` 解决的是：
  - 过程具体怎么表示
  - 失败起点具体怎么定位
  - 定位结果怎么转化为可执行改进信号

- 所以这份计划的完整主张是：
  - 用 `BiomniBench/BixBench` 决定评什么、怎么公平地评；
  - 用 `CodeTracer` 决定过程怎么建模、失败怎么定位、改进怎么闭环。

## Current State Analysis

### 当前代码里已经有的“可追踪状态原料”

- `finish/Renzo_DA_Agent/scripts/run_finish_workflow_comparison.py`
  - 已经能取到：
    - `workflow_plan`
    - `llm_trace`
    - `orchestration_trace`
    - `execution_logs`
    - `validation_result`
    - `artifact_index`
    - turn 级增量快照
  - 这意味着你们已经有足够的原始材料去重建 trace tree，不需要从零加埋点体系。

- `finish/Renzo_DA_Agent/PEER_AGENTS.md`
  - peer agent 运行输入输出已经统一。
  - `agent-<name>-run.json` 已经是稳定的 run 级容器，适合扩成 trace-aware schema。

- `finish/Renzo_DA_Agent/app/orchestration/step_selector_agents.py`
  - 这里是 peer agent 下一步选择的核心入口。
  - 对 `Biomni` 而言，它既是失败 onset 的常见来源，也是未来注入诊断 replay 信号的关键切点。

- `finish/Renzo_DA_Agent/scripts/summarize_formal_peer_runs.py`
  - 当前只做结果扁平化。
  - 它是现有框架里最明显的“信息坍缩点”：很多可以做 onset localization 的证据在这里被丢掉了。

### 当前缺的不是日志，而是“组织日志的方法”

- 现在的输出更接近：
  - 有若干 traces
  - 有若干 step metrics
  - 有最终 summary
- 但缺少：
  - 分层 trace 结构
  - 明确定义的 onset 规则
  - 错误链表示
  - 用于 before/after 对比的诊断 replay 协议

### 当前 smoke 暴露的问题

- `refine-logs/SMOKE_RUN_REPORT_2026-04-14.md`
  - 已经说明正式 benchmark 之前还需要 `workflow evaluability gate`。
  - 这不是因为 CodeTracer 主张这个，而是因为如果 workflow 自己坏掉，trace 再漂亮也没有比较意义。
- 所以本计划里：
  - `evaluable gate` 来自 BiomniBench/BixBench 那条线，是评测可信性的基础；
  - `trace tree + onset localization + replay` 来自 CodeTracer 那条线，是你们方法上的主体创新。

## Assumptions & Decisions

- 主贡献表述调整为：
  - `一个吸收 BiomniBench 与 CodeTracer 双重启发的 bioinformatics R workflow evaluation framework`
  - `一个同时考虑 evaluability 与 process trace 的 benchmark 协议`
  - `一个 failure onset localization 协议`
  - `一个用诊断信号驱动 Biomni 恢复/改进的同预算闭环`
- 本轮只深做 `Biomni`，不同时深改 `STELLA`、`ToolUniverse`。
- before/after 对比必须满足：
  - 同一 verified workflow 集
  - 同一 timeout
  - 同一 max turns
  - 同一 env / cache policy
- `not_evaluable` workflow 仍要记录，但只进入附录噪声分析，不进入主结果表。
- 第一轮 onset localization 先采用规则法和少量人工校验，不引入复杂外部 judge pipeline。

## Proposed Changes

### 1. 新建 trace 协议文档，明确层级状态与 onset 定义

- 新建 `finish/R_WORKFLOW_TRACE_PROTOCOL.md`
- 文档固定以下定义：
  - trace tree 层级：
    - `workflow_run`
    - `turn`
    - `selection_event`
    - `execution_attempt`
    - `validation_event`
    - `artifact_delta`
  - 关键判定对象：
    - `terminal_failure`
    - `failure_onset`
    - `downstream_error_chain`
    - `false_success_claim`
  - stage taxonomy：
    - `input_readiness`
    - `step_selection`
    - `execution`
    - `validation`
    - `summary/reporting`
  - onset 规则：
    - 优先找第一个导致后续状态不可恢复的偏航事件
    - 若最终报错只是下游症状，则不把最后报错点当 onset
  - replay 协议：
    - 只能注入压缩后的诊断信号
    - 不允许放宽 budget
    - 不允许换 workflow 集

### 2. 在单次比较脚本里重建 hierarchical trace tree

- 修改 `finish/Renzo_DA_Agent/scripts/run_finish_workflow_comparison.py`
- 在现有 `agent-<name>-run.json` 基础上新增：
  - `trace_tree`
  - `trace_nodes`
  - `turn_summaries`
  - `stage_summaries`
  - `failure_onset`
  - `error_chain`
  - `diagnostic_replay_hint`
- 具体构造方式：
  - 用现有 `llm_trace` 生成 `selection_event`
  - 用 `orchestration_trace` 连接 turn 与选步理由
  - 用 `execution_logs` 生成 `execution_attempt`
  - 用 `validation_result` 生成 `validation_event`
  - 用 `artifact_index` 与输出 diff 生成 `artifact_delta`
- 每个 node 至少包含：
  - `node_id`
  - `parent_id`
  - `node_type`
  - `stage`
  - `step_id`
  - `status`
  - `evidence_refs`
  - `started_at / ended_at`

### 3. 增加 failure onset localization，而不是只看 first failed step

- 主要修改 `finish/Renzo_DA_Agent/scripts/run_finish_workflow_comparison.py`
- 如逻辑过长，则拆出新 helper：
  - `finish/Renzo_DA_Agent/scripts/localize_failure_onset.py`
- onset 输出字段固定为：
  - `onset_stage`
  - `onset_turn`
  - `onset_step_id`
  - `onset_category`
  - `onset_evidence`
  - `downstream_chain`
  - `terminal_symptom`
- onset category 第一版固定为：
  - `workflow_not_evaluable`
  - `wrong_step_selection`
  - `missing_input_not_detected`
  - `execution_failure_not_recovered`
  - `validation_failure_ignored`
  - `hallucinated_success_summary`

### 4. 保留 evaluability gate，但把它变成 trace 评测的前置条件

- 新建 `finish/tools/check_workflow_evaluability.py`
- 输出：
  - `finish/WORKFLOW_EVALUABILITY_STATUS.json`
  - `finish/WORKFLOW_EVALUABILITY_STATUS.md`
- 该脚本的作用不再是主叙事，而是保证：
  - 我们做 onset localization 的对象是“值得评”的 workflow
  - `workflow 自己坏掉` 不会混入 `agent onset` 统计
- 检查项仍然包括：
  - protocol 合法性
  - 关键输入是否存在
  - smoke 已知硬错误
  - env 是否 ready
- 这一层主要承接 BiomniBench/BixBench 的启发：先保证 benchmark 本身可信，再谈 agent 过程诊断。

### 5. 让批量运行器同时产出主结果和 trace 审计产物

- 修改 `finish/tools/run_release_comparisons.py`
- 新行为：
  - 运行前检查 `SANDBOX_ENV_STATUS.json` 与 `WORKFLOW_EVALUABILITY_STATUS.json`
  - 运行后保证每个 workflow 目录下同时有：
    - `comparison-summary.json`
    - `agent-<name>-run.json`
    - trace-aware 产物
- 这里不增加复杂执行逻辑，只负责强制协议完整性。

### 6. 改造汇总脚本，生成 trace-first benchmark 视图

- 修改 `finish/Renzo_DA_Agent/scripts/summarize_formal_peer_runs.py`
- 新增输出字段：
  - `evaluable`
  - `onset_stage`
  - `onset_category`
  - `onset_step_id`
  - `time_to_onset`
  - `recovery_attempt_count`
  - `false_success_claim`
  - `trace_depth`
  - `error_chain_length`
- 新增两类聚合表：
  - `benchmark_main_table`: success / cost / runtime / completion，仅统计 `evaluable=1`
  - `trace_audit_table`: onset taxonomy / stage distribution / recovery failure / summary faithfulness
- 这样主图不再只是 heatmap，而能讲：
  - 哪类 workflow 容易让 Biomni 在哪一层先偏航
  - 失败是如何沿错误链传导到终局的
- 其中：
  - `benchmark_main_table` 更贴近 BiomniBench/BixBench 的 benchmark 视角；
  - `trace_audit_table` 更贴近 CodeTracer 的 trace 诊断视角。

### 7. 增加一个小型人工 onset review 集，对齐 CodeTracer 的 stage/step supervision 思路

- 新建：
  - `refine-logs/BIOMNI_ONSET_REVIEW.md`
  - `refine-logs/BIOMNI_ONSET_REVIEW.json`
- 只覆盖小批量、代表性的失败 run，不追求大规模标注。
- 每条记录标注：
  - `workflow_id`
  - `agent_name`
  - `gold_onset_stage`
  - `gold_onset_step_id`
  - `gold_onset_reason`
  - `notes`
- 作用：
  - 校验自动 onset localization 是否靠谱
  - 给论文中“failure onset localization”提供更坚实的证据

### 8. 把 Biomni 的第一轮优化改成“诊断信号驱动 replay”

- 主要修改：
  - `finish/Renzo_DA_Agent/app/orchestration/step_selector_agents.py`
  - `finish/Renzo_DA_Agent/scripts/run_finish_workflow_comparison.py`
- 第一轮不做大规模 framework 重构，只做：
  - 在选步时显式注入上一轮 onset 诊断提示
  - 在检测到 `missing_input_not_detected`、`validation_failure_ignored` 等类别时更早停机或切换恢复策略
  - 在总结阶段避免无证据成功宣称
- replay 输入固定为：
  - 上一轮 `failure_onset`
  - 一段压缩后的 `error_chain`
  - 一段允许的恢复建议
- replay 约束固定为：
  - 同 workflow
  - 同 timeout
  - 同 max turns
  - 同模型和 env

### 9. 更新实验计划，把论文主线改写为“trace -> onset -> replay”

- 修改 `refine-logs/EXPERIMENT_PLAN.md`
- 主线改成：
  - `Block 0: Evaluability Gate`
  - `Block 1: Trace Protocol Freeze`
  - `Block 2: Baseline Trace Benchmark`
  - `Block 3: Failure Onset Review`
  - `Block 4: Biomni Diagnostic Replay`
  - `Block 5: Same-set Paired Validation`
- 论文故事固定成：
  - BiomniBench/BixBench 告诉我们 workflow benchmark 不能只看终局分数
  - evaluability gate 让 benchmark 噪声不污染主表
  - CodeTracer 告诉我们 trace tree 可以让 agent 状态可见
  - onset localization 让失败可归因
  - replay 证明诊断信号有操作价值

## Implementation Order

1. 新建 `finish/R_WORKFLOW_TRACE_PROTOCOL.md`，冻结 trace tree、onset、replay 的定义。  
2. 新建 `finish/tools/check_workflow_evaluability.py`，保证进入主 benchmark 的 workflow 可评。  
3. 修改 `finish/Renzo_DA_Agent/scripts/run_finish_workflow_comparison.py`，输出 trace tree、failure onset、error chain、replay hint。  
4. 必要时新增 `finish/Renzo_DA_Agent/scripts/localize_failure_onset.py`，把 onset 逻辑独立出来。  
5. 修改 `finish/tools/run_release_comparisons.py`，强制产出 trace-aware run artifacts。  
6. 修改 `finish/Renzo_DA_Agent/scripts/summarize_formal_peer_runs.py`，生成主结果表和 trace 审计表。  
7. 新建 `refine-logs/BIOMNI_ONSET_REVIEW.{md,json}`，做小批量人工 onset 校验。  
8. 修改 `finish/Renzo_DA_Agent/app/orchestration/step_selector_agents.py` 与相关 replay 入口，只对 `Biomni` 做诊断信号驱动 replay。  
9. 修改 `refine-logs/EXPERIMENT_PLAN.md`，让实验与论文叙事对齐。  

## Verification Steps

- 协议验证
  - `R_WORKFLOW_TRACE_PROTOCOL.md` 是否同时体现：
    - BiomniBench/BixBench 的 `evaluable/process-aware` 评测立场
    - CodeTracer 的 `trace/onset/replay` 技术路线
  - `EXPERIMENT_PLAN.md` 是否把这两条线清楚分工，而不是混成单一口号。

- schema 验证
  - 每个 `agent-<name>-run.json` 都有 `trace_tree` 和 `failure_onset`。
  - `comparison-summary.json` 能区分 `terminal symptom` 与 `true onset`。

- 评测验证
  - `summarize_formal_peer_runs.py` 能输出 onset taxonomy 分布。
  - `not_evaluable` workflow 不会污染主表成功率，但会进入 trace 噪声审计。

- onset 验证
  - 自动 onset localization 与 `BIOMNI_ONSET_REVIEW.json` 的小样本人工标注基本一致。
  - onset 不会总是机械地等于最后失败 step。

- replay 验证
  - `Biomni` replay 版本在相同 workflow、相同 budget 下至少改善一个核心指标。
  - 改善能够被解释为“onset 被修正”而不是“预算放宽”。

## Expected Outcome

- 这套计划完成后，你们的贡献会从“对多个 bio agents 跑 R workflows”升级成：
  - 一个同时吸收 `BiomniBench/BixBench` 与 `CodeTracer` 的 R workflow benchmark；
  - 一个 `evaluable + process-aware` 的评测协议；
  - 一个 `failure onset localization` 协议；
  - 一个用于 `Biomni` 的 `diagnostic replay` 闭环；
  - 一个把 workflow 噪声与 agent 偏航分开的评测框架。
- 这样你们的叙事就不是“只借了一个 benchmark 观点”或“只借了一篇 tracing paper”，而是：
  - 用 BiomniBench/BixBench 解决“评测为什么不该只看终局”；
  - 用 CodeTracer 解决“那过程到底怎么表示、怎么定位、怎么拿去改 agent”；
  - 最后在 `Biomni` 上完成一个真正能落地的闭环。
