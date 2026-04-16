configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_2a_generate_junction_bed"


rule all:
  input:
    "results/finish/ont_2a_generate_junction_bed.done"


rule run_ont_2a_generate_junction_bed:
  output:
    "results/finish/ont_2a_generate_junction_bed.done"
  run:
    run_step(STEP_ID, output[0])
