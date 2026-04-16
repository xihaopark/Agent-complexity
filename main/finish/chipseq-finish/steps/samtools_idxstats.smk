configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "samtools_idxstats"


rule all:
  input:
    "results/finish/samtools_idxstats.done"


rule run_samtools_idxstats:
  output:
    "results/finish/samtools_idxstats.done"
  run:
    run_step(STEP_ID, output[0])
