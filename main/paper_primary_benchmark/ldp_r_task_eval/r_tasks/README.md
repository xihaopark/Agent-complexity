# R-task registry

- **`registry.json`** — canonical list for `batch_runner` / tooling: `pilot_hello` (`status: ready`) plus **145** pipeline-stage stubs (`status: stub`). Paths are relative to `paper_primary_benchmark/`.

Regenerate after changing `task_definitions/`:

```bash
python3 main/paper_primary_benchmark/ldp_r_task_eval/tools/generate_r_task_stubs.py
```

Use `--force` to refresh `OBJECTIVE.md` and `meta.json` inside existing stub directories.

Validate:

```bash
python3 main/paper_primary_benchmark/ldp_r_task_eval/tools/validate_r_task_registry.py
```

The legacy file **`../r_tasks.json`** is deprecated; use **`registry.json`** only.
