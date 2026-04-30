# Paper Skills Library

> **设计哲学**: 建立 agent **自主发现、灵活选择** 的技能生态系统，而非强制的 task→skill 绑定。
> 
> 我们相信：好的 agent 应该能根据场景**判断**什么技能合适，而不是机械地跟随预设映射。

---

## 目录结构

```
paperskills/library/
├── README.md                          # 本文件
├── AGENT_USAGE_GUIDE.md              # ⭐ Agent 使用指南（必读）
├── query.py                           # 精确查询（DOI/Tool/Family）
├── discovery.py                      # ⭐ 场景发现（推荐）
│
├── indices/                           # 索引层
│   ├── master_index.json             # 全部 skill 元数据
│   ├── skill_graph.json              # ⭐ 语义网络（场景/关系/决策）
│   ├── library_index.py              # Python API
│   └── by_*.json                     # 辅助索引
│
├── methods/                           # 方法学文献（核心资产）
│   ├── 10.1186_s13059-014-0550-8/   # DESeq2
│   │   ├── SKILL.md                  # 标准化格式
│   │   └── run_manifest.json
│   └── ... (20+ papers)
│
├── workflows/                        # 工作流语料
│   └── cpl_article/                 # 26 篇 Nextflow 论文
│       └── manifest.json             # 轻量索引（不复制 PDF）
│
└── scripts/                           # 维护工具
    ├── import_external_papers.py     # 批量导入+去重
    └── rebuild_index.py              # 重建索引
```

---

## 快速开始

### 场景驱动发现（推荐）

```bash
# 我不确定用什么工具分析 RNA-seq 差异表达
python paperskills/library/discovery.py --scenario rna_de_analysis

# 输出：
# 📋 Scenario: Differential expression analysis of RNA-seq data
# 💡 Decision Guide: Use DESeq2 for count-based analysis...
# 🔧 Relevant Skills: DESeq2, limma
```

### 多条件匹配

```bash
# 明确条件：小样本 RNA-seq 差异分析
python paperskills/library/discovery.py \
    --analysis differential_expression \
    --data-type rna_seq_counts \
    --design small_sample
```

### 工具链探索

```bash
# 我在用 DESeq2，有什么替代选择？
python paperskills/library/discovery.py --alternatives-to DESeq2

# DESeq2 之后该做什么？
python paperskills/library/discovery.py --downstream-of DESeq2
```

---

## 核心概念

### 从 "Task→Skill 绑定" 到 "场景→相关 Skills"

| 旧模式 | 新模式 |
|--------|--------|
| `task_id` 强制指定一个 skill | Agent 根据场景**自主发现**多个候选 |
| 每个 task 只有一个 "正确" skill | 同一分析可用多种工具，各有优势 |
| 目标是验证 "绑定是否有效" | 目标是帮助 agent **做出明智选择** |
| 硬编码的 ground truth | 灵活的决策支持 |

### Skill 关系网络

```
DESeq2 ──┬── alternatives ──→ limma, edgeR
         ├── complements ───→ kallisto (quantification)
         ├── downstream ────→ clusterProfiler (enrichment)
         └── integrates_with → tximport (如果输入是 transcripts)
```

Agent 可以遍历这个网络，构建完整的分析 pipeline。

---

## Skill 标准格式 (SKILL.md)

```markdown
# ToolName

## Method
方法核心描述。包含：
- 统计模型/算法原理
- 适用数据类型
- 关键假设

## Parameters
关键参数及选择指南

## Commands / Code Snippets
可运行的代码片段

## Notes for R-analysis agent
Agent 专属建议：
- 何时使用 (use_when)
- 何时避免 (not_when)
- 常见陷阱
- 与其他工具的配合
```

---

## Discovery 系统详解

### skill_graph.json 结构

```json
{
  "skills": {
    "doi": {
      "tool": "工具名",
      "primary_analysis": "主要分析类型",
      "applicable_data_types": ["适用数据"],
      "experimental_designs": ["适用设计"],
      "tags": ["特征标签"],
      "strengths": ["优势"],
      "limitations": ["局限"],
      "related_tools": {
        "alternatives": ["替代工具 DOIs"],
        "complements": ["互补工具 DOIs"],
        "downstream": ["下游工具 DOIs"]
      },
      "use_when": ["使用场景"],
      "not_when": ["避免场景"]
    }
  },
  "discovery_rules": {
    "scenario_to_skills": {
      "scenario_name": {
        "description": "场景描述",
        "relevant_skills": ["相关 DOIs"],
        "decision_guide": "选择建议"
      }
    }
  }
}
```

