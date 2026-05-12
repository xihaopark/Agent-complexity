# Paper2Skills 4-Arm 实验运行手册

> 目标: 在 Qwen3 (本地 vLLM) 上运行 Tier A 5个任务的 4-Arm 消融实验
> 日期: 2026-04-23

---

## 前置条件检查清单

### 环境需求

- [ ] **R >= 4.3** 已安装，且以下包可用:
  ```r
  install.packages(c("DESeq2", "limma", "edgeR"))
  # Bioconductor
  if (!require("BiocManager", quietly = TRUE))
      install.packages("BiocManager")
  BiocManager::install(c("DESeq2", "limma", "edgeR", "apeglm", "ashr"))
  ```

- [ ] **Python >= 3.12** 已安装
  ```bash
  python3.12 -m venv .venv-paper2skills
  source .venv-paper2skills/bin/activate
  pip install -r main/paper_primary_benchmark/ldp_r_task_eval/requirements.txt
  ```

- [ ] **Qwen3 via vLLM** 已启动
  ```bash
  # 示例启动命令 (根据你的实际部署调整)
  vllm serve Qwen/Qwen3-32B --tensor-parallel-size 2 --max-model-len 32768
  # 或本地模型路径
  vllm serve /path/to/qwen3 --tensor-parallel-size 1
  ```

- [ ] **Paper PDFs 已下载**
  ```bash
  cd main/paper_primary_benchmark/literature
  export UNPAYWALL_EMAIL='your@email.edu'
  python3 tools/download_open_access_pdfs.py --all
  # 或手动下载关键 papers:
  # - DESeq2: 10.1186/s13059-014-0550-8
  # - limma: 10.1093/nar/gkv007
  ```

---

## 实验架构

### 5个 Tier A 任务

| Task | Family | 核心 Paper 方法 |
|------|--------|----------------|
| deseq2_apeglm_small_n | rna | `lfcShrink(type="apeglm")` |
| deseq2_lrt_interaction | rna | `nbinomLRT` with nested models |
| deseq2_shrinkage_comparison | rna | shrinkage estimator selection |
| limma_voom_weights | rna | `voomWithQualityWeights` |
| limma_duplicatecorrelation | rna | `duplicateCorrelation` |

### 4个实验臂 (Arms)

| Arm | Skill 来源 | 配置要点 |
|-----|-----------|---------|
| **none** | 无技能 | baseline，仅用默认系统提示 |
| **llm_plan** | LLM生成 | 用 LLM 基于任务描述生成 plan，作为 skill 注入 |
| **pipeline** | 代码模板 | 从 workflow R 脚本提取 generic template |
| **paper** | Paper提取 | 从 PDF 提取的方法学内容，通过 vision adapter |

---

## Phase 1: 生成 Ground Truth (Reference)

### 步骤 1.1: 运行 Reference Scripts

```bash
cd main/paper_primary_benchmark/ldp_r_task_eval/tasks/paper_sensitive_v1

# 任务 1: deseq2_apeglm_small_n
cd real/deseq2_apeglm_small_n/workspace
Rscript ../../real_ground_truth/deseq2_apeglm_small_n/reference/script.R
# 验证 output/de_results.csv 生成
cp output/de_results.csv ../../real_ground_truth/deseq2_apeglm_small_n/reference_output/

cd ../..  # back to paper_sensitive_v1

# 任务 2: deseq2_lrt_interaction
cd real/deseq2_lrt_interaction/workspace
Rscript ../../real_ground_truth/deseq2_lrt_interaction/reference/script.R
cp output/interaction_de.csv ../../real_ground_truth/deseq2_lrt_interaction/reference_output/

cd ../..

# 任务 3: deseq2_shrinkage_comparison
cd real/deseq2_shrinkage_comparison/workspace
Rscript ../../real_ground_truth/deseq2_shrinkage_comparison/reference/script.R
cp output/shrunk_de.csv ../../real_ground_truth/deseq2_shrinkage_comparison/reference_output/

cd ../..

# 任务 4: limma_voom_weights
cd real/limma_voom_weights/workspace
Rscript ../../real_ground_truth/limma_voom_weights/reference/script.R
cp output/de_results_weighted.csv ../../real_ground_truth/limma_voom_weights/reference_output/

cd ../..

# 任务 5: limma_duplicatecorrelation
cd real/limma_duplicatecorrelation/workspace
Rscript ../../real_ground_truth/limma_duplicatecorrelation/reference/script.R
cp output/paired_de.csv ../../real_ground_truth/limma_duplicatecorrelation/reference_output/
```

