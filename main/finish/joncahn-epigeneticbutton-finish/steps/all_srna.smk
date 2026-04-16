configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "all_srna"


rule all:
  input:
    "results/finish/all_srna.done"


rule run_all_srna:
  output:
    "results/finish/all_srna.done"
  run:
    run_step(STEP_ID, output[0])
