# Paper Skills Library & Agent/Task 状态报告

> 生成时间: 2026-05-01  
> 基准分支: `exp/paper2skills`

---

## 1. Paper Skills Library 资产总览

### 1.1 已入库论文 (20 篇方法学文献)

| DOI | 工具 | 领域 | 绑定任务数 | 状态 |
|-----|------|------|-----------|------|
| 10.1186/s13059-014-0550-8 | **DESeq2** | rna | 2 (star_deseq2_init/contrast) | ✅ 活跃 |
| 10.1093/nar/gkv007 | **limma** | rna | 1 (dea_limma) | ✅ 活跃 |
| 10.1186/s13059-016-0881-8 | DESeq2 (综述) | rna | 1 (akinyi_deseq2) | ✅ 活跃 |
| 10.1093/bioinformatics/btz436 | **snakePipes** | epigenomics | 7 | ✅ 活跃 |
| 10.1186/s12859-016-0950-8 | **MethPat** | methyl | 6 | ⚠️ 错位 |
| 10.1186/gb-2008-9-9-r137 | **MACS2** | chip | 0 | 🚧 未绑定 |
| 10.1101/2020.10.12.335331 | **Seurat** | scrna | 0 | 🚧 未绑定 |
| 10.1089/omi.2011.0118 | **clusterProfiler** | enrichment | 0 | 🚧 未绑定 |
| 其余 12 篇 | (见 library) | - | 0 | 🚧 未绑定 |

**关键发现**: 
- ✅ 5 篇核心文献已绑定 18 个任务
- ⚠️ 15 篇**有库但无绑定任务**（待命状态）
- ⚠️ **MethPat/MethylKit 错位**: methylKit 任务绑定了 MethPat 论文，需修正

---

## 2. Task Registries 状态

### 2.1 主 Registries 清单

| Registry | Tasks 数 | 用途 | 状态 |
|----------|---------|------|------|
| `registry.json` | 146 | 全量 stubs | 📦 基线 |
| `registry.real.json` | 32 | 实际可跑实验 | ✅ 活跃 |
| `registry.paper_sensitive_v1.json` | **12** | **Paper2Skills 核心** | 🎯 重点 |
| `registry.sample_50.json` | 50 | 采样实验 | ✅ 可用 |
| `registry.remaining_23.json` | 23 | 剩余任务 | 📦 后备 |

### 2.2 Paper-Sensitive V1 详细状态 (12 Tasks)

#### ✅ Verified - Tier A (5/12, 100% Paper Arm 通过)

| Task ID | 核心方法 | 绑定 DOI | Paper Arm Score |
|---------|---------|----------|-----------------|
| deseq2_apeglm_small_n | apeglm shrinkage | 10.1186/s13059-014-0550-8 | **1.0** |
| deseq2_lrt_interaction | LRT interaction | 10.1186/s13059-014-0550-8 | **1.0** |
| deseq2_shrinkage_comparison | shrinkage 比较 | 10.1186/s13059-014-0550-8 | **1.0** |
| limma_voom_weights | voomWithQualityWeights | 10.1093/nar/gkv007 | **1.0** |
| limma_duplicatecorrelation | duplicateCorrelation | 10.1093/nar/gkv007 | **1.0** |

#### 🚧 Scaffold - 待完成 (7/12)

| Task ID | 领域 | DOI 状态 | 库中已有? | 优先级 |
|---------|------|----------|-----------|--------|
| macs2_broad_histone | chip | 10.1186/gb-2008-9-9-r137 | ✅ 可立即启用 | 🔥 高 |
| seurat_sctransform_scaling | scrna | 10.1101/2020.10.12.335331 | ✅ 可立即启用 | 🔥 高 |
| seurat_integration_method | scrna | 10.1101/2020.10.12.335331 | ✅ 可立即启用 | 🔥 高 |
| clusterprofiler_gsea_vs_ora | enrichment | 10.1089/omi.2011.0118 | ✅ 可立即启用 | 🔥 高 |
| combat_seq_batch | rna | TBD_sva | ❌ 需补充 sva paper | 📋 中 |
| edger_robust_filtering | rna | TBD_edgeR | ❌ 需补充 edgeR paper | 📋 中 |
| methylkit_diffmeth_params | methyl | TBD_methylKit | ❌ 需补充 methylKit paper | 📋 中 |

---

## 3. Agent 系统状态

### 3.1 核心配置

