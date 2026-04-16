configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "optional_modules"


rule all:
  input:
    "results/finish/optional_modules.done"


rule run_optional_modules:
  output:
    "results/finish/optional_modules.done"
  run:
    run_step(STEP_ID, output[0])
