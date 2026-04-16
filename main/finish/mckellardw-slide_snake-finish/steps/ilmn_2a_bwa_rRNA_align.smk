configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_2a_bwa_rRNA_align"


rule all:
  input:
    "results/finish/ilmn_2a_bwa_rRNA_align.done"


rule run_ilmn_2a_bwa_rRNA_align:
  output:
    "results/finish/ilmn_2a_bwa_rRNA_align.done"
  run:
    run_step(STEP_ID, output[0])
