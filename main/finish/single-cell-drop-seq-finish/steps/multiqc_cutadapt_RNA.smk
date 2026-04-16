configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "multiqc_cutadapt_RNA"


rule all:
  input:
    "results/finish/multiqc_cutadapt_RNA.done"


rule run_multiqc_cutadapt_RNA:
  output:
    "results/finish/multiqc_cutadapt_RNA.done"
  run:
    run_step(STEP_ID, output[0])
