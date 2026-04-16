configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_1a_merge_fastqs"


rule all:
  input:
    "results/finish/ilmn_1a_merge_fastqs.done"


rule run_ilmn_1a_merge_fastqs:
  output:
    "results/finish/ilmn_1a_merge_fastqs.done"
  run:
    run_step(STEP_ID, output[0])
