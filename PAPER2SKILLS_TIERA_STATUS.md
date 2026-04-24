# Tier A 任务开发完成报告

> 日期: 2026-04-23
> 状态: **5个可执行原型已就绪**

---

## 完成内容概览

### ✅ 文件结构

```
main/paper_primary_benchmark/ldp_r_task_eval/tasks/paper_sensitive_v1/
├── README.md                 # 目录说明
├── INDEX.md                  # 12任务快速索引
├── _generate_scaffold_inputs.py  # 输入数据生成脚本
├── 📁 real/                  # Agent工作区 (12个task)
│   ├── deseq2_apeglm_small_n/     ✅ 有输入数据 + OBJECTIVE + meta
│   ├── deseq2_lrt_interaction/    ✅ 有输入数据 + OBJECTIVE + meta
│   ├── deseq2_shrinkage_comparison/ ✅ 有输入数据 + OBJECTIVE + meta
│   ├── limma_voom_weights/          ✅ 有输入数据 + OBJECTIVE + meta
│   ├── limma_duplicatecorrelation/  ✅ 有输入数据 + OBJECTIVE + meta
│   └── ... (其他7个是骨架，无数据)
└── 📁 real_ground_truth/     # Ground truth (5个Tier A)
    ├── deseq2_apeglm_small_n/reference/script.R       ✅
    ├── deseq2_lrt_interaction/reference/script.R        ✅
    ├── deseq2_shrinkage_comparison/reference/script.R   ✅
    ├── limma_voom_weights/reference/script.R            ✅
    └── limma_duplicatecorrelation/reference/script.R    ✅
```

---

## Tier A: 5个可立即运行的任务

### 任务 1: `deseq2_apeglm_small_n`

**核心陷阱**: n=2 vs n=2 小样本，默认 shrinkage 不稳定
**Paper知识**: `lfcShrink(type="apeglm")` 推荐用于小样本
**原型来源**: `rna-seq-star-deseq2/workflow/scripts/deseq2.R`
**修改**: 将 `type="ashr"` 改为 `type="apeglm"`，使用 `coef=` 而非 `contrast=`

**输入数据**:
- 50 genes × 4 samples (2x condition A, 2x condition B)
- First 5 genes are DE (2x up in B)

**输出**: `output/de_results.csv` (7 columns)

---

### 任务 2: `deseq2_lrt_interaction`

**核心陷阱**: Agent 默认 Wald test 只测 main effects，错过 interaction
**Paper知识**: LRT (likelihood ratio test) with nested models for interaction
**原型来源**: `rna-seq-star-deseq2/workflow/scripts/deseq2-init.R`
**修改**: 添加 `test="LRT"` + `reduced = ~ treatment + time`

**输入数据**:
- 40 genes × 8 samples (2x2 factorial: treatment × time, 2 reps each)
- First 4 genes have interaction effect (high only in trt+t1)

**输出**: `output/interaction_de.csv` (6 columns)

---

### 任务 3: `deseq2_shrinkage_comparison`

**核心陷阱**: Agent 可能用 deprecated `type="normal"` 或 suboptimal choice
**Paper知识**: `apeglm` vs `ashr` 适用场景区分
**原型来源**: `rna-seq-star-deseq2/workflow/scripts/deseq2.R`
**修改**: 展示 `apeglm` 作为 default best choice

**输入数据**:
- 50 genes × 6 samples (3 vs 3)
- First 8 genes are DE

**输出**: `output/shrunk_de.csv` (8 columns, includes shrinkage_method)

---

### 任务 4: `limma_voom_weights`

**核心陷阱**: Plain `voom()` 对 unequal sample quality 敏感
**Paper知识**: `voomWithQualityWeights()` + `arrayWeights` down-weights bad samples
**原型来源**: `epigen-dea_limma/workflow/scripts/limma.R`
**修改**: 添加 `voomWithQualityWeights(dge, design)` + `arrayWeights(v, design)`

**输入数据**:
- 35 genes × 5 samples
- Sample "SQ4" is low quality outlier (seq_depth 5M vs 50M for others)

**输出**: `output/de_results_weighted.csv` (6 columns)

---

### 任务 5: `limma_duplicatecorrelation`

**核心陷阱**: Agent 可能 ignore paired structure, use wrong model
**Paper知识**: `duplicateCorrelation()` for block-level correlation in paired design
**原型来源**: `epigen-dea_limma/workflow/scripts/limma.R` (already has block_var logic!)
**修改**: 强制开启 `block=patient` + `correlation=cons_correlation`

**输入数据**:
- 32 genes × 6 samples (3 patients, each with trt + ctrl)
- Patient-specific baseline effects + treatment effect

