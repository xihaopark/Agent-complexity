configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "copy_qc_plots_for_datavzrd"


rule all:
  input:
    "results/finish/copy_qc_plots_for_datavzrd.done"


rule run_copy_qc_plots_for_datavzrd:
  output:
    "results/finish/copy_qc_plots_for_datavzrd.done"
  run:
    run_step(STEP_ID, output[0])
