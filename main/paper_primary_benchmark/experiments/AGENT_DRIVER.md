# Agent 驱动：实验 → 文献下载 → Paper → Skill

本页把 **ldp 实验**、**文献获取**（含仓库已有能力）、**论文转 Cursor Skill** 串成一条可交给 agent 执行或人工逐步跑的流水线。

## 仓库里已有的文献能力（不必重复造轮）

| 能力 | 位置 | 用途 |
|------|------|------|
| Semantic Scholar / venue 检索 | [`main/.trae/skills/semantic-scholar/SKILL.md`](../../.trae/skills/semantic-scholar/SKILL.md) | 按主题、引用找正式发表论文 |
| Paper 抽取与 Type C skill 说明 | [`paperskills/TYPE_C_PAPER_SKILL.md`](../../../paperskills/TYPE_C_PAPER_SKILL.md)、[`paperskills/PAPERS_EXTRACTED.md`](../../../paperskills/PAPERS_EXTRACTED.md) | 从 PDF 抽文本再合成 skill 的既有范式 |
| SkillFoundry 论文相关 starters | [`modules/SkillFoundry/skills/scientific-knowledge/`](../../../modules/SkillFoundry/skills/scientific-knowledge/) | triage、元数据等脚本化流程 |
| 主 benchmark DOI 映射 | [`literature/workflow_literature_map.json`](../literature/workflow_literature_map.json) | 30 条 workflow → 方法论文 DOI |

本目录下的 **Unpaywall 下载脚本**（[`literature/tools/download_open_access_pdfs.py`](../literature/tools/download_open_access_pdfs.py)）作为 **OA PDF 补链**；若你方已有更全的下载工具，可只保留 DOI 列表，下载步骤换用内部工具即可。

---

## 阶段 1：驱动 ldp / R-task 实验

**单任务冒烟（无 API）**

```bash
python3 main/paper_primary_benchmark/ldp_r_task_eval/run_pilot.py --smoke \
  --config main/paper_primary_benchmark/ldp_r_task_eval/config/pilot_example.yaml \
  --run-id agent_smoke_01
```

**Sample 50 批量冒烟**

```bash
python3 main/paper_primary_benchmark/ldp_r_task_eval/batch_runner.py \
  --registry main/paper_primary_benchmark/ldp_r_task_eval/r_tasks/registry.sample_50.json \
  --smoke
```

**真模型（OpenRouter）**：去掉 `--smoke`，使用 `config/pilot_openrouter.yaml`，并配置 `OPENROUTER_API_KEY` 或 `--openrouter-key-file`。

三臂消融（脚本 / LLM 无 skill / LLM+skill）见 [`llm_skill_ablation/PROTOCOL.md`](llm_skill_ablation/PROTOCOL.md)。

---

## 阶段 2：按 DOI 获取文献（可选 OA PDF）

**权威说明与命令**（环境变量、`--all` / `--metadata-only`、`pdfs/` 目录）见 **[`literature/README.md`](../literature/README.md)**，此处不重复。

快速示例（单 workflow，与主实验对齐）：

```bash
export UNPAYWALL_EMAIL='your@institution.edu'
python3 main/paper_primary_benchmark/literature/tools/download_open_access_pdfs.py \
  --workflow-id rna-seq-kallisto-sleuth-finish
```

**方式 B — 仓库内既有下载/检索工具**：可并行使用 Semantic Scholar skill、或你们自有的下载流水线；DOI 列表仍以 [`workflow_literature_map.json`](../literature/workflow_literature_map.json) 为准。

---

## 阶段 3：Paper → Cursor Skill（`.cursor/skills/`）

使用统一脚本从 **DOI（拉 Crossref 摘要）**、**本地 PDF** 或 **纯文本** 生成最小可用 `SKILL.md`：

```bash
# 仅 DOI（无 PDF 时：用 Crossref 标题/摘要填充 skill 正文）
python3 main/paper_primary_benchmark/literature/tools/paper_to_skill.py \
  --doi 10.1038/nbt.3519 \
  --out-skill-dir .cursor/skills/paper-kallisto-nbt-3519

# 本地 OA PDF（需 pip install pymupdf，可选）
python3 main/paper_primary_benchmark/literature/tools/paper_to_skill.py \
  --pdf main/paper_primary_benchmark/literature/pdfs/10.1038_nbt.3519.pdf \
  --out-skill-dir .cursor/skills/paper-kallisto-nbt-3519

# 已有抽取文本（例如来自 paperskills 流程）
python3 main/paper_primary_benchmark/literature/tools/paper_to_skill.py \
  --text-file path/to/excerpt.txt \
  --title "My paper title" \
  --out-skill-dir .cursor/skills/paper-custom
```

生成后，在 Cursor 中启用对应 **project skill**，或在 `sys_prompt` 中引用 skill 要点做 **LLM+skill** 臂。

---

## Agent 执行清单（可复制到任务描述）

1. 运行阶段 1 中一条命令，确认 `ldp_r_task_eval/runs/` 有 `metadata.json` + `trajectory.jsonl`。
2. 从 `workflow_literature_map.json` 选取目标 `workflow_id`，记录其 `doi`。
3. 尝试阶段 2 下载 OA PDF；若无 OA，仅用 DOI 走阶段 3 的 Crossref 模式。
4. 运行 `paper_to_skill.py` 写入 `.cursor/skills/...`。
5. 再跑阶段 1 的 LLM 实验，对比启用/不启用新 skill 的行为（见 PROTOCOL）。
