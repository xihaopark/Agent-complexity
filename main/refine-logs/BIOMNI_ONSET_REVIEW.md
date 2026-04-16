# Biomni Onset Review

用途:

- 对一小批代表性失败 run 做人工 onset 审查。
- 用于校验自动 `failure_onset` 是否可信。
- 用于整理 `diagnostic_replay_hint` 的 before/after 假设。

## Review Fields

- `workflow_id`
- `agent_name`
- `run_artifact`
- `evaluable`
- `gold_onset_stage`
- `gold_onset_step_id`
- `gold_onset_category`
- `gold_onset_reason`
- `terminal_symptom`
- `replay_hypothesis`
- `notes`

## Current Review Queue

| workflow_id | agent_name | run_artifact | evaluable | gold_onset_stage | gold_onset_step_id | gold_onset_category | gold_onset_reason | terminal_symptom | replay_hypothesis | notes |
|---|---|---|---|---|---|---|---|---|---|---|
