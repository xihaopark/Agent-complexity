## Peer Agents (biomni / stella / tooluniverse)

目标：让 renzo 与其它 agent 以“并排可选”的方式运行 workflow（对比编排与产出），而不是把其它 agent 当作 renzo 的内部子模块。

### 运行方式

对比脚本：

- [run_finish_workflow_comparison.py](file:///lab_workspace/projects/Agent-complexity/main/finish/Renzo_DA_Agent/scripts/run_finish_workflow_comparison.py)

默认会跑：
- renzo（LangGraph 引擎）
- biomni / stella / tooluniverse（peer agent runner）

### 依赖

peer agent 运行需要：
- `OPENROUTER_API_KEY`（所有 agent 统一走 OpenRouter）
- Python 依赖：peer runner 使用 `requests`（OpenRouter）与 renzo 自带的 runners（snakemake/nextflow）
- Biomni 框架代码（本机路径）：默认 `/lab_workspace/projects/Biomni-main`
  - 可用环境变量覆盖：`BIOMNI_REPO_DIR=/abs/path/to/Biomni-main`
- ToolUniverse 官方 Python 包（真实框架模式）
  - 推荐放在独立环境：`peer_envs/tooluniverse`

可选（如果要跑更完整的框架能力，而不是仅 prompt 驱动）：
- Biomni：在对应的 python 环境中 `pip install -e /lab_workspace/projects/Biomni-main`
- STELLA：在对应的 python 环境中 `pip install -r /lab_workspace/projects/RBioBench/agents_run/stella/STELLA/requirements.txt`
- ToolUniverse：在对应的 python 环境中 `pip install tooluniverse`

推荐：用脚本创建独立环境（并排、互不污染）：
- [prepare_peer_agent_envs.sh](file:///lab_workspace/projects/Agent-complexity/main/finish/Renzo_DA_Agent/scripts/prepare_peer_agent_envs.sh)

### 自定义每个 agent 的 Python 解释器（可选）

如果你希望每个 agent 在各自的虚拟环境里运行，使用：

`--agent-pythons biomni=/abs/py,stella=/abs/py,...`

### 强制使用真实框架

对 biomni/stella，推荐开启：
- `--require-real-frameworks`

开启后：
- biomni 必须能初始化并调用 `biomni.agent.A1`
- stella 必须能初始化并调用 `stella_core.manager_agent.run`
- tooluniverse 必须能初始化并调用官方 `tooluniverse.agentic_tool.AgenticTool`

说明：
- 目前 `dswizard` 仍是仓库内的 style baseline，不应纳入“全部真实框架”正式实验；若严格要求所有 agent 都是真实框架，需要先替换成新的真实 agent comparator。

### Biomni shim

Biomni 的 `biomni.agent` 依赖 `newproj` 模块；本项目提供最小 shim 以满足 import：
- `peer_shims/newproj/...`

### Workflow 运行接口（输入/输出）

所有 agent（renzo 与 peers）遵循同一组“运行输入”概念：
- `workflow_dir`: 一个包含 manifest.json 与 steps/ 的 workflow 目录
- `finish_root`: finish 工作流池根目录（供 registry/loader 寻址）
- `data_root`: 本次 run 的数据根目录（运行时写日志/缓存）
- `strict_manifest`: 是否严格依赖 depends_on（true）或允许 skills-only 的非 DAG 编排（false）
- `timeout_per_step`: 单步超时（seconds）

所有 agent 都产出一个 JSON（`agent-<name>-run.json`），核心字段稳定：
- `mode`, `agent_name`, `workflow_id`, `workflow_dir`
- `status`, `workflow_status`
- `step_metrics`（逐步执行结果）
- `observed_outputs` / `declared_outputs`（输出采集与声明输出覆盖）
- `llm_trace`（selector/agent 调用轨迹；renzo 在 `final_state.llm_trace`）

### 行为差异

- renzo：执行 `_worker_agent`（完整 LangGraph：planner/coder/executor/...）
- 其它 agent：执行 `_worker_peer`（peer runner，不使用 renzo 的 LangGraph 图）
  - 使用 standardized workflow skills 组装 steps
  - 使用各自的 selector（biomni/stella/tooluniverse）从 ready steps 中选下一步
  - 通过相同的 runner（snakemake/nextflow）执行 step，保证“执行引擎一致，编排策略可比”
