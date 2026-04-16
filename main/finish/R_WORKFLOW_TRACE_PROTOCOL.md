# R Workflow Trace Protocol

更新日期: 2026-04-14

## 目标

- 为 `finish` 基准中的 bioinformatics R workflows 定义统一的 trace-first 评测协议。
- 同时吸收两条方法线：
  - `BiomniBench / BixBench`: 强调 `evaluable` 区分、过程感知评测、避免只看终局分数。
  - `CodeTracer`: 强调 `hierarchical trace tree`、`failure onset localization`、`diagnostic replay under matched budgets`。

## 基本术语

- `workflow-agent-run`
  - 单个 agent 在单个 workflow 上的一次完整运行。

- `evaluable`
  - 当前 run 对 agent 能力比较有意义。
  - 满足最低条件：
    - workflow protocol 合法；
    - 关键输入存在；
    - 环境已就绪；
    - 当前失败不是已知的 workflow 自身硬错误主导。

- `not_evaluable`
  - 当前 run 不能用于主表 agent 能力比较，但仍需保留到附录与噪声审计表。

- `terminal_failure`
  - 最终暴露出来的失败症状，例如 subprocess 退出、缺输入、验证失败。

- `failure_onset`
  - 最早导致 run 偏离可恢复正常轨迹的事件。
  - 不一定等于最后失败 step，也不一定等于最先出现报错文本的位置。

- `downstream_error_chain`
  - 从 `failure_onset` 开始向后传播的一系列错误事件。

- `diagnostic_replay`
  - 把上一轮 run 中抽取出的诊断信号压缩后，反馈给下一轮同 budget 的 agent 运行。

## Trace Tree 层级

- `workflow_run`
  - 整个 run 的根节点。

- `turn`
  - 一个 agent 决策/执行循环。

- `selection_event`
  - 一次“下一步选哪个 workflow step”的选择事件。

- `execution_attempt`
  - 某个 step 的一次实际执行尝试。

- `validation_event`
  - 对执行结果或 run 状态的检查事件。

- `artifact_delta`
  - 本 turn / 本 step 相对于前一状态新增、删除或改变的输出差异。

## Stage Taxonomy

- `input_readiness`
- `step_selection`
- `execution`
- `validation`
- `summary/reporting`

## Node Schema

每个 trace node 至少包含：

- `node_id`
- `parent_id`
- `node_type`
- `stage`
- `step_id`
- `status`
- `started_at`
- `ended_at`
- `evidence_refs`

可选字段：

- `turn_index`
- `reason`
- `response_excerpt`
- `failure`
- `artifact_paths`

## Evaluability 规则

一个 workflow 进入主 benchmark 表时，必须同时满足：

1. `protocol_ok=true`
2. `inputs_ready=true`
3. `env_ready=true`
4. 未命中已知 workflow-level 硬错误

`not_evaluable` 的典型原因：

- `workflow_protocol_failure`
- `input_or_env_failure`
- `known_smoke_blocker`

## Failure Onset 规则

- 优先找第一个导致后续状态不可恢复的偏航事件。
- 如果最后报错只是下游症状，则不把它标为 onset。
- 如果 workflow 本身不可评，则 onset 类别优先标为 `workflow_not_evaluable`。

第一版 onset category 固定为：

- `workflow_not_evaluable`
- `wrong_step_selection`
- `missing_input_not_detected`
- `execution_failure_not_recovered`
- `validation_failure_ignored`
- `hallucinated_success_summary`

## Replay 规则

- replay 只能注入压缩后的诊断信号，不允许直接人工改 workflow 资产。
- replay 必须保持：
  - 同 workflow
  - 同 timeout
  - 同 max turns
  - 同模型
  - 同 env / cache policy

允许注入的 replay 信号：

- `failure_onset`
- `downstream_error_chain`
- `allowed_recovery_advice`

## 主表与审计表

- `benchmark_main_table`
  - 仅统计 `evaluable=1` 的 runs
  - 核心指标：
    - `workflow success`
    - `step completion ratio`
    - `declared output coverage`
    - `runtime`
    - `llm calls`
    - `tokens`
    - `cost`

- `trace_audit_table`
  - 统计所有 runs
  - 核心指标：
    - `onset_stage`
    - `onset_category`
    - `time_to_onset`
    - `recovery_attempt_count`
    - `false_success_claim`
    - `error_chain_length`

## 论文叙事对应

- `BiomniBench / BixBench` 负责回答：
  - 为什么不能只看终局正确率
  - 为什么要筛掉不可评样本
  - 为什么要保留过程证据

- `CodeTracer` 负责回答：
  - 过程如何结构化表示
  - 失败起点如何定位
  - 定位出的诊断如何变成可执行改进
