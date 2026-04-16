configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "gtf2bed"


rule all:
  input:
    "results/finish/gtf2bed.done"


rule run_gtf2bed:
  output:
    "results/finish/gtf2bed.done"
  run:
    run_step(STEP_ID, output[0])
