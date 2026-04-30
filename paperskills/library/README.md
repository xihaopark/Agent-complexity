# Paper Skills Library（统一文献资产库）

> **定位**：为 Paper2Skills 项目及下游 agent 提供**可检索、分门别类、版本可控**的 paper-derived skills 集合。

---

## 目录结构（四级分类）

```
paperskills/library/
├── indices/                    # 检索索引（JSON/TSV）
│   ├── master_index.json       # 所有 entries 的主索引
│   ├── by_doi.json             # DOI -> entry 快速查找
│   ├── by_tool.json            # 工具名 -> entries
│   ├── by_family.json          # 技术领域 -> entries
│   └── by_task.json            # task_id -> recommended papers
├── methods/                    # 方法学主文献（Type C Paper Skill）
│   ├── 10.1186_s13059-014-0550-8/   # DESeq2
│   ├── 10.1093_nar_gkv007/          # limma
│   └── ...                      # 其余 18+ 篇
├── workflows/                  # 工作流/管线论文（CPL-Article 类）
│   └── cpl_article/            # 26 篇 Nextflow 工作流描述
│       ├── manifest.json       # PMID/标题/工具列表
│       └── annotations/        # BRAT 标注轻量索引
└── references/                 # 综述、指引性文献
    └── rna-seq-best-practices/ # 如 10.1186/s13059-016-0881-8
```

---

## Entry 字段规范（master_index.json）

| 字段 | 类型 | 说明 |
|------|------|------|
| `doi` | str | 标准斜杠 DOI |
| `doi_slug` | str | 目录安全名（`_` 替换） |
| `title` | str | 论文标题（优先 Crossref，次 PDF meta） |
| `authors` | list | 第一/通讯作者简化 |
| `year` | int | 发表年 |
| `tool` | str | 核心工具名（如 DESeq2, MACS2） |
| `family` | str | 技术领域：rna, chip, methyl, scrna, variant, epigenomics... |
| `kind` | str | `method` / `workflow` / `reference` |
| `source` | str | 来源：`extracted_pdf` / `cpl_article` / `external_import` |
| `skill_md_path` | str | 相对本库根目录的 SKILL.md 路径 |
| `pdf_path` | str | 原始 PDF 路径（可留空，版权敏感） |
| `brat_annotated` | bool | 是否有 BRAT/CPL 标注 |
| `tasks_recommended` | list | 推荐应用的 task_id 列表 |
| `extracted_date` | str | ISO 日期 |

---

## Agent 检索接口

```python
from paperskills.library.indices import LibraryIndex

lib = LibraryIndex()

# 按 DOI 查
entry = lib.by_doi("10.1186/s13059-014-0550-8")

# 按工具名查（模糊匹配）
entries = lib.by_tool("DESeq2", fuzzy=True)

# 按技术领域查
entries = lib.by_family("rna")

# 按任务推荐
papers = lib.recommended_for_task("deseq2_lrt_interaction")

# 全文检索（仅限 SKILL.md 文本）
results = lib.search("shrinkage estimation")
```

详见 `indices/` 下各模块。

---

## 与主 benchmark 的衔接

- **methods/** 下的 skill 通过 `main/paper_primary_benchmark/experiments/skills/manifest.json` 被 `batch_runner.py` 读取。
- **workflows/cpl_article/** 是**补充上下文**（工具名 mention 风格），默认**不**直接作为 Paper arm 的 skill 注入，但可在特定 NER/对齐 task 中引用。

---

## 维护流程

1. **新增方法学 PDF**：放入 `literature/pdfs/` → 运行提取脚本 → 生成 `methods/<doi_slug>/` → 更新 `master_index.json`。
2. **新增 CPL 类工作流论文**：更新 `workflows/cpl_article/manifest.json`，不复制全文，仅保留元数据 + BRAT 索引指针。
3. **批量导入外部集合**：使用 `scripts/import_external_papers.py --source-dir /path/to/bio_papers --dry-run` 预检重复，再执行。

---

*Library version: 2026-05-01*  
*Maintainer: Paper2Skills team*
