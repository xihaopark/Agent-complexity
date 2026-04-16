configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "meta_compare_pathways"


rule all:
  input:
    "results/finish/meta_compare_pathways.done"


rule run_meta_compare_pathways:
  output:
    "results/finish/meta_compare_pathways.done"
  run:
    run_step(STEP_ID, output[0])
