configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "sambamba_flagstat"


rule all:
  input:
    "results/finish/sambamba_flagstat.done"


rule run_sambamba_flagstat:
  output:
    "results/finish/sambamba_flagstat.done"
  run:
    run_step(STEP_ID, output[0])
