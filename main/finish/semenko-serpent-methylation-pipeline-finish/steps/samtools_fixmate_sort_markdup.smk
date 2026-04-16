configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "samtools_fixmate_sort_markdup"


rule all:
  input:
    "results/finish/samtools_fixmate_sort_markdup.done"


rule run_samtools_fixmate_sort_markdup:
  output:
    "results/finish/samtools_fixmate_sort_markdup.done"
  run:
    run_step(STEP_ID, output[0])
