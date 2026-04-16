configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "DetectBeadSubstitutionErrors"


rule all:
  input:
    "results/finish/DetectBeadSubstitutionErrors.done"


rule run_DetectBeadSubstitutionErrors:
  output:
    "results/finish/DetectBeadSubstitutionErrors.done"
  run:
    run_step(STEP_ID, output[0])
