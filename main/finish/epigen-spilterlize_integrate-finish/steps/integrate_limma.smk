configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "integrate_limma"


rule all:
  input:
    "results/finish/integrate_limma.done"


rule run_integrate_limma:
  output:
    "results/finish/integrate_limma.done"
  run:
    run_step(STEP_ID, output[0])
