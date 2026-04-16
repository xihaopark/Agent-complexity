configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "diff_translational_eff"


rule all:
  input:
    "results/finish/diff_translational_eff.done"


rule run_diff_translational_eff:
  output:
    "results/finish/diff_translational_eff.done"
  run:
    run_step(STEP_ID, output[0])
