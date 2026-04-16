configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "samtools_flagstat"


rule all:
  input:
    "results/finish/samtools_flagstat.done"


rule run_samtools_flagstat:
  output:
    "results/finish/samtools_flagstat.done"
  run:
    run_step(STEP_ID, output[0])
