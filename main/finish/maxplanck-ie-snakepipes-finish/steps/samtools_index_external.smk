configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "samtools_index_external"


rule all:
  input:
    "results/finish/samtools_index_external.done"


rule run_samtools_index_external:
  output:
    "results/finish/samtools_index_external.done"
  run:
    run_step(STEP_ID, output[0])
