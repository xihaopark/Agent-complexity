# Paper2Skills 项目介绍（对外版）

> 面向：希望了解本 benchmark 如何构建、如何跑实验、如何读结果的同事或合作方。  
> 技术细节仍以仓库内 `main/paper_primary_benchmark/`、`PAPER2SKILLS_FINAL_REPORT_V2.md` 等为准。

---

## 1. 我们在做什么

**Paper2Skills** 研究的是：在**真实生信分析场景**里，把**方法学主文献**（primary method papers）整理成可被 agent 使用的 **skill 上下文**后，是否比「只靠通用 LLM」「只靠管线脚本摘要」更能做出**正确、可复现**的分析。

为此我们做了三件事：

1. **固定一套主实验 workflow**（Snakemake finish 仓库集合），并为每条 workflow 挂上**代表性方法论文**（DOI），而不是假设「一个仓库 = 一篇论文」。
2. **设计一批以 R 为主的独立评测任务（R-task）**：agent 在沙箱工作区里读写文件、跑 shell / `Rscript`，完成 `OBJECTIVE.md` 描述的目标；任务刻意包含「默认写法容易错」的设定，以便区分不同信息条件。
3. **在相同任务与超参下做多臂（arm）对比**，并用离线脚本对照 **paper-guided 参考答案** 打分，衡量各臂的通过率与失败模式。

---

## 2. 论文与方法文献如何收集、如何进项目

### 2.1 起点：主 workflow 集合

主集合来自 **`MAIN_WORKFLOW_SET`（v2）**：约 **30** 条 finish 级 Snakemake 管线 + 少量 smoke，作为后续 baseline 与对比的默认对象。清单与入选理由见 `main/refine-logs/MAIN_WORKFLOW_SET.md` 及对应 JSON。

在 `main/paper_primary_benchmark/` 下用 **`manifest.json`**、`workflows/` 符号链接等提供**统一项目视图**；真实资产仍在 `main/finish/<workflow_id>/`，避免复制整套仓库。

### 2.2 Workflow → 方法论文（DOI 映射）

多数 finish 管线是**组合型** GitHub/Snakemake 项目，往往**没有**一篇论文与仓库一一对应。因此我们维护 **`literature/workflow_literature_map.json`**：

- 为每条主实验 workflow 列出**工具原作者论文或标准引用**（DOI、方法名等），用于 Related Work、复现实验背景，以及给 agent 当 **skill 的元数据入口**。
- 映射表带版本号与审计说明（例如 DOI 纠错、扩展 coverage），见文件内 `disclaimer` 与 `audit_notes`。

### 2.3 开放获取 PDF 与「论文 → Skill」工具链

- **OA PDF**：通过 **Unpaywall**（需设置 `UNPAYWALL_EMAIL`）批量拉取开放获取 PDF，脚本见 `literature/tools/download_open_access_pdfs.py`；PDF 默认落在 `literature/pdfs/`（通常 gitignore，注意版权与使用权）。
- **Paper → Cursor Skill**：可用 `literature/tools/paper_to_skill.py` 等，从 DOI / Crossref / PDF 文本侧生成 skill 目录（具体参数见 `literature/README.md`）。
- 仓库内还可配合既有 **Semantic Scholar** skill、paperskills 里的 Type C 范式等，按主题或引用补文献；总控说明见 `main/paper_primary_benchmark/experiments/AGENT_DRIVER.md`。

**重要约定**：PDF **不会**自动进入每次 rollout 的上下文；**只有**在配置里注入 skill、或在 system prompt 中粘贴摘要/DOI 等，才构成「有文献信息」的实验臂。

---

## 3. Task 如何设计

项目里有两类「task」概念，**正交**，不要混用：

| 类型 | 用途 | 位置（概念上） |
|------|------|----------------|
| **Pipeline task 覆盖层** | 论文与实验管理：把 finish `manifest.json` 里的 **steps** 粗粒度切成若干 stage（输入/输出/标签），方便叙述「做到哪一阶段」。 | `paper_primary_benchmark/task_definitions/*.json` |
| **R-task（ldp 评测）** | 给 **ldp SimpleAgent** 用的独立工作区：无 Snakemake、无 notebook kernel，只靠 shell / Rscript / 文件工具完成分析。 | `ldp_r_task_eval/tasks/...`、`r_tasks/registry*.json` |

Paper2Skills 的核心对比实验建立在 **R-task** 上（尤其是 `tasks/real/` 与 paper-sensitive 子集）。

### 3.1 R-task 的目录与内容

典型 **真实任务** 包含（见 `PAPER2SKILLS_TASK_BLUEPRINT.md`）：

- **`tasks/.../<task_id>/`**：`OBJECTIVE.md`（给 agent 的自然语言目标，可**有意省略**「一步写对」所需的方法细节）、`meta.json`、`input/` 等。
- **`.../real_ground_truth/<task_id>/`**：`reference/script.R`（**按论文建议**写的参考解法）、`reference_output/`（期望产物），用于离线评估；**对 agent 不可见**。

设计时强调的原则包括：**难度**（无 paper 时基线易失败）、**与论文工具一致**、**可评估的输出**（如 TSV/CSV 优于裸 RDS）、**有区分度**（Paper 臂相对 None 臂明显提升）。

### 3.2 四臂（Four-arm）消融在比什么

在相同 registry、任务与超参下，对比四类信息条件（命名与 batch id 约定见评测脚本，如 `evaluate_real_run_v3.py` 中的 arm 识别）：

