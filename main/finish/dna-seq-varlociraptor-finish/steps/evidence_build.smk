configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "evidence_build"


rule all:
  input:
    "results/finish/evidence_build.done"


rule run_evidence_build:
  output:
    "results/finish/evidence_build.done"
  run:
    run_step(STEP_ID, output[0])
