configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "aln"


rule all:
  input:
    "results/finish/aln.done"


rule run_aln:
  output:
    "results/finish/aln.done"
  run:
    run_step(STEP_ID, output[0])
