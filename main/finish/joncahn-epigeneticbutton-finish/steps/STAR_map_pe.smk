configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "STAR_map_pe"


rule all:
  input:
    "results/finish/STAR_map_pe.done"


rule run_STAR_map_pe:
  output:
    "results/finish/STAR_map_pe.done"
  run:
    run_step(STEP_ID, output[0])
