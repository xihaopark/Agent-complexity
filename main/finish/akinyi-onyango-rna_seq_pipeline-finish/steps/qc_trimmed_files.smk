configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "qc_trimmed_files"


rule all:
  input:
    "results/finish/qc_trimmed_files.done"


rule run_qc_trimmed_files:
  output:
    "results/finish/qc_trimmed_files.done"
  run:
    run_step(STEP_ID, output[0])