### 步骤 1.2: 验证 Ground Truth

```bash
# 检查所有 reference_output 目录
ls -lh real_ground_truth/*/reference_output/

# 验证文件格式 (应该都是 CSV/TSV)
head real_ground_truth/deseq2_apeglm_small_n/reference_output/de_results.csv
```

---

## Phase 2: 准备 4-Arm 技能输入

### 步骤 2.1: 准备技能清单 (Skill Manifests)

创建 `experiments/skills_paper2skills_v1/` 目录结构:

```
experiments/skills_paper2skills_v1/
├── none/              # 空技能（baseline）
├── llm_plan/          # LLM生成的计划技能
├── pipeline/          # 从 workflow 代码提取的模板
└── paper/             # 从 PDF 提取的 paper 技能
```

#### Arm 1: none (baseline)

无需准备技能文件。agent 仅使用系统默认提示。

#### Arm 2: llm_plan

对每个任务，用 LLM (Qwen3) 生成一个计划:

```python
# scripts/generate_llm_plan_skills.py
# 伪代码示例

def generate_llm_plan_skill(task_id, objective_md):
    """Generate skill from LLM plan"""
    prompt = f"""
    Based on the following task, create a step-by-step execution plan:
    
    {objective_md}
    
    Provide a concise plan with specific R code snippets where applicable.
    """
    
    # Call Qwen3 via vLLM API
    response = call_vllm(prompt, model="Qwen3-32B")
    
    # Save as skill
    skill_md = f"""# LLM-Generated Plan for {task_id}

## Execution Plan
{response}
"""
    return skill_md
```

#### Arm 3: pipeline

从 workflow R 脚本提取 generic code patterns:

```bash
# 提取 deseq2 workflow 的通用代码
python3 scripts/extract_pipeline_skill.py \
  --source main/finish/workflow_candidates/snakemake-workflows__rna-seq-star-deseq2/workflow/scripts/deseq2.R \
  --task deseq2_apeglm_small_n \
  --output experiments/skills_paper2skills_v1/pipeline/deseq2_apeglm_small_n/SKILL.md

# 提取 limma workflow 的通用代码
python3 scripts/extract_pipeline_skill.py \
  --source main/finish/workflow_candidates/epigen__dea_limma/workflow/scripts/limma.R \
  --task limma_voom_weights \
  --output experiments/skills_paper2skills_v1/pipeline/limma_voom_weights/SKILL.md
```

Pipeline skill 示例 (`deseq2_apeglm_small_n/SKILL.md`):

```markdown
# Pipeline Skill: DESeq2 Differential Expression

## Code Pattern

```r
library(DESeq2)

# Read counts
counts <- read.table(input_counts, header=TRUE, row.names="gene_id")
coldata <- read.table(input_coldata, header=TRUE, row.names="sample")

# Create DESeqDataSet
dds <- DESeqDataSetFromMatrix(countData=counts, colData=coldata, design=~condition)

# Filter and run
dds <- dds[rowSums(counts(dds)) > 1, ]
dds <- DESeq(dds)

# Results
res <- results(dds, contrast=c("condition", "treated", "untreated"))
```

## Common Parameters
- `design`: ~condition for simple 2-group comparison
- `contrast`: specify treatment vs control
```

#### Arm 4: paper

从 PDF 提取技能 (使用现有的 vision adapter):

