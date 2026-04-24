# Type C — paper-derived domain SKILL

Built by `evaluation/scripts/build_paper_type_a_blueprint.py` (SKILL.md merge + optional PDF excerpts). **Not** the Type A workflow playbook. Inject via `skill_blueprint_experiment.py --skill-file … --skill-role paper_domain`.

---

## cdisc_papers/SKILL.md

# cdisc_papers

Reusable Python functions for working with CDISC-aligned clinical research data.

| Topic | Description |
|---|---|
| [cdisc_sdtm](cdisc_sdtm/) | SDTM-oriented data transformations and utilities |
| [cdisc_odm](cdisc_odm/) | ODM XML parsing and flattening helpers |


## cdisc_papers/cdisc_odm/SKILL.md

# cdisc_odm

Utilities for working with CDISC Operational Data Model (ODM) XML exports, focusing on practical flattening and light metadata extraction for downstream analysis in pandas.

| Module | Function(s) | Docs | Description |
|---|---|---|---|
| `clinicaldata_long.py` | `odm_clinicaldata_to_long` | [docs](docs/clinicaldata_long.md) | Flatten ODM ClinicalData (ItemData) to long form |
| `metadata_tables.py` | `odm_metadata_to_tables` | [docs](docs/metadata_tables.md) | Extract common MetaDataVersion definitions to tables |


## cdisc_papers/cdisc_sdtm/SKILL.md

# cdisc_sdtm

Helpers for common transformations when working with CDISC Study Data Tabulation Model (SDTM)-style datasets.

| Module | Function(s) | Docs | Description |
|---|---|---|---|
| `findings_long.py` | `pivot_to_sdtm_findings_long` | [docs](docs/findings_long.md) | Pivot wide CRF items into SDTM Findings-like long form |


---

# Paper text excerpts (truncated)

## A use-case analysis of CDISC:SDTM in academia in an investigator-initiated clinical trial.pdf

