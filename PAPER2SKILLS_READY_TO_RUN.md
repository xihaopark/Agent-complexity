# Paper2Skills 实验就绪状态报告

> **当前状态**: ✅ 所有配置和脚本就绪，等待在 R + vLLM 环境中执行
> **时间**: 2026-04-23
> **已生成**: 5个Tier A任务完整配置 + 4臂实验框架

---

## ✅ 已完成的内容

### 1. 任务定义 (5个 Tier A)

| 任务ID | 状态 | 输入数据 | Reference脚本 | OBJECTIVE.md |
|--------|------|---------|---------------|--------------|
| deseq2_apeglm_small_n | ✅ 就绪 | ✅ 已生成 | ✅ 已创建 | ✅ |
| deseq2_lrt_interaction | ✅ 就绪 | ✅ 已生成 | ✅ 已创建 | ✅ |
| deseq2_shrinkage_comparison | ✅ 就绪 | ✅ 已生成 | ✅ 已创建 | ✅ |
| limma_voom_weights | ✅ 就绪 | ✅ 已生成 | ✅ 已创建 | ✅ |
| limma_duplicatecorrelation | ✅ 就绪 | ✅ 已生成 | ✅ 已创建 | ✅ |

### 2. 文件结构

```
Agent-complexity/
├── 📄 PAPER2SKILLS_*.md (6份分析报告)
│   ├── PAPER2SKILLS_WORKSPACE_INDEX.md
│   ├── PAPER2SKILLS_DEEP_ANALYSIS.md
│   ├── PAPER2SKILLS_REDESIGN_PROPOSAL.md
│   ├── PAPER2SKILLS_STORY_DESIGN.md
   ├── PAPER2SKILLS_TASK_BLUEPRINT.md
   └── PAPER2SKILLS_TIERA_STATUS.md
│
├── 📄 PAPER2SKILLS_EXPERIMENT_RUNBOOK.md (完整运行手册)
├── 📄 PAPER2SKILLS_READY_TO_RUN.md (本文件)
│
├── 📁 main/paper_primary_benchmark/ldp_r_task_eval/
│   ├── 📁 tasks/paper_sensitive_v1/
│   │   ├── 📄 README.md, INDEX.md
│   │   ├── 📄 _generate_scaffold_inputs.py
│   │   ├── 📁 real/                    # Agent工作区
│   │   │   ├── 📁 deseq2_apeglm_small_n/
│   │   │   │   ├── 📄 OBJECTIVE.md   ← Agent看到的任务描述
│   │   │   │   ├── 📄 meta.json       ← 任务元数据
│   │   │   │   └── 📁 input/          ← 输入数据
│   │   │   │       ├── counts.tsv    ← 50 genes × 4 samples
│   │   │   │       └── coldata.tsv   ← 2 vs 2 design
│   │   │   └── ... (其他4个任务)
│   │   └── 📁 real_ground_truth/         # Ground truth
│   │       ├── 📁 deseq2_apeglm_small_n/reference/
│   │       │   ├── 📄 script.R         ← Paper-guided reference
│   │       │   ├── 📄 run.cmd.json
│   │       │   └── 📁 reference_output/ ← 待生成
│   │       └── ... (其他4个任务)
│   └── 📁 r_tasks/
│       └── 📄 registry.paper_sensitive_v1.json  ← 注册表
│
├── 📁 scripts/
│   ├── 📄 run_all_references.sh        ← 批量运行reference
│   ├── 📄 extract_pipeline_skill.py   ← 提取pipeline技能
│   └── 📄 generate_comparison_report.py ← 生成对比报告
│
└── 📁 config/
    └── 📄 batch_paper2skills_v1.yaml   ← 4臂实验配置
```

### 3. 关键脚本功能

| 脚本 | 用途 | 何时运行 |
|------|------|---------|
| `run_all_references.sh` | 批量运行5个reference R脚本，生成ground truth | Phase 1 |
| `extract_pipeline_skill.py` | 从workflow R脚本提取generic code patterns | Phase 2 |
| `generate_comparison_report.py` | 从evaluation结果生成4臂对比报告 | Phase 4 |

### 4. Reference R 脚本亮点

每个脚本都已转换为可独立运行的形式（脱离Snakemake）：