```bash
# 下载或确认 paper PDF 存在
ls main/paper_primary_benchmark/literature/pdfs/10.1186_s13059-014-0550-8.pdf

# 提取 DESeq2 paper 技能
python3 main/paper_primary_benchmark/literature/tools/paper_to_skill.py \
  --pdf main/paper_primary_benchmark/literature/pdfs/10.1186_s13059-014-0550-8.pdf \
  --out-skill experiments/skills_paper2skills_v1/paper/deseq2_apeglm_small_n/SKILL.md \
  --focus "shrinkage estimators, apeglm, small sample sizes"

# 提取 limma paper 技能
python3 main/paper_primary_benchmark/literature/tools/paper_to_skill.py \
  --pdf main/paper_primary_benchmark/literature/pdfs/10.1093_nar_gkv007.pdf \
  --out-skill experiments/skills_paper2skills_v1/paper/limma_voom_weights/SKILL.md \
  --focus "voomWithQualityWeights, arrayWeights, sample quality"
```

---

## Phase 3: 运行 4-Arm 实验

### 步骤 3.1: 配置 Batch Runner

创建 `config/batch_paper2skills_v1.yaml`:

```yaml
experiment_id: paper2skills_v1_tiera
model: openrouter/qwen/qwen3-32b  # 或你的本地 vLLM endpoint
max_steps: 15
temperature: 0.1

arms:
  - name: none
    sys_prompt: |
      You solve R-centric analysis tasks using available tools.
      Read the OBJECTIVE.md carefully and produce the required outputs.
    skill_manifest: null

  - name: llm_plan
    sys_prompt: |
      You solve R-centric analysis tasks. A plan has been generated for this task.
      Follow the plan's guidance but adapt as needed based on actual data inspection.
    skill_manifest: experiments/skills_paper2skills_v1/llm_plan/manifest.json

  - name: pipeline
    sys_prompt: |
      You solve R-centric analysis tasks. A code template from similar workflows is provided.
      Adapt the template pattern to this specific task.
    skill_manifest: experiments/skills_paper2skills_v1/pipeline/manifest.json

  - name: paper
    sys_prompt: |
      You solve R-centric analysis tasks. A method description from the primary literature is provided.
      Trust the paper's guidance when it differs from general knowledge.
    skill_manifest: experiments/skills_paper2skills_v1/paper/manifest.json

tasks:
  - deseq2_apeglm_small_n
  - deseq2_lrt_interaction
  - deseq2_shrinkage_comparison
  - limma_voom_weights
  - limma_duplicatecorrelation

parallel: 1  # Sequential to avoid resource conflict
output_dir: runs/batch_paper2skills_v1
```

### 步骤 3.2: 执行批量运行

```bash
# 激活环境
source .venv-paper2skills/bin/activate

# 运行实验
cd main/paper_primary_benchmark
python3 -m ldp_r_task_eval.batch_runner \
  --config config/batch_paper2skills_v1.yaml \
  --registry r_tasks/registry.paper_sensitive_v1.json \
  --output-dir ldp_r_task_eval/runs/batch_paper2skills_v1
```

### 步骤 3.3: 监控和日志

```bash
# 实时监控
tail -f ldp_r_task_eval/runs/batch_paper2skills_v1/*/logs/*.log

# 检查进度
ls ldp_r_task_eval/runs/batch_paper2skills_v1/*/workspace/output/
```

---

## Phase 4: 评估与对比

### 步骤 4.1: 运行评估器

```bash
# 评估每个 arm 的结果
python3 -m ldp_r_task_eval.tools.evaluate_real_run_v3 \
  --batch-run-id batch_paper2skills_v1 \
  --output ldp_r_task_eval/runs/_evaluations/paper2skills_v1
```

### 步骤 4.2: 生成对比报告

