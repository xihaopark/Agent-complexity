# CPL-Article（补充语料，非方法学 PDF skill）

本目录用于在 **Paper2Skills / paper_primary_benchmark** 中挂载 **CPL-Article** 公开语料：描述 **Nextflow** 工作流的英文文章 + **BRAT** 格式的「生信工具名」标注。与 [`workflow_literature_map.json`](../workflow_literature_map.json) 中的 **方法学主文献 DOI** 是互补关系，不是替代。

| 维度 | `workflow_literature_map` | CPL-Article |
|------|---------------------------|-------------|
| 内容 | 各 Snakemake finish 对应的 **工具论文**（DESeq2、MACS2…） | **26 篇** PMC 论文正文片段 + 工具 mention **金标注** |
| 典型用途 | Paper arm：告诉 agent **怎么分析** | 补充：**工作流论文里工具名怎么写**、NER/对齐类上下文、与 CoPaLink 实验对齐 |
| 格式 | JSON DOI 列表 + 可选 PDF skill | `PMID*.txt` + `PMID*.ann`，5 个 `iteration_*` × `train`/`val` |

## 权威来源与许可

- **数据集**：Sebe et al., *CPL-Article*，Zenodo，<https://doi.org/10.5281/zenodo.18526700>  
- **许可**：**CC BY-NC-SA 2.0**（非商业；衍生需相同方式共享）。使用或写入文档时请保留上述引用与 DOI。  
- 官方说明：26 篇文章、约 36k tokens、669 次工具出现（282 个不同工具名）— 以 Zenodo 页面为准。

## 如何把 zip 放到本目录

任选其一（得到的路径应为 **`literature/cpl_corpus/CPL-Article.zip`**，与仓库根相对）：

1. **从同事本机拷贝**（例如对方 Downloads 里的同名文件）到本目录：  
   `…/main/paper_primary_benchmark/literature/cpl_corpus/CPL-Article.zip`
2. **官方下载**（与 Zenodo 上文件一致）：

```bash
# 在仓库根目录执行
curl -fsSL -o main/paper_primary_benchmark/literature/cpl_corpus/CPL-Article.zip \
  "https://zenodo.org/records/18526700/files/CPL-Article.zip?download=1"
```

`CPL-Article.zip` 与解压目录 `_extract/` 已写入 **`.gitignore`**，避免误提交大文件或与许可不符的再分发；团队各自放置或 curl 即可。

## 目录结构（解压后）

```
CPL-Article/
  iteration_{1..5}/
    train/   PMID*.txt  PMID*.ann
    val/     PMID*.txt  PMID*.ann
```

- **`.txt`**：文章纯文本（CoPaLink / Paper2Skills 侧若做「文章 vs 代码」对齐可参考）。  
- **`.ann`**：[BRAT standoff](https://brat.nlplab.org/standoff.html) 标注，实体类型与工具名边界以文件内容为准。

## 清点与校验

```bash
python3 main/paper_primary_benchmark/literature/tools/cpl_corpus_inventory.py
python3 main/paper_primary_benchmark/literature/tools/cpl_corpus_inventory.py --json
```

可选：`--zip /path/to/CPL-Article.zip` 指向任意位置的副本（例如仍放在 `~/Downloads` 时只做清点）。

## 与「补充 skills」的衔接（建议）

- **当前**：本语料 **尚未** 接入 `batch_runner.py` 的 `manifest.json` Paper arm；作为 **离线资源** 供人工摘取示例、或后续写「CPL 工具命名风格」小 skill。  
- **若要自动注入**：可在 `experiments/skills/` 下新增一篇简短 `SKILL.md`（摘录数条 `.ann` 规则 + 指向本目录路径），并在对应 `manifest.json` 里为 **特定 task_id** 挂上该 skill；需单独评审版权与 prompt 长度。  
- **相关外部项目**：仓库内 `external/sharefair/copalink` 使用同一 CPL 生态（CPL-Code、CPL-Gold 见各自 Zenodo）。

---

*维护：放入或更新 `CPL-Article.zip` 后运行 `cpl_corpus_inventory.py` 核对 `unique_pmids == 26`。*