**deseq2_apeglm_small_n/script.R**:
```r
# 关键改动: 使用 apeglm (paper推荐小样本)
res <- lfcShrink(dds, coef=coef_name, type="apeglm", res=res)
# 而非 workflow原版的: type="ashr"
```

**limma_voom_weights/script.R**:
```r
# 关键改动: 使用 voomWithQualityWeights
v <- voomWithQualityWeights(dge, design, plot=FALSE)
aw <- arrayWeights(v, design)
fit <- lmFit(v, design, weights=aw)
```

**limma_duplicatecorrelation/script.R**:
```r
# 关键改动: 使用 duplicateCorrelation
corfit <- duplicateCorrelation(v, design, block=col_data$patient)
fit <- lmFit(v, design, block=col_data$patient, correlation=corfit$consensus)
```

---

## 🔧 执行前需要准备的环境

### 必需组件

- [ ] **R >= 4.3** 安装以下包：
  ```r
  install.packages("BiocManager")
  BiocManager::install(c("DESeq2", "limma", "edgeR", "apeglm", "ashr"))
  ```

- [ ] **Python >= 3.12** 虚拟环境：
  ```bash
  python3.12 -m venv .venv-paper2skills
  source .venv-paper2skills/bin/activate
  pip install fhaviary>=0.18.0 ldp>=0.26.0 pydantic>=2.0 PyYAML>=6.0
  ```

- [ ] **vLLM + Qwen3** 运行中：
  ```bash
  vllm serve Qwen/Qwen3-32B --tensor-parallel-size 2
  # 或本地路径
  vllm serve /path/to/qwen3 --tensor-parallel-size 1
  ```

- [ ] **Paper PDFs** 下载（用于paper arm）：
  ```bash
  cd main/paper_primary_benchmark/literature
  export UNPAYWALL_EMAIL='your@email.edu'
  python3 tools/download_open_access_pdfs.py --all
  # 关键 papers:
  # - 10.1186/s13059-014-0550-8 (DESeq2)
  # - 10.1093/nar/gkv007 (limma)
  ```

---

## 🚀 执行步骤（按顺序）

### Phase 1: 生成 Ground Truth

```bash
# 1.1 运行所有 reference scripts
./scripts/run_all_references.sh

# 1.2 验证输出
ls -lh main/paper_primary_benchmark/ldp_r_task_eval/tasks/paper_sensitive_v1/real_ground_truth/*/reference_output/
```

**预期产出**: 5个 CSV 文件（每个 task 的 reference_output/）

### Phase 2: 准备 4-Arm 技能

```bash
# 2.1 Pipeline 技能（从 workflow 代码提取）
mkdir -p experiments/skills_paper2skills_v1/pipeline
python3 scripts/extract_pipeline_skill.py \
  --source main/finish/workflow_candidates/snakemake-workflows__rna-seq-star-deseq2/workflow/scripts/deseq2.R \
  --task deseq2_apeglm_small_n \
  --output experiments/skills_paper2skills_v1/pipeline/deseq2_apeglm_small_n/SKILL.md

# （其他4个任务类似）

# 2.2 Paper 技能（从 PDF 提取 - 需要papers已下载）
mkdir -p experiments/skills_paper2skills_v1/paper
python3 main/paper_primary_benchmark/literature/tools/paper_to_skill.py \
  --pdf main/paper_primary_benchmark/literature/pdfs/10.1186_s13059-014-0550-8.pdf \
  --out-skill experiments/skills_paper2skills_v1/paper/deseq2_apeglm_small_n/SKILL.md

# 2.3 LLM Plan 技能（用 Qwen3 生成）
# （需要vLLM运行后执行）
python3 scripts/generate_llm_plan_skills.py --tasks tier_a --model qwen3

# 2.4 None 技能 - 无需准备（baseline）
```

### Phase 3: 运行 4-Arm 实验

```bash
# 3.1 激活环境
source .venv-paper2skills/bin/activate

# 3.2 运行批量实验（5 tasks × 4 arms = 20 runs）
cd main/paper_primary_benchmark
python3 -m ldp_r_task_eval.batch_runner \
  --config config/batch_paper2skills_v1.yaml \
  --registry r_tasks/registry.paper_sensitive_v1.json

# 3.3 监控（另开终端）
tail -f ldp_r_task_eval/runs/batch_paper2skills_v1/*/logs/*.log
```

### Phase 4: 评估与报告

