configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_2a_bwa_rRNA_filtered_fastqc"


rule all:
  input:
    "results/finish/ilmn_2a_bwa_rRNA_filtered_fastqc.done"


rule run_ilmn_2a_bwa_rRNA_filtered_fastqc:
  output:
    "results/finish/ilmn_2a_bwa_rRNA_filtered_fastqc.done"
  run:
    run_step(STEP_ID, output[0])
