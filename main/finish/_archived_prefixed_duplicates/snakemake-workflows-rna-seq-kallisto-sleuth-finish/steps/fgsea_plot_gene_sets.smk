configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "fgsea_plot_gene_sets"


rule all:
  input:
    "results/finish/fgsea_plot_gene_sets.done"


rule run_fgsea_plot_gene_sets:
  output:
    "results/finish/fgsea_plot_gene_sets.done"
  run:
    run_step(STEP_ID, output[0])
