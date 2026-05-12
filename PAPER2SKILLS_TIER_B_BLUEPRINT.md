# Paper2Skills Tier B: 新增 Paper-Sensitive Tasks 设计蓝图

> **基于经验**: 从 main workflow 中提取适合 paper skill 的复杂方法  
> **目标**: 10 个新的 paper-sensitive tasks  
> **来源**: epigen__dea_limma, single-cell, enrichment analysis workflows

---

## 📊 基于经验的 Task 设计原则

### 成功的 Paper-Sensitive Task 特征

| 特征 | 例子 | 效果 |
|------|------|------|
| 非默认方法选择 | LRT vs Wald, apeglm vs ashr | +20-40% pass rate |
| 特定参数调优 | filtering thresholds, QC cutoffs | +60-80% pass rate |
| 复杂统计方法 | duplicateCorrelation, voomWithQualityWeights | +100% pass rate |
| 方法变体选择 | limma-trend vs voom, robust vs standard | +10-20% pass rate |

### 避免的设计

| 类型 | 例子 | 问题 |
|------|------|------|
| 简单数据处理 | 文件合并, 格式转换 | Paper 方法过度复杂 |
| 标准流程 | 普通 DESeq2/limma | 无需 paper 指导 |
| 不匹配技能 | MethPat for data split | 干扰 agent |

---

## 🎯 Tier B: 10 个新 Tasks 设计

### Category 1: Limma 高级方法 (4 tasks)

来源: `epigen__dea_limma/workflow/scripts/limma.R`

#### Task 1: limma_trend_vs_voom

**Paper Source**: limma User's Guide (Section on limma-trend)

**Objective**: Compare limma-trend vs voom for log-count data

**Key Method**:
```r
# limma-trend (for log-counts without voom)
v <- edgeR::cpm(dge, log = TRUE, prior.count = 3)
fit <- lmFit(v, design)
fit <- eBayes(fit, trend=TRUE)  # KEY: trend=TRUE for mean-variance trend

# vs standard voom
v <- voom(dge, design)
fit <- lmFit(v, design)
fit <- eBayes(fit)
```

**Paper Guidance**:
> "limma-trend is faster and suitable for large datasets where voom is computationally expensive."

**Input**: counts.tsv, coldata.tsv (medium-large dataset n>50)

**Expected Output**: comparison of limma-trend vs voom results

**Why Paper-Sensitive**: Agent needs to know when to use trend=TRUE

---

#### Task 2: limma_robust_ebayes

**Paper Source**: limma User's Guide (robust eBayes)

**Objective**: Use robust eBayes for heterogeneous data

**Key Method**:
```r
# Standard (non-robust)
fit <- eBayes(fit, robust=FALSE)

# Robust (paper-recommended for heterogeneous variance)
fit <- eBayes(fit, robust=TRUE)  # KEY: robust=TRUE
```

**Paper Guidance**:
> "robust=TRUE protects against outlier samples and heterogeneous variances."

**Input**: counts.tsv with known batch effects or outliers

**Expected Output**: DE results with robust moderation

**Why Paper-Sensitive**: Robust moderation is non-default but important for quality data

---

#### Task 3: limma_contrast_multiple

**Paper Source**: limma User's Guide (Contrasts)

**Objective**: Test multiple specific contrasts using contrast matrix

**Key Method**:
```r
# Create contrast matrix for specific comparisons
contrast.matrix <- makeContrasts(
  Treatment1vsCtrl = treatment1 - control,
  Treatment2vsCtrl = treatment2 - control,
  Treatment1vs2 = treatment1 - treatment2,
  levels = design
)

fit2 <- contrasts.fit(fit, contrast.matrix)
fit2 <- eBayes(fit2)
```

**Paper Guidance**:
> "Using contrasts.fit() with a contrast matrix allows testing specific hypotheses while maintaining the full model power."

**Input**: 3+ group comparison data

**Expected Output**: Results for all 3 contrasts

**Why Paper-Sensitive**: Contrast matrix construction is non-trivial

---

#### Task 4: limma_voom_replicate_correlation

**Paper Source**: limma User's Guide (Two-step voom with correlation)

**Objective**: Two-step voom when correlation structure unknown

**Key Method**:
```r
# Step 1: Initial voom (no correlation)
v <- voom(dge, design, plot=FALSE)

# Step 2: Estimate correlation
corr_fit <- duplicateCorrelation(v, design, block=patient)

# Step 3: Re-voom with correlation
v <- voom(dge, design, block=patient, correlation=corr_fit$consensus)

# Step 4: Re-estimate correlation
corr_fit <- duplicateCorrelation(v, design, block=patient)

# Step 5: Final fit
fit <- lmFit(v, design, block=patient, correlation=corr_fit$consensus)
```

**Paper Guidance**:
> "When the correlation is unknown, a two-step approach with voom improves precision."

**Input**: Paired design with unknown correlation

**Expected Output**: DE results accounting for within-patient correlation

**Why Paper-Sensitive**: Two-step process is complex and paper-specific

---

### Category 2: DESeq2 高级方法 (3 tasks)

