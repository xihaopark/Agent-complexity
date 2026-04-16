configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_2a_build_rRNA_bwa_index"


rule all:
  input:
    "results/finish/ilmn_2a_build_rRNA_bwa_index.done"


rule run_ilmn_2a_build_rRNA_bwa_index:
  output:
    "results/finish/ilmn_2a_build_rRNA_bwa_index.done"
  run:
    run_step(STEP_ID, output[0])
