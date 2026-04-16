configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "gtf_to_files"


rule all:
  input:
    "results/finish/gtf_to_files.done"


rule run_gtf_to_files:
  output:
    "results/finish/gtf_to_files.done"
  run:
    run_step(STEP_ID, output[0])
