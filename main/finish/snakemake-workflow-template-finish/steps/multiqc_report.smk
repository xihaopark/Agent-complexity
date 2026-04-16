configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "multiqc_report"


rule all:
  input:
    "results/finish/multiqc_report.done"


rule run_multiqc_report:
  output:
    "results/finish/multiqc_report.done"
  run:
    run_step(STEP_ID, output[0])
