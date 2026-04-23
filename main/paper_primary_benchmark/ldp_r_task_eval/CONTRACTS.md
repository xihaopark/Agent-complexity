# ldp / Aviary / fhda 接口摘要（供 RTaskEvalEnv 对齐）

本文件记录在常见安装下的 **异步契约**，便于独立 venv（Python ≥3.12）中对照源码更新。

## 独立环境（推荐）

与 `main/finish/Renzo_DA_Agent` 等子项目分开安装，避免 `ldp` / `fhaviary` 版本冲突：

```bash
python3.12 -m venv .venv-ldp-r-task
source .venv-ldp-r-task/bin/activate   # Windows: .venv-ldp-r-task\Scripts\activate
pip install -r main/paper_primary_benchmark/ldp_r_task_eval/requirements.txt
```

升级依赖后请对照下面各节核对签名；本仓库 **不** 依赖 `fhda` 来运行 `RTaskEvalEnv`（仅 BixBench 原版 `DataAnalysisEnv` 需要）。

## `aviary.env.Environment`（抽象）

- `async def reset(self) -> tuple[Messages, list[Tool]]`
- `async def step(self, action: ToolRequestMessage) -> tuple[Messages, float, bool, bool]`  
  返回：`next_observations`, `reward`, `done`, `truncated`
- 基类提供 `exec_tool_calls(...)` 用于执行 `ToolRequestMessage` 中的工具调用。

来源：`site-packages/aviary/env.py`。

## `fhda.data_analysis_env.DataAnalysisEnv`

- 继承 `NBEnvironment`，在 `reset` 中注入 `problem`、`system_prompt` 等消息。
- 评测 BixBench 原版任务时使用；**本仓库的 `RTaskEvalEnv` 不继承该类**，仅复用 **同一套 `reset`/`step` 签名**，以便与 `ldp.agent.Agent` 及 BixBench 式 `vanilla_rollout` 循环对接。

## `ldp.agent.Agent`

- `async def init_state(self, tools: list[Tool]) -> TAgentState`
- `async def get_asv(self, agent_state, obs: list[Message]) -> tuple[OpResult[ToolRequestMessage], TAgentState, float]`  
  动作取 `action.value`（`ToolRequestMessage`）传入 `environment.step`。

## `ldp.agent.simple_agent.SimpleAgent`

- 构造需 `llm_model` 等（见 `ldp` 文档与 BixBench YAML）。
- 依赖 **LM 后端**（环境变量如 `OPENAI_API_KEY` 或项目所用 OpenRouter 配置，视 `lmi` 集成而定）。

## 建议

- 评测代码与 **Renzo / main/finish** 使用 **不同 venv**，避免与 BixBench 依赖冲突。
- 升级 `ldp`/`aviary`/`fhda` 后重新核对上述签名。