```
120
ORIGINAL PAPER
Nagoya J. Med. Sci. 84. 120–132, 2022
doi:10.18999/nagjms.84.1.120
A use-case analysis of Clinical Data Interchange Standards 
Consortium/Study Data Tabulation Model in academia  
in an investigator-initiated clinical trial
Shizuko Takahara1,2, Toshiki I. Saito3, Yasuhito Imai1, Takahiro Kawakami4 
and Toshinori Murayama1,2
1Innovative Clinical Research Center, Kanazawa University, Kanazawa, Japan 
2Clinical Development, Graduate School of Medical Sciences, Kanazawa University, Kanazawa, Japan 
3Clinical Research Center, National Hospital Organization Nagoya Medical Center, Nagoya, Japan 
4G-link System Consulting K.K., Tokyo, Japan
ABSTRACT
Submitting data compliant with the Clinical Data Interchange Standards Consortium (CDISC) standards 
is mandatory for new drug applications (NDAs). The standards set by CDISC are widely adopted in the 
pharmaceutical business world. Introduction of CDISC standards in academia can be necessary to reduce 
labor, resolve the shortage of data managers in academia, and gain new knowledge through standardized 
data accumulation. However, the introduction of CDISC standards has not progressed in communities 
within the academia that do not apply for NDAs. Therefore, herein, we created study data tabulation 
model (SDTM)-compliant datasets within the academia, without outsourcing, to reduce costs associated 
with investigator-initiated clinical trials. First, we input data from paper case report forms (CRFs) into an 
electronic data capture system with minimal function for paper CRFs, “Ptosh,” which is compatible with 
SDTM. Then, we developed a generic program to convert data exported from Ptosh into fully SDTM-
compliant datasets. The consistency was then verified with an SDTM validator, Pinnacle21 Community 
V3.0.1 (P21C). This resulted in generation of SDTM datasets, resolving all “Rejects” in P21C, thereby 
achieving the required quality level. Although Ptosh directly exports data in SDTM format, manual mapping 
of items on CRFs to SDTM variables prepared in Ptosh is necessary. SDTM mapping requires extensive 
knowledge and skills, and it was assumed that mapping is challenging for the staff without in-depth 
knowledge of CDISC standards and datasets. Therefore, for CDISC dissemination in academia, it is crucial 
to secure the staff, time, and funding to acquire the knowledge.
Keywords: CDISC, SDTM, investigator-initiated clinical trial, clinical data management, academia
Abbreviations:
ALL-RET trial: a phase I/II, open-label, single-arm study of CH5424802 for patients with advanced 
non-small-cell lung cancer harboring a RET fusion gene
CDISC: Clinical Data Interchange Standards Consortium
CDMS: clinical data management system
CRF: case report form
EDC: electronic data capture
NDA: new drug application
Received: February 10, 2020; accepted: June 8, 2021 
Corresponding Author: Shizuko Takahara, MA 
Innovative Clinical Research Center, Kanazawa University ; Clinical Development, Graduate School of  
Medical Sciences, Kanazawa University, 13-1 Takara-machi, Kanazawa 920-8641, Japan 
Tel: +81-76-265-2879, Fax: +81-76-234-4338, E-mail: takahara_shizuko@staff.kanazawa-u.ac.jp


Nagoya J. Med. Sci. 84. 120–132, 2022
doi:10.18999/nagjms.84.1.120
121
Use-case study of CDISC/SDTM in academia
P21C: Pinnacle21 Community V3.0.1
PMDA: Pharmaceuticals and Medical Devices Agency
RECIST: response evaluation criteria in solid tumors
SDTM: Study Data Tabulation Model
This is an Open Access article distributed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International 
License. To view the details of this license, please visit (http://creativecommons.org/licenses/by-nc-nd/4.0/).
INTRODUCTION
In Japan, the Ministry of Health, Labour and Welfare, Pharmaceutical and Food Safety Bureau 
Director published Notification No. 0620-6 “Basic Principles on Electronic Submission of Study 
Data for New Drug Applications” in 2014. From October 2016, submission of electronic data 
that conforms to the Clinical Data Interchange Standards Consortium (CDISC) standards, which 
are the global standards for clinical trial data, is required for new drug applications (NDAs).1-3 
Currently, the CDISC/Study Data Tabulation Model (SDTM), which is the raw data for each 
study, and CDISC/Analysis Data Model, which is the dataset processed for analysis but not 
mentioned in this work, often tend to be submitted to the Pharmaceuticals and Medical Devices 
Agency (PMDA) for NDAs.2 The CDISC/SDTM defines a standard structure for clinical trial data 
tabulations. Each of these tables is called a domain. For example, data on subject demographics 
are assigned to the domain coded as “DM.” Domains are defined for subject demographics, 
laboratory data, vital signs, adverse events and so on, according to the attributes of the dataset. 
Usually, clinical trial data are acquired and mapped to the SDTM variables as part of the data 
management process. Each domain code, variable name, variable order, and display format is 
defined in detail in the SDTM Implementation Guide.4 When receiving CDISC standard data, 
the PMDA uses software called Pinnacle21 Enterprise (P21C) to validate whether the data were 
created according to the rules of the CDISC standard.5 
Overseas, in the United States of America, the Food and Drug Administration requires the 
submission of CDISC data6; in China, CDISC standards are now the preferred standards for 
electronic data submission.6 European and South Korean authorities are considering adopting 
these standards.7 Thus, the submission of CDISC data for NDAs is becoming a standard. 
CDISC standards have spread rapidly in the Japanese pharmaceutical industry. As of October 31, 
2019, 302 consultations have been submitted for electronic data submission by the PMDA, and 
electronic application data have already been submitted for 94 product applications.8
Originally, CDISC standards were not meant for NDAs. CDISC states that accessibility, 
interoperability, and reusability of data enable more meaningful and efficient research that has a 
greater impact on global health.9 Barrie Nelson, vice president of CDISC, quotes “The benefits of 
implementing CDISC standards in research studies are numerous -- fostered efficiency, enhanced 
innovation, increased predictability, complete traceability, improved data quality, reduced costs, and 
streamlined processes -- all ensuring the integrity of your data from end to end”.10 The CDISC 
standards will promote the standardization of operations, leading to laborsaving and high-quality 
trial operations. The standards will also enable meta-analysis of accumulated, standardized data, 
leading to advancements in medicine. PMDA not only requires CDISC data for regulatory review 
but also envisions the use of accumulated, standardized data.11 These benefits are not only for 
pharmaceutical companies but also for academia. Further, the Japan Agency for Medical Research 
and Development (AMED) states that investigator-initiated clinical trials will need to comply with 
CDISC standards from the planning and implementation stages, and they expect that the clinical 
trials contracted with them will be performed according to CDISC standards.12


Nagoya J. Med. Sci. 84. 120–132, 2022
doi:10.18999/nagjms.84.1.120
122
Shizuko Takahara et al
In academia, unlike in pharmaceutical companies, clinical trial protocols are created by 
investigators. In a pharmaceutical company, a description of items to be captured is usually 
standardized. For instance, the number of white blood cells will be denoted as “WBC” even if 
companies have different protocols. However, because each clinical trial protocol within a single 
university is created by a different principal investigator, an item will be denoted in different 
ways in each protocol, such as “White Blood Cell,” “WBC,” or “Leukocytes.” This leads to 
different nomenclatures and database structures for clinical trial data. This will increase data 
management labor, and meta-analysis using multiple datasets from different clinical trials will be 
more difficult. Therefore, the introduction of CDISC standards will help resolve these problems.13 
Although there are good reasons to introduce CDISC standards in academia, the standardiza-
tion is not widespread, at least in Japanese academia. One of the reasons being insufficient 
research funding,14 not only for hiring staff but also to cover the expenses of implementing 
the required information technology (IT) system and the associated staff education. Therefore, 
human resources, such as data managers, are limited, and the daily workload is overwhelming, 
which implies that the scope to exceed the necessary minimum work is limited. Furthermore, 
conditions of employment within academia makes it difficult to hire people with expertise.15 
In addition, because most of the data management staff are employed by hospitals, priority is 
given to those with medical licenses, in contrast to those with IT knowledge. The use of CDISC 
standards is not mandatory in investigator-initiated trials that are not used for NDAs. These trials 
are considered to be the reason for the delayed introduction of CDISC standards in academia.
Therefore, we assessed whether fully SDTM-compliant datasets can be generated within 
academia without outsourcing the task to contract research organizations in an investigator-initiated 
clinical trial in the field of oncology and clarified adequate methods and problems.
METHODS
The investigator-initiated clinical trial “A phase I/II, open-label, single-arm study of CH5424802 
for patients with advanced non-small-cell lung cancer harboring a RET fusion gene” (University 
Hospital Medical Information Network (UMIN) ID: UMIN000020628) (hereinafter referred to as 
the “ALL-RET trial”)16 was the target of this study (hereinafter referred to as “CDISC-study”). 
The CDISC-study is neither an activity through understanding the cause of d

… [truncated]
```

