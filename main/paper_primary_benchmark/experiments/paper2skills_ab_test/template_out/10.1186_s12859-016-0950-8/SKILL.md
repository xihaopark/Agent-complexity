---
name: paper-10-1186_s12859-016-0950-8
description: >-
  Extracted notes from 10.1186_s12859-016-0950-8.pdf
---

# Paper-derived skill

## Extracted text (first pages)

```
SOFTWARE
Open Access
MethPat: a tool for the analysis and
visualisation of complex methylation
patterns obtained by massively parallel
sequencing
Nicholas C. Wong1,2,3,14*
, Bernard J. Pope4,5*, Ida L. Candiloro6, Darren Korbie7, Matt Trau7,8, Stephen Q. Wong9,15,
Thomas Mikeska1,13, Xinmin Zhang10, Mark Pitman11, Stefanie Eggers2, Stephen R. Doyle12
and Alexander Dobrovic1,6,13*
Abstract
Background: DNA methylation at a gene promoter region has the potential to regulate gene transcription.
Patterns of methylation over multiple CpG sites in a region are often complex and cell type specific, with the
region showing multiple allelic patterns in a sample. This complexity is commonly obscured when DNA
methylation data is summarised as an average percentage value for each CpG site (or aggregated across CpG
sites). True representation of methylation patterns can only be fully characterised by clonal analysis. Deep
sequencing provides the ability to investigate clonal DNA methylation patterns in unprecedented detail and
scale, enabling the proper characterisation of the heterogeneity of methylation patterns. However, the sheer
amount and complexity of sequencing data requires new synoptic approaches to visualise the distribution of
allelic patterns.
Results: We have developed a new analysis and visualisation software tool “Methpat”, that extracts and displays
clonal DNA methylation patterns from massively parallel sequencing data aligned using Bismark. Methpat was
used to analyse multiplex bisulfite amplicon sequencing on a range of CpG island targets across a panel of
human cell lines and primary tissues. Methpat was able to represent the clonal diversity of epialleles analysed at
specific gene promoter regions. We also used Methpat to describe epiallelic DNA methylation within the
mitochondrial genome.
Conclusions: Methpat can summarise and visualise epiallelic DNA methylation results from targeted amplicon,
massively parallel sequencing of bisulfite converted DNA in a compact and interpretable format. Unlike
currently available tools, Methpat can visualise the diversity of epiallelic DNA methylation patterns in a sample.
Keywords: DNA methylation, software, visualization, bisulfite, targeted amplicon, epigenetics, epiallele
* Correspondence: nwon@unimelb.edu.au; bjpope@unimelb.edu.au;
alex.dobrovic@onjcri.org.au
1Translational Genomics and Epigenomics Laboratory, Olivia Newton-John
Cancer Research Institute, Heidelberg, Victoria 3084, Australia
4Victorian Life Sciences Computation Initiative (VLSCI), The University of
Melbourne, Parkville, Victoria 3052, Australia
Full list of author information is available at the end of the article
© 2016 Wong et al. Open Access This article is distributed under the terms of the Creative Commons Attribution 4.0
International License (http://creativecommons.org/licenses/by/4.0/), which permits unrestricted use, distribution, and
reproduction in any medium, provided you give appropriate credit to the original author(s) and the source, provide a link to
the Creative Commons license, and indicate if changes were made. The Creative Commons Public Domain Dedication waiver
(http://creativecommons.org/publicdomain/zero/1.0/) applies to the data made available in this article, unless otherwise stated.
Wong et al. BMC Bioinformatics  (2016) 17:98 
DOI 10.1186/s12859-016-0950-8

Background
In mammals, the predominant and most widely studied
DNA methylation mark occurs at CpG dinucleotide
(CpG) palindromic sequences [1]. The vast majority of
methods that investigate DNA methylation utilise bisul-
fite treatment of genomic DNA followed by PCR ampli-
fication to distinguish methylated from unmethylated
CpG
sites
[2–5].
Bisulfite
treatment
discriminates
methylated from unmethylated cytosines by selectively
reacting with unmethylated cytosines to generate uracil.
During the subsequent first step of PCR amplification,
the uracils are read as thymine. Conversely, methylated
cytosines do not react with the bisulfite reagent and
remain as cytosines after PCR amplification [6]. DNA
methylation readouts at single sites employing bisulfite
conversion become analogous to genotyping assays by
detecting either a cytosine or thymidine at the C position
of a CpG site and are interpreted as methylated or
unmethylated cytosines respectively.
An epiallele refers to a distinct pattern of methyla-
tion, typically over a short genomic region [7, 8]. In
addition to the methylation state given for each CpG
site, the pattern of DNA methylation of all CpG
sites across the epiallelic or clonal template can also
be characterised [7]. Indeed, in terms of biological
function, CpG methylation should be often considered
in
an
allelic
fashion
over
multiple
adjacent
CpG
sites [9, 10].
However, currently most studies summarise data into
average percentage values at each CpG site thus losing
the positional pattern information of DNA methylation
across each clonal template [9]. Analysis platforms such
as the Illumina Infinium BeadArray [11], bisulfite pyro-
sequencing [12] and SEQUENOM™EpiTYPER™[13]
use bisulfite mediated chemistry to discriminate the
methylation state of CpG sites but summarise mea-
surements into percentage values across each CpG
site or region of interest. Percentage methylation de-
scribed in most DNA methylation studies hides im-
portant pattern and positional information of DNA
methylation with potential functional and regulatory
relevance [7]. It is only with clonal sequencing ap-
proaches [1, 14, 15], whole genome bisulfite sequencing
[16] or reduced representation bisulfite sequencing
[17], that the methylation state of individual CpG
sites within a genomic DNA template can be readily
measured in a digital sense, as methylated or not,
allele by allele.
Imprinted regions of the genome such as IGF2/H19
and MEST typically display two epialleles, where one is
completely methylated and the other is unmethylated.
The loss of imprinting at such loci leads to syndromic
complications [18, 19]. Average DNA methylation across
these loci are typically presented as 50 % methylation
but the pattern of DNA methylation at each epiallele is
lost [7].
Heterogeneous
DNA
methylation
describes
the
phenomenon where different contiguous CpG sites
have different levels of methylation. DNA methylation
heterogeneity can arise in a variety of ways including
but not limited to: (i) more than a single population of
cells is analysed that differ in DNA methylation at the
locus of interest, (ii) the locus of interest is imprinted
i.e. two different epialleles are present in each cell or,
(iii) the locus is inherently heterogeneous in its DNA
methylation composition. It is only using clonal se-
quencing approaches with allelic outputs, high reso-
lution melting (HRM) [7, 20], or a novel ligation
mediated
approach
[10] that heterogeneous
DNA
methylation can be detected. It is also inferred by
varying methylation at CpG sites e.g. from Pyrose-
quencing. Importantly, the number of methylated
alleles can be substantially underestimated unless
clonal approaches are used [20]. Clonal sequencing
is currently the best method to investigate heteroge-
neous DNA methylation and the extent of epiallelic
methylation
patterns
that
exist
within
a
single
sample [15].
Until recently, it has been cost prohibitive to assess the
complexity of methylation patterns, as large number of
clones need to be individually sequenced to determine the
extent of heterogeneous DNA methylation. As one clone
represents a single epiallele, many tens to hundreds of
clones need to be sequenced to gain a true representation
of different epialleles in a sample. The introduction of
massively parallel sequencing enables the sequencing of
many thousands of DNA templates from multiple regions
simultaneously providing a true representation of the di-
versity and extent of heterogeneous DNA methylation
patterns derived from a given sample. However, as the
number of clones sequenced increases, the ability to
analyse and present this type of data then becomes a
significant challenge, and at this time, there are very
few software tools available to manage such data from
massively parallel sequencing experiments [21, 22].
Some visualisation and analysis tools are available for
Bisulfite Sanger Sequencing including BiQ Analyzer
[23],
MethVisual
[24],
QUMA
[25],
BISMA
[26].
However, these tools do not scale up with massively
parallel sequencing having been designed for Sanger
sequencing. BiQ Analyser HiMod is a tool that en-
ables visualisation of high throughput sequencing of
5-methylcytosine and other methyl-variant modifica-
tions [27] however, results are expressed in percent-
age methylation values masking allelic methylation
patterns.
In this study, we have developed Methpat, a software
tool which processes bisulfite sequencing data following
Wong et al. BMC Bioinformatics  (2016) 17:98 
Page 2 of 14

Bismark alignment [28] and summarises DNA methyla-
tion according to epiallelic methylation patterns. This
software has been used to analyse multiplex bisulfite
amplicon PCR coupled to massively parallel deep se-
quencing on a range of primary haematopoietic tissue
samples and model cancer cell lines to observe the
extent of heterogeneous DNA methylation. Methpat is
also able to create publication-ready, compact visualisa-
tions of the summarised data showing heterogeneous
DNA methylation patterns in a space efficient and
comprehensible manner.
Materials, methods and implementation
Samples, library preparation, sequencing and sequence
alignment. Details of sample preparation, library gener-
ation, sequencing and sequence alignment protocol
employed are summarised in the Additional file 1.
Human samples used in this study were approved for
Table 1 Mapping statistics of bisulfite amplicon libraries
Sample
Mapping Efficiency
Unique Hits
Methylated CpG
Methylated CHG
Methylated CHH
Total C’s analysed
293
52.2 %
7539
64.9 %
0.2 %
0.3 %
316211
40424
55.3 %
9414
37.5 %
0.2 %
0.2 %
351086
910046
42.0 %
7060
32.6 %
0.2 %
0.3 %
299795
12a-cd19
14.9 %
48648
47.9 %
0.4 %
0.5 %
1933767
12a-cd34
30.3 %
85049
36.5 %
0.1 %
0.2 %
3703147
12a-cd45
32.4 %
109173
32.6 %
0.1 %
0.2 %
4714744
12acd33
36.2 %
161885
32.8 %
0.2 %
0.2 %
6997070
6-mda453
54.6 %
201660
84.4 %
0.8 %
1.3 %
9179816
6c-cd19
7.9 %
22258
77.8 %
0.2 %
0.3 %
777739
6c-cd33
27.9 %
20071
35.2 %
0.2 %
0.2 %
851116
6c-cd34
19.5 %
36928
49.7 %
0.2 %
0.2 %
1628107
6ccd45
33.0 %
31087
39.5 %
0.1 %
0.2 %
1314281
9a-cd19
21.2 %
39352
48.7 %
0.2 %
0.3 %
1638757
9a-cd33
31.9 %
125884
35.8 %
0.2 %
0.2 %
5459419
9a-cd34
26.2 %
77870
43.4 %
0.2 %
0.2 %
3321993
9a-cd45
46.6 %
28085
29.8 %
0.2 %
0.2 %
1211803
9awholeblood
31.5 %
97532
30.8 %
0.2 %
0.2 %
4081834
brl
49.3 %
9107
32.7 %
0.2 %
0.4 %
398977
caco
19.6 %
129536
78.1 %
0.2 %
0.2 %
4512574
dg75
51.7 %
10827
57.2 %
0.3 %
0.3 %
489096
ekvx
23.0 %
115915
63.1 %
0.2 %
0.2 %
4494359
hela
43.1 %
41650
55.9 %
0.2 %
0.2 %
1731811
hepg2
39.2 %
24667
63.4 %
0.3 %
0.3 %
971693
ht1080
40.7 %
4586
67.0 %
0.2 %
0.4 %
176188
htb22-col
30.9 %
45576
79.9 %
0.2 %
0.2 %
1863098
jwl
31.3 %
18814
42.7 %
0.2 %
0.2 %
771188
k562
49.7 %
144791
55.9 %
0.3 %
0.3 %
6230391
ls174t
41.2 %
3691
57.2 %
0.2 %
0.3 %
151722
mcf7
30.0 %
87404
71.6 %
0.8 %
0.8 %
3786412
mda-mb231-bag
29.0 %
94811
77.3 %
1.0 %
1.1 %
4171147
nalm6
43.6 %
37669
85.8 %
0.2 %
0.2 %
1569041
nccit
44.0 %
31656
45.7 %
0.4 %
0.3 %
1406165
ovcar8
32.3 %
46864
63.4 %
0.3 %
0.3 %
1917527
sknas
21.6 %
275040
27.7 %
0.1 %
0.2 %
11313285
u231
14.0 %
123302
74.8 %
0.4 %
0.2 %
4389352
Wong et al. BMC Bioinformatics  (2016) 17:98 
Page 3 of 14

Fig. 1 (See legend on next page.)
Wong et al. BMC Bioinformatics  (2016) 17:98 
Page 4 of 14

research by The Royal Children’s Hospital Human
Research Ethics Committee (RCH HREC#27138E).
Methpat—a tool to summarise epiallelic DNA methy-
lation patterns
We have developed the software tool,
Methpat to summarise and visualise the resultant epial-
l

_(truncated)_

