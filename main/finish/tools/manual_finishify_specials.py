from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml


FINISH_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_CANDIDATES = FINISH_ROOT / "workflow_candidates"
VALIDATION_JSON = FINISH_ROOT / "MANUAL_FINISH_VALIDATION.json"
VALIDATION_MD = FINISH_ROOT / "MANUAL_FINISH_VALIDATION.md"

RULE_RE = re.compile(r"^\s*(?:rule|checkpoint)\s+([A-Za-z0-9_.-]+)\s*:")
STEP_NAME_RE = re.compile(r'step_name\s*=\s*"([^"]+)"')


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9._-]+", "-", text.lower().replace("__", "-")).strip("-._")


def rel_from_generated_root(path: Path, finish_dir: Path) -> str:
    return str(path.resolve().relative_to(finish_dir.resolve())).replace("\\", "/")


def rel_to_source(source_path: Path) -> str:
    rel = source_path.resolve().relative_to(FINISH_ROOT.resolve())
    return f"../{str(rel).replace('\\', '/')}"


def runtime_source_path(source_path: Path) -> str:
    return str(source_path.resolve())


def generate_common_smk(dest: Path) -> None:
    content = """from pathlib import Path
import shlex
import subprocess
import sys
import os


def _runtime_helper():
  root = os.environ.get("RENZO_RUNTIME_ROOT", "").strip()
  if root:
    path = (Path(root) / "app" / "finish_step_runtime.py").resolve()
    if path.exists():
      return path
  candidate = (Path(".").resolve().parent / "Renzo_DA_Agent" / "app" / "finish_step_runtime.py").resolve()
  return candidate if candidate.exists() else None


def run_step(step_id, output_path):
  helper = _runtime_helper()
  if helper is None:
    raise RuntimeError("finish_step_runtime.py not found")
  subprocess.run(
    [
      sys.executable,
      str(helper),
      "--config-file",
      "config_basic/config.yaml",
      "--step-id",
      step_id,
      "--output-path",
      str(output_path),
    ],
    check=True,
  )
"""
    dest.write_text(content, encoding="utf-8")


def generate_step_wrapper(dest: Path, step_id: str) -> None:
    content = f"""configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "{step_id}"


rule all:
  input:
    "results/finish/{step_id}.done"


rule run_{step_id.replace('-', '_').replace('.', '_')}:
  output:
    "results/finish/{step_id}.done"
  run:
    run_step(STEP_ID, output[0])
"""
    dest.write_text(content, encoding="utf-8")


def generate_run_workflow(dest: Path, steps: list[str]) -> None:
    content = f"""from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STEPS = {json.dumps(steps, ensure_ascii=False)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cores", default="8")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--from-step")
    parser.add_argument("--to-step")
    return parser.parse_args()


def pick_steps(start: str | None, end: str | None) -> list[str]:
    start_index = STEPS.index(start) if start else 0
    end_index = STEPS.index(end) + 1 if end else len(STEPS)
    if start_index >= end_index:
        raise ValueError("from-step must be earlier than or equal to to-step")
    return STEPS[start_index:end_index]


def main() -> int:
    args = parse_args()
    for step_id in pick_steps(args.from_step, args.to_step):
        command = [
            sys.executable,
            "-m",
            "snakemake",
            "-s",
            f"steps/{{step_id}}.smk",
            "--configfile",
            "config_basic/config.yaml",
            "--cores",
            args.cores,
        ]
        if args.dry_run:
            command.append("-n")
        print(f"== {{step_id}} ==")
        print(" ".join(command))
        proc = subprocess.run(command, cwd=ROOT)
        if proc.returncode != 0:
            return proc.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
"""
    dest.write_text(content, encoding="utf-8")


def parse_rule_order(snakefile: Path) -> list[str]:
    seen: set[str] = set()
    rules: list[str] = []
    for line in snakefile.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = RULE_RE.match(line)
        if not m:
            continue
        rule = m.group(1)
        if rule in seen:
            continue
        seen.add(rule)
        rules.append(rule)
    if "all" in rules:
        rules = [r for r in rules if r != "all"] + ["all"]
    return rules


