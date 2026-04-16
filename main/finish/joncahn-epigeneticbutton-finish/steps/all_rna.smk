configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "all_rna"


rule all:
  input:
    "results/finish/all_rna.done"


rule run_all_rna:
  output:
    "results/finish/all_rna.done"
  run:
    run_step(STEP_ID, output[0])