### 发现模式

1. **scenario-based**: 预设常见分析场景（rna_de_analysis, scrna_clustering 等）
2. **criteria-based**: 多维度匹配（analysis + data_type + design）
3. **relationship-based**: 探索工具关系（alternatives, complements, downstream）

---

## 添加新 Skill

### 方法学论文

1. 放置 PDF 到合适目录（如 `literature/pdfs/`）
2. 运行提取生成 SKILL.md
3. **关键**: 填写 skill_graph.json 中的语义信息
   - `use_when` / `not_when` (帮助 agent 决策)
   - `related_tools` (建立网络关系)
   - `strengths` / `limitations` (客观评估)

### CPL 类工作流论文

```bash
# 只需更新 manifest，不复制全文
# 添加：PMID, title（如果已知）, tags
# 用途：帮助 agent 理解 "这类工作流论文中工具名如何出现"
```

---

## 与 Agent 实验的关系

### 四臂实验 (None/Paper/Pipeline/LLM_Plan) 的新理解

| Arm | 含义 | 如何实施 |
|-----|------|---------|
| **None** | Agent 不查询 library，凭 baseline 能力 | 不注入任何 skill context |
| **Paper** | Agent **可查询** library，自主决定用什么 | 提供 discovery.py 接口，agent 按需检索 |
| **Pipeline** | Agent 参考工作流管线信息 | 提供 workflow 上下文 |
| **LLM_Plan** | Agent 获得 LLM 生成的规划建议 | 提供结构化规划 prompt |

**关键区别**: 旧 Paper arm = "强制绑定某个 skill"；新 Paper arm = "**允许** agent 发现和使用 skills"。

### 评估指标的转变

| 旧指标 | 新指标 |
|--------|--------|
| "绑定 skill 后准确率" | "有 library 访问权时，agent 能否做出合适选择" |
| "完全遵循 paper 建议" | "基于 paper 建议做出明智决策" |
| "skill 是否被使用" | "skill 是否被**恰当地**使用" |

---

## 维护与扩展

### 重建索引

```bash
python paperskills/library/scripts/rebuild_index.py
```

### 批量导入外部论文

```bash
# 预览
python paperskills/library/scripts/import_external_papers.py \
    --source-dir /path/to/papers --dry-run

# 执行
python paperskills/library/scripts/import_external_papers.py \
    --source-dir /path/to/papers
```

### 添加新场景

编辑 `indices/skill_graph.json` → `discovery_rules.scenario_to_skills`

---

## 设计决策 FAQ

**Q: 为什么不强绑定 task→skill？**  
A: 真实生物信息学分析是灵活的。同样的 "RNA-seq DE" 任务，小样本用 DESeq2+apeglm，配对设计用 limma+duplicateCorrelation，批量效应用 ComBat-seq 预处理。强制绑定会抹杀这种灵活性。

**Q: Agent 选错了怎么办？**  
A: 这是重要的评估维度！我们想要的是 "agent 能否学会**判断**什么技能合适"，而不是 "agent 能否记住映射"。选错→反思→修正，是学习过程。

**Q: 如何确保一致性？**  
A: 通过 `use_when` / `not_when` 的明确描述，以及 `discovery.py` 的决策指导。不是强制一致性，而是**知情决策**。

**Q: 评估时怎么知道 agent 选择好不好？**  
A: 多重标准：
1. 结果正确性（是否通过评估）
2. 选择合理性（是否匹配 `use_when`）
3. 效率（是否避免了已知陷阱）

---

## 贡献

添加新 skill 时，请同时更新：
1. `methods/<doi_slug>/SKILL.md` - 技术内容
2. `indices/skill_graph.json` - 语义网络（最关键！）
3. `AGENT_USAGE_GUIDE.md` - 如果使用模式有变化

---

*Library Version: 2026-05-01-discovery*  
*Design: Discovery-oriented, Agent-autonomous*
