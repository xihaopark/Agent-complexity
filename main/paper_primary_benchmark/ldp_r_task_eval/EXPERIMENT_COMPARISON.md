# Paper Arm 对比实验：绑定模式 vs 检索模式

## 实验目的

比较两种 Paper Arm 机制：
1. **绑定模式 (Legacy)**: Task 预绑定特定 skill，直接注入 agent context
2. **检索模式 (Discovery)**: Agent 自主调用 discovery tools，按需获取 skills

核心问题：哪种机制更能帮助 agent 成功完成任务？

---

## 实验设计

### 控制变量

| 变量 | 设置 |
|------|------|
| Agent 模型 | openrouter/openai/gpt-4o |
| Max steps | 15 |
| Temperature | 0.1 |
| Tasks | 同一 registry 子集 |
| 评估标准 | 相同 ground truth |

### 自变量

| 条件 | 机制 | 配置 |
|------|------|------|
| **绑定模式** | `{{SKILL_MD}}` 预注入 | `paper_sweep_15steps.yaml` |
| **检索模式** | Agent 调用 `discover_skills_*()` | `paper_discovery_mode.yaml` |

---

## 运行方法

### 1. 绑定模式 (Baseline)

```bash
cd main/paper_primary_benchmark/ldp_r_task_eval

python batch_runner.py \
    --registry r_tasks/registry.paper_sensitive_v1.json \
    --config config/paper_sweep_15steps.yaml \
    --skill-source paper \
    --run-id paper_binding_mode_$(date +%Y%m%d_%H%M%S)
```

**机制**: `batch_runner` 从 manifest 读取预绑定 skill，渲染到 sys_prompt 的 `{{SKILL_MD}}`

### 2. 检索模式 (Discovery)

```bash
cd main/paper_primary_benchmark/ldp_r_task_eval

# Discovery mode requires modified environment with discovery tools
python batch_runner_discovery.py \
    --registry r_tasks/registry.paper_sensitive_v1.json \
    --config config/paper_discovery_mode.yaml \
    --run-id paper_discovery_mode_$(date +%Y%m%d_%H%M%S)
```

**机制**: 
- `RTaskEvalEnv` 额外注册 discovery tools
- Agent 可以主动调用 `discover_skills_by_scenario()` 等
- 无预绑定 skill 注入

---

## 关键区别

### 绑定模式

```
[Runner] Task: deseq2_apeglm_small_n
         ↓
[Manifest] Lookup: task_id → DOI 10.1186/s13059-014-0550-8
         ↓
[Sys Prompt] {{SKILL_MD}} = DESeq2 skill content
         ↓
[Agent] Receives pre-filled skill
         ↓
[Agent] Uses DESeq2 (or ignores it)
```

**特点**:
- ✅ Skill 立即可用，无需 agent 行动
- ❌ Agent 被动接受，无选择过程
- ❌ 绑定错误时无法纠正

### 检索模式

```
[Runner] Task: deseq2_apeglm_small_n
         ↓
[Sys Prompt] "You have discovery tools... call when uncertain"
         ↓
[Agent] Analyzes task: "small sample RNA DE analysis"
         ↓
[Agent] Calls discover_skills_by_scenario("small_sample_rna")
         ↓
[Tool] Returns: DESeq2 (apeglm) recommended
         ↓
[Agent] Calls get_skill_details("DESeq2")
         ↓
[Agent] Reads use_when, decides DESeq2 is appropriate
         ↓
[Agent] Implements with DESeq2
```

**特点**:
- ✅ Agent 主动评估和选择
- ✅ 可以探索 alternatives
- ✅ 更像人类研究员的工作流程
- ❌ 需要额外 steps 进行 discovery
- ❌ 可能选择 suboptimal（评估维度）

---

## 评估维度

### 1. 任务成功率 (Primary)
- Binary: 是否通过 ground truth 评估

### 2. 工具选择合理性
- Agent 是否选择了适合当前场景的工具
- 对比 discovery guide vs actual choice

### 3. Discovery 行为分析
- 检索模式：agent 调用了几次 discovery？
- 何时调用？（开始/遇到困难/验证）
- 是否探索 alternatives？

### 4. 效率
- 完成所需 steps
- Discovery calls 占比

### 5. 失败模式
- 绑定模式：无视 skill / 误解 skill
- 检索模式：选择错误工具 / 未充分利用 discovery

---

## 预期结果

| 维度 | 绑定模式 | 检索模式 |
|------|----------|----------|
| **成功率** | 高（skill 直接给出） | 中等-高（依赖 agent 判断） |
| **工具选择合理性** | N/A（强制） | 可评估 |
| **发现更好的方法** | ❌ | ✅ 可能 |
| **处理意外情况** | ❌ | ✅ 可探索 alternatives |
| **认知负荷** | 低 | 中等 |

**假设**: 对于简单明确任务，绑定模式更可靠；对于复杂或边界情况，检索模式可能更灵活。

---

## 分析计划

### 定性分析
- Agent trajectory 对比
- Discovery 调用时机和原因
- 选择决策的可解释性

### 定量分析
```python
# 成功率
binding_success = sum(1 for r in binding_results if r.passed)
discovery_success = sum(1 for r in discovery_results if r.passed)

# Discovery 使用率
discovery_usage = mean(r.discovery_calls for r in discovery_results)

# 选择一致性
choice_alignment = sum(
    1 for r in discovery_results
    if r.chosen_tool in r.recommended_tools
) / len(discovery_results)
```

---

## 后续实验

若检索模式表现良好：
1. **混合模式**: 预注入 1-2 个候选，允许探索 alternatives
2. **层次检索**: 先 scenario-level，后 criteria-level
3. **反馈学习**: 记录成功选择，优化 future recommendations

若检索模式表现不佳：
1. 分析 failure modes（选择错误？未使用 discovery？）
2. 改进 guidance（sys prompt 优化）
3. 考虑 hybrid（部分绑定 + discovery for alternatives）

---

## 实施状态

- [ ] 绑定模式 runner: ✅ 已有 `batch_runner.py`
- [ ] 检索模式 runner: 🚧 需 `batch_runner_discovery.py` 或修改现有
- [ ] Discovery tools in RTaskEvalEnv: 🚧 需修改环境
- [ ] Registry 子集: ✅ `registry.paper_sensitive_v1.json` (12 tasks)

---

*Design: 2026-05-01*
*Goal: Evaluate agent autonomy in skill selection*