**输出**: `output/paired_de.csv` (6 columns)

---

## Reference Scripts 详情

每个 script 都做了以下改动：

1. **移除 Snakemake wrapper**: 从 `snakemake@input` 改为 `commandArgs` 风格或直接路径
2. **统一输入格式**: `counts.tsv` (gene_id + samples) + `coldata.tsv` (sample metadata)
3. **统一输出格式**: `write.csv(..., row.names=FALSE)` 标准 CSV
4. **添加 Paper-specific logic**: 每个 script 的核心方法都来自对应的 methods paper

### 示例: deseq2_apeglm_small_n/script.R 关键改动

```r
# 原 workflow (ashr, with contrast)
res <- lfcShrink(dds, contrast=contrast, res=res, type="ashr")

# 我们的 reference (apeglm, with coef - paper recommended for small n)
res <- lfcShrink(dds, coef=coef_name, type="apeglm", res=res)
```

### 示例: limma_duplicatecorrelation/script.R 核心逻辑

```r
# Estimate correlation within patient blocks
corfit <- duplicateCorrelation(v, design, block=col_data$patient)

# Fit with block structure
fit <- lmFit(v, design, block=col_data$patient, correlation=corfit$consensus)
```

---

## 输入数据规格

所有输入数据都是 **synthetic but biologically plausible**:

| Task | Genes | Samples | Special Design |
|------|-------|---------|----------------|
| deseq2_apeglm_small_n | 50 | 4 (2vs2) | 5 DE genes |
| deseq2_lrt_interaction | 40 | 8 (2x2) | 4 interaction genes |
| deseq2_shrinkage_comparison | 50 | 6 (3vs3) | 8 DE genes |
| limma_voom_weights | 35 | 5 | 1 outlier sample (SQ4) |
| limma_duplicatecorrelation | 32 | 6 | 3 patients paired |

---

## 下一步操作

### 立即可以做的

1. **运行 Reference Scripts** 生成 ground truth
   ```bash
   cd main/paper_primary_benchmark/ldp_r_task_eval/tasks/paper_sensitive_v1/real/deseq2_apeglm_small_n/workspace
   Rscript ../../real_ground_truth/deseq2_apeglm_small_n/reference/script.R
   # 输出会写入 output/de_results.csv
   # 然后将此文件复制到 real_ground_truth/.../reference_output/
   ```

2. **验证脚本可运行**
   - 检查 R 包依赖 (DESeq2, limma, edgeR)
   - 确认输入路径正确
   - 验证输出格式

3. **运行 Agent 测试 (None arm)**
   - 用 Qwen3 跑一个 task，看是否会掉入陷阱
   - 验证 None 得分 ~0.3 的预期

### 后续扩展

- **Tier B**: 处理 `seurat_sctransform_scaling` (workflow 已用 SCT，需反向设计陷阱)
- **Tier C**: 放弃或替换无原型的 5 个 task
- **完整实验**: 5个task × 4-arm (none/llm_plan/pipeline/paper) with Qwen3

---

## 文件清单

### 文档
- `README.md` - 目录使用说明
- `INDEX.md` - 12任务快速索引表
- `PAPER2SKILLS_TIERA_STATUS.md` - 本报告

### 注册表
- `r_tasks/registry.paper_sensitive_v1.json` - 机器可读任务清单

### 代码
- `real_ground_truth/*/reference/script.R` - 5个可执行 reference
- `real_ground_truth/*/reference/run.cmd.json` - 运行命令模板
- `_generate_scaffold_inputs.py` - 输入数据生成器

### 数据
- `real/*/input/counts.tsv` - 基因表达矩阵 (5个任务)
- `real/*/input/coldata.tsv` - 样本元数据 (5个任务)
- `real/*/OBJECTIVE.md` - Agent 任务描述 (12个任务)
- `real/*/meta.json` - 任务注册信息 (12个任务)

---

## 关键发现（开发过程中）

1. **并非所有设计的 task 都有 workflow 原型**
   - 12个设计中只有 7 个有对应 R 脚本
   - 5 个 (MACS2, ComBat-seq, clusterProfiler, integration, methylKit) 无原型

2. **Workflow 原型 vs 我们的需求差异**
   - 原型: `deseq2.R` 用 `type="ashr"` (支持 contrast)
   - 我们需要: `type="apeglm"` (paper 推荐小样本)
   - 差异: apeglm 需要 `coef=` 而非 `contrast=`

3. **SCTransform 任务反向设计**
   - Workflow 已经用 SCTransform（好）
   - 我们需要让 Agent 用旧方法失败
   - 解决方案: 设计场景让 SCT 是唯一正确选择

---

*报告完成*
