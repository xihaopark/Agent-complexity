configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "map_reads_bwa"


rule all:
  input:
    "results/finish/map_reads_bwa.done"


rule run_map_reads_bwa:
  output:
    "results/finish/map_reads_bwa.done"
  run:
    run_step(STEP_ID, output[0])
