configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "sm_report_peaks_count_plot"


rule all:
  input:
    "results/finish/sm_report_peaks_count_plot.done"


rule run_sm_report_peaks_count_plot:
  output:
    "results/finish/sm_report_peaks_count_plot.done"
  run:
    run_step(STEP_ID, output[0])
