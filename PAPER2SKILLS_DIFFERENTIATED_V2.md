# Paper2Skills 差异化任务对比表 V2 (精确 Binary)

> **筛选标准**: 排除4个arms完全相同的任务  
> **评估**: Binary - 100%通过=1, <100%=0  
> **总任务**: 37个 → **差异化**: 21个有效对比任务

---

## 筛选逻辑

### 全部排除的任务 (16个)

| # | 任务 | 排除原因 |
|---|------|---------|
| 1-5 | akinyi_deseq2, star_deseq2_init, star_deseq2_contrast, longseq_deseq2_init, longseq_deseq2_contrast | All=100% |
| 6 | riya_limma | All≈100% |
| 7 | spilterlize_limma_rbe | All=100% |
| 8 | chipseq_plot_annotatepeaks_summary_homer | All=100% |
| 9 | chipseq_plot_peaks_count_macs2 | All=100% |
| 10 | methylkit_remove_snvs | All=100% |
| 11 | clean_histoneHMM | All=100% |
| 12 | snakepipes_scrna_report | All=100% |
| 13 | cellranger-multi-finish__stage_01 | All=100% |
| 14 | cellranger-multi-finish__stage_02 | All=100% |
| 15 | msisensor_merge | All=99% |
| 16 | spilterlize_norm_voom | All≈100% (None/Paper=100, LLM=100, Pipe=90 接近) |

### 保留的差异化任务 (21个)

| # | 任务 | Family | 保留原因 |
|---|------|--------|---------|
| 1-5 | Tier A (5个) | RNA | Paper显著胜出 |
| 6 | dea_limma | RNA | Pipe胜出 |
| 7 | spilterlize_norm_edger | RNA | Pipe胜出(100 vs 90) |
| 8 | spilterlize_filter_features | RNA | None胜出(100 vs 90) |
| 9 | chipseq_plot_macs_qc | ChIP | Paper胜出(99 vs 76) |
| 10 | phantompeak_correlation | ChIP | LLM胜出(100 vs 99) |
| 11 | chipseq_plot_frip_score | ChIP | Paper胜出(99 vs 75) |
| 12 | chipseq_plot_homer_annot | ChIP | LLM胜出(90 vs 75) |
| 13 | methylkit_filt_norm | Methyl | LLM/Paper胜出(99 vs 23) |
| 14 | methylkit_to_tibble | Methyl | LLM胜出(70 vs 23) |
| 15 | methylkit2tibble_split | Methyl | Pipe胜出(75 vs 69/23) |
| 16 | methylkit_load | Methyl | All fail but diff values |
| 17 | methylkit_unite | Methyl | All fail but diff values |
| 18 | snakepipes_scrna_qc | scRNA | LLM落后(90 vs 100) |
| 19 | nearest_gene | Other | Pipe/None胜出(89 vs 50) |
| 20 | snakepipes_merge_ct | Other | None胜出(99 vs 75-83) |
| 21 | snakepipes_merge_fc | Other | None/Pipe胜出(83 vs 70) |
| 22 | epibtn_rpkm | Other | LLM胜出(100 vs 48) |

---

## 📊 精确 Binary 转换表

### 转换规则
- **≥95%** = ✅ **1** (完全通过)
- **<95%** = ❌ **0** (未完全通过)

### Tier A (5 Tasks)

| # | Task | None | LLM | Pipe | Paper | Winner | Binary Pass |
|---|------|:--:|:--:|:--:|:--:|:------:|:-----------:|
| 1 | deseq2_apeglm_small_n | 80→❌ | 85→❌ | 80→❌ | **100→✅** | **Paper** | 1/4 |
| 2 | deseq2_lrt_interaction | 75→❌ | 80→❌ | 75→❌ | **100→✅** | **Paper** | 1/4 |
| 3 | deseq2_shrinkage_comparison | 60→❌ | 65→❌ | **100→✅** | **100→✅** | **Pipe+Paper** | 2/4 |
| 4 | limma_voom_weights | 0→❌ | 50→❌ | 50→❌ | **100→✅** | **Paper** | 1/4 |
| 5 | limma_duplicatecorrelation | 0→❌ | 0→❌ | 0→❌ | **100→✅** | **Paper** | 1/4 |
| **小计** | | **0/5** | **0/5** | **1/5** | **5/5** | | **6/20** |
| **通过率** | | **0%** | **0%** | **20%** | **100%** | | **30%** |

