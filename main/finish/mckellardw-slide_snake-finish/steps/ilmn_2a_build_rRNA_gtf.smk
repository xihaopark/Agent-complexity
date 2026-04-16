configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_2a_build_rRNA_gtf"


rule all:
  input:
    "results/finish/ilmn_2a_build_rRNA_gtf.done"


rule run_ilmn_2a_build_rRNA_gtf:
  output:
    "results/finish/ilmn_2a_build_rRNA_gtf.done"
  run:
    run_step(STEP_ID, output[0])
