configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "samtools_sort_candidates"


rule all:
  input:
    "results/finish/samtools_sort_candidates.done"


rule run_samtools_sort_candidates:
  output:
    "results/finish/samtools_sort_candidates.done"
  run:
    run_step(STEP_ID, output[0])
