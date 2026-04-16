configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "count_sample_kmers"


rule all:
  input:
    "results/finish/count_sample_kmers.done"


rule run_count_sample_kmers:
  output:
    "results/finish/count_sample_kmers.done"
  run:
    run_step(STEP_ID, output[0])
