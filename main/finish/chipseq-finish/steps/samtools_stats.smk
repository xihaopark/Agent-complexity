configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "samtools_stats"


rule all:
  input:
    "results/finish/samtools_stats.done"


rule run_samtools_stats:
  output:
    "results/finish/samtools_stats.done"
  run:
    run_step(STEP_ID, output[0])
