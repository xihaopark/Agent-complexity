# Paper2Skills 完整工作区索引
> 生成时间: $(date)
> 分支: exp/paper2skills
> 根路径: main/paper_primary_benchmark/

---

## 📊 项目概览

| 类别 | 数量 | 路径 |
|------|------|------|
| **Tasks (Real)** | 32 | `ldp_r_task_eval/tasks/real/` |
| **Ground Truth** | 32 | `ldp_r_task_eval/tasks/real_ground_truth/` |
| **Paper Skills** | 20 | `experiments/skills/` |
| **LLM Plan Skills** | 33 | `experiments/skills_llm_plan/` |
| **Pipeline Skills** | 17 | `experiments/skills_pipeline/` |
| **Evaluation Results** | 51 JSON + 46 MD | `ldp_r_task_eval/runs/_evaluations*/` |
| **4-Arm Trajectory Archives** | 4 tar.gz (~10MB) | `experiments/llm_skill_ablation/_archive_4arm_final_20260417/` |

---

## 🧠 Agent 框架代码

位置: `main/paper_primary_benchmark/ldp_r_task_eval/`

```
├── __init__.py              # Package init
├── batch_runner.py          # 批量运行器 (17KB)
├── llm_env.py              # LLM 环境配置
├── r_task_env.py           # R 任务环境 (12KB)
├── rollout.py              # Rollout 执行 (6KB)
├── run_pilot.py            # Pilot 运行入口
├── r_tasks.json            # 任务定义
├── r_tasks/                # 任务注册表
│   ├── registry.json
│   ├── registry.real.json          ← 32任务注册表
│   ├── registry.real.smoke.json
│   └── ...
└── config/                 # 实验配置
    ├── paper_sweep_15steps.yaml
    ├── pilot_example.yaml
    └── smoke_v3_d3.yaml
```

---

## 📋 32 Tasks 清单 (Real)

位置: `main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/`

| # | Task ID | 类型 |
|---|---------|------|
| 1 | akinyi_deseq2 | RNA-Seq DE |
| 2 | chipseq_plot_annotatepeaks_summary_homer | ChIP-Seq |
| 3 | chipseq_plot_frip_score | ChIP-Seq |
| 4 | chipseq_plot_homer_annot | ChIP-Seq |
| 5 | chipseq_plot_macs_qc | ChIP-Seq |
| 6 | chipseq_plot_peaks_count_macs2 | ChIP-Seq |
| 7 | clean_histoneHMM | Epigenetics |
| 8 | dea_limma | DE Analysis |
| 9 | epibtn_rpkm | RNA-Seq |
| 10 | longseq_deseq2_contrast | RNA-Seq |
| 11 | longseq_deseq2_init | RNA-Seq |
| 12 | methylkit2tibble_split | Methylation |
| 13 | methylkit_filt_norm | Methylation |
| 14 | methylkit_load | Methylation |
| 15 | methylkit_remove_snvs | Methylation |
| 16 | methylkit_to_tibble | Methylation |
| 17 | methylkit_unite | Methylation |
| 18 | msisensor_merge | Variant |
| 19 | nearest_gene | Annotation |
| 20 | phantompeak_correlation | ChIP-Seq |
| 21 | riya_limma | DE Analysis |
| 22 | snakepipes_merge_ct | scRNA-Seq |
| 23 | snakepipes_merge_fc | scRNA-Seq |
| 24 | snakepipes_scrna_merge_coutt | scRNA-Seq |
| 25 | snakepipes_scrna_qc | scRNA-Seq |
| 26 | snakepipes_scrna_report | scRNA-Seq |
| 27 | spilterlize_filter_features | scRNA-Seq |
| 28 | spilterlize_limma_rbe | DE Analysis |
| 29 | spilterlize_norm_edger | DE Analysis |
| 30 | spilterlize_norm_voom | DE Analysis |
| 31 | star_deseq2_contrast | RNA-Seq |
| 32 | star_deseq2_init | RNA-Seq |

每个 Task 结构:
```
tasks/real/{task_id}/
├── OBJECTIVE.md           # 任务目标
├── meta.json              # 元数据
└── input/                 # 输入数据
```

---

## 🎯 Ground Truth (参考答案)

位置: `main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/`

每个 Ground Truth 包含:
```
real_ground_truth/{task_id}/
├── meta.json
├── reference/
│   ├── script.R           # 参考脚本
│   ├── run.cmd.json       # 运行命令
│   └── wrapper.R
└── reference_output/      # 期望输出
```

---

## 🛠️ Skills 库 (3种来源)

### 1. Paper Skills (20篇论文提取)
位置: `experiments/skills/`

每篇论文一个目录:
```
skills/{doi}/
├── SKILL.md               # 技能描述
└── run_manifest.json      # 运行清单
```

示例 DOIs:
- 10.1038/ncomms14049
- 10.1038/s41467-024-48981-z
- 10.1093/bioinformatics/bts635
- 10.1186/s13059-020-01993-6
- ... (共20篇)

### 2. LLM Plan Skills (33个)
位置: `experiments/skills_llm_plan/`

任务导向技能:
- akinyi_deseq2
- chipseq_plot_*
- methylkit_*
- snakepipes_*
- spilterlize_*
- star_deseq2_*
- ... (共33个)

### 3. Pipeline Skills (17个)
位置: `experiments/skills_pipeline/`

完整 Pipeline 技能:
- cellranger-multi-finish
- maxplanck-ie-snakepipes-finish
- epigen-dea_limma-finish
- RiyaDua-cervical-cancer-snakemake-workflow
- read-alignment-pangenome-finish
- ... (共17个)

---