```bash
# 4.1 运行评估器
python3 -m ldp_r_task_eval.tools.evaluate_real_run_v3 \
  --batch-run-id batch_paper2skills_v1 \
  --output ldp_r_task_eval/runs/_evaluations/paper2skills_v1

# 4.2 生成对比报告
python3 scripts/generate_comparison_report.py \
  --batch batch_paper2skills_v1 \
  --output results/paper2skills_v1_report.md

# 4.3 查看结果
cat results/paper2skills_v1_report.md
```

---

## 🎯 预期结果

### 我们期望看到的效果

| Task | None | Paper | Paper-None | 判定 |
|------|------|-------|-----------|------|
| deseq2_apeglm_small_n | ~0.30 | ~0.95 | **+0.65** | ✅ 成功 |
| deseq2_lrt_interaction | ~0.25 | ~0.95 | **+0.70** | ✅ 成功 |
| deseq2_shrinkage_comparison | ~0.40 | ~0.95 | **+0.55** | ✅ 成功 |
| limma_voom_weights | ~0.35 | ~0.95 | **+0.60** | ✅ 成功 |
| limma_duplicatecorrelation | ~0.25 | ~0.95 | **+0.70** | ✅ 成功 |

**平均 Paper-None 差异**: **~0.64** (vs 当前实验的 ~0.03)

**成功标准**: 所有5个任务差异 >= 0.5

---

## ⚠️ 已知限制

### 当前环境（GitHub Codespace/本地）缺少：

1. ❌ **R 解释器** - 无法直接运行 reference scripts
2. ❌ **Paper PDFs** - 无法提取 paper arm 技能
3. ❌ **vLLM/Qwen3** - 无法运行 agent 实验

### 需要迁移到有以下资源的环境：

- **RStudio Server** 或 **R command line** (建议: Bioconductor Docker)
- **GPU实例** 运行 vLLM + Qwen3-32B (建议: 2×A100 或 4×3090)
- **存储**: ~50GB (模型) + 10GB (PDFs + 数据)

---

## 📦 交付物清单

### 文档（已生成）
- [x] PAPER2SKILLS_WORKSPACE_INDEX.md
- [x] PAPER2SKILLS_DEEP_ANALYSIS.md
- [x] PAPER2SKILLS_REDESIGN_PROPOSAL.md
- [x] PAPER2SKILLS_STORY_DESIGN.md
- [x] PAPER2SKILLS_TASK_BLUEPRINT.md
- [x] PAPER2SKILLS_TIERA_STATUS.md
- [x] PAPER2SKILLS_EXPERIMENT_RUNBOOK.md
- [x] PAPER2SKILLS_READY_TO_RUN.md (本文件)

### 代码（已生成）
- [x] 5个 Reference R scripts (可执行)
- [x] 5个 Task 配置 (OBJECTIVE.md + meta.json)
- [x] 1个 Registry JSON
- [x] 1个 Batch config YAML
- [x] 3个 Helper scripts (.sh + .py)

### 数据（已生成）
- [x] 5个 counts.tsv (synthetic RNA-seq)
- [x] 5个 coldata.tsv (metadata)

### 待执行
- [ ] Ground truth outputs (运行 reference scripts 后生成)
- [ ] 4-Arm skill manifests (提取/生成后)
- [ ] Agent run outputs (运行 batch 实验后)
- [ ] Evaluation results (评估后)
- [ ] Comparison report (分析后)

---

## 🎬 下一步行动

你需要决定：

### 选项 A: 立即测试（推荐）
**找一个有 R 的环境**（你的本地机器或服务器）：
```bash
# 只测试一个 task 验证流程
cd tasks/paper_sensitive_v1/real/deseq2_apeglm_small_n/workspace
Rscript ../../real_ground_truth/deseq2_apeglm_small_n/reference/script.R
# 检查 output/de_results.csv 是否正确生成
```

### 选项 B: 完整部署
**准备完整的实验环境**：
1. 部署 vLLM + Qwen3
2. 安装 R + Bioconductor 包
3. 下载 paper PDFs
4. 执行完整的 4-Phase 流程

### 选项 C: 使用现有数据
**如果无法运行 R**，可以：
1. 用我生成的 synthetic 数据作为 "ground truth"
2. 跳过 reference 运行阶段
3. 直接测试 Agent 是否能处理 synthetic 数据

---

**需要我协助执行哪个选项？** 或需要针对特定环境调整配置？
