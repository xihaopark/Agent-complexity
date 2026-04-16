# Renzo Multi-Agent Development Guide

## Overview

This document defines how to use Cursor's sub-agent (Task tool) system for parallel, modular development of the Renzo data analysis agent. Each module has a dedicated Cursor rule file that defines its conventions and constraints.

## Agent Roster

| Agent Name | Module | Rule File | Key Files |
|------------|--------|-----------|-----------|
| agent-core | LangGraph state machine, nodes, planning, memory | .cursor/rules/agent-core.md | app/agent.py, app/graph.py, app/state.py, app/nodes/ |
| backend-api | FastAPI REST + WebSocket API | .cursor/rules/backend-api.md | backend/api_gateway.py |
| frontend-ui | React + TypeScript UI | .cursor/rules/frontend-ui.md | frontend/src/ |
| sandbox-execution | Docker sandbox, runners | .cursor/rules/sandbox-execution.md | app/sandbox/, app/runners/ |
| workflow-engine | Workflow registry, executor, know-how | .cursor/rules/workflow-engine.md | app/workflows/, workflow_pool/ |
| data-pipeline | Dataset and artifact management | .cursor/rules/data-pipeline.md | app/datasets.py, app/artifacts.py, data/ |
| testing-qa | Tests, QC rules, validation | .cursor/rules/testing-qa.md | tests/, app/validators/ |

## How to Spawn Sub-Agents

### Single-Module Task

For tasks that only affect one module, spawn one sub-agent:

```
User: "Add a new validation rule for empty dataframes"

You (Cursor Agent): Use Task tool to spawn one agent:

Task (testing-qa):
  "Add a new QC validation rule that checks for empty dataframes after code execution.
   - Add check function in renzo/app/validators/rules.py
   - Register it in the QC node (renzo/app/nodes/qc.py)
   - Add unit test in renzo/tests/test_qc.py
   - Follow conventions in .cursor/rules/testing-qa.md"
```

### Multi-Module Task

For features spanning multiple modules, spawn parallel agents:

```
User: "Add experiment export functionality"

You: Spawn 3 parallel Task agents:

Task 1 (agent-core):
  "Add export logic to renzo/app/experiments.py that packages
   all artifacts and datasets for an experiment into a zip file.
   Follow .cursor/rules/agent-core.md conventions."

Task 2 (backend-api):
  "Add GET /api/experiments/{id}/export endpoint in
   renzo/backend/api_gateway.py that streams the zip file.
   Follow .cursor/rules/backend-api.md conventions."

Task 3 (frontend-ui):
  "Add Export button to ExperimentManager component in
   renzo/frontend/src/components/ExperimentManager.tsx.
   Follow .cursor/rules/frontend-ui.md conventions."
```

### Cross-Cutting Changes

For changes that affect shared interfaces (state schema, API contracts):

```
User: "Add a new 'confidence_score' field to agent state"

Step 1: First handle the core change:

Task 1 (agent-core):
  "Add confidence_score: float field to AgentState in renzo/app/state.py.
   Update Planner node to set it. Update Coder to read it.
   Follow .cursor/rules/agent-core.md conventions."

Step 2: After Task 1 completes, spawn dependent tasks in parallel:

Task 2 (backend-api):
  "Include confidence_score in WebSocket plan_update messages
   in renzo/backend/api_gateway.py."

Task 3 (frontend-ui):
  "Display confidence_score in ProgressTracker component
   in renzo/frontend/src/components/ProgressTracker.tsx."

Task 4 (testing-qa):
  "Add tests for confidence_score in planner and coder node tests."
```

## Coordination Rules

### Dependency Order

When changes span modules, respect this dependency order:

1. State schema (app/state.py) -- must be first
2. Core logic (app/nodes/) -- depends on state
3. Backend API (backend/) -- depends on core logic
4. Frontend UI (frontend/) -- depends on API
5. Tests (tests/) -- depends on all above

### Shared Interfaces

These files are shared boundaries. Changes require multi-agent coordination:

- `renzo/app/state.py` -- AgentState schema (affects all nodes)
- `renzo/backend/api_gateway.py` -- API contracts (affects frontend)
- `renzo/app/graph.py` -- Node registration (affects all nodes)
- `renzo/app/nodes/router.py` -- Event routing (affects all nodes)

### Communication Pattern

Agents communicate through state and API contracts:
- agent-core <-> backend-api: through function calls and WebSocket callbacks
- backend-api <-> frontend-ui: through REST/WebSocket API contracts
- agent-core <-> sandbox-execution: through sandbox interface methods
- agent-core <-> workflow-engine: through workflow executor interface
- agent-core <-> data-pipeline: through dataset/artifact helper functions
- testing-qa: reads all modules, writes only to tests/ and validators/

## Best Practices

1. **Read the rule file first**: Every sub-agent prompt should reference the relevant rule file
2. **One module per agent**: Each Task agent should focus on ONE module
3. **State changes first**: If modifying AgentState, do it before other changes
4. **Test alongside code**: Include test updates in the same task when possible
5. **Check dependencies**: Before spawning parallel tasks, check if any depend on others
6. **Max 4 parallel agents**: Cursor supports up to 4 concurrent Task agents
7. **Verify after merge**: After parallel tasks complete, verify integration works
8. **Apply changes with minimal update**: After editing code, run `./scripts/quick_restart.sh` when only `app/` or `.env` changed (no full rebuild). Run `./scripts/update.sh` only when `backend/` (api_gateway, Dockerfile) or `frontend/` changed. See `.cursor/rules/deploy-after-edit.md`.