| 组件 | 位置 | 状态 |
|------|------|------|
| `RTaskEvalEnv` | `r_task_env.py` | ✅ 代码就绪 |
| `SimpleAgent` | `ldp.agent` | ✅ 代码就绪 |
| `batch_runner.py` | 批量执行 | ✅ 四臂 (none/paper/pipeline/llm_plan) 支持 |
| `paper_sweep_15steps.yaml` | Paper Arm 配置 | ✅ `{{SKILL_MD}}` 占位符 |

### 3.2 环境状态 ⚠️

```bash
Python: 3.10.16
aviary: ❌ 未安装
ldp:    ❌ 未安装 (Python 3.10 环境)
```

**需要激活/创建 venv**:
```bash
cd main/paper_primary_benchmark/ldp_r_task_eval
python3.12 -m venv .venv-ldp-r-task
source .venv-ldp-r-task/bin/activate
pip install -r requirements.txt  # fhaviary>=0.18, ldp>=0.26
```

---

## 4. Paper Skill → Task 绑定机制

### 4.1 Skill Injection 流程

```
config/paper_sweep_15steps.yaml
    sys_prompt: |
      ...instructions...
      {{SKILL_MD}}  <-- 占位符

batch_runner.py
    _resolve_task_skill()
      ├─ skill_source='paper'
      ├─ manifest["by_task_id"] → skill_md_inline
      └─ fallback: manifest["by_workflow_id"] → disk SKILL.md
    
    _render_sys_prompt()
      └─ {{SKILL_MD}} → replaced with skill text
```

### 4.2 绑定缺口分析

| 库中有 Skill | 有绑定 Task | 缺口说明 |
|-------------|------------|---------|
| ✅ 20 篇 | ✅ 5 篇绑定 18 tasks | 15 篇待命 |
| ✅ MACS2 | ❌ 无 task | 需创建 ChIP QC task |
| ✅ Seurat | ❌ 无 task | scaffold 4个可启用 |
| ✅ clusterProfiler | ❌ 无 task | scaffold 1个可启用 |
| ❌ sva/ComBat-seq | ❌ 无 task | 需补充文献 |
| ❌ edgeR | ❌ 无 task | 需补充文献 |

---

## 5. 行动建议 (Action Items)

### 🔥 立即执行 (可立即提升实验覆盖)

1. **启用 4 个高价值 Scaffold Tasks**
   ```bash
   # 这些 DOI 已在库，只需注册到 manifest 的 by_task_id
   - macs2_broad_histone (10.1186/gb-2008-9-9-r137)
   - seurat_sctransform_scaling (10.1101/2020.10.12.335331)
   - seurat_integration_method (10.1101/2020.10.12.335331)
   - clusterprofiler_gsea_vs_ora (10.1089/omi.2011.0118)
   ```

2. **修复 MethPat → methylKit 错位**
   - methylKit 任务目前绑定 MethPat 论文
   - 需补充真正的 methylKit 方法论文

3. **搭建隔离 venv**
   ```bash
   python3.12 -m venv .venv-ldp-r-task
   pip install fhaviary>=0.18.0 ldp>=0.26.0
   ```

### 📋 中期补充 (扩充 paper 库)

4. **补充 3 篇缺失核心论文**
   - sva/ComBat-seq (batch correction)
   - edgeR (robust fitting)
   - methylKit (正确替换 MethPat)

5. **导入外部论文集合**
   ```bash
   # 待同事提供 bio_papers 目录
   python paperskills/library/scripts/import_external_papers.py \
       --source-dir /path/to/bio_papers --dry-run
   ```

### 🔬 实验运行

6. **重跑 Paper Arm 验证新启用 tasks**
   ```bash
   python batch_runner.py \
       --registry registry.paper_sensitive_v1.json \
       --config config/paper_sweep_15steps.yaml \
       --skill-source paper
   ```

---

## 6. 文件速查

| 操作 | 命令/路径 |
|------|----------|
| 查询 library | `python paperskills/library/query.py --tool DESeq2` |
| 检查 task 状态 | `cat main/paper_primary_benchmark/ldp_r_task_eval/r_tasks/registry.paper_sensitive_v1.json` |
| 重建索引 | `python paperskills/library/scripts/rebuild_index.py` |
| 批量导入 | `python paperskills/library/scripts/import_external_papers.py --source-dir <path>` |
| 查看 runs | `ls main/paper_primary_benchmark/ldp_r_task_eval/runs/` |

---

**结论**: Library 基础设施已完成，20 篇核心文献就绪，5 篇已产生 Tier A 验证结果。下一步关键是**启用 4 个待命的 scaffold tasks** 和**修复 methylation 论文错位**，即可将有效验证 task 数从 5 提升到 9+。
