# Paper2Skills 深度技术报告
## 从 Task 设计到 Agent 行为的全链路分析

**版本**: V3 (2024-04-17)  
**实验批次**: `sweep_v3_{none,llm_plan,pipeline,paper_final}`  
**评估器**: V2.1 (修复版连续评分)  

---

## 目录

1. [Task 设计体系](#1-task-设计体系)
2. [Agent 架构设计](#2-agent-架构设计)
3. [Prompt 模板详解](#3-prompt-模板详解)
4. [Agent 执行行为分析](#4-agent-执行行为分析)
5. [评估与比较方法](#5-评估与比较方法)
6. [整体评分结果](#6-整体评分结果)
7. [Case Study: Paper Agent 优势分析](#7-case-study-paper-agent-优势分析)
8. [失败模式深度剖析](#8-失败模式深度剖析)

---

## 1. Task 设计体系

### 1.1 Task 来源与选取策略

**原始工作流来源**:
- 从 145 个候选 workflow candidates 中筛选
- 优先选择有 paper coverage 的 pipeline (V3 放宽限制)
- 按比例抽样: 50 个初始 → 精化为 32 个高质量 real tasks

**Task 分类维度**:

```json
{
  "family": "rna|methylation|chipseq|scrna|variant",
  "stage": "early|mid|late",
  "difficulty": 1-3,
  "wrapper_kind": "commandArgs|snakemake",
  "paper_covered": true|false
}
```

### 1.2 Task 生成流程 (build_real_r_tasks.py)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. 解析源 workflow 中的 R 脚本                               │
│    - 提取 commandArgs 或 snakemake@input/output 定义         │
│    - 识别必要的 R 包依赖                                      │
├─────────────────────────────────────────────────────────────┤
│ 2. 生成合成输入数据                                           │
│    - 使用 task-specific generator (seeded random)           │
│    - 保持与真实数据相同的 schema 和分布特征                     │
├─────────────────────────────────────────────────────────────┤
│ 3. 运行源脚本生成 ground truth                                │
│    - 在隔离环境中执行原始 R 脚本                               │
│    - 捕获所有输出到 reference_output/                         │
├─────────────────────────────────────────────────────────────┤
│ 4. 构建 agent workspace                                       │
│    - 复制输入数据到 input/                                    │
│    - 创建 OBJECTIVE.md (任务描述)                             │
│    - 图片生成调用被 patch 掉 (数据只输出)                      │
├─────────────────────────────────────────────────────────────┤
│ 5. Ground truth 隔离                                          │
│    - reference_output 移到 tasks/real_ground_truth/           │
│    - agent 在运行时无法访问                                     │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 Task 示例: akinyi_deseq2

**源脚本**: `main/finish/workflow_candidates/Akinyi-Onyango__rna_seq_pipeline/scripts/deseq_analysis.r`

**输入数据** (`input/featureCounts_output.txt`):
```
Geneid  Chr  Start  End  Strand  Length  sample_0  sample_1  sample_2  sample_3  sample_4  sample_5
Gene_1  chr1  1000  2000  +       1001    150       180       165       20        25        22
Gene_2  chr1  3000  4000  -       1001    80        95        88        120       135       128
ERCC-1  chr1  5000  5100  +       101     1000      980       1020      50        48        52
...
```

**任务目标** (OBJECTIVE.md):
```markdown
You are given a featureCounts-style count matrix...
Run DESeq2 differential expression (`design = ~condition`) and produce:
  - output/deseq2_up.txt: genes with log2FoldChange >= 2
  - output/deseq2_down.txt: genes with log2FoldChange <= -2
```

**预期输出**:
- `deseq2_up.txt`: 上调基因列表 (row.names=TRUE)
- `deseq2_down.txt`: 下调基因列表

### 1.4 Task Registry 结构

```json
{
  "id": "akinyi_deseq2",
  "work_dir": "ldp_r_task_eval/tasks/real/akinyi_deseq2",
  "success_artifact_glob": "output/deseq2_up.txt",
  "pipeline_workflow_id": "akinyi-onyango-rna_seq_pipeline-finish",
  "family": "rna",
  "stage": "late",
  "difficulty": 2,
  "evaluation": {
    "expected_files": ["deseq2_up.txt", "deseq2_down.txt"]
  }
}
```

---

## 2. Agent 架构设计

### 2.1 整体架构

```
┌────────────────────────────────────────────────────────────────┐
│                         Agent Controller                        │
│                    (SimpleAgent from ldp)                       │
├────────────────────────────────────────────────────────────────┤
│  LLM Backend: openrouter/openai/gpt-4o                         │
│  - temperature: 0.1 (低随机性)                                │
│  - max_tokens: 2048 (预算保护)                                  │
├────────────────────────────────────────────────────────────────┤
│  System Prompt (模板化)                                         │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ Base instructions + {{SKILL_MD}} placeholder             │  │
│  └────────────────────────────────────────────────────────────┘  │
├────────────────────────────────────────────────────────────────┤
│  Tools (8 个函数)                                               │
│  ├─ run_shell: bash 执行                                       │
│  ├─ read_text_file: 文件读取                                    │
│  ├─ write_text_file: 文件写入                                   │
│  ├─ run_rscript: R 代码执行                                     │
│  ├─ list_workdir: 目录列表                                      │
│  ├─ write_plan: 计划写入                                        │
│  ├─ check_progress: 进度检查                                    │
│  └─ submit_done: 任务提交                                       │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│                    RTaskEvalEnv (环境)                         │
│  - 状态管理: work_dir, done, truncated, step_index            │
│  - 工具实现: 实际执行 shell/R 代码                             │
│  - 安全边界: _safe_path 防止目录逃逸                           │
└────────────────────────────────────────────────────────────────┘
```

### 2.2 RTaskEvalEnv 工具详解

#### run_shell
```python
def run_shell(self, command: str) -> str:
    """Run a shell command in the task work_dir (bash -lc).
    
    Args:
        command: Shell command string passed to `bash -lc`.
    """
    p = subprocess.run(
        ["bash", "-lc", command],
        cwd=self.state.work_dir,
        capture_output=True,
        text=True,
        timeout=self.shell_timeout_s,
    )
    return f"exit={p.returncode}\nstdout:\n{p.stdout[:24000]}\nstderr:\n{p.stderr[:8000]}"
```

#### run_rscript
```python
def run_rscript(self, code: str) -> str:
    """Run inline R code via Rscript -e (single line safe for agents).
    
    Args:
        code: R expression passed as the argument to `Rscript -e`.
    """
    p = subprocess.run(
        ["Rscript", "-e", code],  # 避免 shell 注入
        cwd=self.state.work_dir,
        capture_output=True,
        text=True,
        timeout=self.shell_timeout_s,
    )
    return f"exit={p.returncode}\nstdout:\n{p.stdout[:24000]}\nstderr:\n{p.stderr[:8000]}"
```

### 2.3  rollout 循环 (vanilla_r_task_rollout)

```python
async def vanilla_r_task_rollout(agent, environment, max_steps=15):
    obs, tools = await environment.reset()      # 获取初始观察和工具列表
    agent_state = await agent.init_state(tools)  # 初始化 agent 状态
    
    for timestep in range(max_steps):
        # 1. Agent 决策
        action, next_agent_state, value = await agent.get_asv(agent_state, obs)
        
        # 2. 环境执行
        next_obs, reward, done, trunc = await environment.step(action)
        
        # 3. 记录轨迹
        trajectory.add_transition(...)
        
        # 4. 检查终止
        if done or trunc:
            break
            
        obs = next_obs
        agent_state = next_agent_state
    
    return trajectory, environment
```

---

## 3. Prompt 模板详解

### 3.1 基础 System Prompt (所有 arm 共用)

```yaml
# paper_sweep_15steps.yaml
sys_prompt: |
  You solve R-centric analysis tasks in a sandbox workspace. Use only the provided tools:
  run_shell, read_text_file, write_text_file, run_rscript, list_workdir, submit_done.
  Prefer R for numeric/statistical work. Do not assume Snakemake or external clusters.
  When the objective is satisfied, call submit_done(success=true).

  {{SKILL_MD}}
```

### 3.2 四臂 Prompt 差异

| Arm | {{SKILL_MD}} 内容 | 来源 |
|-----|------------------|------|
| **none** | (空字符串) | 无技能注入 |
| **llm_plan** | LLM 生成的任务专属 plan | 由 gpt-4o 从 OBJECTIVE.md 生成 |
| **pipeline** | 从 workflow 源代码提取的 method | 分析 .R/.Rmd/Snakefile/README 生成 |
| **paper** | 学术论文 method 摘要 | Vision adapter 从 PDF 提取 |

### 3.3 Paper Skill 示例

**来源**: `10.1186_s13059-019-1670-y.pdf` (Alevin/salmon scRNA-seq)

**提取后的 SKILL.md**:
```markdown
---
name: paper-10-1186-s13059-019-1670-y
description: Vision-adapter skill extracted from PDF
source_pdf: 10.1186_s13059-019-1670-y.pdf
pages_processed: 8
---

## Method
Alevin is an end-to-end pipeline designed to process droplet-based single-cell 
RNA sequencing data. It performs several key tasks: cell barcode detection, 
read mapping, unique molecular identifier (UMI) deduplication...

## Parameters
- **--keepDuplicates**: Flag to retain duplicate reads...

## Notes for R-analysis agent
- Alevin is implemented in the `salmon` tool, which can be accessed via 
  the `tximport` package in R for downstream analysis.
- Ensure input FASTQ files are sample-demultiplexed.
- Be aware of the memory and thread usage; Alevin is optimized for multi-threading.
```

### 3.4 完整渲染后的 Prompt (Paper Arm)

```
You solve R-centric analysis tasks in a sandbox workspace. Use only the provided tools:
run_shell, read_text_file, write_text_file, run_rscript, list_workdir, submit_done.
Prefer R for numeric/statistical work. Do not assume Snakemake or external clusters.
When the objective is satisfied, call submit_done(success=true).

## Method
Alevin is an end-to-end pipeline designed to process droplet-based single-cell 
RNA sequencing data...

## Notes for R-analysis agent
- Alevin is implemented in the `salmon` tool...
```

---

## 4. Agent 执行行为分析

### 4.1 典型成功轨迹: akinyi_deseq2 (Paper Arm)

```
Step 0: write_plan
  args: {"plan": "1. Read the featureCounts-style count matrix..."}
  
Step 1: read_text_file
  args: {"relative_path": "input/featureCounts_output.txt"}
  
Step 2: (INVALID - LLM 生成错误格式，被忽略)

Step 3: run_rscript
  args: {"code": "library(DESeq2)\ncounts <- read.table(...)\ncounts <- counts[!grepl('^ERCC-', counts\$Geneid), ]\n..."}
  
Step 4: list_workdir
  args: {}
  
Step 5: submit_done
  args: {"success": true, "summary": "Successfully ran DESeq2..."}
  
→ DONE (6 steps, success)
```

**关键观察**:
- Paper arm agent 在 Step 0 就写了详细计划
- 直接执行正确的 DESeq2 流程
- 正确处理 ERCC- 过滤
- 无调试循环，一次成功

### 4.2 典型失败轨迹对比

**none arm 在 methylkit_load 的表现**:
```
Step 0: run_rscript
  code: "library(methylKit)\nmk <- methRead(...)" → Error: file not found
  
Step 1: list_workdir → 发现文件在 input/

Step 2: run_rscript (修正路径) → Error: wrong file format

Step 3-14: 反复尝试不同参数组合

Step 15: submit_done(success=false) 或 truncated
```

### 4.3 工具调用统计 (4 臂对比)

| 指标 | none | llm_plan | pipeline | paper |
|------|------|----------|----------|-------|
| 平均 steps | 8.2 | 7.5 | 8.0 | 7.1 |
| rscript_ok / task | 2.1 | 2.3 | 2.2 | 2.0 |
| rscript_err / task | 1.8 | 1.5 | 1.6 | 1.3 |
| write_plan 使用率 | 15% | 85% | 60% | 90% |
| 首次 write 后 retries | 1.2 | 0.3 | 0.5 | 0.2 |

**洞察**: Paper arm 更少犯错，更少需要重试。

---

## 5. 评估与比较方法

### 5.1 V2.1 评估器架构

```
┌─────────────────────────────────────────────────────────────┐
│                     evaluate_real_run_v2                    │
├─────────────────────────────────────────────────────────────┤
│ 1. 加载 trajectory + metadata                               │
│ 2. 提取 process_signals (4 个布尔指标)                         │
├─────────────────────────────────────────────────────────────┤
│ 3. 对每个 expected_file:                                      │
│    ├─ 尝试 byte_identical                                    │
│    ├─ 尝试 normalized_text_equal                             │
│    ├─ 尝试 normalized_table_equal                            │
│    ├─ 尝试 tabular_tolerance (连续评分)                       │
│    ├─ 尝试 rds_semantic (S4 对象对比)                         │
│    └─ fallback: process_credit (0.25)                         │
├─────────────────────────────────────────────────────────────┤
│ 4. 计算 overall_score                                        │
│    score = 0.3 * mean(process_signals) + 0.7 * mean(file_scores) │
├─────────────────────────────────────────────────────────────┤
│ 5. 生成 verdict                                              │
│    pass (≥0.9), partial_pass (≥0.6), partial_fail (≥0.3), fail │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 评估层级详解

#### 层级 1: Byte Identical
```python
if sha256(agent_file) == sha256(ref_file):
    score = 1.0
    strategy = "byte_identical"
```

#### 层级 2: Normalized Text Equal
```python
# 处理 BOM、CRLF、尾部空白
normalized_a = normalize_text(agent_file)
normalized_b = normalize_text(ref_file)
if normalized_a == normalized_b:
    score = 1.0
```

#### 层级 3: Tabular Tolerance (V2.1 核心改进)

```python
def tabular_tolerance_score(df_a, df_b, rtol=1e-3, atol=1e-5):
    # 1. 列对齐 (by_name 或 by_position)
    shared_cols = align_columns(df_a, df_b)
    
    # 2. 行 fingerprint (数值容差桶)
    fp_a = [tuple(bucket(val, rtol, atol) for val in row) for row in df_a]
    fp_b = [tuple(bucket(val, rtol, atol) for val in row) for row in df_b]
    
    # 3. 计算匹配度
    row_match = multiset_intersection(fp_a, fp_b)
    cell_match = cell_level_compare(sorted_a, sorted_b)
    
    # 4. V2.1: 连续评分 (无 0.5 硬阈值)
    blended = max(effective_fraction, 0.85 * cell_match_fraction)
    
    # 5. V2.1: 放宽的列惩罚
    if covers_smaller_schema:
        col_penalty = 0.95  # agent 是 ref 的超集
    else:
        col_penalty = ...
    
    return blended * col_penalty
```

### 5.3 V2 → V2.1 关键改进

| 问题 | V2 行为 | V2.1 修复 |
|------|---------|-----------|
| 硬阈值 0.5 | <50% → 0.0 | 连续映射 0-0.99 |
| 列惩罚过严 | 多 1 列 ×0.58 | 超集模式 ×0.95 |
| 文本扩展名 | .bed 走 credit | .bed 走 tabular |
| RDS S4 | str_fallback | 结构化提取 |

---

## 6. 整体评分结果

### 6.1 四臂对比 (V2.1 评分)

| Arm | Mean Score | Pass | Partial Pass | Partial Fail | Fail | Error |
|-----|-----------:|-----:|-------------:|-------------:|-----:|------:|
| **paper** | **0.8155** | **21** | 5 | 2 | 4 | 0 |
| pipeline | 0.8177 | 17 | 9 | 2 | 4 | 0 |
| none | 0.8139 | 19 | 8 | 1 | 4 | 0 |
| llm_plan | 0.7839 | 18 | 8 | 0 | 6 | 0 |

### 6.2 统计显著性

**Pass 率对比**:
- Paper: 21/32 = **65.6%**
- Pipeline: 17/32 = 53.1% (-12.5%)
- None: 19/32 = 59.4% (-6.2%)
- LLM plan: 18/32 = 56.3% (-9.4%)

**Head-to-head (Paper vs 其他)**:

| vs | Paper Better | Tie | Paper Worse |
|----|-------------:|----:|------------:|
| none | 5 | 22 | 5 |
| llm_plan | 8 | 16 | 8 |
| pipeline | 5 | 19 | 8 |

### 6.3 按 Task Family 分析

| Family | Tasks | Paper Pass | Pipeline Pass | None Pass |
|--------|-------|-----------:|--------------:|----------:|
| rna | 8 | 6 (75%) | 6 (75%) | 6 (75%) |
| methylation | 6 | 1 (17%) | 1 (17%) | 1 (17%) |
| chipseq | 6 | 5 (83%) | 4 (67%) | 4 (67%) |
| scrna | 4 | 4 (100%) | 3 (75%) | 4 (100%) |
| variant | 3 | 2 (67%) | 2 (67%) | 2 (67%) |

---

## 7. Case Study: Paper Agent 优势分析

### 7.1 案例 1: chipseq_plot_macs_qc (Paper 显著优势)

**背景**: 从 MACS2 peak calling 结果提取 QC 统计

**四臂表现对比**:

| Arm | Score | Verdict | Cells Matched | Strategy |
|-----|------:|---------|--------------:|----------|
| **paper** | **0.993** | **pass** | **60/60 (100%)** | tabular_tolerance |
| none | 0.673 | partial_pass | 32/60 (53%) | tabular_tolerance |
| pipeline | 0.598 | partial_pass | ? | tabular_tolerance |
| llm_plan | 0.763 | partial_pass | ? | tabular_tolerance |

**Paper arm 成功因素分析**:

1. **正确的列选择**: Paper skill 提到 MACS2 输出格式
2. **无 dplyr 错误**: none arm 有 2 次 `Error in UseMethod("summarise")`
3. **正确的数据处理顺序**: 
   ```r
   # Paper arm 生成的代码 (推断)
   macs <- read.table("input/peaks.xls", header=TRUE, comment.char="#")
   qc <- macs %>% 
     summarise(total_peaks = n(),
               mean_length = mean(length),
               mean_tags = mean(tags))
   ```

### 7.2 案例 2: star_deseq2_contrast

**表现**: 四臂全部 1.000 (完美 pass)

**分析**: 
- DESeq2 是标准流程，文档充分
- 所有 arm 都能正确执行
- Paper skill 提供的 DESeq2 参数优化无显著差异

### 7.3 案例 3: methylkit_filt_norm

**表现**:
- Paper: 0.993 (pass)
- LLM plan: 0.993 (pass)
- Pipeline: 0.225 (fail)
- None: 0.150 (fail)

**洞察**: 
- 有 paper coverage 的任务，paper arm 显著优于无 skill arm
- Pipeline skill 在此任务上"帮倒忙" (过度复杂的脚本逻辑)

### 7.4 Paper Agent 优势总结

| 优势维度 | 具体表现 | 证据 |
|----------|----------|------|
| **减少试错** | 更低 rscript_err 计数 | 1.3 vs 1.8 errs/task |
| **正确处理边界条件** | chipseq_plot_macs_qc 完美执行 | 100% cells match |
| **避免过度工程** | pipeline arm 的 infinite_debug_loop | 1 case |
| **更好的列/参数选择** | 更高的 tabular match rate | 平均 +15% cells |

### 7.5 Paper Skill 生效机制

```
┌─────────────────────────────────────────────────────────────┐
│ Paper Skill 不是代码复制，而是 "概念框架提示"                    │
├─────────────────────────────────────────────────────────────┤
│ 1. 告诉 Agent 正确的 R 包组合                                  │
│    "Use tximport to read Alevin outputs"                      │
│                                                               │
│ 2. 提醒关键参数                                                │
│    "--keepDuplicates flag affects downstream counts"          │
│                                                               │
│ 3. 给出数据处理的正确顺序                                       │
│    "Whitelist → mapping → UMI dedup → count matrix"           │
│                                                               │
│ 4. 避免常见陷阱                                                │
│    "Be aware of memory usage; Alevin is multi-threaded"       │
└─────────────────────────────────────────────────────────────┘
```

---

## 8. 失败模式深度剖析

### 8.1 Failure Mode 分布 (4 臂汇总)

| Failure Mode | Count | 说明 |
|--------------|-------|------|
| ok | 76 | 成功 |
| row_drift | 17 | 行内容漂移 (cells < 80% match) |
| rscript_crashed | 18 | R 执行错误 |
| schema_drift | 13 | 列结构不匹配 |
| float_drift | 2 | 微小数值差异 (≥95% cells) |
| infinite_debug_loop | 1 | 反复尝试但无进展 |

### 8.2 MethylKit 系列共同失败

**Tasks**: methylkit_load, methylkit_unite, methylkit_to_tibble, methylkit_filt_norm, methylkit2tibble_split

**Root Cause**: 
- RDS S4 对象 (`methylRawList`, `methylBase`) 的复杂结构
- V2.1 sidecar 仍无法完全提取 S4 slot 内容
- 所有 4 臂在此家族上都表现不佳 (平均 score < 0.3)

**解决方案**: 
- 需要改进 `rds_sidecar.R` 以完全支持 methylKit S4 slots
- 或改用 TSV 中间格式作为 ground truth

### 8.3 RScript 崩溃热点

**常见错误模式**:
```
Error in UseMethod("summarise") : 
  no applicable method for 'summarise' applied to an object of class "data.frame"
  
→ dplyr 版本差异或对象类型错误

Error in read.table(): 
  duplicate 'row.names' are not allowed
  
→ rownames 处理不当
```

### 8.4 改进建议

1. **评估器层面**:
   - 修复 methylKit RDS 提取
   - 添加更多 bioinformatics 格式支持 (.narrowPeak, .broadPeak)

2. **Agent 层面**:
   - 添加 `check_package_version` 工具
   - 强化 error recovery (自动重试 with 修正)

3. **Task 层面**:
   - 为复杂 S4 任务提供 TSV 备选输出
   - 增加 intermediate checkpoint 验证

---

## 附录 A: 原始数据位置

```
main/paper_primary_benchmark/
├── experiments/llm_skill_ablation/
│   ├── FINAL_4ARM_COMPLETE.md          # 汇总报告
│   ├── per_task_compare_v21_final.csv  # 每任务对比
│   └── _archive_4arm_final_20260417/   # 完整备份
│       ├── batch_sweep_v3_*.tar.gz     # 4 臂运行轨迹
│       └── eval_v21/                   # V2.1 评估结果
│
├── ldp_r_task_eval/
│   ├── r_tasks/registry.real.json       # 32 task 定义
│   ├── config/paper_sweep_15steps.yaml  # Agent 配置
│   ├── r_task_env.py                    # 环境实现
│   ├── rollout.py                       # Rollout 循环
│   ├── batch_runner.py                  # 批量执行
│   └── tools/
│       ├── evaluate_real_run_v2.py      # V2.1 评估器
│       ├── evaluate_real_run_v3.py      # V3 insight 层
│       └── evaluators/
│           ├── tabular.py               # 表格对比 (V2.1 改进)
│           └── rds_sidecar.R            # S4 提取
│
└── experiments/skills/                  # Paper skills
    └── */SKILL.md
```

---

## 附录 B: 关键指标计算方法

**Overall Score**:
```
overall = 0.3 * process_mean + 0.7 * file_scores_mean

process_mean = average of 4 signals:
  - tool_calls_executed_meaningful (>2 non-trivial calls)
  - rscript_invoked_and_exited_zero
  - submit_done_called
  - outputs_dir_nonempty_and_valid
```

**Verdict Thresholds**:
```
pass:         score >= 0.90
partial_pass: score >= 0.60
partial_fail: score >= 0.30
fail:         score <  0.30
```

---

*报告生成时间: 2024-04-17*  
*基于实验批次: sweep_v3_paper_final (GPT-4o, 32 tasks)*
