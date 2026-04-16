configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "map_reads_vg"


rule all:
  input:
    "results/finish/map_reads_vg.done"


rule run_map_reads_vg:
  output:
    "results/finish/map_reads_vg.done"
  run:
    run_step(STEP_ID, output[0])
