# LLM × Skill 消融实验协议（主 benchmark / R-task）

## 目的

在相同 **registry、任务、超参** 下，区分三类信号：

1. **脚本基线（无 LLM）**：只测环境与轨迹落盘。
2. **LLM、无文献 skill**：不注入 `workflow_literature_map` / 不加载 `paper-primary-literature-methods`。
3. **LLM + 文献 skill**：在对话或系统提示中可引用映射表中的 **DOI/方法名**（或启用 Cursor skill）。

## 角色分工（可由不同人或不同运行批次承担）

| 角色 | 职责 | 验证点 |
|------|------|--------|
| **Runner-A（脚本）** | 只跑 `--smoke` | 退出码 0、每条有 `trajectory.jsonl` |
| **Runner-B（LLM 裸跑）** | OpenRouter + 最短 `sys_prompt`（不提 DOI） | 能否完成 `output/result.txt` |
| **Runner-C（LLM+skill）** | 同 B，但 prompt/skill 含对应 workflow 的 1–2 条引用 | 与 B 对比步数/错误类型（探索性） |

## 固定变量

- `registry`：建议先用 `r_tasks/registry.sample_50.json` 或单条 `pilot_hello`。
- `max_steps`、`agent.llm_model`：B 与 C **必须一致**。
- 随机种子：对 LLM 若可设 seed，B/C 对齐。

## 记录字段

每次运行保存 `metadata.json` 中已有字段；额外建议实验笔记中记录：**arm（A/B/C）、skill 是否启用、workflow_id**。

## 与文献下载的关系

文献 PDF 不自动进入 agent 上下文；**skill 或手工粘贴摘要/DOI** 才构成「有 skill」条件。PDF 下载见 `literature/tools/download_open_access_pdfs.py`。
