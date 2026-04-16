configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "fix_mate"


rule all:
  input:
    "results/finish/fix_mate.done"


rule run_fix_mate:
  output:
    "results/finish/fix_mate.done"
  run:
    run_step(STEP_ID, output[0])
