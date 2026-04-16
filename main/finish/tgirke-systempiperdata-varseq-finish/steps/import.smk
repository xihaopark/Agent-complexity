configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "import"


rule all:
  input:
    "results/finish/import.done"


rule run_import:
  output:
    "results/finish/import.done"
  run:
    run_step(STEP_ID, output[0])
