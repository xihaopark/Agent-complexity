## workflow overview

This workflow is a best-practice workflow for calling Fusions using Arriba.
The workflow is built using [snakemake](https://snakemake.readthedocs.io/en/stable/) and consists of the following steps:

1. Download genome reference from Ensembl
2. Generate STAR index of the reference genome (`STAR`).
3. Align reads (`STAR`).
4. Call and filter fusions (`Arriba`).
5. Create fusion plots for all fusions that pass the filters (Arriba's `draw_fusions.sh`).

## workflow setup

There are three things that you need to set up to run this workflow:

1. In the unit sheet `config/units.tsv`, specify where to find raw FASTQ files and which units belong to which sample.
2. In the sample sheet `config/samples.tsv`, specify which samples belong to which `group` of samples and what type (`alias`) of sample they are.
3. Go through the whole workflow configuration file `config/config.yaml` and adjust it for your analysis.
   The options are explained in detailed comments within the file.

# sample sheet

Add samples to `config/samples.tsv`. For each sample, the columns `sample_name`, `group`, `alias` and `platform` have to be defined. 

* The `sample_name` clearly identifies an individual biological sample.
* Multiple samples sharing the same `group` indicate that they belong together in some way, for example that they come from the same patient.
* `alias`es represent the type of the sample within its group. They are meant to be some abstract description of the sample type, and should thus be used consistently across groups. A classic example would be a combination of the `tumor` and `normal` aliases.
* The `platform` column needs to contain the used sequencing plaform (one of 'CAPILLARY', 'LS454', 'ILLUMINA', 'SOLID', 'HELICOS', 'IONTORRENT', 'ONT', 'PACBIO’).
* The same `sample_name` entry can be used multiple times within a `samples.tsv` sample sheet, with only the value in the `group` column differing between repeated rows. This way, you can use the same sample for variant calling in different groups, for example if you use a panel of normal samples when you don't have matched normal samples for tumor variant calling.

In addition, the optional `sv_file` column can be filled with the path for sample-specific structural variant calls, meant to improve the fusion calling and filtering by Arriba.
The provided files [need to be in one of the formats that Arriba accepts](https://github.com/suhrig/arriba/wiki/04-Input-files#structural-variant-calls-from-wgs).

Missing values can be specified by empty columns or by writing `NA`. Lines can be commented out with `#`.

# unit sheet

For each sample, add one or more sequencing units (runs, lanes or replicates) to the unit sheet `config/units.tsv`.
* Each unit has a `unit_name`. This can be a running number, or an actual run, lane or replicate id.
* Each unit has a `sample_name`, which associates it with the biological sample it comes from. This information is used to merged all the units of a sample before read mapping and duplicate marking.
* For each unit, you need to specify either of these columns:
  * `fq1` only for single end reads. This can point to any FASTQ file on your system
  * `fq1` and `fq2` for paired end reads. These can point to any FASTQ files on your system

Missing values can be specified by empty columns or by writing `NA`. Lines can be commented out with `#`.
