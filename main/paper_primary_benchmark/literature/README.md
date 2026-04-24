# 主实验 workflow ↔ 方法学文献

## 说明

- **30 个 finish workflow** 多为 GitHub/Snakemake **组合管线**，往往**没有**一篇论文与仓库 1:1 对应。
- [`workflow_literature_map.json`](workflow_literature_map.json) 为每条 workflow 列出 **代表性方法论文**（工具原作者论文或标准引用），用于复现实验背景、写 Related Work、或给 agent 当 **skill 上下文**。
- **版权**：请只下载与使用您有权使用的 PDF；开放获取链接依赖 [Unpaywall](https://unpaywall.org/) API。

## Paper → Skill（Crossref / PDF 文本）

```bash
python3 main/paper_primary_benchmark/literature/tools/paper_to_skill.py --doi 10.1038/nbt.3519 \
  --out-skill-dir .cursor/skills/paper-kallisto-nbt-3519
```

若 HTTPS 证书报错，可 `pip install certifi`（脚本会优先使用 certifi 的 CA 包）。

## 下载开放获取 PDF

需要设置邮箱（Unpaywall 要求）：

```bash
export UNPAYWALL_EMAIL='your@email.edu'
python3 main/paper_primary_benchmark/literature/tools/download_open_access_pdfs.py --all
```

PDF 默认写入 `literature/pdfs/`（目录已 gitignore，避免误提交版权材料）。

仅拉取元数据（不下载）：

```bash
python3 main/paper_primary_benchmark/literature/tools/download_open_access_pdfs.py --all --metadata-only
```

## 与 Cursor skills 的关系

项目内 skills 见仓库根 [`.cursor/skills/`](../../.cursor/skills/)：`paper-primary-literature-methods` 告诉 agent 如何查阅本目录；`paper-benchmark-llm-ablation` 描述 **有 skill / 无 skill / 脚本基线** 三种实验臂。
