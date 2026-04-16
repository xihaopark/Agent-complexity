configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "perform_pairwise_diff_peaks"


rule all:
  input:
    "results/finish/perform_pairwise_diff_peaks.done"


rule run_perform_pairwise_diff_peaks:
  output:
    "results/finish/perform_pairwise_diff_peaks.done"
  run:
    run_step(STEP_ID, output[0])