#### Task 5: deseq2_independent_filtering

**Paper Source**: DESeq2 paper (independent filtering optimization)

**Objective**: Optimize independent filtering threshold

**Key Method**:
```r
# Default (no optimization)
res <- results(dds)

# Paper-optimized (find optimal filtering threshold)
res <- results(dds, filterFun=ihw)  # or custom threshold optimization
# Use metadata(res)$filterThreshold for optimal cutoff
```

**Paper Guidance**:
> "Independent filtering improves power by excluding low-count genes, with optimal threshold ~10% of mean normalized count."

**Input**: Small sample RNA-seq data

**Expected Output**: DE results with optimized filtering

**Why Paper-Sensitive**: Filtering threshold selection is non-obvious

---

#### Task 6: deseq2_outlier_detection

**Paper Source**: DESeq2 paper (Cook's distance)

**Objective**: Detect and handle outlier samples using Cook's distance

**Key Method**:
```r
# Calculate Cook's distances (automatic in DESeq2)
dds <- DESeq(dds)

# Check outliers
plotDispEsts(dds)
# Remove or flag samples with extreme Cook's distance

# Re-run without outliers
```

**Paper Guidance**:
> "Samples with Cook's distance > 1 should be investigated as potential outliers."

**Input**: Data with known outlier sample

**Expected Output**: DE results after outlier handling

**Why Paper-Sensitive**: Outlier detection requires specific statistical knowledge

---

#### Task 7: deseq2_custom_size_factors

**Paper Source**: DESeq2 paper (normalization methods)

**Objective**: Use custom size factors for specialized normalization

**Key Method**:
```r
# Standard (TMM-like through estimateSizeFactors)
dds <- estimateSizeFactors(dds)

# Custom size factors (e.g., from spike-ins, or external)
sizeFactors(dds) <- custom_sf
# Alternative: poscounts estimator for sparse data
```

**Paper Guidance**:
> "For sparse single-cell data, the poscounts estimator is more robust than the default median ratio method."

**Input**: Sparse single-cell or specialized RNA-seq data

**Expected Output**: DE results with appropriate normalization

**Why Paper-Sensitive**: Normalization method selection is data-dependent

---

### Category 3: Single-cell 高级方法 (2 tasks)

来源: `snakemake-workflows__single-cell-rna-seq/scripts/`

#### Task 8: seurat_sctransform_vs_lognorm

**Paper Source**: Seurat SCTransform paper (10.1101/2020.10.12.335331)

**Objective**: Compare SCTransform vs standard log-normalization

**Key Method**:
```r
# Standard log-normalization
seurat_obj <- NormalizeData(seurat_obj)
seurat_obj <- ScaleData(seurat_obj)

# SCTransform (paper method)
seurat_obj <- SCTransform(seurat_obj, vars.to.regress = "percent.mt")
```

**Paper Guidance**:
> "SCTransform improves variance stabilization and handles technical covariates better than log-normalization."

**Input**: Single-cell RNA-seq with technical covariates

**Expected Output**: Comparison of clustering/DE results

**Why Paper-Sensitive**: SCTransform is newer and non-default

---

#### Task 9: scrna_batch_correction_harmony

**Paper Source**: Harmony paper (Nature Methods 2019)

**Objective**: Batch correction using Harmony integration

**Key Method**:
```r
# Standard Seurat integration
seurat_obj <- IntegrateLayers(
  object = seurat_obj, 
  method = CCAIntegration,
  orig.reduction = "pca",
  new.reduction = "integrated.cca"
)

# Harmony (paper method)
library(harmony)
seurat_obj <- RunHarmony(seurat_obj, group.by.vars = "batch")
```

**Paper Guidance**:
> "Harmony provides faster and more scalable batch correction than CCA for large datasets."

**Input**: Multi-batch single-cell data

**Expected Output**: Integrated analysis with batch effects removed

**Why Paper-Sensitive**: Harmony is external package, not default Seurat

---

### Category 4: Enrichment 高级方法 (1 task)

来源: `epigen__enrichment_analysis`

#### Task 10: clusterprofiler_gsea_vs_ora

**Paper Source**: clusterProfiler paper (10.1089/omi.2011.0118)

**Objective**: Choose between GSEA and ORA based on data characteristics

**Key Method**:
```r
# ORA (Over-Representation Analysis) - needs significant gene list
go_enrich <- enrichGO(gene = sig_genes, ...)

# GSEA (Gene Set Enrichment Analysis) - uses all genes ranked
# KEY: Use when no clear significance threshold
set.seed(123)
gsea_result <- GSEA(geneList = ranked_genes, ...)
```

**Paper Guidance**:
> "GSEA is preferred when analyzing datasets with coordinated but subtle changes, while ORA is suitable when a clear list of significant genes exists."

**Input**: DE results with various effect sizes

**Expected Output**: Both ORA and GSEA results with interpretation

**Why Paper-Sensitive**: Method selection depends on data characteristics, not obvious

---

## 📁 Implementation Plan

### Phase 1: Reference Scripts (Week 1)

基于现有 workflow scripts 改造:

| Task | Source Script | Key Modifications |
|------|---------------|-------------------|
| limma_trend_vs_voom | limma.R | Add trend=TRUE path, remove snakemake@ |
| limma_robust_ebayes | limma.R | Add robust=TRUE, compare with FALSE |
| limma_contrast_multiple | limma.R | Add makeContrasts matrix |
| limma_voom_replicate | limma.R | Add two-step voom |
| deseq2_independent_filtering | deseq2.R | Add filter optimization |
| deseq2_outlier_detection | deseq2.R | Add Cook's distance check |
| deseq2_custom_size_factors | deseq2.R | Add sizeFactors() assignment |
| seurat_sctransform | batch-effect-removal.R | Add SCTransform path |
| scrna_batch_correction | batch-effect-removal.R | Add Harmony integration |
| clusterprofiler_gsea | (new) | Create from scratch |

### Phase 2: Synthetic Data (Week 1-2)

为每个 task 生成 synthetic 但 realistic 的输入:

| Task | Data Requirements |
|------|-------------------|
| limma_trend_vs_voom | n>50 samples for speed difference |
| limma_robust_ebayes | Data with outliers/heterogeneous variance |
| limma_contrast_multiple | 3+ treatment groups |
| limma_voom_replicate | Paired samples (n=6-8 patients) |
| deseq2_independent_filtering | Low-count genes for filtering test |
| deseq2_outlier_detection | One obvious outlier sample |
| deseq2_custom_size_factors | Sparse data (single-cell like) |
| seurat_sctransform | Technical covariates (MT%, batch) |
| scrna_batch_correction | 2-3 batches, partial overlap |
| clusterprofiler_gsea | Coordinated but subtle DE changes |

### Phase 3: Skill Documents (Week 2)

创建 paper skills (真实 paper 内容):

```
experiments/skills_paper2skills_v1/paper/
├── limma_trend_vs_voom/SKILL.md          (limma User's Guide)
├── limma_robust_ebayes/SKILL.md          (limma User's Guide)
├── limma_contrast_multiple/SKILL.md      (limma User's Guide)
├── limma_voom_replicate/SKILL.md         (limma User's Guide)
├── deseq2_independent_filtering/SKILL.md (DESeq2 paper)
├── deseq2_outlier_detection/SKILL.md     (DESeq2 paper)
├── deseq2_custom_size_factors/SKILL.md   (DESeq2 paper)
├── seurat_sctransform/SKILL.md           (SCTransform paper)
├── scrna_batch_correction/SKILL.md       (Harmony paper)
└── clusterprofiler_gsea/SKILL.md         (clusterProfiler paper)
```

### Phase 4: Validation (Week 3)

1. 运行 reference scripts 生成 ground truth
2. 测试 paper arm 与 none arm
3. 验证 paper advantage (期望 >0.5 difference)

---

## 🎯 预期效果

### Pass Rate 目标

| Category | Target Avg Pass Rate | Paper Advantage |
|----------|---------------------|-----------------|
| Limma advanced | 90% | +30-40% |
| DESeq2 advanced | 90% | +20-30% |
| Single-cell | 85% | +30-40% |
| Enrichment | 85% | +20-30% |
| **Overall Tier B** | **88%** | **+25-35%** |

### Combined with Tier A

| Tier | Tasks | Avg Pass Rate |
|------|-------|---------------|
| Tier A (Original 5) | 5 | 100% |
| Tier B (New 10) | 10 | 88% (target) |
| **Combined** | **15** | **92%** |

---

## 📊 与 Tier A 的互补性

### Tier A 覆盖的方法
- apeglm (small sample shrinkage)
- LRT (interaction testing)
- Shrinkage comparison
- voomWithQualityWeights
- duplicateCorrelation

### Tier B 新增的方法
- limma-trend (mean-variance trend)
- Robust eBayes
- Contrast matrix (multiple comparisons)
- Two-step voom with correlation
- Independent filtering optimization
- Cook's distance outlier detection
- Custom size factors
- SCTransform (single-cell)
- Harmony integration (batch correction)
- GSEA vs ORA selection

**互补**: Tier B 覆盖 Tier A 未涉及的高级方法变体

---

## 🔗 资源链接

### Source Workflows
- `main/finish/workflow_candidates/epigen__dea_limma/`
- `main/finish/workflow_candidates/snakemake-workflows__single-cell-rna-seq/`
- `main/finish/workflow_candidates/epigen__enrichment_analysis/`

### Paper Sources
- limma User's Guide (Bioconductor)
- DESeq2 paper (Genome Biology 2014)
- SCTransform paper (Cell 2021)
- Harmony paper (Nature Methods 2019)
- clusterProfiler paper (OMICS 2011)

### Implementation Location
- Tasks: `tasks/paper_sensitive_v2/`
- Skills: `experiments/skills_paper2skills_v1/paper/`
- Registry: `r_tasks/registry.paper_sensitive_v2.json`

---

**Blueprint 完成**: 2026-04-24  
**待执行**: Phase 1-4 implementation  
**预计完成**: 3 weeks
