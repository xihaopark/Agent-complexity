# Agent 自主查询 Skill 机制设计

> **核心原则**: Skills 真实反映 paper 内容，agent 自主选择是否使用  
> **不是**: 强制灌输 skills  
> **而是**: agent 遇到困难时主动查询

---

## 🎯 设计目标

### 现状问题
- 强制给 agent 灌输 skill，可能干扰其自由发挥
- 为 task 修改 skill 会污染 paper 的真实性
- paper 表现差是因为 skill 与任务不匹配

### 新设计
- **Skill = 参考资料** (像查文档)
- **Agent 自主选择**: 困难时查询，不匹配时忽略
- **Paper 保持纯净**: 不修改以适应 task

---

## 🔧 机制设计

### 方案 1: Two-Step Agent (推荐)

```python
# Step 1: Agent 尝试解决 (无 skill)
attempt_1 = agent.run(objective, skills=None)

if attempt_1.score < 0.5:
    # Step 2: Agent 查询 skill 并重试
    skill = retrieve_skill(task_id)  # 从 paper 检索
    relevance = agent.assess_relevance(objective, skill)
    
    if relevance > 0.7:
        # Skill 相关，使用它
        attempt_2 = agent.run(objective, skills=skill)
    else:
        # Skill 不相关，继续自由发挥
        attempt_2 = agent.run(objective, skills=None, retry=True)
```

### 方案 2: Agent 自主决策

```python
# Agent 内部决策流程
class AdaptiveAgent:
    def solve(self, objective):
        # 首先尝试 baseline 方法
        code = self.generate_code(objective)
        result = self.execute(code)
        
        if result.success and result.score > 0.8:
            return result  # 成功，无需 skill
        
        # 遇到困难，查询 skill
        available_skills = self.retrieve_skills()
        
        for skill in available_skills:
            relevance = self.assess(skill, objective)
            if relevance > 0.7:
                # 尝试使用 skill
                code_with_skill = self.generate_code(
                    objective, 
                    context=f"Paper guidance: {skill}"
                )
                result = self.execute(code_with_skill)
                
                if result.score > result.previous_score:
                    return result  # Skill 有帮助
        
        # 没有有用的 skill，继续 baseline
        return result
```

---

## 📋 Implementation Plan

### 第一步: 恢复原始 Skills

将之前为 task 定制的修改回滚，保持 paper 原貌：

```markdown
# deseq2_apeglm_small_n/SKILL.md (原始)

> Source: Love, Huber & Anders (2014)

## Method from Paper
For small samples, use apeglm shrinkage.

## Implementation
res <- lfcShrink(dds, coef=2, type="apeglm", res=res)

## When to Use
n < 5 per group
```

**不添加**: 输出格式说明、鲁棒代码模式等额外信息

### 第二步: 创建 Agent 查询接口

```python
# skill_retrieval.py

class SkillRetriever:
    """Agent 可以查询 skills，但不被强制灌输"""
    
    def __init__(self, skills_dir):
        self.skills = self.load_all_skills(skills_dir)
    
    def query(self, task_description, agent_confidence):
        """
        Agent 主动查询 relevant skills
        
        Args:
            task_description: agent 对 task 的理解
            agent_confidence: agent 对自己方案的信心 (0-1)
        
        Returns:
            list of (skill, relevance_score)
        """
        if agent_confidence > 0.8:
            return []  # Agent 有信心，不需要 skill
        
        # 检索可能相关的 skills
        candidates = []
        for skill_id, skill_content in self.skills.items():
            relevance = self.calculate_relevance(
                task_description, 
                skill_content
            )
            if relevance > 0.6:
                candidates.append((skill_id, skill_content, relevance))
        
        return sorted(candidates, key=lambda x: x[2], reverse=True)
```

### 第三步: 新实验流程

