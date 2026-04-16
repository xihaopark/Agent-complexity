configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "primer_to_bed"


rule all:
  input:
    "results/finish/primer_to_bed.done"


rule run_primer_to_bed:
  output:
    "results/finish/primer_to_bed.done"
  run:
    run_step(STEP_ID, output[0])
