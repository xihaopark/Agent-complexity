configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bustools_sort"


rule all:
  input:
    "results/finish/bustools_sort.done"


rule run_bustools_sort:
  output:
    "results/finish/bustools_sort.done"
  run:
    run_step(STEP_ID, output[0])