```python
# run_adaptive_agent.py

def run_adaptive_experiment(task, arms=["adaptive"]):
    """
    新实验模式: agent 自主决定是否使用 skill
    """
    results = {}
    
    for arm in arms:
        if arm == "adaptive":
            # Agent 自主选择
            result = run_with_agent_choice(task)
        elif arm == "none":
            # Baseline: 无 skill
            result = run_without_skill(task)
        elif arm == "forced_paper":
            # 旧模式: 强制灌输 (对比用)
            result = run_with_forced_skill(task, "paper")
        
        results[arm] = result
    
    return results


def run_with_agent_choice(task):
    """Agent 自主选择是否查询 skill"""
    
    # Attempt 1: 自由发挥
    agent = AdaptiveAgent()
    result1 = agent.attempt(task)
    
    if result1.score >= 0.8:
        return {
            'score': result1.score,
            'method': 'baseline_sufficient',
            'skill_used': False
        }
    
    # 遇到困难，查询可用 skills
    skills = skill_retriever.query(
        task_description=agent.task_analysis,
        agent_confidence=result1.confidence
    )
    
    if not skills:
        return {
            'score': result1.score,
            'method': 'baseline_no_relevant_skill',
            'skill_used': False
        }
    
    # 尝试最相关的 skill
    best_skill = skills[0]
    result2 = agent.attempt(task, skill=best_skill)
    
    if result2.score > result1.score:
        return {
            'score': result2.score,
            'method': 'skill_helped',
            'skill_used': True,
            'skill_id': best_skill[0],
            'relevance': best_skill[2]
        }
    else:
        return {
            'score': result1.score,
            'method': 'skill_not_helpful',
            'skill_used': False
        }
```

---

## 📊 预期效果

### 对比旧模式 vs 新模式

| 场景 | 旧模式 (强制灌输) | 新模式 (自主查询) |
|------|------------------|------------------|
| Skill 匹配 | ✅ 有效 | ✅ 有效 |
| Skill 不匹配 | ❌ 干扰 agent | ✅ Agent 忽略 |
| 简单任务 | ⚠️ 过度复杂 | ✅ 保持简单 |
| 复杂任务 | ✅ 有帮助 | ✅ 主动使用 |

### 解决原 4 个失败案例

| Task | 旧模式问题 | 新模式行为 |
|------|-----------|-----------|
| methylkit2tibble_split | MethPat skill 不匹配 | Agent 发现不匹配，忽略 skill，自由发挥 (应该成功) |
| nearest_gene | snakePipes skill 不匹配 | Agent 忽略，使用简单方法 |
| snakepipes_merge_* | 复杂 skill 干扰 | Agent 选择简单方法 |

---

## 🔬 理论支持

### 为什么自主查询更好

1. **Relevance Assessment**: Agent 能判断 skill 是否与当前任务相关
2. **Fallback Mechanism**: 不匹配时有退路 (baseline)
3. **No Forced Interference**: 不匹配的 skill 不会干扰
4. **Preserves Paper Purity**: 不修改 skill 内容

### 与 RAG (Retrieval-Augmented Generation) 类比

- **RAG**: LLM 检索文档片段，自主决定是否使用
- **本设计**: Agent 检索 paper skills，自主决定是否使用
- **优势**: 避免无关信息干扰

---

## 🚀 下一步行动

### 立即执行 (1 天)

1. **回滚 Skills**: 恢复原始 paper skills (去掉 task-specific 修改)
2. **实现查询机制**: 创建 `SkillRetriever` 类
3. **修改 Agent Prompt**: 添加自主决策逻辑

### 测试 (1-2 天)

1. **测试原 4 个失败案例**: 验证新模式是否成功
2. **测试 5 个新 tasks**: 验证 paper skills 仍有效
3. **对比实验**: 旧模式 vs 新模式

### 代码示例

```python
# 新的 agent prompt
two_step_prompt = """
You are a bioinformatics expert. Solve the following task.

## Step 1: Attempt with your baseline knowledge
Write R code and execute it.

## Step 2: If Step 1 fails or score < 0.5
Query available paper-derived skills:
{skills_available}

Assess relevance of each skill to this task.
If relevance > 0.7, use the skill guidance.
If relevance < 0.7, continue with baseline methods.

## Decision
Explain why you chose to use or ignore the paper skill.
"""
```

---

## 💡 关键洞察

**你的观点完全正确**:
- Skills 是参考资料，不是指令
- Agent 应该有自主权
- 强制灌输不匹配的技能会适得其反
- 保持 paper 内容纯净很重要

**新模式的价值**:
- 既保留 paper 知识的价值
- 又避免不匹配时的干扰
- 更符合真实研究场景 (研究员查文献)

---

*设计完成*: 2026-04-23  
*待实现*: 回滚 skills + 实现查询机制 + 测试验证
