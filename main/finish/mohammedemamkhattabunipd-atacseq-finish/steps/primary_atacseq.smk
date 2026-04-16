configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "primary_atacseq"


rule all:
  input:
    "results/finish/primary_atacseq.done"


rule run_primary_atacseq:
  output:
    "results/finish/primary_atacseq.done"
  run:
    run_step(STEP_ID, output[0])
