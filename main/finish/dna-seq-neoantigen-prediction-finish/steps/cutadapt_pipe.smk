configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "cutadapt_pipe"


rule all:
  input:
    "results/finish/cutadapt_pipe.done"


rule run_cutadapt_pipe:
  output:
    "results/finish/cutadapt_pipe.done"
  run:
    run_step(STEP_ID, output[0])
