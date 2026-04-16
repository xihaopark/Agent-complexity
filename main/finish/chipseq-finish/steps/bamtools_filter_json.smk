configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bamtools_filter_json"


rule all:
  input:
    "results/finish/bamtools_filter_json.done"


rule run_bamtools_filter_json:
  output:
    "results/finish/bamtools_filter_json.done"
  run:
    run_step(STEP_ID, output[0])
