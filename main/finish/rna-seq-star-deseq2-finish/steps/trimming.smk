"""
Step 1: Trimming / 步骤1：质量修剪

Trim adapters and low-quality bases from raw FASTQ reads using fastp.
使用 fastp 对原始 FASTQ 数据进行接头去除和低质量碱基修剪。

Usage / 使用方法:
  snakemake -s steps/trimming.smk --configfile config_basic/config.yaml --cores 8

Input / 输入:
  Raw FASTQ files defined in units.tsv / units.tsv 中定义的原始 FASTQ 文件

Output / 输出:
  results/trimmed/{sample}/ - Trimmed FASTQ files and QC reports / 修剪后的 FASTQ 文件和质控报告
"""

configfile: "config_basic/config.yaml"


include: "common.smk"


rule all:
  """
  Target rule for trimming step / 质量修剪步骤的目标规则

  收集所有样本的修剪后 FASTQ 文件作为目标输出。
  根据样本是双端还是单端，生成不同的目标文件列表。
  """
  input:
    expand(
      [
        "results/trimmed/{unit.sample_name}/{unit.sample_name}-{unit.unit_name}_R1.fastq.gz",
        "results/trimmed/{unit.sample_name}/{unit.sample_name}-{unit.unit_name}_R2.fastq.gz",
      ],
      unit=units.loc[
        units.apply(lambda u: is_paired_end(u["sample_name"]), axis=1)
      ].itertuples(),
    ),


rule fastp_pe:
  """
  Paired-end adapter trimming with fastp / 使用 fastp 进行双端测序数据的接头修剪

  对双端测序数据执行：
  - 自动检测或指定接头序列并去除
  - 修剪低质量碱基
  - 生成 HTML/JSON 格式的质控报告
  """
  input:
    sample=get_units_fastqs,
  output:
    trimmed=[
      "results/trimmed/{sample}/{sample}-{unit}_R1.fastq.gz",
      "results/trimmed/{sample}/{sample}-{unit}_R2.fastq.gz",
    ],
    unpaired1="results/trimmed/{sample}/{sample}-{unit}.unpaired.R1.fastq.gz",
    unpaired2="results/trimmed/{sample}/{sample}-{unit}.unpaired.R2.fastq.gz",
    failed="results/trimmed/{sample}/{sample}-{unit}_paired.failed.fastq.gz",
    html="results/trimmed/{sample}/{sample}-{unit}.html",
    json="results/trimmed/{sample}/{sample}-{unit}.json",
  log:
    "logs/trimmed/{sample}/{sample}-{unit}.log",
  params:
    adapters=lambda wc: (
      units.loc[(wc.sample, wc.unit), "fastp_adapters"]
      if pd.notna(units.loc[(wc.sample, wc.unit), "fastp_adapters"])
      and str(units.loc[(wc.sample, wc.unit), "fastp_adapters"]).strip()
      else "--detect_adapter_for_pe"
    ),
    extra=lambda wc: (
      units.loc[(wc.sample, wc.unit), "fastp_extra"]
      if pd.notna(units.loc[(wc.sample, wc.unit), "fastp_extra"])
      and str(units.loc[(wc.sample, wc.unit), "fastp_extra"]).strip()
      else "--trim_poly_x --poly_x_min_len 7 --trim_poly_g --poly_g_min_len 7"
    ),
  threads: 8
  conda:
    "../environment.yaml"
  wrapper:
    "v7.2.0/bio/fastp"


rule fastp_se:
  """
  Single-end adapter trimming with fastp / 使用 fastp 进行单端测序数据的接头修剪

  功能与 fastp_pe 相同，但针对单端测序数据。
  """
  input:
    sample=get_units_fastqs,
  output:
    trimmed="results/trimmed/{sample}/{sample}-{unit}_single.fastq.gz",
    failed="results/trimmed/{sample}/{sample}-{unit}_single.failed.fastq.gz",
    html="results/trimmed/{sample}/{sample}-{unit}_single.html",
    json="results/trimmed/{sample}/{sample}-{unit}.json",
  log:
    "logs/trimmed/{sample}/{sample}-{unit}.log",
  params:
    adapters=lambda wc: (
      units.loc[(wc.sample, wc.unit), "fastp_adapters"]
      if pd.notna(units.loc[(wc.sample, wc.unit), "fastp_adapters"])
      and str(units.loc[(wc.sample, wc.unit), "fastp_adapters"]).strip()
      else ""
    ),
    extra=lambda wc: (
      units.loc[(wc.sample, wc.unit), "fastp_extra"]
      if pd.notna(units.loc[(wc.sample, wc.unit), "fastp_extra"])
      and str(units.loc[(wc.sample, wc.unit), "fastp_extra"]).strip()
      else "--trim_poly_x --poly_x_min_len 7 --trim_poly_g --poly_g_min_len 7"
    ),
  threads: 4
  conda:
    "../environment.yaml"
  wrapper:
    "v7.2.0/bio/fastp"