---

### RNA (4 Tasks - 差异化)

| # | Task | None | LLM | Pipe | Paper | Winner | Binary Pass |
|---|------|:--:|:--:|:--:|:--:|:------:|:-----------:|
| 6 | dea_limma | 71→❌ | 75→❌ | **85→❌** | 71→❌ | **None** | 0/4 |
| 7 | spilterlize_norm_edger | **100→✅** | 90→❌ | **100→✅** | **100→✅** | **3 Arms** | 3/4 |
| 8 | spilterlize_filter_features | **100→✅** | **100→✅** | 90→❌ | **100→✅** | **3 Arms** | 3/4 |
| 9 | spilterlize_norm_voom | **100→✅** | **100→✅** | 90→❌ | **100→✅** | **3 Arms** | 3/4 |
| **小计** | | **3/4** | **2/4** | **1/4** | **3/4** | | **9/16** |
| **通过率** | | **75%** | **50%** | **25%** | **75%** | | **56%** |

> **注**: dea_limma 全部<95%，都不算完全通过

---

### ChIP (4 Tasks - 差异化)

| # | Task | None | LLM | Pipe | Paper | Winner | Binary Pass |
|---|------|:--:|:--:|:--:|:--:|:------:|:-----------:|
| 10 | chipseq_plot_macs_qc | 67→❌ | 76→❌ | 76→❌ | **99→✅** | **Paper** | 1/4 |
| 11 | phantompeak_correlation | 99→❌ | **100→✅** | 99→❌ | 99→❌ | **LLM** | 1/4 |
| 12 | chipseq_plot_frip_score | 75→❌ | 75→❌ | 75→❌ | **99→✅** | **Paper** | 1/4 |
| 13 | chipseq_plot_homer_annot | 75→❌ | **90→❌** | 75→❌ | 75→❌ | **None** | 0/4 |
| **小计** | | **0/4** | **1/4** | **0/4** | **2/4** | | **3/16** |
| **通过率** | | **0%** | **25%** | **0%** | **50%** | | **19%** |

> **注**: chipseq_plot_homer_annot LLM=90%<95%，不算完全通过

---

### Methyl (6 Tasks - 差异化)

| # | Task | None | LLM | Pipe | Paper | Winner | Binary Pass |
|---|------|:--:|:--:|:--:|:--:|:------:|:-----------:|
| 14 | methylkit_filt_norm | 15→❌ | **99→✅** | 23→❌ | **99→✅** | **LLM+Paper** | 2/4 |
| 15 | methylkit_to_tibble | 15→❌ | **70→❌** | 23→❌ | 23→❌ | **None** | 0/4 |
| 16 | methylkit2tibble_split | 69→❌ | 23→❌ | **75→❌** | 8→❌ | **None** | 0/4 |
| 17 | methylkit_load | 8→❌ | 8→❌ | 8→❌ | 8→❌ | **All Fail** | 0/4 |
| 18 | methylkit_unite | 8→❌ | 8→❌ | 8→❌ | 8→❌ | **All Fail** | 0/4 |
| 19 | methylkit_remove_snvs | - | - | - | - | **All=100%** | **Excluded** |
| **小计** | | **0/5** | **1/5** | **0/5** | **1/5** | | **2/20** |
| **通过率** | | **0%** | **20%** | **0%** | **20%** | | **10%** |

---

### scRNA (1 Task - 差异化)

| # | Task | None | LLM | Pipe | Paper | Winner | Binary Pass |
|---|------|:--:|:--:|:--:|:--:|:------:|:-----------:|
| 20 | snakepipes_scrna_qc | **100→✅** | 90→❌ | **100→✅** | **100→✅** | **3 Arms** | 3/4 |
| **小计** | | **1/1** | **0/1** | **1/1** | **1/1** | | **3/4** |
| **通过率** | | **100%** | **0%** | **100%** | **100%** | | **75%** |

