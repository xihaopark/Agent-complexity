configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "gene_motif_enrichment_analysis_RcisTarget"


rule all:
  input:
    "results/finish/gene_motif_enrichment_analysis_RcisTarget.done"


rule run_gene_motif_enrichment_analysis_RcisTarget:
  output:
    "results/finish/gene_motif_enrichment_analysis_RcisTarget.done"
  run:
    run_step(STEP_ID, output[0])
