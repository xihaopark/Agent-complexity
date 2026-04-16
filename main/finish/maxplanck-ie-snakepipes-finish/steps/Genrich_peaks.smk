configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "Genrich_peaks"


rule all:
  input:
    "results/finish/Genrich_peaks.done"


rule run_Genrich_peaks:
  output:
    "results/finish/Genrich_peaks.done"
  run:
    run_step(STEP_ID, output[0])
