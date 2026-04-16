configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "link_bam"


rule all:
  input:
    "results/finish/link_bam.done"


rule run_link_bam:
  output:
    "results/finish/link_bam.done"
  run:
    run_step(STEP_ID, output[0])
