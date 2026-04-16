configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "HMMRATAC_peaks"


rule all:
  input:
    "results/finish/HMMRATAC_peaks.done"


rule run_HMMRATAC_peaks:
  output:
    "results/finish/HMMRATAC_peaks.done"
  run:
    run_step(STEP_ID, output[0])
