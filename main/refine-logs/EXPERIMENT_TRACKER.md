# Experiment Tracker

| Run ID | Milestone | Purpose | System / Variant | Split / Workflow Set | Metrics | Priority | Status | Notes |
|--------|-----------|---------|------------------|----------------------|---------|----------|--------|-------|
| R001 | M0 | smoke benchmark | all agents / current runner | 3-workflow smoke set | result JSON completeness, metric parsing, failure taxonomy, infra health | MUST | BLOCKED | 当前暴露 workflow readiness 问题，见 `SMOKE_RUN_REPORT_2026-04-14.md` |
| R002 | M0 | smoke result review | all agents | same 3-workflow smoke set | success matrix, env stability, usage logging completeness | MUST | BLOCKED | 需先修 workflow protocol / input staging |
| R003 | M1 | baseline benchmark 正式运行 | Renzo | 30-workflow main set | success, runtime, llm_calls, tokens, cost | MUST | TODO | 与 peer agents 并排比较 |
| R004 | M1 | baseline benchmark 正式运行 | Biomni | 30-workflow main set | success, runtime, llm_calls, tokens, cost | MUST | TODO | 要求真实框架 |
| R005 | M1 | baseline benchmark 正式运行 | DSWizard | 30-workflow main set | success, runtime, llm_calls, tokens, cost | MUST | TODO | 与 Renzo 同协议 |
| R006 | M1 | baseline benchmark 正式运行 | STELLA | 30-workflow main set | success, runtime, llm_calls, tokens, cost | MUST | TODO | 要求真实框架 |
| R007 | M1 | baseline benchmark 正式运行 | ToolUniverse | 30-workflow main set | success, runtime, llm_calls, tokens, cost | MUST | TODO | 与 Renzo 同协议 |
| R008 | M2 | benchmark report v1 | all agents | 30-workflow main set | success matrix, failure taxonomy, paired diagnostics | MUST | TODO | 输出 paper-ready report |
| R009 | M3 | targeted adjustment design | selected agent A | same 30-workflow set | hypothesis clarity, expected metric deltas | MUST | TODO | 问题 -> 改动 -> 预期 |
| R010 | M3 | targeted adjustment implementation | selected agent A after fix | same 30-workflow set | success, runtime, llm_calls, tokens, cost | MUST | TODO | 与 before 版本成对对比 |
| R011 | M4 | same-set rerun validation | selected agent A before vs after | identical 30-workflow set | paired success delta, paired runtime delta, paired token delta | MUST | TODO | 排除 workflow 变化因素 |
| R012 | M3 | targeted adjustment design | selected agent B | same 30-workflow set | hypothesis clarity, expected metric deltas | NICE | TODO | 第二优先级 agent |
| R013 | M4 | same-set rerun validation | selected agent B before vs after | identical 30-workflow set | paired success delta, paired runtime delta, paired token delta | NICE | TODO | 视 M3 结果决定 |
| R014 | M5 | large-scale benchmark phase 1 | top-performing agents | expanded workflow pool | scaled success, runtime, llm_calls, cost | NICE | TODO | 只有闭环验证成立后才启动 |
