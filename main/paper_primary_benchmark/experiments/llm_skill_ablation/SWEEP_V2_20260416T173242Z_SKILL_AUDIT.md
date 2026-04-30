# Skill injection audit — TS `20260416T173242Z`

Each (arm, task) row below confirms that the skill block in the rendered system prompt is the one the batch runner was asked to inject. sha256 values are 64-hex in metadata; the table shows the first 8 chars and cross-references the expected value from the Phase-2 resolver dry run (`_ROUTER_STATUS.md §2`). `skill_char_len` is the exact string length of the rendered block (including the wrapper section header).

| arm | task | injected | sha256 (8) | expected | char_len | md_path | lookup |
|-----|------|:--------:|------------|---------:|---------:|---------|--------|
| `none` | `akinyi_deseq2` | — | — | — | — | — | — |
| `none` | `star_deseq2_init` | — | — | — | — | — | — |
| `none` | `star_deseq2_contrast` | — | — | — | — | — | — |
| `none` | `methylkit_load` | — | — | — | — | — | — |
| `none` | `methylkit_unite` | — | — | — | — | — | — |
| `none` | `methylkit_to_tibble` | — | — | — | — | — | — |
| `paper` | `akinyi_deseq2` | ✓ | `482a3490` | `482a3490` | 1701 | `experiments/skills/10.1186_s13059-016-0881-8/SKILL.md` | `by_task_id` / `akinyi_deseq2` |
| `paper` | `star_deseq2_init` | ✓ | `4aaf2fb8` | `4aaf2fb8` | 1881 | `main/paper_primary_benchmark/experiments/skills/10.1186_s13059-014-0550-8/SKILL.md` | `by_workflow_id` / `rna-seq-star-deseq2-finish` |
| `paper` | `star_deseq2_contrast` | ✓ | `4aaf2fb8` | `4aaf2fb8` | 1881 | `main/paper_primary_benchmark/experiments/skills/10.1186_s13059-014-0550-8/SKILL.md` | `by_workflow_id` / `rna-seq-star-deseq2-finish` |
| `paper` | `methylkit_load` | ✓ | `7a926c67` | `7a926c67` | 1395 | `main/paper_primary_benchmark/experiments/skills/10.1186_s12859-016-0950-8/SKILL.md` | `by_workflow_id` / `fritjoflammers-snakemake-methylanalysis-finish` |
| `paper` | `methylkit_unite` | ✓ | `7a926c67` | `7a926c67` | 1395 | `main/paper_primary_benchmark/experiments/skills/10.1186_s12859-016-0950-8/SKILL.md` | `by_workflow_id` / `fritjoflammers-snakemake-methylanalysis-finish` |
| `paper` | `methylkit_to_tibble` | ✓ | `7a926c67` | `7a926c67` | 1395 | `main/paper_primary_benchmark/experiments/skills/10.1186_s12859-016-0950-8/SKILL.md` | `by_workflow_id` / `fritjoflammers-snakemake-methylanalysis-finish` |
| `pipeline` | `akinyi_deseq2` | ✓ | `4efe17fd` | `4efe17fd` | 3077 | `experiments/skills_pipeline/akinyi-onyango-rna_seq_pipeline-finish/SKILL.md` | `by_workflow_id` / `akinyi-onyango-rna_seq_pipeline-finish` |
| `pipeline` | `star_deseq2_init` | ✓ | `e9a3bc65` | `e9a3bc65` | 4000 | `experiments/skills_pipeline/rna-seq-star-deseq2-finish/SKILL.md` | `by_workflow_id` / `rna-seq-star-deseq2-finish` |
| `pipeline` | `star_deseq2_contrast` | ✓ | `e9a3bc65` | `e9a3bc65` | 4000 | `experiments/skills_pipeline/rna-seq-star-deseq2-finish/SKILL.md` | `by_workflow_id` / `rna-seq-star-deseq2-finish` |
| `pipeline` | `methylkit_load` | ✓ | `98666787` | `98666787` | 3836 | `experiments/skills_pipeline/fritjoflammers-snakemake-methylanalysis-finish/SKILL.md` | `by_workflow_id` / `fritjoflammers-snakemake-methylanalysis-finish` |
| `pipeline` | `methylkit_unite` | ✓ | `98666787` | `98666787` | 3836 | `experiments/skills_pipeline/fritjoflammers-snakemake-methylanalysis-finish/SKILL.md` | `by_workflow_id` / `fritjoflammers-snakemake-methylanalysis-finish` |
| `pipeline` | `methylkit_to_tibble` | ✓ | `98666787` | `98666787` | 3836 | `experiments/skills_pipeline/fritjoflammers-snakemake-methylanalysis-finish/SKILL.md` | `by_workflow_id` / `fritjoflammers-snakemake-methylanalysis-finish` |
| `llm_plan` | `akinyi_deseq2` | ✓ | `3a889efd` | `3a889efd` | 2418 | `experiments/skills_llm_plan/akinyi_deseq2/SKILL.md` | `by_task_id` / `akinyi_deseq2` |
| `llm_plan` | `star_deseq2_init` | ✓ | `f169268d` | `f169268d` | 2217 | `experiments/skills_llm_plan/star_deseq2_init/SKILL.md` | `by_task_id` / `star_deseq2_init` |
| `llm_plan` | `star_deseq2_contrast` | ✓ | `06cd791a` | `06cd791a` | 1987 | `experiments/skills_llm_plan/star_deseq2_contrast/SKILL.md` | `by_task_id` / `star_deseq2_contrast` |
| `llm_plan` | `methylkit_load` | ✓ | `db18cc3a` | `db18cc3a` | 1903 | `experiments/skills_llm_plan/methylkit_load/SKILL.md` | `by_task_id` / `methylkit_load` |
| `llm_plan` | `methylkit_unite` | ✓ | `dc8aedc7` | `dc8aedc7` | 2708 | `experiments/skills_llm_plan/methylkit_unite/SKILL.md` | `by_task_id` / `methylkit_unite` |
| `llm_plan` | `methylkit_to_tibble` | ✓ | `0da2c673` | `0da2c673` | 2267 | `experiments/skills_llm_plan/methylkit_to_tibble/SKILL.md` | `by_task_id` / `methylkit_to_tibble` |

**Audit result:** all 24 (arm, task) pairs match expectations — no cross-arm leakage, skills injected exactly where expected.
