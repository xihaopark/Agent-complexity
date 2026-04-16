"""
Step 4: MultiQC Report / 步骤4：MultiQC 汇总报告

Aggregate all QC results into a single interactive HTML report using MultiQC.
使用 MultiQC 将所有质控结果汇总为一个交互式 HTML 报告。

Usage / 使用方法:
  snakemake -s steps/multiqc_report.smk --configfile config_basic/config.yaml --cores 1

Input / 输入:
  results/star/ - STAR alignment outputs / STAR 比对输出
  results/qc/rseqc/ - RSeQC QC results from step 3 / 步骤3的 RSeQC 质控结果
  logs/rseqc/ - RSeQC log files / RSeQC 日志文件

Output / 输出:
  results/qc/multiqc_report.html - Aggregated QC report / 汇总质控报告
"""

configfile: "config_basic/config.yaml"


include: "common.smk"


rule all:
  """
  Target rule for MultiQC report step / MultiQC 汇总步骤的目标规则
  """
  input:
    "results/qc/multiqc_report.html",


rule multiqc:
  """
  Generate MultiQC report / 生成 MultiQC 汇总报告

  扫描 STAR 比对日志、RSeQC 分析结果和 RSeQC 日志目录，
  自动识别并汇总所有支持的工具输出，生成交互式 HTML 报告。

  使用 shell 命令直接调用 multiqc（替代原 wrapper），
  因为 wrapper 的 Python API 与统一 conda 环境中的 multiqc 版本不兼容。
  """
  input:
    expand(
      "results/star/{unit.sample_name}-{unit.unit_name}/Aligned.sortedByCoord.out.bam",
      unit=units.itertuples(),
    ),
    expand(
      "results/qc/rseqc/{unit.sample_name}-{unit.unit_name}.junctionanno.junction.bed",
      unit=units.itertuples(),
    ),
    expand(
      "results/qc/rseqc/{unit.sample_name}-{unit.unit_name}.junctionsat.junctionSaturation_plot.pdf",
      unit=units.itertuples(),
    ),
    expand(
      "results/qc/rseqc/{unit.sample_name}-{unit.unit_name}.infer_experiment.txt",
      unit=units.itertuples(),
    ),
    expand(
      "results/qc/rseqc/{unit.sample_name}-{unit.unit_name}.stats.txt",
      unit=units.itertuples(),
    ),
    expand(
      "results/qc/rseqc/{unit.sample_name}-{unit.unit_name}.inner_distance_freq.inner_distance.txt",
      unit=units.itertuples(),
    ),
    expand(
      "results/qc/rseqc/{unit.sample_name}-{unit.unit_name}.readdistribution.txt",
      unit=units.itertuples(),
    ),
    expand(
      "results/qc/rseqc/{unit.sample_name}-{unit.unit_name}.readdup.DupRate_plot.pdf",
      unit=units.itertuples(),
    ),
    expand(
      "results/qc/rseqc/{unit.sample_name}-{unit.unit_name}.readgc.GC_plot.pdf",
      unit=units.itertuples(),
    ),
    expand(
      "logs/rseqc/rseqc_junction_annotation/{unit.sample_name}-{unit.unit_name}.log",
      unit=units.itertuples(),
    ),
  output:
    "results/qc/multiqc_report.html",
  log:
    "logs/multiqc.log",
  shell:
    "multiqc"
    " results/star results/qc/rseqc logs/rseqc"
    " -o results/qc"
    " -n multiqc_report.html"
    " --force"
    " > {log} 2>&1"