## Current Applications and Future Directions for the CDISC Operational Data Model Standard- A Methodological Review

```
Methodological Review
Current applications and future directions for the CDISC Operational
Data Model standard: A methodological review
Sam Hume a,⇑, Jozef Aerts b, Surendra Sarnikar a, Vojtech Huser c
a Dakota State University, College of Business and Information Systems, 820 N Washington Ave, Madison, SD 57042, United States
b FH Joanneum University of Applied Sciences, Eggenberger Allee 11, 8020 Graz, Austria
c Lister Hill National Center for Biomedical Communications, National Library of Medicine, National Institutes of Health, 8600 Rockville Pike, Bld 38a, Rm 9N919,
Bethesda, MD 20894, United States
a r t i c l e
i n f o
Article history:
Received 1 May 2015
Revised 21 February 2016
Accepted 22 February 2016
Available online 2 March 2016
Keywords:
ODM
Deﬁne-XML
CDISC
Interoperability
Clinical trial
EHR
a b s t r a c t
Introduction: In order to further advance research and development on the Clinical Data Interchange
Standards Consortium (CDISC) Operational Data Model (ODM) standard, the existing research must be
well understood. This paper presents a methodological review of the ODM literature. Speciﬁcally, it
develops a classiﬁcation schema to categorize the ODM literature according to how the standard has been
applied within the clinical research data lifecycle. This paper suggests areas for future research and devel-
opment that address ODM’s limitations and capitalize on its strengths to support new trends in clinical
research informatics.
Methods: A systematic scan of the following databases was performed: (1) ABI/Inform, (2) ACM Digital,
(3) AIS eLibrary, (4) Europe Central PubMed, (5) Google Scholar, (5) IEEE Xplore, (7) PubMed, and (8)
ScienceDirect. A Web of Science citation analysis was also performed. The search term used on all data-
bases was ‘‘CDISC ODM.” The two primary inclusion criteria were: (1) the research must examine the use
of ODM as an information system solution component, or (2) the research must critically evaluate ODM
against a stated solution usage scenario. Out of 2686 articles identiﬁed, 266 were included in a title level
review, resulting in 183 articles. An abstract review followed, resulting in 121 remaining articles; and
after a full text scan 69 articles met the inclusion criteria.
Results: As the demand for interoperability has increased, ODM has shown remarkable ﬂexibility and has
been extended to cover a broad range of data and metadata requirements that reach well beyond ODM’s
original use cases. This ﬂexibility has yielded research literature that covers a diverse array of topic areas.
A classiﬁcation schema reﬂecting the use of ODM within the clinical research data lifecycle was created to
provide a categorized and consolidated view of the ODM literature. The elements of the framework
include: (1) EDC (Electronic Data Capture) and EHR (Electronic Health Record) infrastructure; (2) plan-
ning; (3) data collection; (4) data tabulations and analysis; and (5) study archival. The analysis reviews
the strengths and limitations of ODM as a solution component within each section of the classiﬁcation
schema. This paper also identiﬁes opportunities for future ODM research and development, including
improved mechanisms for semantic alignment with external terminologies, better representation of
the CDISC standards used end-to-end across the clinical research data lifecycle, improved support for
real-time data exchange, the use of EHRs for research, and the inclusion of a complete study design.
Conclusions: ODM is being used in ways not originally anticipated, and covers a diverse array of use cases
across the clinical research data lifecycle. ODM has been used as much as a study metadata standard as it
has for data exchange. A signiﬁcant portion of the literature addresses integrating EHR and clinical
research data. The simplicity and readability of ODM has likely contributed to its success and broad
implementation as a data and metadata standard. Keeping the core ODM model focused on the most fun-
damental use cases, while using extensions to handle edge cases, has kept the standard easy for develop-
ers to learn and use.
 2016 Elsevier Inc. All rights reserved.
http://dx.doi.org/10.1016/j.jbi.2016.02.016
1532-0464/ 2016 Elsevier Inc. All rights reserved.
⇑Corresponding author. Tel.: +1 484 354 0873.
E-mail addresses: swhume@gmail.com (S. Hume), jozef.aerts@fh-joanneum.at (J. Aerts), surendra.sarnikar@dsu.edu (S. Sarnikar), vojtech.huser@nih.gov (V. Huser).
Journal of Biomedical Informatics 60 (2016) 352–362
Contents lists available at ScienceDirect
Journal of Biomedical Informatics
journal homepage: www.elsevier.com/locate/yjbin


1. Introduction
Clinical research is essential for advancing medicine and
improving patient quality of life. The expansive scope of clinical
research combined with the pervasiveness of technology has given
rise to increasing volumes of data, and strategies are needed to
process and exchange it effectively. As clinical trials continue to
grow in complexity, systematic mechanisms to collect, process,
analyze, and integrate data across systems and organizational
boundaries have become increasingly important. Clinical research
can no longer be considered an isolated venture and is increasingly
conducted in network structures where seamless data exchange is
critical to operational efﬁciency and effectiveness. Clinical data
standards improve the efﬁciency and quality of clinical research
and more broadly of healthcare delivery in general.
Within the realm of healthcare informatics there exists a broad
array of data standards that meet a variety of needs. The Clinical
Data Interchange Standards Consortium (CDISC) creates data stan-
dards for clinical research that complement, and in a growing
number of cases, interact with a variety of healthcare standards.
The CDISC Operational Data Model (ODM) standard is a document
and exchange standard created speciﬁcally to support the needs of
clinical research.
The ODM standard [1] plays a key role in clinical research infor-
matics, including areas such as data exchange, archival, U.S. Food
and Drug Administration (FDA) submission, and interoperability
with healthcare data. Within the highly data-centric domain of
clinical research, the XML-based ODM is the standard exchange
format for case report form (CRF) data and metadata [2]. Interest
in ODM as a research topic has grown signiﬁcantly over the last
several years with increasing interest in the CDISC data standards
from regulatory authorities such as the FDA [3,4] and the Japanese
Pharmaceutical and Medical Devices Agency (PMDA), as well as
from the considerable resources being allocated to healthcare data
interoperability [5,6]. The FDA has stated that, ‘‘improving the efﬁ-
ciency and effectiveness of medical product development is a
national priority” [7]. Regulatory electronic submissions have
grown more complex with the average submission now a stagger-
ing 3.4 million pages, an increase of 1423% since 2005 [8]. With
this scale, inefﬁciencies in the clinical research data lifecycle add
signiﬁcant time and expense to new medical product development.
Increasing efﬁciency requires that the networked organizations
participating in clinical development exchange data seamlessly.
The 2014 CDISC business case claims that using CDISC standards
from the beginning of the process can save approximately $180
million per submission [1].
The ODM standard was originally published for review as v0.8
in early 2000, and at that time was called the CDISC DAIS (Data
Acquisition and Interchange Standard) model. The original objec-
tive when work started in 1999 was to address the data inter-
change and study archival use cases. Kubick et al. [9] described
ODM as established to support the essential information needs of
electronic data capture (EDC) systems and paper CRF data entry
systems. Other key requirements included a 21 CFR Part 11 compli-
ant audit trail, and long-term data archival support [10].
ODM was not originally developed based on an existing clinical
research or healthcare data model, but instead was designed using
a bottom-up approach to meet the established data interchange,
archival, and audit trail requirements. The initial focus was on a
general, vendor neutral structure and syntax; industry level data
models and semantics were given little consideration. For example,
an effort was made to align ODM with the Biomedical Research
Integrated Domain Group (BRIDG) model, but this was long after
ODM was originally published. In another example, converting
openEHR’s Archetype Deﬁnition Language (ADL) to ODM has been
demonstrated [11], but has not been a consideration in ODM’s
requirements. ODM was designed in relative isolation to meet
the needs of the CDISC community, and ODM’s relationship to clin-
ical research data models has come from usage rather than from an
explicit effort to design or generate the XML from an existing
model.
The ﬁrst production version of ODM was published in October
2000 and was demonstrated in two Connectathon events in 2001
[12]. The current ODM version, v1.3.2, was published in December
of 2013. ODM, now based on XML schema, remains under active
development by the CDISC XML Technologies Team, and while
the original ODM requirements remain highly relevant, use of the
standard has extended well beyond the original design.
In response to increasing demands for interoperability, ODM
has been extended over the years to cover a broad range of data
and metadata needs [13]. This versatility has yielded research liter-
ature that reﬂects a diverse array of topic areas. The base ODM
standard itself can be used to address a number of use cases, but
standardized extensions have also been published including: (1)
Deﬁne-XML for dataset metadata [14], (2) Dataset-XML for dataset
data [15], (3) SDM-XML for Study Design Model [16], (4) CT-XML
for Controlled Terminology [17], and (5) Analysis Results Metadata
[18] for Deﬁne-XML v2. Fig. 1 highlights 

… [truncated]
```