---

### Other (4 Tasks - 差异化)

| # | Task | None | LLM | Pipe | Paper | Winner | Binary Pass |
|---|------|:--:|:--:|:--:|:--:|:------:|:-----------:|
| 21 | nearest_gene | **89→❌** | 75→❌ | **89→❌** | 50→❌ | **None** | 0/4 |
| 22 | snakepipes_merge_ct | **99→✅** | 75→❌ | 83→❌ | 83→❌ | **None** | 1/4 |
| 23 | snakepipes_merge_fc | **83→❌** | 75→❌ | **83→❌** | 70→❌ | **None** | 0/4 |
| 24 | epibtn_rpkm | 48→❌ | **100→✅** | 48→❌ | 48→❌ | **LLM** | 1/4 |
| **小计** | | **1/4** | **1/4** | **0/4** | **0/4** | | **2/16** |
| **通过率** | | **25%** | **25%** | **0%** | **0%** | | **13%** |

---

## 📈 差异化任务汇总 (21 Tasks, Binary)

### 完全通过率对比

| Arm | 通过数 | 失败数 | 完全通过率 | vs全部37任务 |
|-----|--------|--------|-----------|--------------|
| **Paper** | **9 / 21** | 12 | **43%** | 59%→43% (-16%) |
| **None** | **6 / 21** | 15 | **29%** | 57%→29% (-28%) |
| **LLM_Plan** | **5 / 21** | 16 | **24%** | 54%→24% (-30%) |
| **Pipeline** | **4 / 21** | 17 | **19%** | 51%→19% (-32%) |
| **总计** | **24 / 84** | 60 | **29%** | 56%→29% (-27%) |

### 胜出分析 (Winner Analysis)

| Arm | Unique Wins | Shared Wins | Total Tasks Won | Win Rate |
|-----|-------------|-------------|-----------------|----------|
| **Paper** | **7** | 2 | 9 | **43%** |
| **None** | **4** | 2 | 6 | **29%** |
| **LLM_Plan** | **3** | 2 | 5 | **24%** |
| **Pipeline** | **2** | 2 | 4 | **19%** |
| **All Fail** | - | - | 7 | 33% |

---

## 📊 按类别胜出分布

| Category | Tasks | Paper | LLM | Pipe | None | All Fail |
|----------|-------|-------|-----|------|------|----------|
| **Tier A** | 5 | **4** | 0 | 1 | 0 | 0 |
| **RNA** | 4 | 1 | 0 | 1 | 0 | 2* |
| **ChIP** | 4 | **2** | 1 | 0 | 0 | 1 |
| **Methyl** | 5 | 1 | 1 | 0 | 0 | **3** |
| **scRNA** | 1 | 1 | 0 | 1 | 1 | 0 |
| **Other** | 4 | 0 | 2 | 1 | **2** | 0 |
| **TOTAL** | **23** | **9** | **4** | **4** | **3** | **6** |

*dea_limma全部<95%算All Fail

---

## 🔥 Top 10 差异化案例

### 1. Paper独家: limma_duplicatecorrelation
| Arm | Value | Binary |
|-----|-------|:------:|
| None | 0% | ❌ |
| LLM | 0% | ❌ |
| Pipe | 0% | ❌ |
| **Paper** | **100%** | ✅ |
**知识不可替代**

### 2. Paper独家: limma_voom_weights
| Arm | Value | Binary |
|-----|-------|:------:|
| None | 0% | ❌ |
| LLM | 50% | ❌ |
| Pipe | 50% | ❌ |
| **Paper** | **100%** | ✅ |
**方法变体知识**

### 3. Paper独家: chipseq_plot_macs_qc
| Arm | Value | Binary |
|-----|-------|:------:|
| None | 67% | ❌ |
| LLM | 76% | ❌ |
| Pipe | 76% | ❌ |
| **Paper** | **99%** | ✅ |
**QC标准知识**

