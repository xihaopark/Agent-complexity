# Snakemake workflow: `star-arriba-fusion-calling`

[![Snakemake](https://img.shields.io/badge/snakemake-≥8.0.0-brightgreen.svg)](https://snakemake.github.io)
[![GitHub actions status](https://github.com/snakemake-workflows/star-arriba-fusion-calling/workflows/Tests/badge.svg?branch=main)](https://github.com/snakemake-workflows/star-arriba-fusion-calling/actions?query=branch%3Amain+workflow%3ATests)
[![run with conda](http://img.shields.io/badge/run%20with-conda-3EB049?labelColor=000000&logo=anaconda)](https://docs.conda.io/en/latest/)
[![workflow catalog](https://img.shields.io/badge/Snakemake%20workflow%20catalog-darkgreen)](https://snakemake.github.io/snakemake-workflow-catalog/docs/workflows/snakemake-workflows/star-arriba-fusion-calling)

A standardized snakemake workflow to map RNAseq reads with [star](https://github.com/alexdobin/STAR) and call fusions on the resulting alignment files with [arriba](https://github.com/suhrig/arriba/wiki/01-Home).
The main input are RNAseq reads; as a second input, users can provide structural variant calls to improve arriba's filtering.

- [Snakemake workflow: `star-arriba-fusion-calling`](#snakemake-workflow-name)
  - [Usage](#usage)
  - [Deployment options](#deployment-options)
  - [Authors](#authors)
  - [References](#references)

## Usage

The usage of this workflow is described in the [Snakemake Workflow Catalog](https://snakemake.github.io/snakemake-workflow-catalog/docs/workflows/snakemake-workflows/star-arriba-fusion-calling).

Detailed information about input data and workflow configuration can also be found in the [`config/README.md`](config/README.md).

If you use this workflow in a paper, don't forget to give credits to the authors by citing the URL of this repository or its DOI.

## Deployment options

To run the workflow from command line, change the working directory.

```bash
cd path/to/snakemake-workflow-name
```

Adjust options in the default config file `config/config.yaml`.
Before running the complete workflow, you can perform a dry run using:

```bash
snakemake --dry-run
```

To run the workflow with test files using **conda**:

```bash
snakemake --cores 2 --sdm conda --directory .test
```

## Authors

- David Lähnemann
  - German Cancer Consortium (DKTK), partner site Essen-Düsseldorf, A partnership between DKFZ and University Hospital Essen
  - Bioinformatics and Computational Oncology, Institute for AI in Medicine (IKIM), University Hospital Essen, University of Duisburg-Essen, Essen, Germany
  - https://orcid.org/0000-0002-9138-4112
- Felix Mölder
  - Institute of Pathology, University Hospital Essen, University of Duisburg-Essen, Essen, Germany
  - Bioinformatics and Computational Oncology, Institute for AI in Medicine (IKIM), University Hospital Essen, University of Duisburg-Essen, Essen, Germany
  - https://orcid.org/0000-0002-3976-9701


## References

> Dobin, A., Davis, C. A., Schlesinger, F., Drenkow, J., Zaleski, C., Jha, S., Batut, P., Chaisson, M., & Gingeras, T. R. _STAR: ultrafast universal RNA-seq aligner_. Bioinformatics (Oxford, England), 29(1), 15–21, **2013**. https://doi.org/10.1093/bioinformatics/bts635

> Sebastian Uhrig, Julia Ellermann, Tatjana Walther, Pauline Burkhardt, Martina Fröhlich, Barbara Hutter, Umut H. Toprak, Olaf Neumann, Albrecht Stenzinger, Claudia Scholl, Stefan Fröhling and Benedikt Brors. _Accurate and efficient detection of gene fusions from RNA sequencing data_. Genome Research. March 2021 31: 448-460; Published in Advance January 13, **2021**. https://doi.org/10.1101/gr.257246.119

> Köster, J., Mölder, F., Jablonski, K. P., Letcher, B., Hall, M. B., Tomkins-Tinch, C. H., Sochat, V., Forster, J., Lee, S., Twardziok, S. O., Kanitz, A., Wilm, A., Holtgrewe, M., Rahmann, S., & Nahnsen, S. _Sustainable data analysis with Snakemake_. F1000Research, 10:33, 10, 33, **2021**. https://doi.org/10.12688/f1000research.29032.2.
