configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "fastp_pipe"


rule all:
  input:
    "results/finish/fastp_pipe.done"


rule run_fastp_pipe:
  output:
    "results/finish/fastp_pipe.done"
  run:
    run_step(STEP_ID, output[0])
