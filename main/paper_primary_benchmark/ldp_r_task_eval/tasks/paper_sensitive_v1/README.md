# Paper-sensitive R-tasks (v1 scaffold)

This directory holds **12 draft tasks** designed to maximize the chance that **PDF-derived paper skills** help agents (see `PAPER2SKILLS_TASK_BLUEPRINT.md` at repo root).

## Status

- **Scaffold**: `OBJECTIVE.md`, `meta.json`, minimal `input/` placeholders, and ground-truth skeletons are present for review.
- **Not ready for automated scoring**: reference outputs are placeholders until you run a paper-guided reference pipeline and freeze `reference_output/`.

## Layout

```
paper_sensitive_v1/
├── README.md                 # this file
├── INDEX.md                  # one-line summary table
├── real/<task_id>/           # agent workspace template
│   ├── OBJECTIVE.md
│   ├── meta.json
│   └── input/
└── real_ground_truth/<task_id>/
    ├── meta.json
    ├── reference/README.md   # expected analysis notes / stub
    └── reference_output/     # to be filled after reference run
```

## Registry

Machine-readable list: `../../r_tasks/registry.paper_sensitive_v1.json`.

## Relation to existing 32 tasks

These live **beside** `tasks/real/` (the 32-task benchmark) and do **not** modify that registry until you explicitly merge after validation.
