configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "sort_bnd_bcfs"


rule all:
  input:
    "results/finish/sort_bnd_bcfs.done"


rule run_sort_bnd_bcfs:
  output:
    "results/finish/sort_bnd_bcfs.done"
  run:
    run_step(STEP_ID, output[0])
