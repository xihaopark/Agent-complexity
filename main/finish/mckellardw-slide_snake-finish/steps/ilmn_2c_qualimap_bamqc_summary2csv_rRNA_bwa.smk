configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_2c_qualimap_bamqc_summary2csv_rRNA_bwa"


rule all:
  input:
    "results/finish/ilmn_2c_qualimap_bamqc_summary2csv_rRNA_bwa.done"


rule run_ilmn_2c_qualimap_bamqc_summary2csv_rRNA_bwa:
  output:
    "results/finish/ilmn_2c_qualimap_bamqc_summary2csv_rRNA_bwa.done"
  run:
    run_step(STEP_ID, output[0])
