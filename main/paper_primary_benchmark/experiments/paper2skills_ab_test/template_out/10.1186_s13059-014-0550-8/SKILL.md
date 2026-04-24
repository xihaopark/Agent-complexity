---
name: paper-10-1186_s13059-014-0550-8
description: >-
  Extracted notes from 10.1186_s13059-014-0550-8.pdf
---

# Paper-derived skill

## Extracted text (first pages)

```
Love et al. Genome Biology  (2014) 15:550 
DOI 10.1186/s13059-014-0550-8
METHOD
Open Access
Moderated estimation of fold change and
dispersion for RNA-seq data with DESeq2
Michael I Love1,2,3, Wolfgang Huber2 and Simon Anders2*
Abstract
In comparative high-throughput sequencing assays, a fundamental task is the analysis of count data, such as read
counts per gene in RNA-seq, for evidence of systematic changes across experimental conditions. Small replicate
numbers, discreteness, large dynamic range and the presence of outliers require a suitable statistical approach. We
present DESeq2, a method for differential analysis of count data, using shrinkage estimation for dispersions and fold
changes to improve stability and interpretability of estimates. This enables a more quantitative analysis focused on the
strength rather than the mere presence of differential expression. The DESeq2 package is available at http://www.
bioconductor.org/packages/release/bioc/html/DESeq2.html.
Background
The rapid adoption of high-throughput sequencing (HTS)
technologies for genomic studies has resulted in a need
for statistical methods to assess quantitative differences
between experiments. An important task here is the anal-
ysis of RNA sequencing (RNA-seq) data with the aim
of finding genes that are differentially expressed across
groups of samples. This task is general: methods for it are
typically also applicable for other comparative HTS assays,
including chromatin immunoprecipitation sequencing,
chromosome conformation capture, or counting observed
taxa in metagenomic studies.
Besides the need to account for the specifics of count
data, such as non-normality and a dependence of the vari-
ance on the mean, a core challenge is the small number
of samples in typical HTS experiments – often as few as
two or three replicates per condition. Inferential methods
that treat each gene separately suffer here from lack of
power, due to the high uncertainty of within-group vari-
ance estimates. In high-throughput assays, this limitation
can be overcome by pooling information across genes,
specifically, by exploiting assumptions about the similarity
of the variances of different genes measured in the same
experiment [1].
*Correspondence: sanders@fs.tum.de
2Genome Biology Unit, European Molecular Biology Laboratory,
Meyerhofstrasse 1, 69117 Heidelberg, Germany
Full list of author information is available at the end of the article
Many methods for differential expression analysis of
RNA-seq data perform such information sharing across
genes for variance (or, equivalently, dispersion) estima-
tion. edgeR [2,3] moderates the dispersion estimate for
each gene toward a common estimate across all genes, or
toward a local estimate from genes with similar expres-
sion strength, using a weighted conditional likelihood.
Our DESeq method [4] detects and corrects dispersion
estimates that are too low through modeling of the depen-
dence of the dispersion on the average expression strength
over all samples. BBSeq [5] models the dispersion on
the mean, with the mean absolute deviation of disper-
sion estimates used to reduce the influence of outliers.
DSS [6] uses a Bayesian approach to provide an estimate
for the dispersion for individual genes that accounts for
the heterogeneity of dispersion values for different genes.
baySeq [7] and ShrinkBayes [8] estimate priors for a
Bayesian model over all genes, and then provide posterior
probabilities or false discovery rates (FDRs) for differential
expression.
The most common approach in the comparative anal-
ysis of transcriptomics data is to test the null hypothesis
that the logarithmic fold change (LFC) between treat-
ment and control for a gene’s expression is exactly zero,
i.e., that the gene is not at all affected by the treatment.
Often the goal of differential analysis is to produce a list of
genes passing multiple-test adjustment, ranked by P value.
However, small changes, even if statistically highly signif-
icant, might not be the most interesting candidates for
© 2014 Love et al.; licensee BioMed Central. This is an Open Access article distributed under the terms of the Creative Commons
Attribution License (http://creativecommons.org/licenses/by/4.0), which permits unrestricted use, distribution, and reproduction
in any medium, provided the original work is properly credited. The Creative Commons Public Domain Dedication waiver
(http://creativecommons.org/publicdomain/zero/1.0/) applies to the data made available in this article, unless otherwise stated.

Love et al. Genome Biology  (2014) 15:550 
Page 2 of 21
further investigation. Ranking by fold change, on the other
hand, is complicated by the noisiness of LFC estimates for
genes with low counts. Furthermore, the number of genes
called significantly differentially expressed depends as
much on the sample size and other aspects of experimen-
tal design as it does on the biology of the experiment –
and well-powered experiments often generate an over-
whelmingly long list of hits [9]. We, therefore, developed
a statistical framework to facilitate gene ranking and visu-
alization based on stable estimation of effect sizes (LFCs),
as well as testing of differential expression with respect to
user-defined thresholds of biological significance.
Here we present DESeq2, a successor to our DESeq
method [4]. DESeq2 integrates methodological advances
with several novel features to facilitate a more quantita-
tive analysis of comparative RNA-seq data using shrinkage
estimators for dispersion and fold change. We demon-
strate the advantages of DESeq2’s new features by describ-
ing a number of applications possible with shrunken fold
changes and their estimates of standard error, including
improved gene ranking and visualization, hypothesis tests
above and below a threshold, and the regularized loga-
rithm transformation for quality assessment and cluster-
ing of overdispersed count data. We furthermore compare
DESeq2’s statistical power with existing tools, revealing
that our methodology has high sensitivity and precision,
while controlling the false positive rate. DESeq2 is avail-
able [10] as an R/Bioconductor package [11].
Results and discussion
Model and normalization
The starting point of a DESeq2 analysis is a count matrix
K with one row for each gene i and one column for each
sample j. The matrix entries Kij indicate the number of
sequencing reads that have been unambiguously mapped
to a gene in a sample. Note that although we refer in this
paper to counts of reads in genes, the methods presented
here can be applied as well to other kinds of HTS count
data. For each gene, we fit a generalized linear model
(GLM) [12] as follows.
We model read counts Kij as following a negative bino-
mial distribution (sometimes also called a gamma-Poisson
distribution) with mean μij and dispersion αi. The mean is
taken as a quantity qij, proportional to the concentration
of cDNA fragments from the gene in the sample, scaled by
a normalization factor sij, i.e., μij = sijqij. For many appli-
cations, the same constant sj can be used for all genes in
a sample, which then accounts for differences in sequenc-
ing depth between samples. To estimate these size factors,
the DESeq2 package offers the median-of-ratios method
already used in DESeq [4]. However, it can be advanta-
geous to calculate gene-specific normalization factors sij
to account for further sources of technical biases such as
differing dependence on GC content, gene length or the
like, using published methods [13,14], and these can be
supplied instead.
We use GLMs with a logarithmic link, log2 qij
=

r xjrβir, with design matrix elements xjr and coefficients
βir. In the simplest case of a comparison between two
groups, such as treated and control samples, the design
matrix elements indicate whether a sample j is treated
or not, and the GLM fit returns coefficients indicating
the overall expression strength of the gene and the log2
fold change between treatment and control. The use of
linear models, however, provides the flexibility to also ana-
lyze more complex designs, as is often useful in genomic
studies [15].
Empirical Bayes shrinkage for dispersion estimation
Within-group variability, i.e., the variability between repli-
cates, is modeled by the dispersion parameter αi, which
describes the variance of counts via Var Kij = μij + αiμ2
ij.
Accurate estimation of the dispersion parameter αi is crit-
ical for the statistical inference of differential expression.
For studies with large sample sizes this is usually not
a problem. For controlled experiments, however, sample
sizes tend to be smaller (experimental designs with as lit-
tle as two or three replicates are common and reasonable),
resulting in highly variable dispersion estimates for each
gene. If used directly, these noisy estimates would com-
promise the accuracy of differential expression testing.
One sensible solution is to share information across
genes. In DESeq2, we assume that genes of similar aver-
age expression strength have similar dispersion. We here
explain the concepts of our approach using as examples a
dataset by Bottomly et al. [16] with RNA-seq data for mice
of two different strains and a dataset by Pickrell et al. [17]
with RNA-seq data for human lymphoblastoid cell lines.
For the mathematical details, see Methods.
We first treat each gene separately and estimate gene-
wise dispersion estimates (using maximum likelihood),
which rely only on the data of each individual gene
(black dots in Figure 1). Next, we determine the location
parameter of the distribution of these estimates; to allow
for dependence on average expression strength, we fit a
smooth curve, as shown by the red line in Figure 1. This
provides an accurate estimate for the expected dispersion
value for genes of a given expression strength but does not
represent deviations of individual genes from this overall
trend. We then shrink the gene-wise dispersion estimates
toward the values predicted by the curve to obtain final
dispersion values (blue arrow heads). We use an empiri-
cal Bayes approach (Methods), which lets the strength of
shrinkage depend (i) on an estimate of how close true dis-
persion values tend to be to the fit and (ii) on the degrees
of freedom: as the sample size increases, the shrinkage
decreases in strength, and eventually becomes negligi-
ble. Our approach therefore accounts for gene-specific

Love et al. Genome Biology  (2014) 15:550 
Page 3 of 21
Figure 1 Shrinkage estimation of dispersion. Plot of dispersion estimates over the average expression strength (A) for the Bottomly et al. [16]
dataset with six samples across two groups and (B) for five samples from the Pickrell et al. [17] dataset, fitting only an intercept term. First, gene-wise
MLEs are obtained using only the respective gene’s data (black dots). Then, a curve (red) is fit to the MLEs to capture the overall trend of
dispersion-mean dependence. This fit is used as a prior mean for a second estimation round, which results in the final MAP estimates of dispersion
(arrow heads). This can be understood as a shrinkage (along the blue arrows) of the noisy gene-wise estimates toward the consensus represented
by the red line. The black points circled in blue are detected as dispersion outliers and not shrunk toward the prior (shrinkage would follow the
dotted line). For clarity, only a subset of genes is shown, which is enriched for dispersion outliers. Additional file 1: Figure S1 displays the same data
but with dispersions of all genes shown. MAP, maximum a posteriori; MLE, maximum-likelihood estimate.
variation to the extent that the data provide this informa-
tion, while the fitted curve aids estimation and testing in
less information-rich settings.
Our approach is similar to the one used by DSS [6],
in that both methods sequentially estimate a prior dis-
tribution for the true dispersion values around the fit,
an

_(truncated)_