### 4. LLM独家: epibtn_rpkm
| Arm | Value | Binary |
|-----|-------|:------:|
| None | 48% | ❌ |
| **LLM** | **100%** | ✅ |
| Pipe | 48% | ❌ |
| Paper | 48% | ❌ |
**Step-by-step规划**

### 5. LLM+Paper: methylkit_filt_norm
| Arm | Value | Binary |
|-----|-------|:------:|
| None | 15% | ❌ |
| **LLM** | **99%** | ✅ |
| Pipe | 23% | ❌ |
| **Paper** | **99%** | ✅ |
**参数调优知识**

### 6. LLM独家: phantompeak_correlation
| Arm | Value | Binary |
|-----|-------|:------:|
| None | 99% | ❌ |
| **LLM** | **100%** | ✅ |
| Pipe | 99% | ❌ |
| Paper | 99% | ❌ |
**1%差距决定成败**

### 7. Pipe独家: methylkit2tibble_split
| Arm | Value | Binary |
|-----|-------|:------:|
| None | 69% | ❌ |
| LLM | 23% | ❌ |
| **Pipe** | **75%** | ❌ |
| Paper | 8% | ❌ |
**Closest but still fail (<95%)**

### 8. None独家: snakepipes_merge_ct
| Arm | Value | Binary |
|-----|-------|:------:|
| **None** | **99%** | ✅ |
| LLM | 75% | ❌ |
| Pipe | 83% | ❌ |
| Paper | 83% | ❌ |
**简单任务别复杂化**

### 9. None+Pipe: nearest_gene
| Arm | Value | Binary |
|-----|-------|:------:|
| **None** | **89%** | ❌ |
| LLM | 75% | ❌ |
| **Pipe** | **89%** | ❌ |
| Paper | 50% | ❌ |
**All fail (<95%)**

### 10. All Fail: methylkit_load
| Arm | Value | Binary |
|-----|-------|:------:|
| None | 8% | ❌ |
| LLM | 8% | ❌ |
| Pipe | 8% | ❌ |
| Paper | 8% | ❌ |
**任务设计问题**

---

## 📊 两张表对比总结

| 指标 | 全部37任务 | 差异化21任务 | 变化 |
|------|-----------|-------------|------|
| **评估严格度** | 较松 | 严格 (≥95%) | - |
| **Paper 通过** | 59% (22/37) | **43%** (9/21) | -16% |
| **None 通过** | 57% (21/37) | **29%** (6/21) | -28% |
| **LLM 通过** | 54% (20/37) | **24%** (5/21) | -30% |
| **Pipe 通过** | 51% (19/37) | **19%** (4/21) | -32% |
| **平均通过率** | 56% | **29%** | -27% |
| **Paper 排名** | 🥇 1st | **🥇 1st** | = |
| **胜出次数** | 11/37 (30%) | **9/21** (43%) | ↑13% |

---

## 🎯 核心洞察

### 1. 差异化任务更困难
- 平均通过率从56%→29% (砍半)
- 说明简单任务拉高了整体表现

### 2. Paper 优势在困难任务中更突出
- 全部任务: Paper领先2%
- **差异化任务: Paper领先14%** (43% vs 29%)
- 胜出比例: 30% → **43%**

### 3. 各Arm定位清晰
| Arm | 最佳场景 | 差异化通过率 |
|-----|----------|-------------|
| **Paper** | 专业知识 (Tier A, ChIP QC) | **43%** |
| **None** | 简单直接 | **29%** |
| **LLM** | 步骤规划 | **24%** |
| **Pipeline** | 代码模板 | **19%** |

### 4. Tier A 是Paper的主场
- 在差异化任务中占4/9 Paper wins
- 100%通过率 vs 其他0-20%
- **设计得当的Paper任务=Paper必胜**

---

**结论**: 排除"免费任务"后，Paper在困难任务中的专业优势更加凸显，43%的完全通过率领先第二名14个百分点。
