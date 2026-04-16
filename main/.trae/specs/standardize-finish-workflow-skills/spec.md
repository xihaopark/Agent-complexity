# Finish Workflow Step 审核与 Skill 标准化 Spec

## Why
当前 `finish/` 下的 workflow 已经被拆分为多个 step，但不同 workflow 的 step 粒度、元数据完备度、以及与 `Renzo_DA_Agent` 的接入方式并不统一。需要先审核现有 step 拆分是否合理，再在不破坏现有结构的前提下，把所有可复用 step 标准化为可编排的 skill，并建立可复现实验来比较“直接运行 workflow”和“由 agent 自主选择并编排 step skill 运行”两种模式。

## What Changes
- 审核 `finish/` 下所有 workflow 的现有 step 划分，定义“可直接复用 / 需要调整”的判定标准。
- 统一每个 workflow 的 step 元数据，明确 step 的输入、输出、依赖、边界与可独立执行条件。
- 为所有确认保留的 step 定义标准 skill 规范，包括命名、目录结构、说明文档、输入输出契约和调用约束。
- 建立 workflow → step → skill 的映射关系，并定义 agent 编排时的选择边界。
- 定义两类运行实验：
-  基线实验：按 workflow 原始 step 顺序完整运行一次并记录输出。
-  agent 实验：仅提供 workflow 总体输入输出约束，由 agent 决定调用哪些 step skill 以及编排顺序，再运行并记录结果。
- 定义统一的运行记录规范，保存输出清单、运行日志、可观察的 agent 推理轨迹、执行结果和对比结论。

## Impact
- Affected specs: finish workflow step 规范、workflow manifest 规范、step skill 规范、Renzo workflow 对比实验规范
- Affected code: `finish/*-finish/steps/*`、`finish/*-finish/manifest.json`、`finish/*-finish/know-how.md`、`.trae/skills/*`、`finish/Renzo_DA_Agent/*`

## ADDED Requirements
### Requirement: Step 拆分审核
系统 SHALL 对 `finish/` 下每个 workflow 的现有 step 做结构审核，并为每个 step 产出明确结论：可复用、需合并、需进一步拆分、或缺少必要元数据。

#### Scenario: 现有 step 拆分合理
- **WHEN** 某个 step 拥有单一职责、输入输出清晰、依赖边界明确，且可以作为独立执行单元被单独调用
- **THEN** 该 step 被标记为“可复用”，并沿用现有 step 文件与执行入口

#### Scenario: 现有 step 拆分不合理
- **WHEN** 某个 step 同时承担多个不可分离阶段、依赖跨越不清晰、或无法定义稳定输入输出
- **THEN** 该 step 被标记为“需调整”，并记录建议的重构方向

### Requirement: 标准 Step Skill 定义
系统 SHALL 为每个被确认保留的 step 定义一个标准 skill，使其具备统一的名称、用途说明、触发时机、必需输入、期望输出、依赖前置条件、执行入口和失败处理约束。

#### Scenario: 从 step 生成标准 skill
- **WHEN** 某个 workflow step 被判定为可复用
- **THEN** 系统为该 step 生成对应 skill 规格，并将 step 的边界直接映射为 skill 的输入输出契约

#### Scenario: skill 供 agent 编排
- **WHEN** agent 需要在 workflow 运行期间决定下一步执行内容
- **THEN** agent 仅可在该 workflow 允许的 step skill 集合内做选择，并遵循依赖关系和输入输出约束

### Requirement: Workflow I/O 与 Step I/O 规范化
系统 SHALL 为每个 workflow 定义规范化的总体输入和总体输出，同时为每个 step 定义规范化的输入、输出与依赖，以支撑 direct run 与 agent orchestrated run 的一致对比。

#### Scenario: 记录 workflow 总体 I/O
- **WHEN** 某个 workflow 被纳入对比实验
- **THEN** 系统记录该 workflow 的规范输入、规范输出、默认运行入口、step 顺序和 step 依赖图

#### Scenario: 记录 step I/O
- **WHEN** 某个 step 被纳入 skill 集
- **THEN** 系统记录其最小输入集合、产物输出集合、执行命令入口和对上游产物的依赖

### Requirement: 基线运行实验
系统 SHALL 支持对每个 workflow 执行一次完整的基线运行，使用 workflow 既有的标准入口或既定 step 顺序完成执行，并保存运行结果。

#### Scenario: 执行 direct workflow run
- **WHEN** 用户要求进行 workflow 基线运行对比
- **THEN** 系统按 workflow 原始或既定顺序完整运行一次，并记录实际输出文件、日志、状态和失败信息

### Requirement: Agent 自主编排实验
系统 SHALL 支持只向 agent 提供 workflow 总体输入输出和可用 skill 集，而不预先固定中间 step 顺序，由 agent 自主决定 step skill 的选取与组合并执行一次完整运行。

#### Scenario: 执行 agent orchestrated run
- **WHEN** agent 获得 workflow 总体输入输出定义、step skill 集合和运行环境
- **THEN** agent 自主决定调用哪些 step skill、按何顺序执行、何时重试或终止，并记录完整执行过程

### Requirement: 运行记录与对比输出
系统 SHALL 为 direct run 与 agent orchestrated run 统一保存可比对的实验记录，至少包括输出清单、执行状态、日志、可观察的 agent 推理轨迹、step 选择序列和最终对比结论。

#### Scenario: direct run 成功或失败
- **WHEN** 基线运行结束
- **THEN** 系统保存最终状态、输出产物索引、日志位置和失败原因（如失败）

#### Scenario: agent run 成功或失败
- **WHEN** agent 编排运行结束
- **THEN** 系统保存最终状态、输出产物索引、agent 的可观察计划/决策轨迹、实际调用的 skill 序列、日志位置和失败原因（如失败）

## MODIFIED Requirements
### Requirement: Finish Workflow 接入元数据
系统 SHALL 为 `finish/` 下每个纳入对比实验的 workflow 提供统一的接入元数据，使 `Renzo_DA_Agent` 可以稳定发现 workflow、理解 step 列表、读取输入输出契约，并驱动 direct run 与 agent orchestrated run。

#### Scenario: workflow 元数据已存在且完整
- **WHEN** 某个 workflow 已具备可被 `Renzo_DA_Agent` 读取的规范化元数据
- **THEN** 系统沿用现有定义，并补足缺失字段而不改变已验证通过的 step 结构

#### Scenario: workflow 元数据缺失或不一致
- **WHEN** 某个 workflow 缺少根级 manifest、缺少 know-how，或 step 输出定义与真实产物不一致
- **THEN** 系统补齐或修正元数据，使 workflow、step、skill 与实际运行结果一致

## REMOVED Requirements
- 暂无