1. **None**：不注入基于主文献的 skill / 不在 prompt 中给对应 DOI 方法指引（裸 LLM 能力上限为主）。
2. **LLM_Plan**：在「规划」层面给予额外结构化提示，但**不等同于**完整论文级细节（用于分离「会写计划」与「懂方法论文」）。
3. **Pipeline**：利用 **管线溯源**（workflow id、stage、family 等）作为上下文，代表「只知仓库管线、不知论文细论证」的情形。
4. **Paper**：注入由 **workflow_literature_map + 论文衍生 skill** 构成的方法上下文，检验「文献进上下文」的收益。

具体每条 run 的 `skill.arm` 等元数据会写入 `metadata.json`，便于事后按臂聚合。

---

## 4. 实验如何执行

### 4.1 环境与 Agent 循环

- **评测环境**：`RTaskEvalEnv`（`ldp_r_task_eval/r_task_env.py`）实现与 **aviary `Environment`**、**ldp `Agent`** 一致的 `reset` / `step` 异步契约（摘要见 `CONTRACTS.md`）。
- **工具**：工作区列表、读写字典文件、**shell**、**Rscript**、可选的 `write_plan` / `check_progress` / **`submit_done`** 等。
- **Agent**：`ldp` 的 **`SimpleAgent`**：每步将对话历史交给 LLM（经 LiteLLM，可配置 OpenRouter 等），解析为 **ToolRequestMessage**，再交给环境执行；`sys_prompt` 由各臂配置决定。
- **Rollout**：`vanilla_r_task_rollout`（`rollout.py`）负责 BixBench 式 observe→act 循环，并落盘 **`trajectory.jsonl`**、**`metadata.json`** 等。

### 4.2 单条与批量

- **单任务 pilot**：`run_pilot.py` + YAML（如 `config/pilot_example.yaml`、`pilot_openrouter.yaml`）。
- **批量**：`batch_runner.py` 读取 **`r_tasks/registry.json`**（或 `registry.real.json`、sample 子集等）；`--smoke` 为无 LLM 的脚本化成功路径，用于 CI 与环境自检。

### 4.3 依赖与隔离

推荐 **Python ≥3.12**，独立 venv：`pip install -r main/paper_primary_benchmark/ldp_r_task_eval/requirements.txt`。与仓库内其他子项目（如 BixBench 原版环境）分开安装，避免 `ldp` / `aviary` 版本冲突。

---

## 5. 如何评估 Agent

### 5.1 环境内「成功」信号

`RTaskEvalEnv` 的轨迹奖励与 **是否产生约定成功产物** 相关：默认关注工作区内是否存在 **`output/result.txt`**（或任务配置的 `success_artifact_glob`）。这保证「跑完并声明完成」可被自动判定；**数值是否正确**需依赖下游评估器或参考答案比对（见主目录 README 说明）。

### 5.2 离线评估器（V2 / V3）

- **`tools/evaluate_real_run_v2.py`**：对每次 run 的工作区输出与 **ground truth** 做对照，产生**逐任务分数**与策略标签（具体指标以脚本与 `EVALUATION_V3.md` 等文档为准）。
- **`tools/evaluate_real_run_v3.py`**：在 V2 之上增加 **insight** 层（无 LLM）：如 `failure_mode`、`actionable_fix`、**`skill_tokens_matched`**（agent 是否在工具参数中「露出」skill 中的关键 token，作为「是否读到 skill」的弱信号）等；大批量时可 `--insight-only` 复用已缓存的 V2 JSON。

### 5.3 汇报口径：从连续分数到 Binary 完全通过

内部曾用 **pass rate（步骤完成比例）** 等细粒度指标（见 `PAPER2SKILLS_PASSRATE_SUMMARY.md`）。对外的主要结论表（见 **`PAPER2SKILLS_FINAL_REPORT_V2.md`**）采用 **Binary**：**完全通过 = 1，否则 = 0**，便于在四臂之间直接对比「整题是否做对」。

解读建议：

- 先看 **全量任务** 上的完全通过率，再看 **剔除「四臂全过」后的差异化子集**，避免「简单题」稀释信号。
- 结合 V3 的 **failure_mode** 与 case study，讨论「缺的是论文知识、管线信息，还是实现与 I/O 细节」。

---

## 6. 文档与代码导航（给读者自用）

| 主题 | 路径 |
|------|------|
| 主 benchmark 总览与 ldp R-task 说明 | `main/paper_primary_benchmark/README.md` |
| 文献映射与下载、paper_to_skill | `main/paper_primary_benchmark/literature/README.md` |
| LLM × skill 三臂协议（概念上与四臂实验一致轴） | `experiments/llm_skill_ablation/PROTOCOL.md` |
| 实验驱动总流程 | `experiments/AGENT_DRIVER.md` |
| Task 设计蓝图与构建五步法 | `PAPER2SKILLS_TASK_BLUEPRINT.md` |
| 最终结果与表格、案例 | `PAPER2SKILLS_FINAL_REPORT_V2.md` |
| ldp / aviary 接口摘要 | `ldp_r_task_eval/CONTRACTS.md` |

---

## 7. 一句话总结

我们从 **固定生信 finish 集合** 出发，用 **workflow → 主文献 DOI** 建立方法学锚点，再构造 **对默认做法敏感** 的 **R 沙箱任务**，在 **None / LLM_Plan / Pipeline / Paper** 四臂下用同一套 **rollout + 离线对照** 评估 agent，从而量化 **「把论文装进 skill」** 是否带来可复现的收益。

---

*文档生成说明：结构与事实对齐仓库内 README、literature 工具说明、ldp_r_task_eval 实现及现有 Paper2Skills 报告；若集合规模或臂命名有更新，请以对应源文件为准。*
