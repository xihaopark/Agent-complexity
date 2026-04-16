configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_3b_fastqc_unmapped"


rule all:
  input:
    "results/finish/ilmn_3b_fastqc_unmapped.done"


rule run_ilmn_3b_fastqc_unmapped:
  output:
    "results/finish/ilmn_3b_fastqc_unmapped.done"
  run:
    run_step(STEP_ID, output[0])