def make_finish_workflow(
    *,
    workflow_id: str,
    description: str,
    source_repo_name: str,
    steps: list[dict],
    top_config: dict,
    know_how_lines: list[str],
    input_hints: list[str] | None = None,
) -> Path:
    finish_dir = FINISH_ROOT / workflow_id
    if finish_dir.exists():
        shutil.rmtree(finish_dir)
    (finish_dir / "config_basic").mkdir(parents=True)
    (finish_dir / "steps").mkdir()
    (finish_dir / "workflow").mkdir()
    (finish_dir / "results" / "finish").mkdir(parents=True)

    config = {"workflow_id": workflow_id, "source_cores": 8, **top_config, "steps": {}}
    manifest_steps = []
    prev_step = None
    ordered_step_ids = []
    for step in steps:
        step_id = step["id"]
        ordered_step_ids.append(step_id)
        config["steps"][step_id] = {k: v for k, v in step.items() if k not in {"id", "name", "targets"}}
        manifest_steps.append(
            {
                "id": step_id,
                "name": step.get("name", step_id),
                "targets": step.get("targets", [step_id]),
                "params": {
                    "snakefile": f"steps/{step_id}.smk",
                    "configfile": "config_basic/config.yaml",
                    "cores": 1,
                    "run_directory": ".",
                    "use_conda": False,
                    "shared_conda_env": "snakemake",
                },
                "outputs": [f"results/finish/{step_id}.done"],
                "depends_on": [prev_step] if prev_step else [],
            }
        )
        prev_step = step_id
        generate_step_wrapper(finish_dir / "steps" / f"{step_id}.smk", step_id)

    generate_common_smk(finish_dir / "steps" / "common.smk")
    generate_run_workflow(finish_dir / "run_workflow.py", ordered_step_ids)
    (finish_dir / "workflow" / "agent-steps.md").write_text("\n".join(know_how_lines) + "\n", encoding="utf-8")
    (finish_dir / "config_basic" / "config.yaml").write_text(
        yaml.safe_dump(config, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    manifest = {
        "id": workflow_id,
        "name": workflow_id.replace("-", " "),
        "engine": "snakemake",
        "entry_point": "run_workflow.py",
        "description": description,
        "version": "0.1",
        "aliases": [workflow_id.replace("-finish", "")],
        "tags": ["finish", "manual", "candidate", "r-workflow"],
        "url": f"https://github.com/{source_repo_name.replace('__', '/')}",
        "know_how": "workflow/agent-steps.md",
        "know_how_files": ["workflow/agent-steps.md"],
        "discovery": {
            "kind": "finish_workflow",
            "family": "candidate",
            "aliases": [workflow_id.replace("-finish", "")],
            "retained_steps": ordered_step_ids,
            "supports_partial_run": True,
            "runner": "python3 run_workflow.py --cores 8",
            "standard_step_skills": False,
            "generated_by": "tools/manual_finishify_specials.py",
            "split_mode": "manual-special",
            "source_repo": source_repo_name,
        },
        "input_hints": input_hints or [],
        "output_hints": ["results/finish/*.done"],
        "steps": manifest_steps,
    }
    (finish_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return finish_dir


def create_lwang_workflows() -> list[Path]:
    repo = WORKFLOW_CANDIDATES / "lwang-genomics__NGS_pipeline_sn"
    config_path = repo / "config.yaml"
    outputs: list[Path] = []
    for stem in ["rna_seq", "chip_seq", "atac_seq"]:
        snakefile = repo / f"{stem}.smk"
        rules = parse_rule_order(snakefile)
        steps = []
        prev = None
        for rule in rules:
            spec = {
                "id": rule,
                "name": rule.replace("_", " "),
                "targets": ["all"] if rule == "all" else [rule],
                "summary": rule,
                "requires": [runtime_source_path(config_path)],
                "snakemake": {
                    "snakefile": runtime_source_path(snakefile),
                    "directory": runtime_source_path(repo),
                    "configfile": runtime_source_path(config_path),
                    "use_conda": False,
                    "cores": "{source_cores}",
                    "scheduler": "greedy",
                },
            }
            if rule == "all":
                spec["snakemake"]["targets"] = ["all"]
            else:
                spec["snakemake"]["root_target"] = "all"
                spec["snakemake"]["until"] = [rule]
            if prev:
                spec["depends_on"] = [prev]
            prev = rule
            steps.append(spec)
        workflow_id = f"lwang-genomics-ngs_pipeline_sn-{stem}-finish"
        outputs.append(
            make_finish_workflow(
                workflow_id=workflow_id,
                description=f"Manual finish workflow for {stem} from lwang-genomics NGS_pipeline_sn.",
                source_repo_name="lwang-genomics__NGS_pipeline_sn",
                steps=steps,
                top_config={},
                know_how_lines=[
                    f"# {workflow_id}",
                    "",
                    f"- Source repo: `lwang-genomics__NGS_pipeline_sn`",
                    f"- Source snakefile: `{rel_to_source(snakefile)}`",
                    "- Each step maps to one source Snakemake rule.",
                ],
                input_hints=[rel_to_source(config_path)],
            )
        )
    return outputs


def create_astro_workflow() -> Path:
    repo = WORKFLOW_CANDIDATES / "gersteinlab__ASTRO"
    finish_id = "gersteinlab-astro-finish"
    finish_dir = FINISH_ROOT / finish_id
    config_path = finish_dir / "config_basic" / "source_config.json"
    top_config = {
        "source_root": runtime_source_path(repo),
        "astro_config": "{workflow_dir}/config_basic/source_config.json",
        "command_conda_env": "renzo-wf-astro",
    }
    steps = [
        {
            "id": "demultiplexing",
            "name": "Demultiplexing",
            "targets": ["demultiplexing"],
            "summary": "ASTRO step 1",
            "requires": ["config_basic/source_config.json"],
            "command": (
                "bash -lc 'cd {source_root} && PYTHONPATH={source_root}/python "
                f"{sys.executable} -m ASTRO.ASTRO_run --json_file_path {{astro_config}} --steps 1'"
            ),
        },
        {
            "id": "genome_mapping",
            "name": "Genome Mapping",
            "targets": ["genome_mapping"],
            "summary": "ASTRO step 2",
            "requires": ["config_basic/source_config.json"],
            "depends_on": ["demultiplexing"],
            "command": (
                "bash -lc 'cd {source_root} && PYTHONPATH={source_root}/python "
                f"{sys.executable} -m ASTRO.ASTRO_run --json_file_path {{astro_config}} --steps 2'"
            ),
        },
        {
            "id": "feature_counting",
            "name": "Feature Counting",
            "targets": ["feature_counting"],
            "summary": "ASTRO step 3",
            "requires": ["config_basic/source_config.json"],
            "depends_on": ["genome_mapping"],
            "command": (
                "bash -lc 'cd {source_root} && PYTHONPATH={source_root}/python "
                f"{sys.executable} -m ASTRO.ASTRO_run --json_file_path {{astro_config}} --steps 4'"
            ),
        },
    ]
    finish_dir = make_finish_workflow(
        workflow_id=finish_id,
        description="Manual finish workflow for ASTRO split by its native bitwise step control.",
        source_repo_name="gersteinlab__ASTRO",
        steps=steps,
        top_config=top_config,
        know_how_lines=[
            f"# {finish_id}",
            "",
            "- Source repo: `gersteinlab__ASTRO`",
            "- Split according to native ASTRO `--steps` semantics: 1 / 2 / 4.",
        ],
        input_hints=["config_basic/source_config.json"],
    )
    config_path.write_text(
        json.dumps(
            {
                "R1": "",
                "R2": "",
                "barcode_file": "",
                "outputfolder": "",
                "starref": "",
                "gtffile": "",
                "PrimerStructure": "",
                "StructureUMI": "",
                "StructureBarcode": "",
                "threadnum": 8,
                "steps": 7,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return finish_dir


def create_st_pipeline_workflow() -> Path:
    repo = WORKFLOW_CANDIDATES / "jfnavarro__st_pipeline"
    finish_id = "jfnavarro-st_pipeline-finish"
    finish_dir = FINISH_ROOT / finish_id
    script_rel = runtime_source_path(repo / "stpipeline" / "scripts" / "st_pipeline_run.py")
    top_config = {
        "source_root": runtime_source_path(repo),
        "fastq1": "",
        "fastq2": "",
        "ids": "",
        "ref_map": "",
        "ref_annotation": "",
        "exp_name": "st_pipeline_run",
        "output_folder": "{workflow_dir}/source_outputs",
        "temp_folder": "{workflow_dir}/source_temp",
        "command_conda_env": "renzo-wf-st-pipeline",
    }
    step1_cmd = (
        f"bash -lc 'cd {{source_root}} && {sys.executable} {script_rel} "
        "{{fastq1}} {{fastq2}} --ids {{ids}} --ref-map {{ref_map}} --ref-annotation {{ref_annotation}} "
        "--expName {exp_name} --output-folder {output_folder} --temp-folder {temp_folder} "
        "--disable-mapping --disable-barcode --disable-annotation --disable-umi'"
    )
    step2_cmd = (
        f"bash -lc 'cd {{source_root}} && {sys.executable} {script_rel} "
        "{{fastq1}} {{fastq2}} --ids {{ids}} --ref-map {{ref_map}} --ref-annotation {{ref_annotation}} "
        "--expName {exp_name} --output-folder {output_folder} --temp-folder {temp_folder} "
        "--disable-trimming'"
    )
    steps = [
        {
            "id": "filtering",
            "name": "Filtering",
            "targets": ["filtering"],
            "summary": "ST pipeline filtering and trimming stage",
            "requires": [],
            "command": step1_cmd,
        },
        {
            "id": "mapping_to_dataset",
            "name": "Mapping To Dataset",
            "targets": ["mapping_to_dataset"],
            "summary": "ST pipeline mapping, barcode, annotation, and dataset stages",
            "requires": [],
            "depends_on": ["filtering"],
            "command": step2_cmd,
        },
    ]
    return make_finish_workflow(
        workflow_id=finish_id,
        description="Manual finish workflow for st_pipeline split into preprocessing and downstream execution.",
        source_repo_name="jfnavarro__st_pipeline",
        steps=steps,
        top_config=top_config,
        know_how_lines=[
            f"# {finish_id}",
            "",
            "- Source repo: `jfnavarro__st_pipeline`",
            "- Step 1 runs filtering only.",
            "- Step 2 resumes with `--disable-trimming` and completes downstream stages.",
        ],
        input_hints=[],
    )


def create_gammon_workflow() -> Path:
    repo = WORKFLOW_CANDIDATES / "gammon-bio__rnaseq_pipeline"
    top_config = {
        "source_root": runtime_source_path(repo),
        "sample_table": runtime_source_path(repo / "examples" / "sample_table.csv"),
        "project_name": "gammon_pipeline",
        "command_conda_env": "renzo-wf-gammon-rnaseq",
    }
    steps = [
        {
            "id": "get_refs",
            "name": "Get Refs",
            "targets": ["get_refs"],
            "summary": "Fetch reference files",
            "command": "bash -lc 'cd {source_root} && bash scripts/get_refs.sh --species human --build GRCh38'",
        },
        {
            "id": "rename_fastqs",
            "name": "Rename Fastqs",
            "targets": ["rename_fastqs"],
            "summary": "Normalize FASTQ file naming",
            "depends_on": ["get_refs"],
            "command": "bash -lc 'cd {source_root} && bash scripts/rename_fastqs.sh'",
        },
        {
            "id": "salmon_pipeline",
            "name": "Salmon Pipeline",
            "targets": ["salmon_pipeline"],
            "summary": "Run salmon pipeline end to end",
            "depends_on": ["rename_fastqs"],
            "command": "bash -lc 'cd {source_root} && THREADS={source_cores} bash salmon_pipeline.sh all'",
        },
        {
            "id": "run_deseq2",
            "name": "Run DESeq2",
            "targets": ["run_deseq2"],
            "summary": "Run DESeq2 downstream analysis",
            "depends_on": ["salmon_pipeline"],
            "requires": [runtime_source_path(repo / "examples" / "sample_table.csv")],
            "command": (
                "bash -lc 'cd {source_root} && Rscript scripts/run_deseq2.R "
                "--quant_dir out/salmon --gtf data/references/gtf/Homo_sapiens.GRCh38.110.gtf "
                "--sample_table {sample_table} --group_col condition --project_name {project_name}'"
            ),
        },
    ]
    return make_finish_workflow(
        workflow_id="gammon-bio-rnaseq_pipeline-finish",
        description="Manual finish workflow for gammon-bio RNA-seq pipeline split by its documented shell/R stages.",
        source_repo_name="gammon-bio__rnaseq_pipeline",
        steps=steps,
        top_config=top_config,
        know_how_lines=[
            "# gammon-bio-rnaseq_pipeline-finish",
            "",
            "- Source repo: `gammon-bio__rnaseq_pipeline`",
            "- Split following documented pipeline stages in the README.",
        ],
        input_hints=[rel_to_source(repo / "examples" / "sample_table.csv")],
    )


def create_mohammed_workflow() -> Path:
    repo = WORKFLOW_CANDIDATES / "mohammedemamkhattabunipd__ATACseq"
    steps = [
        {
            "id": "primary_atacseq",
            "name": "Primary ATACseq",
            "targets": ["primary_atacseq"],
            "summary": "Run main ATACseq analysis script",
            "command": f"bash -lc 'cd {runtime_source_path(repo)} && Rscript ATACseq.R'",
        },
        {
            "id": "downstream_atacseq",
            "name": "Downstream ATACseq",
            "targets": ["downstream_atacseq"],
            "summary": "Run downstream ATACseq analysis script",
            "depends_on": ["primary_atacseq"],
            "command": f"bash -lc 'cd {runtime_source_path(repo)} && Rscript ATACseq_downstream.R'",
        },
    ]
    return make_finish_workflow(
        workflow_id="mohammedemamkhattabunipd-atacseq-finish",
        description="Manual finish workflow for Signac-based ATACseq scripts.",
        source_repo_name="mohammedemamkhattabunipd__ATACseq",
        steps=steps,
        top_config={"command_conda_env": "renzo-wf-signac-atacseq"},
        know_how_lines=[
            "# mohammedemamkhattabunipd-atacseq-finish",
            "",
            "- Source repo: `mohammedemamkhattabunipd__ATACseq`",
            "- Split into primary preprocessing/embedding and downstream integration/marker analysis.",
        ],
    )


def create_saidmlonji_workflow() -> Path:
    repo = WORKFLOW_CANDIDATES / "saidmlonji__rnaseq_pipeline"
    steps = [
        {
            "id": "alignment_qc",
            "name": "Alignment QC",
            "targets": ["alignment_qc"],
            "summary": "Run primary RNAseq analysis script",
            "command": f"bash -lc 'cd {runtime_source_path(repo)} && Rscript RNAseq_analysis.R'",
        },
        {
            "id": "gene_counting",
            "name": "Gene Counting",
            "targets": ["gene_counting"],
            "summary": "Run gene counting script",
            "depends_on": ["alignment_qc"],
            "command": f"bash -lc 'cd {runtime_source_path(repo)} && Rscript gene_counting.R'",
        },
        {
            "id": "deseq2_analysis",
            "name": "DESeq2 Analysis",
            "targets": ["deseq2_analysis"],
            "summary": "Run DESeq2 downstream analysis",
            "depends_on": ["gene_counting"],
            "command": f"bash -lc 'cd {runtime_source_path(repo)} && Rscript deseq2_analysis.R'",
        },
    ]
    return make_finish_workflow(
        workflow_id="saidmlonji-rnaseq_pipeline-finish",
        description="Manual finish workflow for saidmlonji RNA-seq pipeline split across its documented R scripts.",
        source_repo_name="saidmlonji__rnaseq_pipeline",
        steps=steps,
        top_config={"command_conda_env": "renzo-wf-saidmlonji-rnaseq"},
        know_how_lines=[
            "# saidmlonji-rnaseq_pipeline-finish",
            "",
            "- Source repo: `saidmlonji__rnaseq_pipeline`",
            "- Split across repository R scripts for analysis, counting, and DE steps.",
        ],
    )


def create_300bcg_workflow() -> Path:
    repo = WORKFLOW_CANDIDATES / "epigen__300BCG_ATACseq_pipeline"
    top_config = {
        "source_root": runtime_source_path(repo),
        "sample_yaml": "",
        "sample_name": "",
        "genome": "hg38",
        "command_conda_env": "renzo-wf-300bcg",
    }
    nbexec = "jupyter nbconvert --to notebook --execute"
    steps = [
        {
            "id": "prepare_references",
            "name": "Prepare References",
            "targets": ["prepare_references"],
            "summary": "Prepare genome references and chromosome sizes",
            "command": (
                "bash -lc 'cd {source_root} && mkdir -p references/hg38 && "
                "echo Prepare FASTA, Bowtie2 index, GTF, and chrom sizes as documented in README.MD'"
            ),
        },
        {
            "id": "parse_regulatory_build",
            "name": "Parse Regulatory Build",
            "targets": ["parse_regulatory_build"],
            "summary": "Parse regulatory build files into project reference assets",
            "depends_on": ["prepare_references"],
            "command": (
                "bash -lc 'cd {source_root} && "
                f"{sys.executable} pipeline/parse_reg_build_file.py "
                "references/homo_sapiens.GRCh38.Regulatory_Build.regulatory_features.20190329.gff.gz "
                "references/hg38.chrom.sizes'"
            ),
        },
        {
            "id": "prepare_pipeline_input",
            "name": "Prepare Pipeline Input",
            "targets": ["prepare_pipeline_input"],
            "summary": "Generate pipeline annotations and sample inputs",
            "depends_on": ["parse_regulatory_build"],
            "command": f"bash -lc 'cd {{source_root}} && {nbexec} notebooks/0000.01-Prepare_pipeline_input.ipynb'",
        },
        {
            "id": "run_pipeline",
            "name": "Run Pipeline",
            "targets": ["run_pipeline"],
            "summary": "Run looper pipeline over all samples",
            "depends_on": ["prepare_pipeline_input"],
            "command": (
                "bash -lc 'cd {source_root} && "
                "python -m looper run ./pipeline/bcg_pipeline.yaml'"
            ),
        },
        {
            "id": "summarize_pipeline",
            "name": "Summarize Pipeline",
            "targets": ["summarize_pipeline"],
            "summary": "Summarize looper results",
            "depends_on": ["run_pipeline"],
            "command": "bash -lc 'cd {source_root} && python -m looper summarize ./pipeline/bcg_pipeline.yaml'",
        },
        {
            "id": "create_annotations",
            "name": "Create Annotations",
            "targets": ["create_annotations"],
            "summary": "Create complete metadata annotations",
            "depends_on": ["summarize_pipeline"],
            "command": f"bash -lc 'cd {{source_root}} && {nbexec} notebooks/0001.01-Create_Annotations.ipynb'",
        },
        {
            "id": "qc_stats",
            "name": "QC Stats",
            "targets": ["qc_stats"],
            "summary": "Compute QC and QC flags",
            "depends_on": ["create_annotations"],
            "command": f"bash -lc 'cd {{source_root}} && {nbexec} notebooks/0001.02-QC.stats.ipynb'",
        },
        {
            "id": "quantification",
            "name": "Quantification",
            "targets": ["quantification"],
            "summary": "Create count matrix, binary matrix, and signal tracks",
            "depends_on": ["qc_stats"],
            "command": f"bash -lc 'cd {{source_root}} && {nbexec} notebooks/0001.03-Quantification.ipynb'",
        },
        {
            "id": "features_analysis_a",
            "name": "Features Analysis A",
            "targets": ["features_analysis_a"],
            "summary": "Prepare UROPA configuration and feature characterization jobs",
            "depends_on": ["quantification"],
            "command": f"bash -lc 'cd {{source_root}} && {nbexec} notebooks/0001.04.a-Features_analysis.ipynb'",
        },
        {
            "id": "features_analysis_b",
            "name": "Features Analysis B",
            "targets": ["features_analysis_b"],
            "summary": "Aggregate feature annotation results",
            "depends_on": ["features_analysis_a"],
            "command": f"bash -lc 'cd {{source_root}} && {nbexec} notebooks/0001.04.b-Features_analysis.ipynb'",
        },
    ]
    return make_finish_workflow(
        workflow_id="epigen-300bcg-atacseq_pipeline-finish",
        description="Manual finish workflow for epigen 300BCG ATAC-seq pipeline split by documented pipeline and notebook stages.",
        source_repo_name="epigen__300BCG_ATACseq_pipeline",
        steps=steps,
        top_config=top_config,
        know_how_lines=[
            "# epigen-300bcg-atacseq_pipeline-finish",
            "",
            "- Source repo: `epigen__300BCG_ATACseq_pipeline`",
            "- Split according to the documented 4-part pipeline: references, looper run, summarize, and postprocessing notebooks.",
        ],
        input_hints=[],
    )


def extract_systempiper_steps(rmd_path: Path) -> list[str]:
    steps: list[str] = []
    seen: set[str] = set()
    for line in rmd_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = STEP_NAME_RE.search(line)
        if not m:
            continue
        step = m.group(1)
        if step in seen:
            continue
        seen.add(step)
        steps.append(step)
    return steps


def create_systempiper_workflow(workflow_name: str, rmd_path: Path, title: str) -> Path:
    finish_id = f"tgirke-systempiperdata-{workflow_name}-finish"
    helper = runtime_source_path(FINISH_ROOT / "tools" / "systempiper_step_runner.R")
    top_config = {
        "workflow_name": workflow_name,
        "workdir": "{workflow_dir}/systempiper_runtime/" + workflow_name,
        "rmd_file": runtime_source_path(rmd_path),
        "command_conda_env": "renzo-wf-systempiper",
    }
    step_names = extract_systempiper_steps(rmd_path)
    steps = []
    prev = None
    for step_name in step_names:
        step = {
            "id": step_name,
            "name": step_name.replace("_", " "),
            "targets": [step_name],
            "summary": step_name,
            "command": (
                f"bash -lc 'Rscript {helper} "
                "--workflow-name {workflow_name} "
                "--workdir {workdir} "
                "--rmd-file {rmd_file} "
                f"--step {step_name}'"
            ),
        }
        if prev:
            step["depends_on"] = [prev]
        prev = step_name
        steps.append(step)
    return make_finish_workflow(
        workflow_id=finish_id,
        description=f"Manual finish workflow for systemPipeRdata {title} template split by Rmd step_name declarations.",
        source_repo_name="tgirke__systemPipeRdata",
        steps=steps,
        top_config=top_config,
        know_how_lines=[
            f"# {finish_id}",
            "",
            "- Source repo: `tgirke__systemPipeRdata`",
            f"- Source Rmd: `{rel_to_source(rmd_path)}`",
            "- Step order is extracted from `appendStep(..., step_name=...)` declarations.",
        ],
        input_hints=[rel_to_source(rmd_path)],
    )


def create_systempiper_workflows() -> list[Path]:
    repo = WORKFLOW_CANDIDATES / "tgirke__systemPipeRdata" / "inst" / "extdata" / "workflows"
    specs = [
        ("rnaseq", repo / "rnaseq" / "systemPipeRNAseq.Rmd", "RNA-seq"),
        ("chipseq", repo / "chipseq" / "systemPipeChIPseq.Rmd", "ChIP-seq"),
        ("riboseq", repo / "riboseq" / "systemPipeRIBOseq.Rmd", "RIBO-seq"),
        ("varseq", repo / "varseq" / "systemPipeVARseq.Rmd", "VAR-seq"),
        ("spscrna", repo / "SPscrna" / "SPscrna.Rmd", "scRNA-seq"),
    ]
    out = []
    for workflow_name, rmd_path, title in specs:
        out.append(create_systempiper_workflow(workflow_name, rmd_path, title))
    return out


def validate_workflow(finish_dir: Path, timeout: int = 120) -> dict:
    command = [sys.executable, "run_workflow.py", "--dry-run", "--cores", "1"]
    completed = subprocess.run(
        command,
        cwd=str(finish_dir),
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    manifest = json.loads((finish_dir / "manifest.json").read_text(encoding="utf-8"))
    return {
        "workflow_id": manifest["id"],
        "workflow_dir": str(finish_dir),
        "step_count": len(manifest["steps"]),
        "status": "passed" if completed.returncode == 0 else "failed",
        "returncode": completed.returncode,
        "stdout_tail": "\n".join(completed.stdout.splitlines()[-20:]),
        "stderr_tail": "\n".join(completed.stderr.splitlines()[-20:]),
    }


def write_validation(results: list[dict]) -> None:
    VALIDATION_JSON.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    lines = [
        "# Manual Finish Validation",
        "",
        f"- Total workflows validated: {len(results)}",
        f"- Passed: {sum(1 for row in results if row['status'] == 'passed')}",
        "",
        "| Workflow | Status | Steps | Return Code |",
        "|---|---|---:|---:|",
    ]
    for row in results:
        lines.append(f"| `{row['workflow_id']}` | {row['status']} | {row['step_count']} | {row['returncode']} |")
    VALIDATION_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["convert", "validate", "convert-and-validate"])
    args = parser.parse_args()

    generated: list[Path] = []
    if args.command in {"convert", "convert-and-validate"}:
        generated.extend(create_lwang_workflows())
        generated.append(create_astro_workflow())
        generated.append(create_st_pipeline_workflow())
        generated.append(create_gammon_workflow())
        generated.append(create_mohammed_workflow())
        generated.append(create_saidmlonji_workflow())
        generated.append(create_300bcg_workflow())
        generated.extend(create_systempiper_workflows())
        print(json.dumps([path.name for path in generated], indent=2, ensure_ascii=False))

    if args.command in {"validate", "convert-and-validate"}:
        if not generated:
            patterns = [
                "lwang-genomics-ngs_pipeline_sn-rna_seq-finish",
                "lwang-genomics-ngs_pipeline_sn-chip_seq-finish",
                "lwang-genomics-ngs_pipeline_sn-atac_seq-finish",
                "gersteinlab-astro-finish",
                "jfnavarro-st_pipeline-finish",
                "gammon-bio-rnaseq_pipeline-finish",
                "mohammedemamkhattabunipd-atacseq-finish",
                "saidmlonji-rnaseq_pipeline-finish",
                "epigen-300bcg-atacseq_pipeline-finish",
                "tgirke-systempiperdata-rnaseq-finish",
                "tgirke-systempiperdata-chipseq-finish",
                "tgirke-systempiperdata-riboseq-finish",
                "tgirke-systempiperdata-varseq-finish",
                "tgirke-systempiperdata-spscrna-finish",
            ]
            generated = [FINISH_ROOT / name for name in patterns if (FINISH_ROOT / name).exists()]
        results = [validate_workflow(path) for path in generated]
        write_validation(results)
        print(json.dumps(results, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
