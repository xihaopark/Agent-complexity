configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "samtools_statistics"


rule all:
  input:
    "results/finish/samtools_statistics.done"


rule run_samtools_statistics:
  output:
    "results/finish/samtools_statistics.done"
  run:
    run_step(STEP_ID, output[0])