## 📈 实验结果 (Runs)

位置: `main/paper_primary_benchmark/ldp_r_task_eval/runs/`

### 批量运行批次 (~20个 batch)
```
batch_pav_smoke_202604161542/
batch_pav_smoke_202604161544/
batch_pav_smoke_202604161545/
batch_pav_smoke_202604161547/
batch_pav_smoke_202604161548/
batch_real_no_skill_v2/
batch_real_with_skill_v2/
batch_skill_route_smoke_*/
batch_smoke_v3_d3_*/
batch_sweep_pav_*/
...
```

每个 batch 结构:
```
batch_{name}/{task_id}/
├── metadata.json          # 运行元数据
├── trajectory.jsonl       # 执行轨迹
└── workspace/             # Agent 工作目录
    ├── OBJECTIVE.md
    ├── .plan.md
    ├── meta.json
    ├── input/             # 输入数据
    └── output/            # Agent 生成输出
```

### 评估结果 (51 JSON + 46 MD)
位置: `runs/_evaluations/` 和 `runs/_evaluations_v21/`

关键文件:
- `pav_smoke_202604161542.json/md`
- `real_no_skill_v2.json/md`
- `real_with_skill_v2.json/md`
- `skill_route_smoke_*.json/md`
- `sweep_v2_*.json/md`
- `sweep_v3_*.json/md` (v2, v3, per_file variants)
- `sweep_vanilla_*.json/md`

---

## 📦 4-Arm Trajectory 归档

位置: `experiments/llm_skill_ablation/_archive_4arm_final_20260417/`

| 文件 | 大小 | 内容 |
|------|------|------|
| batch_sweep_v3_llm_plan_20260416T194356Z.tar.gz | 2.0M | LLM Plan Arm |
| batch_sweep_v3_none_20260416T194356Z.tar.gz | 2.8M | No Skill Arm |
| batch_sweep_v3_paper_final.tar.gz | 2.5M | Paper Skill Arm |
| batch_sweep_v3_pipeline_20260416T194356Z.tar.gz | 2.6M | Pipeline Skill Arm |

评估结果:
- `eval_v2/` - V2 评估器结果 (JSON + MD)
- `eval_v21/` - V2.1 评估器结果 (JSON + MD)

---

## 📄 核心报告文档

位置: `main/paper_primary_benchmark/`

| 文档 | 行数 | 内容 |
|------|------|------|
| `COMPREHENSIVE_TECHNICAL_REPORT.md` | 666行 | 深度技术报告 |
| `FINAL_4ARM_COMPLETE.md` | - | 4臂对比总结 |
| `AGENT_EXECUTION_METHOD.md` | - | Agent 方法论流程图 |
| `AGENT_FRAMEWORK_DIAGRAM.md` | - | 架构图 |
| `AGENT_METHODOLOGY_DIAGRAM.md` | - | 方法论图 |

位置: `experiments/llm_skill_ablation/`

| 文档 | 用途 |
|------|------|
| `PROTOCOL.md` | 实验协议 |
| `INSIGHTS_REPORT.md` | 洞察报告 |
| `PAPER_SKILL_ADVOCACY.md` | Paper Skill 论证 |
| `SKILL_COVERAGE_V3.md` | 技能覆盖 V3 |
| `SKILL_FIDELITY_AUDIT.md` | 技能保真度审计 |
| `TASK_QUALITY_AUDIT.md` | 任务质量审计 |
| `FINAL_REPORT_V3.md` | V3 最终报告 |
| `per_task_compare_v21_final.csv` | 32任务对比数据 |

---

## 🔧 工具脚本

位置: `experiments/llm_skill_ablation/tools/`

- `aggregate_sweep.py` - 聚合扫 sweep 结果
- `aggregate_sweep_v2.py` - V2 版本
- `aggregate_sweep_v3.py` - V3 版本
- `build_insights_report.py` - 生成洞察报告
- `retry_paper_arm_f3.py` - Paper Arm 重试

位置: `experiments/skills_llm_plan/tools/`
- `generate_llm_plan_skill.py` - 生成 LLM Plan Skill

位置: `experiments/skills_pipeline/tools/`
- `build_manifest.py` - 构建清单
- `generate_pipeline_skill.py` - 生成 Pipeline Skill

---

## 🗂️ 外部 Paper2Skills 参考

位置: `external/Paper2Skills/`

```
├── run_skill_creator.py           # 技能创建入口
├── src/
│   ├── agents/scientific_skills_creator/  # Agent 实现
│   │   ├── agent.py
│   │   ├── prompt.py
│   │   └── tools.py
│   ├── tool_wrappers/            # 工具包装
│   │   ├── bash_tool.py
│   │   ├── file_tools.py
│   │   ├── multimodal_tools.py
│   │   └── search_tools.py
│   ├── base_agent.py
│   ├── execution.py
│   ├── state.py
│   └── llm_config.py
└── example_data/                  # 示例数据
```

---

## 🚀 快速访问命令

```bash
# 查看所有 Tasks
cd main/paper_primary_benchmark/ldp_r_task_eval/tasks/real && ls

# 查看某个 Task
cat tasks/real/akinyi_deseq2/OBJECTIVE.md

# 查看评估结果
cat runs/_evaluations/sweep_v3_paper_final.v3.json

# 解压 4-Arm Archive
cd experiments/llm_skill_ablation/_archive_4arm_final_20260417
tar -tzf batch_sweep_v3_paper_final.tar.gz | head

# 查看 Skills
cat experiments/skills/10.1038_ncomms14049/SKILL.md
```

---

*索引生成完成。所有路径相对于: main/paper_primary_benchmark/*
