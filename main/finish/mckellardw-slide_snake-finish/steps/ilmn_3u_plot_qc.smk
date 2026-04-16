configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_3u_plot_qc"


rule all:
  input:
    "results/finish/ilmn_3u_plot_qc.done"


rule run_ilmn_3u_plot_qc:
  output:
    "results/finish/ilmn_3u_plot_qc.done"
  run:
    run_step(STEP_ID, output[0])
