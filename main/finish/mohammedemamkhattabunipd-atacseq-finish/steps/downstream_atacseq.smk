configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "downstream_atacseq"


rule all:
  input:
    "results/finish/downstream_atacseq.done"


rule run_downstream_atacseq:
  output:
    "results/finish/downstream_atacseq.done"
  run:
    run_step(STEP_ID, output[0])
