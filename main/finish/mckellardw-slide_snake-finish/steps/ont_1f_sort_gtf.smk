configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_1f_sort_gtf"


rule all:
  input:
    "results/finish/ont_1f_sort_gtf.done"


rule run_ont_1f_sort_gtf:
  output:
    "results/finish/ont_1f_sort_gtf.done"
  run:
    run_step(STEP_ID, output[0])
