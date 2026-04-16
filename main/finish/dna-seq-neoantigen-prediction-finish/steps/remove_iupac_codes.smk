configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "remove_iupac_codes"


rule all:
  input:
    "results/finish/remove_iupac_codes.done"


rule run_remove_iupac_codes:
  output:
    "results/finish/remove_iupac_codes.done"
  run:
    run_step(STEP_ID, output[0])
