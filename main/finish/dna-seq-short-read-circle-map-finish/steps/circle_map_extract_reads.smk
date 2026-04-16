configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "circle_map_extract_reads"


rule all:
  input:
    "results/finish/circle_map_extract_reads.done"


rule run_circle_map_extract_reads:
  output:
    "results/finish/circle_map_extract_reads.done"
  run:
    run_step(STEP_ID, output[0])