```python
# scripts/compare_4arms.py
import pandas as pd
import json

arms = ['none', 'llm_plan', 'pipeline', 'paper']
tasks = [
    'deseq2_apeglm_small_n',
    'deseq2_lrt_interaction',
    'deseq2_shrinkage_comparison',
    'limma_voom_weights',
    'limma_duplicatecorrelation'
]

results = []
for task in tasks:
    for arm in arms:
        eval_file = f"ldp_r_task_eval/runs/_evaluations/paper2skills_v1/{task}_{arm}.json"
        try:
            with open(eval_file) as f:
                data = json.load(f)
            results.append({
                'task': task,
                'arm': arm,
                'score': data['overall_score'],
                'verdict': data['verdict']
            })
        except FileNotFoundError:
            results.append({
                'task': task,
                'arm': arm,
                'score': 0,
                'verdict': 'missing'
            })

df = pd.DataFrame(results)
pivot = df.pivot(index='task', columns='arm', values='score')
print(pivot)
print("\nDifferences (Paper - None):")
print(pivot['paper'] - pivot['none'])
```

---

## 预期结果

### 我们期望看到的效果

| Task | None | LLM_Plan | Pipeline | Paper | 预期 Paper-None 差 |
|------|------|----------|----------|-------|-------------------|
| deseq2_apeglm_small_n | ~0.30 | ~0.40 | ~0.50 | **~0.95** | **+0.65** |
| deseq2_lrt_interaction | ~0.25 | ~0.35 | ~0.45 | **~0.95** | **+0.70** |
| deseq2_shrinkage_comparison | ~0.40 | ~0.50 | ~0.60 | **~0.95** | **+0.55** |
| limma_voom_weights | ~0.35 | ~0.45 | ~0.50 | **~0.95** | **+0.60** |
| limma_duplicatecorrelation | ~0.25 | ~0.35 | ~0.40 | **~0.95** | **+0.70** |

### 关键指标

- **平均 Paper-None 差异**: 预期 **~0.64**
- **当前实验差异**: 仅 **~0.03**
- **改进倍数**: **~21x**

---

## 故障排除

### 问题 1: R 包缺失

```bash
# 在 R 控制台中
install.packages("BiocManager")
BiocManager::install(c("DESeq2", "limma", "edgeR", "apeglm", "ashr"))
```

### 问题 2: vLLM 连接失败

```bash
# 检查 vLLM 是否运行
curl http://localhost:8000/v1/models

# 确认模型名匹配 config 中的设置
```

### 问题 3: Paper PDF 下载失败

```bash
# 手动下载 DOI 对应的 PDF
# DESeq2: https://doi.org/10.1186/s13059-014-0550-8
# limma: https://doi.org/10.1093/nar/gkv007

# 放入目录
cp ~/Downloads/s13059-014-0550-8.pdf \
   main/paper_primary_benchmark/literature/pdfs/10.1186_s13059-014-0550-8.pdf
```

### 问题 4: Agent 卡住或不调用工具

- 检查 `max_steps` 是否足够 (建议 15-20)
- 检查 `temperature` 是否过低 (0.1 适合确定性任务)
- 查看 agent 日志中的 tool 调用序列

---

## 附录: 一键运行脚本

创建 `run_full_experiment.sh`:

```bash
#!/bin/bash
set -e

echo "=== Paper2Skills 4-Arm Experiment Runner ==="

# Phase 1: Ground Truth
echo "[1/4] Generating ground truth..."
python3 scripts/run_all_references.py --tasks tier_a

# Phase 2: Skill Preparation
echo "[2/4] Preparing 4-arm skills..."
python3 scripts/prepare_all_skills.py --arms all

# Phase 3: Batch Run
echo "[3/4] Running 4-arm experiment..."
python3 -m ldp_r_task_eval.batch_runner \
  --config config/batch_paper2skills_v1.yaml

# Phase 4: Evaluation
echo "[4/4] Evaluating results..."
python3 -m ldp_r_task_eval.tools.evaluate_real_run_v3 \
  --batch-run-id batch_paper2skills_v1

python3 scripts/generate_comparison_report.py \
  --batch batch_paper2skills_v1 \
  --output results/paper2skills_v1_report.md

echo "=== Complete! Report: results/paper2skills_v1_report.md ==="
```

---

*运行手册完成 - 按步骤执行即可重现完整 4-Arm 实验*