## Visualizing and Validating Metadata Traceability within the CDISC Standards.pdf

```
 
 
Visualizing and Validating Metadata Traceability within the CDISC 
Standards  
Sam Hume, MS1, Surendra Sarnikar, PhD2, Lauren Becnel, PhD3, Dorine Bennett, EdD1 
1Dakota State University, Madison, SD; 2California State University, East Bay, Hayward, 
CA; 3Clinical Data Interchange Standards Consortium, Austin, TX 
Abstract 
The Food & Drug Administration has begun requiring that electronic submissions of regulated clinical studies 
utilize the Clinical Data Information Standards Consortium data standards. Within regulated clinical research, 
traceability is a requirement and indicates that the analysis results can be traced back to the original source data. 
Current solutions for clinical research data traceability are limited in terms of querying, validation and 
visualization capabilities.  This paper describes (1) the development of metadata models to support computable 
traceability and traceability visualizations that are compatible with industry data standards for the regulated 
clinical research domain, (2) adaptation of graph traversal algorithms to make them capable of identifying 
traceability gaps and validating traceability across the clinical research data lifecycle, and (3) development of a 
traceability query capability for retrieval and visualization of traceability information.  
Introduction 
Traceability plays a critical role in supporting clinical research analysis results because the strength of the study 
results depend on the source data and the quality and reproducibility of the processes used1. From a regulatory 
perspective the US Food and Drug Administration (FDA) has stated that the results presented in a Clinical Study 
Report (CSR) must be traceable back to the original data elements2 to preserve an unbroken chain of data from its 
source to the point of consumption. Traceability helps the regulatory reviewer to understand “the relationships 
between the analysis results, analysis datasets, tabulation datasets, and source data3”.  
 
Despite the importance of traceability requirements for regulated clinical research, the ability to easily trace data 
back to its source remains limited. The FDA has identified a lack of traceability as one of the top seven data 
standards issues4, and it has been cited as a key to the FDA’s ability to successfully review submission data5.  
“Messy data” that is difficult to understand can delay the FDA’s ability to complete the review of a New Drug 
Application6 potentially delaying the availability of an important new treatment.  
 
The technology available to support the systematic review of submission datasets has limited support for assessing 
traceability7. Today, no tools exist capable of tracing a data element from the protocol through to the CSR tables, 
listings, and figures8. Current federal regulations, such as 21 CFR Part 119, describe traceability needs, but do not 
prescribe how traceability should be achieved. The current lack of traceability may impede efficient and fully 
transparent decision making7. 
 
The Clinical Data Information Standards Consortium (CDISC) Operational Data Model v1.3.2 (ODM-XML) and 
Define-XML v2.0 standards provide the models that represent the metadata for data artifacts such as case report 
forms (CRFs) and datasets created for use in clinical research. These standards also contain detailed metadata 
describing data elements, controlled terminology, and the methods used for derivations and transformations of the 
data. Define-XML is currently required as part of a standards-compliant regulatory submission10 to the FDA or 
Japanese Pharmaceutical and Medical Devices Agency (PMDA) and plays a key role in establishing traceability for 
the submission datasets. 
 
Two fundamental limitations hinder traceability effectiveness in today’s solutions: (1) gaps exist in the computable 
traceability provided by the CDISC standard metadata models, for example the existing traceability metadata is 
descriptive and does not explicitly reference the available source variable metadata; and (2) the metadata gaps 
prevent full data lifecycle traceability validation and visualization, for example there is no automated way to query 
158


 
the traceability of a given analysis variable back to the source data. These limitations are a significant hindrance to 
the in-depth and thorough analysis of  available evidence in the regulatory decision making process7. 
 
Despite considerable existing research on provenance and traceability, determining the appropriate analytic 
capabilities and query mechanisms to answer traceability questions remains an open research opportunity11, 12.  
In order to address these limitations, this paper presents a framework for clinical research data traceability named 
Trace-XML that (1) includes a new extensible markup language (XML) extension compatible with the existing 
CDISC Define-XML industry standard for clinical research metadata, and (2) proposes new algorithms that identify 
the traceability gaps and validate full life-cycle traceability within a clinical study.  Using the design science 
research (DSR) methodology13, 14 Trace-XML enables standardized clinical study metadata to be represented as a 
graph displaying the full, interconnected history of each data element. Here, we describe the program and how its 
graph-based representation of the traceability metadata found in CDISC standard Define-XML and ODM-XML files 
enables detailed, granular traces through the clinical research data lifecycle.  
 
The research objectives addressed in this paper include: (1) development of metadata models to support computable 
traceability and traceability visualizations that are compatible with industry data standards for the regulated clinical 
research domain, (2) adaptation of graph traversal algorithms to make them capable of identifying traceability gaps 
and validating traceability across the clinical research data lifecycle, and (3) development of a traceability query 
capability for retrieval and visualization of traceability information.  
Methods 
Trace-XML Development, Testing and Validation. Following the design science research methodology build and 
evaluate cycles15, a prototype software application was developed in Java to implement Trace-XML including the 
creation of the traceability graph and the algorithms for querying and validating traceability. JDOM 2 was used to 
process the XML in the Java application. The BaseX 8.5.2 XML database engine XQuery 3.1 processor was used to 
implement the traceability query tool. The Define-XML extension was implemented in XML schema. The 
traceability graph is represented using the GraphML v1.0 schema. The Trace-XML prototype discussed in this paper 
rendered GraphML for two open-source graph visualization and editing tools: yEd v3.1.6 and Gephi v0.9.1.  
 
The development of the Trace-XML application provides “proof-by-demonstration” of the theoretical foundations of 
the artifacts developed for this research project16. The scientific evaluation of artifacts is the essence of information 
systems as design science research17. In addition to testing the artifact, analytical methods have been used as the 
primary means of evaluation. The analytical evaluation proves that reachability, traceability, and completeness are 
demonstrated within Trace-XML through the application of graph theory and specific traversal algorithms. 
 
Trace-XML Framework. The Trace-XML framework consists of 3 layers: (1) the Information Product Map (IP-
MAP) model: a high-level view of the manufacturing process for creating an information product (IP); (2) the CDISC 
standards metadata: metadata describing the IPs, data elements, and computations at a detailed level of granularity; 
and (3) a graph model: traceability throughout the clinical research data lifecycle that supports traceability 
visualization, validation, and queries. Layer 1 applies the IP-MAP research to use IPs to represent computable 
traceability within clinical research data at a higher level of abstraction. Layer 2 represents the detailed study metadata 
provided by the ODM-XML and Define-XML files. This detailed study metadata maps into the higher-level IP-MAP 
representation found in Layer 1 of the framework. Layer 3 includes the algorithms that generate the graph, identify 
any traceability gaps, and validate the completed graph. Generating the graph for Layer 3 uncovered traceability gaps 
in the CDISC standards metadata in Layer 2. Trace-XML addresses these traceability gaps through the development 
of an extension to the Define-XML standard.  
Accessibility and License.  The system documentation and instructions on accessing the software will be made 
available at http://www.cdisc.org. The software will be released under the Apache License, version 2.0. 
Results 
In this research the CDISC standards provide the domain models and metadata for the data element level 
traceability, and this benefits users as these semantics are known within the regulated clinical research domain. 
However, computable traceability across the clinical research lifecycle is not possible using the CDISC standards 
because the traceability metadata provided in the Origin element provides only descriptive metadata used to identify 
the prior step in the process. Therefore, a Trace-XML extension to Define-XML was developed to include specific 
159


 
references to source variables found in a study’s Define-XML and ODM-XML files.  The new Source and 
SourceItem elements (Figure 1) containing the source variable references are identified using the trc namespace 
prefix used to classify Trace-XML extension content. The leafID provides a reference to the ODM-XML or Define-
XML file containing the reference and the ItemOID contains the reference to the source variable. Optional 
identifying information can also be provided in SourceItem, including a formal expression containing an XPath 
statement.  
 
 
Figure 1. Exampl

… [truncated]
```

