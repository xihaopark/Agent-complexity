configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "create_igv_peaks"


rule all:
  input:
    "results/finish/create_igv_peaks.done"


rule run_create_igv_peaks:
  output:
    "results/finish/create_igv_peaks.done"
  run:
    run_step(STEP_ID, output[0])
