configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "sort_alignments"


rule all:
  input:
    "results/finish/sort_alignments.done"


rule run_sort_alignments:
  output:
    "results/finish/sort_alignments.done"
  run:
    run_step(STEP_ID, output[0])
