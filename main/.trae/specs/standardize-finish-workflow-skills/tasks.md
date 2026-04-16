# Tasks

- [ ] Task 1: 盘点 `finish/` 下全部 workflow，并审核现有 step 拆分是否合理。
  - [ ] SubTask 1.1: 列出所有 workflow、现有 step 文件、运行入口和已有元数据文件。
  - [ ] SubTask 1.2: 依据“单一职责、边界清晰、输入输出可定义、可独立执行”标准审核每个 step。
  - [ ] SubTask 1.3: 为每个 workflow 形成“沿用现有 step / 需调整”的结论与理由。

- [ ] Task 2: 为所有确认保留的 step 定义统一 skill 规范。
  - [ ] SubTask 2.1: 确定标准 skill 的命名规则、目录布局和 `SKILL.md` 模板。
  - [ ] SubTask 2.2: 为每个 step 明确 skill 的用途、触发条件、输入、输出、依赖和失败处理规则。
  - [ ] SubTask 2.3: 建立 workflow → step → skill 的映射表。

- [ ] Task 3: 统一 workflow 级接入元数据与 I/O 契约。
  - [ ] SubTask 3.1: 确认每个 workflow 的规范输入、规范输出、默认入口和 step 依赖关系。
  - [ ] SubTask 3.2: 检查各 workflow 的 manifest/know-how 缺口与输出定义不一致问题。
  - [ ] SubTask 3.3: 定义需要补齐或修正的 metadata 项，以支持 `Renzo_DA_Agent` 统一发现与执行。

- [ ] Task 4: 设计并实现 direct run 基线实验。
  - [ ] SubTask 4.1: 选定每个 workflow 的完整运行入口与执行参数。
  - [ ] SubTask 4.2: 运行一次完整 workflow，并记录输出文件、日志、状态和失败信息。
  - [ ] SubTask 4.3: 形成 direct run 的实验记录格式，便于与 agent run 对比。

- [ ] Task 5: 设计并实现 agent 自主编排实验。
  - [ ] SubTask 5.1: 仅向 agent 暴露 workflow 总体输入输出、可用 skill 集和必要环境信息。
  - [ ] SubTask 5.2: 通过 `finish/Renzo_DA_Agent` 执行一次 agent orchestrated run，由 agent 自主选择与组合 step skill。
  - [ ] SubTask 5.3: 记录 agent 的可观察思考轨迹、skill 选择序列、执行结果和失败信息。

- [ ] Task 6: 产出统一对比结果。
  - [ ] SubTask 6.1: 对比 direct run 与 agent orchestrated run 的输出完整性和执行结果。
  - [ ] SubTask 6.2: 汇总每个 workflow 的 step 合理性结论、skill 清单与实验结果。
  - [ ] SubTask 6.3: 整理最终交付内容，确保失败案例也被完整记录。

# Task Dependencies
- Task 2 depends on Task 1
- Task 3 depends on Task 1
- Task 4 depends on Task 3
- Task 5 depends on Task 2
- Task 5 depends on Task 3
- Task 6 depends on Task 4
- Task 6 depends on Task 5
