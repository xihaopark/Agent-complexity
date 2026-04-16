configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bismark_map_pe"


rule all:
  input:
    "results/finish/bismark_map_pe.done"


rule run_bismark_map_pe:
  output:
    "results/finish/bismark_map_pe.done"
  run:
    run_step(STEP_ID, output[0])
