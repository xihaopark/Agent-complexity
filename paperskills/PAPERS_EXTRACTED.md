# Papers — full text extract (PyMuPDF)

Direct `page.get_text("text")` dump per page; no vision, no agent. Comparable to `ReadPdfTool` long-PDF **text** mode.

---

## A use-case analysis of CDISC:SDTM in academia in an investigator-initiated clinical trial.pdf

_Path: `/Users/park/code/Paper2Skills-main/papers/A use-case analysis of CDISC:SDTM in academia in an investigator-initiated clinical trial.pdf`_

### Page 1

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


### Page 2

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


### Page 3

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
The CDISC-study is neither an activity through understanding the cause of diseases and their 
pathology, nor is it an activity through improving measures to prevent injury and disease as 
well as diagnostic and treatment measures in medical care or through verifying those measures’ 
validity. Therefore, we think that it is outside the scope of the Ethical Guidelines for Medical 
and Health Research Involving Human Subjects.17
The ALL-RET trial had already started data collection with paper case report forms (CRFs) at 
the planning stage of the CDISC-study. We used “Ptosh” as the clinical data management system 
(CDMS). “Ptosh” was jointly developed by the National Hospital Organization Nagoya Medical 
Center and the Nonprofit Organization for Supporting Clinical Research.18 It is an electronic data 
capture (EDC) system with minimal functions for paper CRFs, and it can export data in SDTM 
format. An EDC is a system that creates electronic CRFs, and the data entered in the database 
becomes the original CRF. However, as data collection was already progressing with the paper 
CRFs in the ALL-RET trial, we decided not to use Ptosh as the EDC system, but rather as a 
CDMS for paper CRFs. In contrast to the EDC system, which is a web-based application where 
the data are directly input at trial sites, the CDMS is a system for data management staff to 
input and manage CRFs at the datacenter and is based on the paper-based CRF data.
A general CDMS or an EDC system exports files for each input screen, and the mapping to 


### Page 4

Nagoya J. Med. Sci. 84. 120–132, 2022
doi:10.18999/nagjms.84.1.120
123
Use-case study of CDISC/SDTM in academia
SDTM will be performed using those files. However, in Ptosh, regardless of the input screen 
and structure, variables can be consistently mapped to SDTM (Fig. 1). Therefore, datasets in 
SDTM-format can be obtained without any programming; however, the datasets are not complete 
SDTM datasets for NDA. Ptosh can output integrated data in SDTM format from one input 
screen with multiple domains, or vice versa, and can aggregate data from multiple input screens 
for one domain.
We mapped CDISC/SDTM variables to CRF items for the ALL-RET trial, built a database 
and input screens on Ptosh (Fig. 2(A)), and entered CRF data into the database using input 
screens (Fig. 2(B)).
SDTM datasets exported by Ptosh are incomplete; thus, post-processing is required to make 
them fully SDTM-compliant. Therefore, we developed a program using Base SAS, that is a 
software provided by SAS Institute Inc., to process these datasets. (Fig. 2(C))
In addition to CRF data, SDTM standards also require a description of a protocol outline 
called a trial design dataset. We manually created the trial design datasets using Microsoft Excel 
to avoid rejection by P21C. (Fig. 2(D))
The processed SDTM domain file and the minimum trial design datasets were verified by 
P21C. (Fig. 2(E))
Finally, as a part of the data management work of the ALL-RET trial, we used the complete 
SDTM datasets to create a list of patients, adverse events, and response evaluation criteria in 
solid tumors (RECIST) transitions for safety monitoring (Fig. 2(F)). Although RECIST is used 
for efficacy evaluation, the transition was monitored so that investigational drug administration 
Fig. 1  Contrast for concept of creating SDTMs between general EDC or CDMS, and Ptosh
Concept of creating SDTMs using general EDC or CDMS is shown on the left side, and Ptosh on the right 
side. Ptosh can output data in SDTM format directly, whereas general EDC and CDMS create files for each 
input screen and later create SDTM datasets using conversion programs.


### Page 5

Nagoya J. Med. Sci. 84. 120–132, 2022
doi:10.18999/nagjms.84.1.120
124
Shizuko Takahara et al
would not be continued even though it deserves progressive disease (PD).
In addition to the data management system, the first author, who is in charge of data manage-
ment, self-learned SDTM using materials published on the web, attended a half-day seminar 
conducted by UMIN, the official SDTM training provided by CDISC, and participated in a 
CDISC Japan User Group/SDTM team.
RESULTS
We, the academic staff for data management, mapped the CRF items to SDTM variables 
and built a database in Ptosh. The contents of paper CRFs were input into the database, and 
data were exported in SDTM format. The exported data required minimal processing to avoid 
problems in P21 validation.
In the CDISC study, we obtained 22 domains directly from Ptosh (Fig. 3). In Ptosh, multiple 
Fig. 2  Outline of the CDISC-study
First, (A) we mapped CDISC/SDTM variables to CRF items for the ALL-RET trial and built a database and 
input screens on Ptosh, (B) entered the CRF data of the ALL-RET trial into the Ptosh database, (C) processed 
the exported SDTM-format data from Ptosh with SAS Macros, (D) manually created trial design datasets, and 
then (E) used P21C to validate SDTM datasets. (F) We created three lists using the SDTM datasets.
AE: adverse events


### Page 6

Nagoya J. Med. Sci. 84. 120–132, 2022
doi:10.18999/nagjms.84.1.120
125
Use-case study of CDISC/SDTM in academia
domains can be mapped on the same input screen, and variables from one domain can be 
distributed on multiple input screens, exporting data in SDTM format in an integrated way.
An adverse event entered into Ptosh in Japanese (Fig. 4a) was exported directly in SDTM 
format in English as the second row of AE (Adverse Events) domain data (Fig. 4b). With 
adequate license, a medical dictionary for regulatory activities (MedDRA) can be automatically 
coded by selecting and inputting the symptom name of the adverse event on the input screen. 
Even if the input screen was in Japanese, all Ptosh outputs were created using Controlled 
Terminology in English; the terminologies were specified by CDISC.
RECIST data is divided into three domains, TU (Tumor Identification), TR (Tumor Results), 
and RS (Disease Response) in SDTM. TU comprises the names of target and non-target lesions. 
Each TU record represents one lesion. TR includes the size of target lesions or presence of 
non-target lesions. A TR record represents each lesion for each visit. RS includes the assessments 
for target lesions, non-target lesions, new lesions, or overall responses. An RS record represents 
an assessment on a visit. It is necessary to link these TU and TR records using Link ID, and 
this link can be generated by Link ID on pre-mapped CRFs in Ptosh (Fig. 5). 
The data exported from Ptosh are not completely SDTM-compliant. Most variables for prefixed 
data or input data will be exported from Ptosh. However, most variables for derived data will be 
Fig. 3  Exported files from Ptosh
State where 22 domain files for the ALL-RET trial were exported from Ptosh (unprocessed). Each domain file 
for CDISC was created directly from Ptosh.


### Page 7

Nagoya J. Med. Sci. 84. 120–132, 2022
doi:10.18999/nagjms.84.1.120
126
Shizuko Takahara et al
missing or exported as blank. For example, an exported DM (Demographics) domain does not 
contain any data derived from other domains (eg, study drug administration end date, death status, 
date of death, etc). We needed to post-process the exported data to fill these derived variables. 
Fig. 4a  Screen for adverse events in Ptosh (test data)
All input screens are shown in Japanese. It also shows that MedDRA coding can be performed directly in the 
system.
Fig. 4b  Unprocessed AE domain data output from Ptosh
Part of the unprocessed AE domain data output from Ptosh. As shown in Fig. 4a, the data was entered by 
selecting the Japanese options, but all the data were stored in English. MedDRA coding stores not only the 
code but also English terms. AEACN, AEREL, and AEOUT are all stored in the Controlled Terminology terms 
in English characters. The dataset item names are SDTM-compliant.


### Page 8

Nagoya J. Med. Sci. 84. 120–132, 2022
doi:10.18999/nagjms.84.1.120
127
Use-case study of CDISC/SDTM in academia
Additionally, we needed to delete extra records with blank data, which will not be exported from 
the current version of Ptosh. For example, a patient has 3 target and 3 non-target lesions in 
the ALL-RET trial (Fig. 5). However, because 5 and 7 input fields were prepared on the input 
screen for target and non-target lesions, 5 and 7 records are exported with 2 extra-records for 
target lesions and 4 extra for non-target lesions (Fig. 5). We developed a processing program 
to complete SDTM datasets using Base SAS. This program was created as a general-purpose 
macro so that it can be used in other studies. 
In the validation of P21C, we reduced “Reject” and “Error” items by modifying the mapping 
in Ptosh for the ALL-RET trial. Finally, 0 rejects and 8 errors were left. All 8 errors were 
explainable. They were caused by a lack of data on the cases that dropped out before the start 
of treatment and the inconsistency in the dates of cases that were discontinued without treatment. 
PMDA will not accept any data with “Reject,” but it will accept data with “Error” that include 
explanations regarding the causes of the violations and the reasons why such errors cannot be 
corrected.19 Therefore, if the data included no “Reject” by the Pinnacle 21 Community, a free 
version of Pinnacle 21 Enterprise,20 then it implies that our data is suitable for submission to 
the PMDA. There was no “Reject” from the P21C validator; therefore, we were able to obtain 
SDTM-compliant datasets, which is sufficient for NDA.
Fig. 5  Unprocessed output data from Ptosh for the TU, TR, and RS domains
Data output from Ptosh for the TU, TR, and RS domains for the RECIST evaluation. TU and TR data are ap-
propriately linked by TULNKID and TRLNKID. In this sample data, there are 3 target lesions and 3 non-target 
lesions, but the input screen allows for 5 target lesions and 7 non-target lesions to be entered. Therefore, the 
lesions that have not been input are output as blanks, and these records require processing to be deleted later.


### Page 9

Nagoya J. Med. Sci. 84. 120–132, 2022
doi:10.18999/nagjms.84.1.120
128
Shizuko Takahara et al
DISCUSSIONS
This study makes the following contributions:
1. We developed a method with which the data management staff of academia can output fully 
SDTM-compliant datasets, validated by P21C, in investigator-initiated trials without outsourcing.
2. The software, which exported data in SDTM format, was shown to be useful and an 
adequate method in academia.
Effects of Standardization and Laborsaving using SDTM Datasets
We developed a program to create three lists from the fully SDTM-compliant datasets 
(Fig. 2(F)). The program is not specific to the ALL-RET trial, and it can be applied without 
modification for SDTM datasets from any clinical trial regardless of subspecialties. Likewise, 
other general programs can be developed for other lists, aggregations, graphs, statistics, etc, if 
SDTM datasets are available. Standardizing SDTM datasets may lead to reduced labor, which 
is a significant advantage even for clinical studies without NDA. In addition to the CRF data 
management work, it seems possible to build a common central monitoring system within 
academia with SDTM datasets.
How Did We Choose Ptosh?
We usually use DEMAND, a CDMS provided by Densuke Systems Co., Ltd. (currently 
transferred to G-Link System Consulting K.K. by business transfer), as the CDMS for paper 
CRFs in Kanazawa University. DEMAND is built using the same design concept as the “general 
EDC or CDMS” shown in Fig. 1. Therefore, DEMAND has templates corresponding to the 
SDTM domains and Controlled Terminology, which is a CDISC standard dictionary. For domains 
with a simple structure, such as an adverse event that consists of one event and one record, a 
template with the AE domain structure can be easily created. However, clinical trial data are not 
limited to such simple structures. In particular, data belonging to the “Findings” domain class in 
SDTM have a single record per item; therefore, the data structure is completely different from 
the “general EDC and CDMS” referred to in Fig. 1 (Fig. 6 and 7). Also, in SDTM, data must 
be written in English character strings, and not in codes, such as numerical values (Fig. 7); 
however, it is cumbersome to manually enter all data in English character strings. If there is no 
function to convert input code to terminology or select input on the input screens, it cannot be 
put to practical use. There are other limitations with the data. For instance, the TU, TR, and 
RS domains must be linked to each other.
We concluded that using DEMAND alone may not be sufficient to output the data of all 
CRFs from the ALL-RET trial to SDTM and decided to use Ptosh for SDTM output. However, 
Ptosh has the following limitations. To use Ptosh, it is necessary that staff who are familiar 
with SDTM perform SDTM mapping to build the input screens. They must carefully design the 
input screens. In a general system, shown in Fig. 1, SDTM knowledge is not required for the 
construction of input screens; this knowledge is required only during the development stage of 
the conversion program. Also, for long-term clinical studies, Ptosh design will be based on the 
SDTM version prior to the start of operations, and new SDTM versions or therapeutic areas may 
be newly released at the time of data fixing. This may require minor modifications of exported 
data from Ptosh in the future.


### Page 10

Nagoya J. Med. Sci. 84. 120–132, 2022
doi:10.18999/nagjms.84.1.120
129
Use-case study of CDISC/SDTM in academia
Use of Ptosh, an EDC, as a CDMS and Role Sharing Between It and a General CDMS
In the CDISC-study, because we planned to output SDTM datasets with paper CRFs and 
Fig. 6  Contrast for image of output data between general EDC or CDMS, and Ptosh
General CRF for the presence of symptoms and an image of the output data. In the output data from general 
EDC or CDMS, one record represents the contents of one CRF. In SDTM, however, one record represents each 
item. Thus, SDTM can be used universally irrespective of the items prepared for each clinical trial.
Fig. 7  Contrast for image of output data between general EDC or CDMS, and Ptosh
CRF that describes an adverse event and images of output data. In a general EDC or CDMS, choices are stored 
as code. However, SDTMs must be created as English strings specified by Controlled Terminology. In the case 
of a system that can be entered only with a code, it will be necessary to create another program later to convert 
every data point entered by code.


### Page 11

Nagoya J. Med. Sci. 84. 120–132, 2022
doi:10.18999/nagjms.84.1.120
130
Shizuko Takahara et al
CDMS, and the ALL-RET trial had started with paper CRFs, we decided to use Ptosh as the 
CDMS. However, because Ptosh is an EDC system with minimal functionalities as a CDMS, it 
is designed to create electronic CRFs. Usually, only investigators, sub-investigators, or research 
coordinators at trial sites are allowed to input data directly into the electronic CRFs in EDC. 
We used the Ptosh version available as of January 2019 because it had a minimum CDMS 
function called “substitute input” that allowed data center staff to input data from paper CRFs 
filed by trial site members. However, this is not recommended as the function is now obsolete 
and could be abolished in the future.
Ptosh is an EDC system without the general data management functions present in many 
CDMSs. For example, Ptosh does not have the double-entry-and-compare function (the method 
of two people entering the same CRFs separately and comparing the data to find and correct 
input errors). Therefore, we performed collating by reading out all items in all cases. However, 
collating by reading out is more error-prone than double-entry.21 It is more efficient to consider 
using a CDMS with double-entry function at least for the numerical data in the LB (Laboratory 
Test Results) and VS (Vital Signs) domains of SDTM. 
Issues of SDTM Output by Academia
Regardless of the disease area, many items are easily standardized. These include the patient’s 
basic background items (such as date of birth and sex), adverse events, concomitant medications, 
clinical tests and vital signs, RECIST evaluation (oncology area only), and dropouts. However, 
current disease history, study intervention, and special tests for efficacy evaluation depend largely 
on the disease and the characteristics of the clinical study, and complete standardization is 
difficult.13 The items that are difficult to standardize are also the items where SDTM mapping 
is difficult. Advanced knowledge of CDISC standards is required to perform these mappings. 
Therefore, advanced education on CDISC standards is essential for the staff.
We saved time and costs for the CDISC-study by obtaining scientific research grants. As we 
had prior knowledge of CDISC standards, we could map items on CRFs to SDTM variables 
when we started to work on Ptosh. However, it is conceivable that sparing the required time 
and costs is difficult for most academic institutions, especially in Japan.
The first author is a clinical data manager and has previously worked as a system engineer, 
having acquired knowledge of programming and relational databases. However, it may be difficult 
for staff with only user-level knowledge of the system to be ready to work immediately after 
CDISC training. Therefore, it is reasonable to consider hiring those who have a good working 
knowledge and experience with databases and IT systems.
It is difficult to establish an employment quota for such human resources. In academia, there 
are some organizations in which medical staff simultaneously serve as data managers because 
these organizations belong to a hospital; they may not have an employment quota for the data 
management department unless they are medical staff. Also, there are many organizations that 
have employees on short-term contracts, eg, for up to five years. It is futile for the department 
to educate such employees, given that they will leave the organization after the contract expires, 
and by that time they may have become full-fledged CDISC experts.
We hope that academia as a whole will take a top-down approach in introducing CDISC 
standards from the perspective of anticipating future standardization and labor savings, and in 
securing research funding and staff, as well as staff training. In addition to Ptosh, other SDTM 
output tools are becoming available for SDTM dataset output in academia. For example, REDCap 
is an EDC system developed at Vanderbilt University in the US and widely used in academia 
worldwide. It does not have the capability to output SDTM by itself, but REDCap2SDTM, an 
SDTM dataset output add-on program, has been developed by Osaka University (now transferred 


### Page 12

Nagoya J. Med. Sci. 84. 120–132, 2022
doi:10.18999/nagjms.84.1.120
131
Use-case study of CDISC/SDTM in academia
to Osaka City University).22 In this way, an environment for CDISC compliance in academia is 
being arranged.
To spread the use of CDISC standards in academia, it is important to ensure that they are 
fully used, sufficient education regarding CDISC is provided, and costs are secured to build and 
use the system.
ACKNOWLEDGMENTS
The authors express their gratitude to Matsuo Yamamoto and Kaori Nagai of the Clinical 
Research Center of National Hospital Organization Nagoya Medical Center for their support 
concerning Ptosh.
Although we did not use DEMAND in the CDISC-study, we received a significant amount 
of cooperation at the start of the CDISC-study. We thank Atsushi Imamura, Noriyuki Suzuki, 
and Eiichi Ando of Densuke Systems Co., Ltd. (as of the start of the CDISC-study in 2015).
For the ALL-RET trial, we express our gratitude to Dr. Seiji Yano and Dr. Shinji Takeuchi 
from the Cancer Research Institute of Kanazawa University for their cooperation in implementing 
the CDISC. We also thank Prof. Kenichi Yoshimura from the Medical Center for Translational and 
Clinical Research, Hiroshima University Hospital, and Prof. Satoshi Teramukai of the Department 
of Biostatistics, Kyoto Prefectural University of Medicine Graduate School of Medical Science, 
for the guidance provided in the CDISC-study. We appreciate Nanayo Aoki, Mayumi Noda, 
Yukiko Sawamoto, and Nahoko Okitani of the Innovative Clinical Research Center, Kanazawa 
University, for the feedback on the data center operation task for the ALL-RET trial.
CONFLICTS OF INTEREST STATEMENT
The authors have no conflicts of interest to disclose.
FUNDING STATEMENT
The CDISC-study was performed using grant-in-aid research (Grant-in-Aid for Scientific 
Research on Innovative Areas JP15K15250) from the Japan Society for the Promotion of Science.
REFERENCES
  1	
Pharmaceutical and Medical Device Agency. Holding of the briefing session for the operation based on 
the “Basic Principles on Electronic Submission of Study Data for New Drug Applications [in Japanese].” 
Pharmaceutical and Medical Device Agency. https://www.pmda.go.jp/review-services/drug-reviews/about-
reviews/p-drugs/0026.html. Accessed May 10, 2021.
  2	
Head of Pharmaceutical and Food Safety Bureau, Ministry of Health, Labour and Welfare. Basic Principles 
on Electronic Submission of Study Data for New Drug Applications. Pharmaceutical and Medical Device 
Agency. https://www.pmda.go.jp/files/000153708.pdf [in English], https://www.pmda.go.jp/files/000159962.
pdf [in Japanese]. Accessed May 10, 2021.
  3	
Head of Pharmaceutical Evaluation Division, Pharmaceutical Safety and Environmental Health Bureau, 
Ministry of Health, Labour and Welfare. Revision of Basic Principles on Electronic Submission of Study 
Data for New Drug Applications. Pharmaceutical and Medical Device Agency. https://www.pmda.go.jp/
files/000234977.pdf [in English], https://www.pmda.go.jp/files/000234491.pdf [in Japanese]. Accessed May 
10, 2021.


### Page 13

Nagoya J. Med. Sci. 84. 120–132, 2022
doi:10.18999/nagjms.84.1.120
132
Shizuko Takahara et al
  4	
Study Data Tabulation Model Version 1.7 (Final). CDISC. https://www.cdisc.org/standards/foundational/sdtm/
sdtm-v1-7/html. Accessed May 10, 2021.
  5	
Technical Information Regarding Submission of Application Electronic Data (FAQ, Data Standard Catalog 
etc.)[in Japanese]. Pharmaceutical and Medical Device Agency. https://www.pmda.go.jp/review-services/
drug-reviews/about-reviews/p-drugs/0028.html. Accessed May 10, 2021.
  6	
Global Regulatory Requirements. Clinical Data Interchange Standards Consortium. https://www.cdisc.org/
resources/global-regulatory-requirements. Accessed May 10, 2021.
  7	
CDISC Vision and Mission. CDISC Wiki [in Japanese]. https://wiki.cdisc.org/pages/viewpage.
action?pageId=32812989. Last Updated January 17, 2017. Accessed May 10, 2021.
  8	
Business track record in 2019 and future approaches. Pharmaceutical and Medical Device Agency [in 
Japanese]. https://www.pmda.go.jp/files/000233224.pdf. Published December 2019. Accessed May 10, 2021.
  9	
CDISC. Clear data. Clear impact. Clinical Data Interchange Standards Consortium. https://www.cdisc.org/. 
Accessed May 10, 2021.
10	
Barrie N. FDA Binding guidance: a pivotal milestone for CDISC Standards. Appl Clin Trials. 
2016;25(12):42–42.
11	
New Drug Review with Electronic Data. Pharmaceutical and Medical Device Agency. https://www.pmda.
go.jp/english/review-services/reviews/0002.html. Accessed May 10, 2021.
12	
Joining the Clinical Data Interchange Standards Consortium (CDISC) and Activity Status. Japan Agency 
for Medical and Research Development. https://www.amed.go.jp/en/aboutus/collaboration/cdisc.html. Last 
Updated April 7, 2017. Accessed May 10, 2021.
13	
Takahara S: CDISC Public Symposium Proceedings – Significance and issues regarding CDISC deployment 
in academia. Japan Agency for Medical and Research Development [in Japanese]. https://www.amed.go.jp/
content/000003726.pdf#page=135. Published March 24, 2017. Accessed May 10, 2021.
14	
Sawanobori K, Sakushima K, Arato T, Shichinohe H, Sato N, Houkin K. Challenges Identified in the 
Project for the Development of Human Cell Therapy Products in Hokkaido University: Mid-term Review. 
Regul Sci Med Prod. 2017;7(2):91–97. doi:10.14982/rsmp.7.91.
15	
Todaka K. Clinical Study and Medical Product Development: Role of the Academic Research Organization 
[in Japanese]. J Jpn Surg Assoc. 2016;77(5):1292–1294. doi:10.3919/jjsa.77.1292.
16	
Browsing of UMIN-CTR Clinical Trial Registration Information. University Hospital Medical Information 
Network. https://upload.umin.ac.jp/cgi-open-bin/ctr/ctr.cgi?recptno=R000023806. Accessed May 10, 2021.
17	
Ethical Guidelines for Medical and Health Research Involving Human Subjects. Ministry of Health, Labour 
and Welfare. https://www.mhlw.go.jp/content/10600000/000757250.pdf. Accessed May 10, 2021.
18	
Saito IT, Saito MA, Kondo S, Nagai K, Nishioka E, Horibe K. Computerization of Clinical Trial 
Data Management at the Clinical Research Core Hospital in Japan [in Japanese]. Regul Sci Med Prod. 
2015;5(1):61–71. doi:10.14982/rsmp.5.61.
19	
FAQs on Electronic Study Data Submission. Pharmaceutical and Medical Device Agency [in Japanese]. 
https://www.pmda.go.jp/review-services/drug-reviews/about-reviews/p-drugs/0029.html#Q116. Accessed April 
5, 2021.
20	
Is there a timeline for when Pinnacle21 Community begins to support new PMDA validation rule? 
Pinnacle21. https://www.pinnacle21.com/forum/there-timeline-when-pinnacle21-community-begins-support-
new-pmda-validation-rule. Accessed May 10, 2021.
21	
Ohashi Y, Tsuji A. Clinical Trial Data Management [in Japanese]. Tokyo: Igaku-Shoin Ltd; 2004.
22	
Yamamoto K, Ota K, Akiya I, Shintani A. A pragmatic method for transforming clinical research data from 
the research electronic data capture “REDCap” to Clinical Data Interchange Standards Consortium (CDISC) 
Study Data Tabulation Model (SDTM): Development and evaluation of REDCap2SDTM. J Biomed Inform. 
2017;70:65–76. doi:10.1016/j.jbi.2017.05.003
References End


---

## Current Applications and Future Directions for the CDISC Operational Data Model Standard- A Methodological Review

_Path: `/Users/park/code/Paper2Skills-main/papers/Current Applications and Future Directions for the CDISC Operational Data Model Standard- A Methodological Review`_

### Page 1

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


### Page 2

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
[18] for Deﬁne-XML v2. Fig. 1 highlights the CDISC foundational
Fig. 1. ODM-based standards supporting the CDISC foundational standards content.
S. Hume et al. / Journal of Biomedical Informatics 60 (2016) 352–362
353


### Page 3

standards covered by ODM, and standardized extensions such as
Clinical Data Acquisition Standards Harmonization (CDASH) that
describes the basic data collection ﬁelds for domains, the Study
Data Tabulation Model (SDTM) that describes a standard structure
for study data tabulations, and the Analysis Data Model (ADaM)
that describes metadata models and examples for analysis datasets
[1]. In addition to the extensions listed above, numerous propri-
etary extensions have been proposed in the research literature or
implemented by practitioners. ODM’s useful form hierarchy struc-
ture, and its use of extensions to expand its applicability across a
broad range of use cases has increased interest in ODM as a
research topic.
In order to further advance research on the ODM standard, the
existing research must be well understood. This paper presents a
systematic review of the ODM literature and uses a classiﬁcation
schema to organize and analyze the literature. It serves as a focal
point for future ODM oriented research. Due to the number and
size of the XML examples demonstrating ODM’s features and lim-
itations, it was not feasible to include them in this paper. Instead, a
website has been established as a repository for the example ﬁles
at http://www.odm-review.com.
2. Material and methods
2.1. Research method
The literature search started with a systematic scan of online
academic and conference databases in the information systems
and healthcare domains performed by the lead author. The follow-
ing databases were searched: (1) ABI/Inform, (2) ACM Digital, (3)
AIS eLibrary, (4) Europe Central PubMed, (5) Google Scholar, (5)
IEEE Xplore, (7) PubMed, and (8) ScienceDirect. A backward and
forward reference search using Web of Science citation analysis
for papers that passed screening was also performed with contri-
butions from all authors. The search term used on all databases
was ‘‘CDISC ODM.”
Two primary inclusion criteria were used in the selection of
ODM research for examination within the proposed framework:
(1) the research must examine the use of ODM as an information
system solution component, or (2) the research must critically
evaluate ODM against a stated solution usage scenario. Research
papers not meeting these criteria were excluded from this analysis.
Articles not written in the English language were also excluded
from the search.
Out of 2686 articles identiﬁed, 266 were included in a title level
review resulting in 183 articles. An abstract review followed
resulting in 121 remaining articles. After full text scanning of the
121 articles, 69 met the inclusion criteria and were included in
the ﬁnal analysis.
After reviewing the articles, a gap was identiﬁed in the litera-
ture regarding Deﬁne-XML, an ODM standard widely used in prac-
tice, but not well described in the academic literature. To address
this gap an archive of 26,659 practitioner articles maintained at
lexjansen.com was searched for ‘‘CDISC Deﬁne-XML.” Inclusion cri-
teria were added to narrow the relevant articles to only those pre-
sented in 2013–2014 that provided a detailed description of the
process for creating Deﬁne-XML ﬁles. Four additional articles were
added to the ﬁnal analysis based on this search.
As the articles where selected for inclusion, they were also cat-
egorized by the clinical research data lifecycle phase(s) addressed
by the ODM solutions discussed in the article. The authors collab-
oratively developed this classiﬁcation schema represented by the
process diagram shown in Fig. 2 and described in the next section.
A consensus-based analysis process, with input from all authors,
was used to review and update a categorized list of articles pro-
duced by the lead author. Each article included in the ﬁnal analysis
was assigned to at least one data lifecycle category, with 26% of the
articles addressing multiple categories.
2.2. Classiﬁcation schema created for the methodological review
The purpose of establishing an ODM classiﬁcation schema was
to provide a categorized and consolidated view of the ODM
research literature. The authors used Fig. 1 as the basis for the clas-
siﬁcation schema. They consolidated the ODM use cases described
in the literature into the different clinical research data lifecycle
phases to yield a manageable number of categories and expanded
Fig. 1 to include the missing phases shown in Fig. 2: EDC and EHR
infrastructure, and study archival.
Each phase in the clinical research data lifecycle shown in Fig. 2
represents a category in the classiﬁcation schema. The categories
of the proposed classiﬁcation schema reﬂect the diverse array of
use cases found in the ODM literature. A brief description of each
of the ﬁve clinical research data lifecycle categories follows. Subse-
quent sections expand upon the applications of ODM in these ﬁve
categories with details from the referenced literature.
The EDC and EHR Infrastructure phase of the lifecycle focuses
on setting up the EDC data collection system and the EHR integra-
tion infrastructure to support future clinical research studies. This
phase occurs once, and the infrastructure may be reused across
multiple studies. After the EDC and EHR integration infrastructure
has been setup, each of the remaining phases is executed for each
clinical research study executed. The Planning phase covers creat-
ing a study protocol and representing it in a machine-readable
Fig. 2. Phases in the clinical research data lifecycle used by the ODM classiﬁcation schema.
354
S. Hume et al. / Journal of Biomedical Informatics 60 (2016) 352–362


### Page 4

format, formulating a study design, submitting a study to clinical
trial registries (such as ClinicalTrials.gov), setting up a study within
an EDC or other clinical data management system (CDMS), creating
CRFs, deﬁning a study schedule of events, and importing CRFs from
form libraries. The Data Collection phase of the lifecycle focuses
on the data collection and interchange that occurs during study
execution and represents an original ODM use case [19]. The Data
Tabulations and Analysis phase in the lifecycle combines the third
and fourth phases shown in Fig. 1 and focuses on the generation of
datasets in support of standardized tabulations, analysis datasets,
reporting and regulatory submissions. Study Archival is the ﬁnal
phase of the data lifecycle and focuses on archiving the study data
and metadata such that it complies with the federal regulations
[10]. It represents another original ODM use case [19].
3. Results
3.1. EDC and EHR infrastructure
3.1.1. ODM usage in EDC and EHR infrastructure
Though not an original ODM use case, the ODM literature in EDC
and EHR infrastructure [1,2,20–44] identiﬁes a surprising number of
projects using ODM as a means of integrating Electronic Health
Record (EHR) systems with clinical research systems [25]. Single
Source, or collecting data once electronically with multiple uses
in healthcare and clinical research, uses ODM to reduce the data
capture burden at the investigator sites by bridging HL7 CDA and
the EDC system [26,27]. In Single Source, clinical care data ﬂows
into the EHR database, while the clinical trial data is sent to an
EDC system in a parallel data ﬂow [26] eliminating redundant data
entry, reducing source data veriﬁcation, and making the data avail-
able in a more timely fashion [28,29].
The Single Source proof-of-concept Starbrite study conducted at
the Duke Clinical Research Institute [27,28,30] captured data via
the HL7 CDA, provided automated integration with ODM, and
showed nearly a 75% overlap between the two. Others, such as El
Fadly et al. [31] found that the overlap was only 30–50%, and in
El Fadly et al. [32] it was only 13.4%. Interoperability between
HL7 CDA and ODM has also been demonstrated by [32–36] and
has been particularly effective for lab, demographic, medication,
and vital signs data.
The x4T (exchange for Trials) system discussed in [37–39] is
another Single Source implementation. The use of the x4T as a
mediator between ODM and the EHR data reduced documentation
time by 70% while increasing completed mandatory data elements
from 82% to 100% [39]. The ‘‘Extraction and Investigator Veriﬁca-
tion” scenario identiﬁed in the Electronic Source Data Interchange
(eSDI) document [29] inspired the x4T architecture [39] that is
based on technologies such as the eXist XML database, XQuery,
XForms, and ODM. Integrating x4T into routine patient care has
improved data quality, as well as the data collection and documen-
tation workﬂow [39].
The CDISC Healthcare Link Initiative, in conjunction with IHE
QRPH (Integrating the Health Enterprise Quality, Research and
Public Health) has produced the Retrieve Form for Data-capture
(RFD) integration proﬁle as a means of integrating EHR and clinical
research data. When used with ODM, RFD establishes an auto-
mated method to capture form-based EHR data for secondary uses
including clinical research, disease registries, and safety reporting
[40]. RFD pre-populates ODM-based CDASH [24] CRFs with data
extracted from an EHR system in HL7 CCD format [35]. This
approach supports eSource by saving both the HL7 CCD and
ODM XML to a regulatory compliant archive.
The RE-USE project used ODM metadata templates to support
data interchange between HL7-based EHR data and clinical
research data [32,41] using a CDA/ODM mediator [31]. RE-USE
included the use of an ODM metadata message to create the CRF
in the EHR, and the use of an ODM data message created using
the ODM mediator to exchange data [31]. In RE-USE ODM sup-
ported the use of healthcare terminologies such as SNOMED-CT
[42], as well as binding data elements to concepts such as SNOMED
3.5 VF [32]. Combining ODM and HL7 using a semantic interoper-
ability framework has enabled data interchange between EHR and
EDC systems [23,32,35].
The SALUS (Scalable, Standard based Interoperability Frame-
work for Sustainable Proactive Post Market Safety Studies) project
addresses the lack of uniﬁed ‘‘models of use” in healthcare and
clinical research by creating a common ‘‘model of meaning”. SALUS
has developed a large knowledge base containing 4.7 million tri-
ples representing BRIDG, ODM, HL7 CDA, the CDISC content stan-
dards, and the relevant terminologies [21]. SALUS uses this
knowledge base as the foundation of a semantic framework for
achieving interoperability between clinical research systems using
ODM, and EHR systems using HL7 CDA.
A large medical forms library chose ODM as its standard for rep-
resenting form metadata [33]. This ODM-based medical forms
repository used the BRIDG model to harmonize data elements to
facilitate integration with HL7 CDA documents [33].
3.1.2. ODM enhancement opportunities identiﬁed in the literature for
EDC and EHR Infrastructure
While ODM has been used to successfully integrate clinical
research systems with EHR-based HL7 CDA and other medical
record data formats in a limited number of cases [42], most note
that their research projects used manual mapping to accomplish
interoperability at the syntactic level [25,27,34]. Kush et al. [27]
state that a general, reusable mapping between ODM and CDA
would have been challenging in their project as each of the stan-
dards approaches semantics differently.
The lack of a common underlying reference model between rou-
tine healthcare and clinical research makes achieving semantic
interoperability difﬁcult [34,35]. Semantic interoperability enables
a clinical observation to be represented using different information
models while maintaining the same meaning. Information models
for representing clinical observations include HL7 Reference Infor-
mation Model (RIM), CEN/ISO 13606, and BRIDG [22,35]. CDISC
standards like ODM and SDTM also represent clinical data models.
In addition to semantic differences, structural differences
between standards can also impede interoperability. For example,
ODM forms support 3 levels of depth, while HL7 CDA’s nested
observations can be unlimited in number. This disparity is at least
partially a reﬂection of the difference between protocol-driven clinical
research and the event-driven healthcare domain.
Clinical research and healthcare lack a common set of termi-
nologies making ODM/EHR integration challenging as similar data
items may have values expressed using different vocabularies
[34,45]. HL7 CDA and ODM also represent controlled terminologies
differently. The HL7 CDA standard uses the HL7 RIM to provide an
external semantics source [27]. ODM tends to deﬁne its own codes
without explicitly accounting for semantics [27,45,46].
3.2. Planning
3.2.1. ODM usage in planning
The ODM literature on planning activities covers a broad range
of topics [2,11,13,20–23,45,47–68]. The SDM-XML study design
ODM extension, covering a portion of the protocol requirements,
is currently available for use [16]. Despite being limited in scope,
SDM-XML has been successfully applied in a number of projects.
Aerts [47] showed how SDM-XML could be used to generate a
caBIG Patient Study Calendar. Nepochatov [48] used study design
S. Hume et al. / Journal of Biomedical Informatics 60 (2016) 352–362
355


### Page 5

metadata combined with core ODM metadata to generate study
setups that included not only CRFs, but also a study calendar for
each subject. ODM extended with SDM-XML was used by the IMI
(Europe’s Innovative Medicines Initiative) EHR4CR project to sup-
port the patient recruitment process [20]. The SALUS project [21]
used SDM-XML annotated with CDASH variables to demonstrate
the automatic completion of research CRFs with EHR data.
Willoughby et al. [49] stated that registrations can be submitted
to the World Health Organization (WHO) registry, International
Clinical Trial Registry Platform (ICTRP), using an ODM extension
[48]. Huser [51] mapped the ClinicalTrials.gov schema to ODM
and implemented an extension to address the gaps. In 2015, a draft
ODM-based CTR-XML standard was published to represent infor-
mation for submissions to clinical trial registries, such as Clini-
calTrials.gov, EUDRACT, or WHO ICTRP [1].
In addition to representing elements of protocol, ODM metadata
transformations can be used to generate CRFs, setup EDC systems,
conﬁgure decision support systems, and drive integration with
other clinical systems as described in [2,45,52–56]. ODM’s expres-
sive metadata language makes it the language of choice for
describing CRF content [52]. The CDISC CDASH standard [24] CRF
content has been published in ODM, and can be exported from
the CDISC SHARE metadata repository [69] as ODM.
Some clinical data software depends completely on ODM meta-
data for study setup and maintenance [2,53]. Kuchinke et al. [58]
demonstrated the transfer of a complete clinical study designed
in a system at one research center, exported as an ODM ﬁle, and
imported by a different system at a different research center with-
out using any additional software tools. In addition to the basic CRF
elements, ODM includes partial support for cross-element valida-
tion and derivations [59]. ODM’s vendor extension mechanism
provides the means to add support for proprietary study setup
and data collection features [52].
ODM’s ability to represent a broad range of CRF types was
demonstrated in Bruland et al. [60] where all Clinical Data Ele-
ments (CDEs), including their semantic concepts, from 3012 forms
in the National Cancer Institute’s (NCI) Cancer Data Standards Reg-
istry and Repository were effectively mapped to ODM. The seman-
tic concepts were captured using ODM Alias elements [60]. ODM
semantic alignment is often achieved by using the Alias Name attri-
bute to contain the code, and the Context attribute to contain the
name of the code system [14,61,62], but in other cases imple-
menters might choose to use a proprietary extension that more
explicitly represents speciﬁc semantic annotations [11,17,22].
ODM is capable of supporting the requirements of a CDE repos-
itory model by adding the necessary features using vendor exten-
sions [45]. Eli Lilly and Company demonstrated the use of ODM as a
repository [63]. Dugas and Briel [64] use ODM for a large EHR and
clinical research data model repository consisting of 3320 medical
forms with 102,677 data elements [23,62,64]. ODM has also been
shown to align with the ISO 11179 metadata registry standard,
with the exception of a standard representation for ISO 11179’s
Data Element Concept (DEC) [13].
3.2.2. ODM enhancement opportunities identiﬁed in the literature for
planning
The main limitation restricting the use of ODM to support pro-
tocol has been the lack of a complete implementation model,
despite the availability of the BRIDG-based PRM (Protocol Repre-
sentation Model) content model published in 2010 [49,70]. The
draft CTR-XML trial registries standard will expand ODM’s ability
to represent study level elements including the WHO 20-item min-
imum dataset [71].
As previously described, ODM has made broad use of the Alias
element to capture semantic information, but ODM lacks a formal
mechanism for capturing semantics. ODM does not specify the use
of speciﬁc clinical items such as CDASH, nor does it provide a speci-
ﬁc mechanism for pointing to the source of a particular CDE.
Instead, ODM provides a hierarchical container for deﬁning clinical
data items according to the needs of a given study [65], as shown in
Fig. 3. The lack of a source deﬁnition for a clinical data item was
highlighted when the ISO 11179 DECs were found missing from
the ODM model [13]. Studies that use CDASH CRFs achieve seman-
tic alignment through a shared data standard, rather than through
speciﬁc semantics [66]. ODM does not provide a mechanism for
capturing the logical relationships between data elements used
on different CRFs [66,67]. Again, Alias can be used to address this
shortcoming, but Alias currently relies on a common naming strat-
egy to be effective.
By design, ODM does not include the presentation metadata
needed to direct the visual rendering of CRFs [52]. Vendor exten-
sions can be used to add the needed presentation metadata in
ODM, but creating a single, standard extension to support a diverse
set of clinical research software systems would be challenging [52].
This lack of metadata to describe the visual representation of CRF
data ﬁelds can signiﬁcantly alter a user’s experience with a CRF
that is created in one system and then transferred for use in
another [58]. ODM also lacks the metadata to represent the content
ownership and context of use metadata as is found in copyrighted
data collection instruments [45].
ODM supports multi-language CRFs, but simply applying xml:
lang, a standard XML attribute for identifying language, to all
ODM elements, instead of using the ODM speciﬁc TranslatedText
within just ﬁve elements, broadens ODM’s multi-language support
while eliminating an unnecessary level in the XML hierarchy [59].
De Melo et al. [52] cite a number of technically related ODM
shortcomings, including a lack of support for arrays, that could
be beneﬁcial for capturing the value of repeating data elements.
Fig. 3. ODM metadata (left) and data hierarchies.
356
S. Hume et al. / Journal of Biomedical Informatics 60 (2016) 352–362


### Page 6

The ODM form hierarchy only supports two levels, Items within
ItemGroups, as shown in Fig. 3, but repeating data element CRF pro-
cessing requirements could demand at least one additional layer in
the hierarchy [52]. ODM also lacks a standard language to express
computations and validations in the ConditionDef and MethodDef
elements [45,72].
3.3. Data collection
3.3.1. ODM usage in data collection
Data interchange, a key process in the data collection phase, is
an original ODM use case, was the focus of ODM v1.0, and has been
covered broadly in the literature [2,13,26,35,43,45,46,52,53,57,58,
60,62–64,73–85]. ODM’s basic hierarchical structure is particularly
well suited for data capture [84]. In addition to its maturity, other
noted ODM strengths include its relative simplicity and adaptabil-
ity afforded by its vendor extension mechanism. Generating ODM
exports to support data interchange is reasonably straightforward
[83]. A large number of clinical research software vendors support
the ODM-based exchange of clinical study data and metadata
[2,46,58,75]. ODM has also been used to support forms outside of
clinical
research,
as
was
demonstrated
by
the
ODM-based
exchange of forensic autopsy data [57]. Most systems that support
ODM data interchange do so via a ﬁle export and import mecha-
nism [58,76,86], but some use a more modern ODM-based web
services approach [53,77,78]. As a data interchange standard,
ODM has demonstrated its usefulness as both a document and a
message format. As the use of ODM to exchange data, data and
metadata, or metadata alone has grown, the need for tools that val-
idate ODM content, such as the ODM Checker [58], has increased in
importance.
ODM has been used as the basis for data transformation sys-
tems in support of data integration. In Dugas and Dugas-Breit
[62], ODM was the basis for an automated transformation tool to
convert study data models into different formats including ofﬁce
documents, and statistical datasets. In this case, using semantically
annotated ODM helped drive automated transformations while
preserving the original semantics. The open-source compareODM
tool in Dugas et al. [81] compared semantically enriched ODM
forms and was able to automatically derive the differences
between two versions of a form including identical, matching, or
similar data items [43]. ODM has been used to integrate clinical
research data into the i2b2 (Informatics for Integrating Biology
and the Bedside) data model including both ontology and fact data
[26,46]. Leroux and Lefort [82] used ODM to drive the creation of
RDF data cubes from longitudinal study data.
The base ODM standard has also been considered for use as a
submission standard. In 2007 the FDA announced a pilot to test
electronic CRF submissions in ODM instead of the currently
required PDF format [87]. The FDA commented that PDF CRFs did
not meet their needs, and that a suitable replacement would pro-
vide access to the CRF data, metadata, and audit trail [87]. That
pilot was put on hold prior to completion.
3.3.2. ODM enhancement opportunities identiﬁed in the literature for
data collection
ODM’s relative simplicity has at times also been a limiting fac-
tor impacting all aspects of interoperability including data map-
ping,
representing
semantics,
data
types,
and
terminology
support. The ODM hierarchical structure, based on the elements
shown in Fig. 3, most clearly expresses CRF-oriented data [82,84],
and in the cases of the Deﬁne-XML and Dataset-XML, extensions
have been used to represent tabular datasets [14,15].
Despite its usefulness as an interchange standard, ODM pro-
vides limited support for data mapping information due to the lack
of semantics associated with the data elements [45]. The use of the
CDASH standard [24] CRF data elements in ODM format helps by
providing standard naming conventions, and ultimately BRIDG
[88] was intended to provide the missing semantics. However,
applications using BRIDG to support data interchange semantics
have been limited, and BRIDG does not include the bindings to con-
trolled terminologies [85].
ODM does not provide the formal mechanisms needed to cap-
ture the semantics necessary for automated interchange [35]. As
noted previously, Alias can be used to represent semantics, but
since Alias can contain any content its usefulness in support of
automated interpretation is limited [60]. Vendor extensions can
be developed to represent semantics in ODM, but these extensions
are not part of the normative ODM standard [2,52].
3.4. Data tabulations and analysis
3.4.1. ODM usage in data tabulations and analysis
The Deﬁne-XML standard is an ODM extension that provides
metadata to describe tabular datasets that, when used within the
context of the CDISC content standards, typically describes all the
SDTM, ADaM, or SEND datasets for a study [9,89–93]. Deﬁne-
XML plays a key role in establishing traceability in regulatory sub-
mission datasets [94]. The FDA added Deﬁne-XML to its Study Data
Speciﬁcations in March of 2005 [3,9], and in December 2016 it will
become a requirement for submissions to the FDA [3,14]. The FDA
requirement to use the relatively archaic SAS V5 XPORT format for
submission data has necessitated that the metadata be provided in
a separate document [9]. To support the submission process, the
ability to validate the Deﬁne-XML metadata has become increas-
ingly important necessitating the development of validation rules
and the tools that apply them, such as OpenCDISC [95] or the CDISC
Deﬁne.xml Checker [96]. Kubick et al. [9] also note that the type of
rich metadata provided in Deﬁne-XML is necessary for supporting
integrated clinical research data repositories.
As a metadata standard, Deﬁne-XML can be used to support
process automation much like the ODM metadata has been used
to generate CRFs and aid in study setup. However, in practice it
is often generated post hoc to satisfy the needs of a submission.
A more modern approach is to create the Deﬁne-XML metadata
before the datasets are created and use it as a speciﬁcation that
drives the creation of study datasets. Maddox [90,91] describes
how sponsors create Deﬁne-XML ﬁles as a speciﬁcation for the ser-
vice providers that will produce the SDTM submission [89–92].
Dataset-XML is a new CDISC standard that represents tabular
datasets in an ODM-based format and provides an alternative to
the SAS V5 XPORT format. Despite being a new standard, the FDA
has elected to pilot Dataset-XML as a possible alternative for sub-
missions [4]. Dataset-XML provides a truly vendor neutral dataset
exchange format without the limitations inherent in the older SAS
V5 XPORT format.
3.4.2. ODM enhancement opportunities identiﬁed in the literature for
data tabulations and analysis
Kubick et al. [9] note that Deﬁne-XML, though a signiﬁcant
improvement over deﬁne.pdf, still maintains an unnatural separa-
tion of metadata and data for clinical study datasets. The availabil-
ity
of
Dataset-XML
to
complement
Deﬁne-XML
provides
opportunities to further advance the available tools and subse-
quently improve reviewer productivity [9,15].
3.5. Study archival
3.5.1. ODM usage in study archival
The lifespan of regulated clinical trial data can extend to
50 years, and requires audit trails and investigator signatures.
Archival in a proprietary format demanded that the data collection
S. Hume et al. / Journal of Biomedical Informatics 60 (2016) 352–362
357


### Page 7

software and its operating environment, which often included the
hardware, be archived to provide a validated platform to work with
the data. ODM provides a non-proprietary means to archive data
that meets the US federal regulations, and does not require the
archival of proprietary software to support the use of the data
[74,97].
As an XML standard, ODM is well suited as a long-term archival
solution that maintains the integrity of the data and metadata as
captured from the original systems in a system-neutral, open for-
mat. ODM maintains the clinical data collected for a study, a full
audit trail, electronic signatures, and the basic information needed
for 21 CFR Part 11 and good clinical practice compliance [10,73].
Kuchinke et al. [97] describe ODM as a structure that organizes
the archived metadata and data together into a hierarchy based
on the ‘‘CRF metaphor”. An increasing number of EDC systems
directly export to ODM facilitating its use for archival [86].
3.5.2. ODM enhancement opportunities identiﬁed in the literature for
study archival
While ODM provides the means to function as an archive for the
study data and metadata, this represents one component of a com-
plete study archive that would include other artifacts such as the
study master ﬁle [97]. As noted previously, since ODM does not
maintain presentation metadata it must be maintained in an
extension, style sheet, or some other application capable of visually
rendering the CRFs. File size has also been noted as an issue in
ODM archives with ﬁle sizes ranging up to 2 GB per study [97].
Kuchinke et al. [97] note that using ODM as the source docu-
ment archive to permit the destruction of the original paper data
requires a legally compliant electronic signature. The ODM stan-
dard does not specify the level at which signatures should be cre-
ated, and legally valid electronic signatures can be challenging to
administer and maintain [97].
4. Discussion
Originally, ODM was collaboratively developed by a small CDISC
team to meet the speciﬁc needs of clinical research data collection
and management systems. From a data modeling perspective,
ODM covered the fundamental elements of form-based data to
meet the needs of regulated clinical research. ODM usage has
expanded to cover new phases of the clinical research lifecycle,
and now covers tabular data models in addition to the original
hierarchical form-based model. As a standard authored by clinical
research and XML experts, ODM has maintained an ease of under-
standing and use that has eluded XML standards generated from
models, such as those generated using the HL7 RIM. The HL7 RIM
put the needs of modelers ahead of the needs of implementers
[98] making HL7 v3 difﬁcult to implement, while ODM focused
more directly on the needs of implementers. The ODM form-
based model represents CRF data elements in a relatively simple
manner, and limits the use of modeling abstractions favored by
many of the healthcare information models, such as the HL7 RIM
or BRIDG. ODM has itself been used as a model by software imple-
menters creating solutions for clinical research. ODM has more in
common with the relatively new HL7 Fast Healthcare Interoper-
ability Resources (FHIR) standard, as the two share a number of
design principles such as making use of extensions for edge cases
and human readability.
4.1. Categorizing the literature by clinical research data lifecycle phase
The ODM literature reference counts by lifecycle phase for arti-
cles that met the inclusion criteria for this paper are shown in
Table 1.
A total of 85 literature articles address the initial 3 phases of the
clinical research data lifecycle, while only 8 articles address the last
2 phases. Tables 2 and 3 in Appendix A provide a succinct synopsis
of the most salient points identiﬁed for each lifecycle phase. The
literature provides more coverage for study metadata than for clin-
ical data. Almost no academic articles cover Deﬁne-XML, despite
the fact that it is the most widely used ODM-based standard due
to its position as a component of FDA regulatory submissions
[3,14]. The disparity between practitioner use and academic
research may stem from the fact that academic institutions rarely
pursue drug commercialization directly, but typically partner with
bio-pharmaceutical companies to manage that phase of drug
development when applicable. Many academic research projects
are limited to a single site or integrated delivery network and
therefore have had no need to transfer data between sites or to a
regulator. This is rapidly changing with new data sharing perspec-
tives and requirements [99].
4.2. Recommendations for future research and development
The recommendations for future ODM research and develop-
ment were developed from (1) gaps in the literature, (2) ODM
enhancement opportunities identiﬁed in the literature and, (3)
new clinical research trends. These recommendations will be pro-
vided as inputs into a formal requirements analysis for the next
version of ODM planned by the CDISC XML Technologies team to
begin in 2016. All authors provided input into the recommenda-
tions, and an informal consensus process was used to determine
the following list.
4.2.1. Add support for RESTful web services
In current practice clinical research data transfers predomi-
nantly occur in periodic batches, often times by sending the data
for a full study in each exchange. Although the web-services based
CDISC SHARE API returns ODM-based content and some vendors
have implemented ODM-based web services [100], ODM lacks
explicit support for modern exchange mechanisms like RESTful
web services. The ODM speciﬁcation does not include the means
to automatically retrieve information using web services, as is
the case in HL7 FHIR [101]. Leroux et al. [102] made a comparison
and mapping between HL7 FHIR and CDISC ODM with the goal of
achieving semantic interoperability between clinical research and
healthcare. They present an approach to integrating ODM with
FHIR leading to a mapping of hierarchical ODM ClinicalData ele-
ments to a set of FHIR resources [102]. Adding RESTful web ser-
vices support to ODM and specifying a standardized web services
API for the incremental exchange of ODM content would advance
the state of practice today. Future ODM research and development
would beneﬁt by an examination of the HL7 FHIR approach to sup-
porting RESTful interfaces, document-oriented aggregation, and
semantic interoperability [98,102].
Table 1
Article references by lifecycle phase.
EDC and EHR
infrastructure
Planning
Data collection
Data tabulations
and analysis
Study
archival
Article references
[1,2,20–44]
[2,11,13,20–23,45,47–68]
[2,13,26,35,43,45,46,52,53,57,58,60,62–64,73–85]
[9,89–93]
[74,97]
Article counts
27
30
28
6
2
358
S. Hume et al. / Journal of Biomedical Informatics 60 (2016) 352–362


### Page 8

4.2.2. Extend ODM to enable full lifecycle data traceability
Data ﬁtness is fundamental to FDA submissions, and validation
rules for the CDISC standards continue to grow in their importance
as a key to applying the standards effectively [94]. As the use of
validation has grown for FDA submissions, validating CDISC data-
sets has also grown into a common practice for Contract Research
Organizations performing data services for sponsoring organiza-
tions. Inquiries into data quality within the context of ODM-
based standards and the optimal means of ensuring quality, both
before and during the validation step, would beneﬁt the clinical
research community. The FDA has identiﬁed a lack of traceability
as one of the top 7 data standards issues [103]. Today no tools exist
capable of tracing a data element from the protocol through to the
clinical study report tables, listings, and ﬁgures [104]. No query
capability exists to easily assess traceability within the context of
the CDISC standards. Given ODM’s role in representing study meta-
data, machine-readable traceability represents another opportu-
nity for further development of ODM-based standards [94].
4.2.3. Extend and evaluate ODM as an end-to-end standard
representing all phases of the clinical research data lifecycle
ODM has a cogent, stable underlying data model that, through
extensions, has also proven quite versatile [13] with regard to its
ability to represent study setup and CRF metadata. New Protocol-
XML and CTR-XML extensions will broaden the existing lifecycle
coverage provided by extensions, including Deﬁne-XML, Dataset-
XML, SDM-XML, and CT-XML. This list of extensions represents
an increasingly comprehensive set of metadata that supports the
automated generation of a growing number of study artifacts.
Research highlighting ODM’s use in an end-to-end context from
protocol through submission, where each state in the data lifecycle
has an explicit relationship to the next, could help identify gaps or
innovations that would improve its effectiveness to support clini-
cal research process automation.
Study data archival is a strength of ODM and when linked to
SDTM datasets, ADaM datasets, and EHRs it can become part of
an end-to-end archive. Deﬁne-XML and Dataset-XML could aid in
the archival of datasets, making it possible to archive the study
datasets along with the ODM-based CRF data. New Protocol-XML
and CTR-XML extensions will further extend the types of informa-
tion that ODM can archive. The archival of study data is a time con-
suming and expensive proposition. Research into extensions that
enhance ODM’s ability to function as an end-to-end data archive
that captures a broader set of study artifacts would make a useful
addition to the knowledge base.
Several efforts are underway to progress the development of a
standardized protocol [105]. These efforts will form the foundation
of a Protocol-XML standard scheduled to begin development in late
2016. A project to enhance CTR-XML to include study results is also
planned to commence in late 2016. As these standards are
released, an academic examination of their relative strengths and
weaknesses could expedite their maturation. With the availability
of a Protocol-XML standard, research into the tools and techniques
for building studies based on a structured protocol would improve
the quality and efﬁciency of the clinical research data lifecycle.
4.2.4. Extend ODM’s ability to represent semantics in a standardized
way
Despite the fact that the use of semantically annotated ODM
was a clear trend in the research literature, scalable semantic inter-
operability within healthcare and clinical research remains an
unsolved problem [61]. The need to provide a standardized way
to link to external code systems that does not rely on naming con-
ventions was mentioned by a number of articles [23,32,60,61].
ODM and healthcare standards like HL7 CDA provide the means
to develop structural and syntactic alignment, but comparing or
integrating data elements across different standards models
requires the addition of semantics provided by external code sys-
tems [61]. Currently, the semantics used by most EHR and EDC sys-
tems are localized to the speciﬁc system [32]. Future research
recommending an optimal approach to coding ODM data elements
and CodeListItems using external code systems, such that the
semantics are interpretable by software within a stated context,
will accelerate the Healthcare Link agenda [33,60,61].
4.2.5. Extend ODM to more completely represent MDR metadata
ODM-based standards will play an increasing role in clinical
research metadata repositories (MDR), and several research arti-
cles have highlighted the use of ODM in MDRs, including its align-
ment with ISO 11179 [13,60]. As the number and use of MDRs
grows, there will be opportunities to extend ODM to include the
additional metadata needed to better support metadata libraries
as demonstrated by the Eli Lilly ODM library [63]. The CDISC
SHARE MDR [69] currently exports CDASH metadata in ODM and
SDTM, ADaM, and SEND metadata in Deﬁne-XML. However, new
ODM features are required to represent the additional metadata
managed by the MDR, such as identifying the relationships
between CDASH and SDTM variables, the CDASH prompt, CRF com-
pletion instructions, CDASH and SDTM core, and the CDISC notes.
ODM would beneﬁt from research that explores the additional
metadata features needed to expand ODM’s role as a standard for
representing metadata library content.
4.2.6. Examine the use of ODM in the submission context to
complement Deﬁne-XML
Research exists on the automated analysis of CRFs [43,81], but
none have analyzed the CRF from a regulatory perspective. The
beneﬁts proposed in the 2007 FDA pilot [87] could be explored.
For example, examining mechanisms for analyzing the ODM audit
trail for fraud detection would be highly relevant. An analysis of
how end-to-end traceability could be enhanced using ODM CRFs
together with Deﬁne-XML would improve the case for submitting
CRF data as ODM.
4.2.7. Examine the use of Deﬁne-XML to drive automation
Deﬁne-XML’s broad use by industry has been driven by the
FDA’s requirement that ‘‘a properly functioning deﬁne.xml ﬁle is
an important part of the submission of standardized electronic
datasets and should not be considered optional” [106]. Deﬁne-
XML can be used to specify metadata in support of the automated
generation of datasets, and it is being used in this manner by the
FDA’s Janus Clinical Trial Repository. As Deﬁne-XML’s role in driv-
ing the automation of end-to-end data management, data analysis,
and aggregation increases, an evaluation of Deﬁne-XML’s adequacy
to support these use cases would help drive future development of
the standard.
Using Deﬁne-XML together with the new Dataset-XML standard
creates a number of opportunities to enhance how datasets are
organized and represented for regulatory submission and data
interchange [4]. Combining Dataset-XML’s support for tabular data
structures with ODM’s hierarchical structures could prove useful to
capture the growing blend of heterogeneous data structures found
in a future where a broad array of third party devices are used to
capture patient data. Dataset-XML was designed to complement
Deﬁne-XML, but as a new standard no literature exists analyzing
the ﬁtness of Dataset-XML as a dataset standard.
4.2.8. Create a set of standard validation rules to validate ODM-based
standards across the clinical research data lifecycle
Now that datasets can be represented using an ODM-based
extension, opportunities exist to create a standardized language
for validating Deﬁne-XML and Dataset-XML content. A W3C stan-
S. Hume et al. / Journal of Biomedical Informatics 60 (2016) 352–362
359


### Page 9

dard language like XQuery has been used to process ODM-based
content [2], and when combined with the schema and schematron
rules might provide a standardized, executable language that
works across all ODM-based standards. Additional research is
needed to determine a vendor neutral formalism for expressing
validation logic for verifying the structure and content of ODM-
based CRFs as well as Dataset-XML datasets. Validation rules have
become a prerequisite for the use of a standard in a regulatory sub-
mission context, and expressing unambiguous validation rules that
can easily be converted to a computable format would advance the
acceptance of the standards.
4.2.9. Extend ODM to better support data transformations and model-
driven development
Research contributing to an optimal solution for incorporating
data mapping metadata into ODM, as noted in [45], would beneﬁt
the development of ODM as a standard that not only represents
data and metadata states within the clinical research data lifecycle,
but also describes how to transition from state-to-state in support
of an end-to-end data standard.
ODM is used as much for study metadata as it is for data. ODM’s
ﬂexibility and relative simplicity make efﬁcient software based
generation of data structures and CRFs possible [27]. The feasibility
of model-driven architecture (MDA) in clinical research has been
signiﬁcantly improved by the availability of XML models like
ODM. XML models support MDA’s ability to generate useful soft-
ware applications [54]. De Melo et al. [52] used ODM metadata
in an MDA application to generate user interfaces for mobile
devices. More research exploring ways to extend ODM to support
code generation and other model driven approaches to software
development could help improve both the productivity and quality
of automated clinical research data processing.
4.2.10. Add support for sharing de-identiﬁed data in support of
secondary use
Open science, data sharing, and transparency are topics cur-
rently being explored by the clinical research community, but so
are topics such as patient privacy and informed consent compli-
ance. Standards like ODM beneﬁt data sharing and open science
because diverse, non-standard ways of collecting and representing
clinical research data make it overly complex to integrate, pool, or
share data for secondary analysis [107]. The FDA has stated that
making de-identiﬁed and masked clinical data available for study
by external experts could aid in the development of innovative
new medical products, while also meeting the expectations of
the patients by maximizing the use of their data [7]. Sharing unde-
cipherable data, or data not supported by existing tools, does not
advance the cause of openness and transparency. Thus, the CDISC
standards must support a standard means of de-identifying data-
sets, including the ODM-based standards. Additional research
demonstrating how ODM can be effectively used and extended in
support of secondary use and big data would be of keen interest
to the academic and practitioner communities. Improved ODM
data citation support, to include an extension to better support
the Dublin Core, would make attribution easier and encourage data
sharing [108].
5. Conclusions
The relative simplicity and human readability of ODM has
undoubtedly contributed to its success and broad implementation
as a data and metadata standard. Maintaining a coherent core ODM
model that accommodates most use cases, while supporting exten-
sions to handle edge cases, has kept the standard easy for develop-
ers to learn and use. The selection of ODM for use in cases outside
of clinical research, such as for representing medical forms or
exchanging autopsy data, is a testament to the utility of its health-
care forms-oriented design. However, updates to ODM are needed
both to address limitations as well as to keep it relevant as new
automation and interoperability opportunities arise in both clinical
research and healthcare. Based on the applications of ODM
described in the literature, the future success of ODM may depend
on how well it links to: (1) content described by other healthcare
standards, (2) controlled terminologies, (3) externally deﬁned
semantics identifying ODM content, and (4) other ODM-based
standards representing the different phases of the clinical research
data lifecycle from protocol through analysis results.
Conﬂict of interest
Sam Hume performed this work as a student at Dakota State
University, but he is the co-lead of the CDISC XML Technologies
Team. CDISC did not fund this research, and we made every effort
to give equal time to the strengths and limitations of the CDISC
ODM standard. In fact, the limitations will be used as input to a
roadmap for future ODM development.
Acknowledgments
This research was supported in part (VH) by the Intramural
Research Program of the National Institutes of Health (NIH)/
National Library of Medicine (NLM)/Lister Hill National Center for
Biomedical Communications (LHNCBC). We wish to thank Wayne
Table 2
Summary of ODM strengths.
Lifecycle phase
Summary of key ODM strengths
EDC and EHR
infrastructure
ODM’s ﬂexibility and relative simplicity have enabled it to be successfully applied across a number of EHR integration and single source
projects. The Retrieve Form for Data Capture Proﬁle (RFD) is a technical framework available to support EHR and ODM integration. ODM is
broadly accepted for data collection in clinical research making it the logical target for EHR integration. ODM is increasingly listed alongside
HL7 CDA as a supported XML format for healthcare informatics applications. Several European projects are currently working on EHR and
EDC integration, including semantic interoperability
Planning
ODM metadata has become the language of choice for describing CRFs, and has been used broadly for generating user interfaces. The ability
to design a study in one system, export it in ODM, and import it into another system has been demonstrated. A study design ODM extension,
SDM-XML v1.0, is currently available, and a draft CTR-XML clinical trial registry extension has been released for public review
Data collection
The ODM standard is mature, stable, relatively simple to work with, and supported by a broad number of data capture software vendors. The
ODM model includes the information necessary to support the clinical research data collection process, including audit trail and digital
signatures. Clinical research data web services using ODM have been demonstrated, and ODM has been shown to work as a document or a
message
Data tabulations and
analysis
Deﬁne-XML supports ﬂexibility in structural representations, and provides a rich set of metadata describing the clinical research datasets.
Deﬁne-XML is broadly used in practice due to its position as a required component of a FDA regulatory submission. Dataset-XML is a new
standard for representing data as tabular datasets, such as SDTM or ADaM, that complements the Deﬁne-XML metadata
Study archival
ODM maintains all the clinical data collected for a study together with the study metadata, and also contains the full audit trail, including
electronic signatures. A signiﬁcant number of data capture and management systems directly export to ODM as an out-of-the-box feature
360
S. Hume et al. / Journal of Biomedical Informatics 60 (2016) 352–362


### Page 10

Kubick, Rebecca Kush, and Landen Bain of CDISC, and Sally Cassells
of Next Step Clinical Systems for their insightful comments on a
draft version of this work. Sam Hume and Sally Cassells co-lead
the CDISC XML Technologies Team.
Appendix A. Summary of ﬁndings
See Tables 2 and 3.
References
[1] CDISC, Clinical Data Interchange Standards Consortium, 2014 <http://www.
cdisc.org/>.
[2] C. Forster, G. Vossen, Exploiting XML Technologies in Medical Information
Systems, in: BLED 2012, 2012.
[3] FDA, Study Data Speciﬁcations v1.5.1, FDA, 2010.
[4] FDA, Transport Format for the Submission of Regulatory Study Data; Notice of
Pilot Project, D.o.H.a.H. Services (Ed.), United States Government: Federal
Register, 2013, pp. 70954–70955.
[5] ONC, The Standards and Interoperability Framework, 2015 <http://wiki.
siframework.org/> (27-Jan-2015).
[6] D. Blumenthal, Launching HITECH, N. Engl. J. Med. 362 (5) (2010) 382–385.
[7] FDA, Availability of Masked and De-identiﬁed Non-Summary Safety and
Efﬁcacy Data; Request for Comments, D.o.H.a.H. Services (Ed.), United States
Government: Federal Register, 2013, pp. 33421–33423.
[8] K. Getz, Technology Regulation Consolidation and Study Volunteer Trends,
2013.
[9] W.R. Kubick, S. Ruberg, E. Helton, Toward a comprehensive CDISC submission
data standard, Drug Inform. J. 41 (3) (2007) 373–382.
[10] FDA, Guidance for Industry Part 11, Electronic Records; Electronic Signatures
– Scope and Application, FDA (Ed.), 2003, FDA.gov.
[11] S. Garde et al., Can openEHR archetypes empower multi-centre clinical
research?, Stud Health Technol. Inform. 116 (2005) 971–976.
[12] S. Hume, Connecting at the Connectathon, in: Applied Clinical Trials, 2001,
UBM Advanstar.
[13] S. Ngouongo, M. Löbe, J. Stausberg, The ISO/IEC 11179 norm for metadata
registries: does it cover healthcare standards in empirical research?, J
Biomed. Inform. 46 (2) (2013) 318–327.
[14] CDISC, Deﬁne-XML Speciﬁcation Version 2.0, CDISC, 2013.
[15] CDISC,
CDISC
Dataset-XML
Speciﬁcation
Version
1.0,
Clinical
Data
Interchange Standards Consortium, 2014.
[16] CDISC, CDISC Study Design Model in XML (SDM-XML), Clinical Data
Interchange Standards Consortium, 2011.
[17] CDISC, Representing Controlled Terminology in ODM, CDISC, 2011.
[18] CDISC, Analysis Results Metadata Speciﬁcation Version 1.0 for Deﬁne-XML
Version 2 – Draft, Clinical Data Interchange Standards Consortium: CDISC,
2014.
[19] CDISC, Overview of the CDISC Operational Data Model for Clinical Data
Acquisition and Archive (based on CDISC ODM DTD 1.1 DRAFT), CDISC, 2001.
[20] G. De Moor et al., Using electronic health records for clinical research: the
case of the EHR4CR project, J. Biomed. Inform. 53 (2015) 162–173.
[21] G.B. Laleci, M. Yuksel, A. Dogac, Providing semantic interoperability between
clinical care and clinical research domains, IEEE J. Biomed. Health Inform. 17
(2) (2013) 356–369.
[22] P. Bruland, M. Dugas, Transformations between CDISC ODM and openEHR
Archetypes, Stud. Health Technol. Inform. 205 (2014) 1225.
[23] B. Breil, M. Dugas, Analyses of medical data models-identifying common
concepts and items in a repository of medical forms, Stud. Health Technol.
Inform. 192 (2012) 1052–1052.
[24] CDISC, Clinical Data Acquisition Standards Harmonization (CDASH), Clinical
Data Interchange Standards Consortium, 2011.
[25] C. Daniel et al., Standard-based integration proﬁles for clinical research and
patient safety, in: AMIA Summits on Translational Science Proceedings, 2013,
2013, p. 47.
[26] C. Ohmann, W. Kuchinke, Future developments of medical informatics from
the viewpoint of networked clinical research, Meth. Inform. Med. 48 (1)
(2009) 45–54.
[27] R. Kush et al., Implementing single source: the STARBRITE proof-of-concept
study, J. Am. Med. Inform. Assoc. 14 (5) (2007) 662–673.
[28] A. Anastasiou, E. Ifeachor, J. Zajicek, Data modeling methods in clinical trials:
experiences from the clinical trial methods in neurodegenerative diseases
project, Trials 12 (Suppl. 1) (2011) A15.
[29] CDISC, Leveraging the CDISC Standards to Facilitate the use of Electronic
Source Data within Clinical Trials, CDISC eSDI Group, 2006.
[30] L. Alschuler, L. Bain, R. Kush, Improving data collection for patient care and
clinical trials, Sci. Career Mag. Mar. 26 (2004).
[31] A.N. El Fadly et al., CDA Template for eCRFs REUSE Project, in: International
HL7 Interoperability Conference, Kyoto, Japan, 2009.
[32] A.N. El Fadly et al., Integrating clinical research with the healthcare
enterprise: from the RE-USE project to the EHR4CR platform, J. Biomed.
Inform. 44 (2011) S94–S102.
[33] B. Breil et al., Multilingual medical data models in ODM format–a novel form-
based approach to semantic interoperability between routine health-care and
clinical research, Appl. Clin. Inf. 3 (2012) 276–289.
[34] A. El Fadly et al., Electronic Healthcare Record and clinical research in
cardiovascular radiology. HL7 CDA and CDISC ODM interoperability, in: AMIA
Annual Symposium Proceedings, American Medical Informatics Association,
2007.
[35] G.B.L. Erturkmen et al., Building the semantic interoperability architecture
enabling sustainable proactive post market safety studies, 2011.
[36] A. Fadly et al., Aligning HL7 CDA Templates and CDISC ODM: An Experiment
in Cardiovascular Radiology, in: Medinfo 2007: Proceedings of the 12th
World Congress on Health (Medical) Informatics; Building Sustainable Health
Systems, IOS Press, 2007.
[37] P.
Bruland,
C.
Forster,
M.
Dugas,
x4T-EDC:
a
prototype
for
study
documentation based on the single source concept, in: 24th International
Conference of the European Federation for Medical Informatics, 2012.
[38] P. Dziuballe et al., The single source architecture x4T to connect medical
documentation and clinical research, Stud. Health Technol. Inform. 169
(2010) 902–906.
[39] P. Bruland et al., Does single-source create an added value? Evaluating the
impact
of
introducing
x4T
into
the
clinical
routine
on
workﬂow
modiﬁcations, data quality and cost–beneﬁt, Int. J. Med. Inform. 83 (12)
(2014) 915–928.
[40] CDISC, CDISC Healthcare Link Initiative, <http://www.cdisc.org/healthcare-
link>, 2014 (cited 2014 18-Dec-2014)
[41] A. El Fadly et al., The REUSE project: EHR as single datasource for biomedical
research, Stud. Health Technol. Inform. 160 (Pt 2) (2010) 1324–1328.
[42] B. Bernhard et al., HIS-based Kaplan-Meier plots-a single source approach for
documenting and reusing routine survival information, BMC Med. Inform.
Decis. Mak. 11 (2011).
[43] R. Krumm et al., The need for harmonized structured documentation and
chances of secondary use–Results of a systematic analysis with automated
form comparison for prostate and breast cancer, J. Biomed. Inform. (2014).
[44] M. Marcos et al., Interoperability of clinical decision-support systems and
electronic health records using archetypes: a case study in clinical trial
eligibility, J. Biomed. Inform. 46 (4) (2013) 676–689.
[45] R.L. Richesson, P. Nadkarni, Data standards for clinical research data
collection forms: current status and challenges, J. Am. Med. Inform. Assoc.
18 (3) (2011) 341–346.
[46] T. Ganslandt et al., Unlocking data for clinical research – The German i2b2
Experience, Appl. Clin. Inform. 2 (1) (2011) 116.
Table 3
Summary of ODM limitations.
Lifecycle phase
Summary of key ODM limitations
EDC and EHR
infrastructure
Most of the health IT integration successes have accomplished interoperability at the syntactic level. As long as the mapping needed for
interoperability between healthcare and clinical research remains a manual process, this will prevent the large scale adoption of the ODM/
CDA integration. Integration between terminologies is particularly challenging since HL7 uses terminologies differently than ODM.
Integrating semantics typically relies on ODM’s Alias element which relies on a common naming strategy rather than a more formal
mechanism
Planning
By design, ODM does not include presentation information. ODM does not include a standard language for expressing computation and
validation logic, including regular expression support. The main limitation restricting the use of ODM support for protocol has been the lack
of a completed content model
Data collection
A standardized approach to using ODM with web services has not emerged. ODM does not include the metadata to capture the semantics or
mapping information needed to facilitate computable semantic interoperability with other systems
Data tabulations and
analysis
Deﬁne-XML, though a signiﬁcant improvement over deﬁne.pdf, still maintains an unnatural separation of metadata and data for clinical
study datasets. Minimal academic research has investigated Deﬁne-XML despite its importance to practitioners
Study archival
ODM is not a comprehensive study archive that represents or provides links to the study documentation that must be archived in addition to
the study data. Since ODM does not maintain presentation oriented metadata a style sheet or some other mechanism for recreating the visual
aspects of the clinical data system must be maintained. File size has sometimes been noted as an issue with XML and ODM archives
S. Hume et al. / Journal of Biomedical Informatics 60 (2016) 352–362
361


### Page 11

[47] J. Aerts, Generating a caBIG patient study calendar from a study design in
ODM with study design model extension, CDISC J. (2011).
[48] N.S. Nepochatov, Translational research web application framework, Transl.
Res. (2009).
[49] C. Willoughby et al., A standard computable clinical trial protocol: the role of
the BRIDG model, Drug Inform. J. 41 (3) (2007) 383–392.
[50] G. Karam, International clinical trials registry platform, in: CDISC European
Interchange 2014, Paris, France, 2014.
[51] V.
Huser,
Using
CDISC
standards
to
create
formal
and
computable
representations of human clinical research protocols, in: NIH Research
Festival, NIH, Bethesda, MD, 2014.
[52] G.M. De Melo, J. Nagler-Ihlein, M. Weber. Generating user interfaces from
CDISC ODM for mobile devices, in: International Conference on Mobile
Business, 2006, ICMB’06, IEEE, 2006.
[53] E. Tröger et al., Ophthabase: a generic extensible patient registry system, Acta
Ophthalmol. 86 (s243) (2008).
[54] C. Crichton et al., Metadata-driven software for clinical trials, in: Proceedings
of the 2009 ICSE Workshop on Software Engineering in Health Care, IEEE
Computer Society, 2009.
[55] E. Domínguez et al., Model-driven development based transformation of
stereotyped class diagrams to XML schemas in a healthcare context,
Advances in Conceptual Modeling–Foundations and Applications, 2007, pp.
44–53.
[56] L.L. Fu, T. Chen, Web-based case report form design for clinical trial, Appl.
Mech. Mater. 39 (2011) 19–24.
[57] T. Kiuchi et al., Legal medicine information system using CDISC ODM, Leg.
Med. 15 (6) (2013) 332–334.
[58] W. Kuchinke et al., Extended cooperation in clinical studies through exchange
of CDISC metadata between different study software solutions, Methods Inf.
Med. 45 (4) (2006) 441.
[59] J. Yeom, S. Jung, H. Kim, Language Supports for Multinational Clinical Trials in
CDISC Platform, 2013.
[60] P. Bruland et al., Interoperability in clinical research: from metadata registries
to semantically annotated CDISC ODM, Stud. Health Technol. Inform. 180
(2012) 564.
[61] B. Breil et al., Semantic enrichment of medical forms-semi-automated coding
of ODM-elements via web services, Stud. Health Technol. Inform. 180 (2011)
1102–1104.
[62] M. Dugas, S. Dugas-Breit, Integrated data management for clinical studies:
automatic transformation of data models with semantic annotations for
principal investigators, data managers and statisticians, PLoS ONE 9 (2)
(2014) e90492.
[63] LillyODMLibrary, E.L.a. Company (Ed.), <http://lillyodmlibrary.codeplex.com/
>, 2012 (no longer available).
[64] M. Dugas, B. Breil, Open Medical Data Models: A Prototype of an Exchange
Platform for Medical Forms, 2012.
[65] A. Shabo, S. Rabinovici-Cohen, P. Vortman, Revolutionary impact of XML on
biomedical information interoperability, IBM Syst. J. 45 (2) (2006) 361–372.
[66] D. Abler et al., Models for forms, in: Proceedings of the Compilation of the Co-
located Workshops on DSM’11, TMC’11, AGERE!’11, AOOPES’11, NEAT’11, &
VMIL’11, ACM, 2011.
[67] J. Davies et al., The cancergrid experience: metadata-based model-driven
engineering for clinical trials. Science of Computer Programming, 2013.
[68] P.M. Nadkarni, R. Kemp, C. Parikh, Leveraging a clinical research information
system to assist biospecimen data and workﬂow management: a hybrid
approach, J. Clin. Bioinform. 1 (2011) 22.
[69] CDISC, CDISC SHARE, <http://cdisc.org/cdisc-share>, 2015 (27-Jan-2015).
[70] CDISC, CDISC Protocol Representation Model Version 1.0, CDISC: cdisc.org,
2010.
[71] V. Huser et al., Standardizing data exchange for clinical research protocols
and case report forms: an assessment of the suitability of the clinical data
interchange standards consortium (CDISC) operational data model (ODM), J.
Biomed. Inform. 57 (2015) 88–99.
[72] CDISC, Speciﬁcation for the Operational Data Model, Clinical Data Interchange
Standards Consortium, 2013.
[73] P.-Y. Lastic, The Convergence of Healthcare and Clinical Research Standards,
2007.
[74] T. Souza, R. Kush, J.P. Evans, Global clinical data interchange standards are
here!, Drug Discov Today 12 (3) (2007) 174–181.
[75] J.
Bickel,
J.
Gregoric,
i2b2
Community:
ODM
to
i2b2
importer,
<https://community.i2b2.org/wiki/display/ODM2i2b2/Home>
2014
(29-
Nov-2014).
[76] G.
Jiang
et
al.,
A
collaborative
framework
for
representation
and
harmonization of clinical study data elements using semantic MediaWiki,
in: AMIA Summits on Translational Science Proceedings, 2010, 2010, p. 11.
[77] T.M. Deserno et al., Integrating image management and analysis into
OpenClinica using web services, in: SPIE Medical Imaging, International
Society for Optics and Photonics, 2013.
[78] D. Haak et al., OC ToGo: bed site image integration into OpenClinica with
mobile devices, in: SPIE Medical Imaging, International Society for Optics and
Photonics, 2014.
[79] F. Lingli, D. Sheng, C. Tao, Clinical data management system, in: International
Conference on Biomedical Engineering and Computer Science (ICBECS), 2010,
2010.
[80] S.A. Wang et al., Performance of using Oracle XMLDB in the evaluation of
CDISC ODM for a clinical study informatics system, in: 17th IEEE Symposium
on Computer-Based Medical Systems, 2004, CBMS 2004, Proceedings, IEEE,
2004.
[81] M. Dugas et al., Automated UMLS-based comparison of medical forms, PLoS
ONE 8 (7) (2013) e67883.
[82] H. Leroux, L. Lefort, Using CDISC ODM and the RDF data cube for the semantic
enrichment of longitudinal clinical trial data, in: SWAT4LS, Citeseer, 2012.
[83] C.A. Brandt et al., Metadata-driven creation of data marts from an EAV-
modeled clinical research database, Int. J. Med. Inform. 65 (3) (2002) 225–
242.
[84] L. Lefort, H. Leroux, Design and generation of linked clinical data cubes, in: 1st
International Workshop on Semantic Statistics (SemStats), 2013.
[85] D.B. Fridsma et al., The BRIDG project: a technical report, J. Am. Med. Inform.
Assoc. 15 (2) (2008) 130–137.
[86] CDISC, ODM Certiﬁed Products <http://cdisc.org/odm-certiﬁed-products>,
2014.
[87] FDA, Electronic Case Report Form Submission; Notice of Pilot Project, D.o.H.a.
H. Services (Ed.), Federal Register, 2007, pp. 11370–11371.
[88] BRIDG, BRIDG Model Release 3.2 User’s Guide, BRIDG Semantic Coordination
Committee: NCI, 2012.
[89] M. Wheeldon, K. Burges, Discover Deﬁne-XML, in: PharmaSUG 2014, San
Diego, CA, 2014.
[90] J. Maddox, Round trip ticket – using the deﬁne.xml ﬁle to send and receive
your study speciﬁcations, in: PhUSE 2013, Brussels, Belgium, 2013.
[91] J. Maddox, Round trip ticket – using the deﬁne.xml ﬁle to send and receive
your study speciﬁcations, in: PhamaSUG 2014, San Diego, CA, 2014.
[92] G. Lightfoot, L. Jansen, Two-way Ticket, Please. . . All aboard the SAS Clinical
Standards Toolkit 1.5 Express, in: PhUSE 2013, Brussels, Belgium, 2013.
[93] H. Leroux et al., A method for the semantic enrichment of clinical trial data,
in: Health Informatics: Building a Healthcare Future Through Trusted
Information: Selected Papers from the 20th Australian National Health
Informatics Conference (HIC 2012), IOS Press, 2012.
[94] FDA, C. CDER (Ed.), Study Data Technical Conformance Guide, FDA, 2014.
[95] OpenCDISC, <http://www.opencdisc.org/>, 2014.
[96] J. Aerts, XML4Pharma <http://www.xml4pharma.com/>, 2014.
[97] W. Kuchinke et al., CDISC standard-based electronic archiving of clinical
trials, Methods Inf. Med. 48 (5) (2009) 408.
[98] G. Grieve, E. Kramer, L. McKenzie, Introduction to HL7 FHIR, in: HL7 Working
Group Meeting, Baltimore, MD: HL7, 2012.
[99] IOM, Sharing Clinical Trial Data: Maximizing Beneﬁts, Minimizing Risk,
Institute of Medicine, Washington, DC, 2015.
[100] A. Newbigging, Using web service technologies for incremental, real-time
data transfers from EDC to SAS, in: PhUSE 2010, PhUSE, Berlin, Germany,
2010.
[101] D. Raths, Top ten tech trends: catching FHIR, in: Healthcare Informatics,
Vendome
Healthcare
Media,
2014,
<http://www.healthcare-
informatics.com/>.
[102] H. Leroux, A. Metke-Jimenez, M. Lawley, ODM on FHIR: towards achieving
semantic interoperability of clinical study data, in: SWAT4LS International
Conference, Cambridge, England, 2015.
[103] D. Chhatre, A. Malla, CDER/CBER’s Top 7 CDISC Standards Issues, FDA, 2012.
[104] A. Dootson, Tracing data elements through a standard data ﬂow, in: PhUSE
2011, PhUSE, Brighton, UK, 2011.
[105] W. Kubick, 2015 CDISC Technical Plan, CDISC: cdisc.org, 2015.
[106] FDA, CDER Common Data Standards Issues Document Version 1.1, FDA, 2011.
[107] R. Kush, M. Goldman, Fostering responsible data sharing through standards,
N. Engl. J. Med. 370 (23) (2014) 2163.
[108] L. Hoyle et al., Comprehensive Citation Across the Data Life Cycle Using DDI,
2014.
362
S. Hume et al. / Journal of Biomedical Informatics 60 (2016) 352–362


---

## Visualizing and Validating Metadata Traceability within the CDISC Standards.pdf

_Path: `/Users/park/code/Paper2Skills-main/papers/Visualizing and Validating Metadata Traceability within the CDISC Standards.pdf`_

### Page 1

 
 
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


### Page 2

 
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


### Page 3

 
references to source variables found in a study’s Define-XML and ODM-XML files.  The new Source and 
SourceItem elements (Figure 1) containing the source variable references are identified using the trc namespace 
prefix used to classify Trace-XML extension content. The leafID provides a reference to the ODM-XML or Define-
XML file containing the reference and the ItemOID contains the reference to the source variable. Optional 
identifying information can also be provided in SourceItem, including a formal expression containing an XPath 
statement.  
 
 
Figure 1. Example Trace-XML extension to Define-XML shown with the trc namespace prefix 
The ability to explicitly reference source variables enables the Trace-XML software to generate the edges that 
connect the variables, computational methods, datasets, sub-forms, and forms into a graph representation. The 
ODM-XML and Define-XML content provides the variables, computational methods, datasets, sub-forms, and 
forms that become the nodes in the graph. The source references for each variable provided by the Trace-XML 
extension are added to the Origin element and a directed edge is created between the source and the target. The data 
flow within the clinical research lifecycle, from data collection through analysis results, is represented by directed 
edges within the graph. Any derivation or transformation that impacts the variable is also represented in the graph. 
Tracing a variable’s lineage requires following these edges from analysis content back to the data collection 
metadata. Each node on the graph can be opened to reveal the detailed metadata pulled from the ODM-XML or 
Define-XML content, such as a description of an algorithm used to transform the variable.  
 
Much of the metadata needed to generate the graph edges was retrieved using the CDISC SHARE metadata 
repository Application Programming Interface (API). When the CDISC CDASH standards are used the SHARE 
metadata can be applied by the Trace-XML software to automatically create the extended source reference metadata 
required by the Define-XML extension. Trace-XML saves the graph as XML using the standard GraphML XML 
format. This format is supported by a number of open-source software tools for viewing, filtering, and analyzing the 
resulting graph. 
 
Figure 2 shows a hierarchical visualization of a Trace-XML graph fragment for a study lifecycle that includes data 
collection, standardized tabulations, and analysis datasets. This example fragment highlights the demographic 
domain and shows a relatively small portion of a complete study graph that might include over 20 domains. 
Visualization tools, such as the yEd software used to render Figure 2, support the graph navigation and partitioning 
needed to analyze large graphs. A depth-first search (DFS) algorithm is used to establish reachability, which 
represents the flow of the data from collection through analysis, a forward trace.  
<ItemDef OID="SDTM.IT.USUBJID" Name="USUBJID" DataType="text" Length="30" SAS> 
    <Description> 
      <TranslatedText xml:lang="en">Unique Subject Identifier</TranslatedText> 
    </Description> 
    <def:Origin Type="Derived"> 
        <trc:Source> 
            <trc:SourceItem leafID="LF.ODM" ItemOID="ODM.IT.Common.StudyID"/> 
 
            <trc:SourceItem leafID="LF.ODM" ItemOID="ODM.IT.Common.SubjectID"/> 
        </trc:Source>              
    </def:Origin> 
</ItemDef> 
160


### Page 4

 
 
Figure 2. Full lifecycle Trace-XML graph fragment in a hierarchical layout  
 
Reachability must be established to prove traceability exists within the graph generated from the ODM-XML and 
Define-XML files. Given the directed graph, or digraph, Ga, any node m is reachable from node n in Ga if there 
exists a directed path from n to m. A DFS algorithm for digraphs will identify all and only those nodes reachable 
from a given node n in the digraph Ga18, 19.  Nodes that cannot be reached, but are expected to be reachable, are 
flagged as potential validation issues. Nodes with an Origin Type of “CRF”, “Derived”, and “Predecessor” must be 
reachable to be valid. The reachability test proceeds end-to-end across the clinical research lifecycle. The example 
used in this paper shows reachability that starts with the data collection CRF content in an ODM-XML file, connects 
to nodes in a standardized tabulation Define-XML file, which in turn connects to nodes in an analysis Define-XML 
file. Once reachability has been established, it can be shown that if node m is reachable from node n, then node n is 
traceable from node m. Thus, achieving reachability for the nodes in Ga asserts that traceability also exists18. 
 
Traceability can be visually assessed using the generated graph by viewing a predecessor sub-graph (Figure 3). This 
view is created from the full study graph and provides a complete view of traceability for the selected variable, in 
this case the vital signs analysis baseline flag. In Figure 3 the ODM-XML and Define-XML node identifiers are 
listed to the left of the predecessor graph and the metadata details for the selected node are shown on the right.  
 
Figure 3. A traceability view created from the full study graph 
 
161


### Page 5

 
Once traceability has been confirmed, the full trace of any individual variable or node can be shown in a report that 
returns the basic metadata for each node. The Trace-XML query takes as input the unique identifier of the variable, 
or node, of interest and returns every connected node that precedes it. The digraph with confirmed traceability 
makes this feasible. Trace-XML uses XQuery to return the metadata for each preceding node in the trace. The 
metadata shown below (Table 1) lists a sub-set of the information returned from a traceability query of the Pooled 
Site Group 1 analysis variable. The actual results include more details, such as a description of the computation 
method listed in #3.  
 
Table 1.  Example Trace-XML query results for the Pooled Site Group 1 analysis variable 
# 
OID 
Phase 
Element 
Type 
Description 
1 
ADAM.IT.ADSL.SITEGR1 
Analysis 
ItemDef 
Variable 
Pooled site group 1  
2 
ADAM.IG.ADSL 
Analysis 
ItemGroupDef 
Dataset 
Subject level analysis 
dataset 
3 
ADAM.MT.ADSL.SITEGR1 
Analysis 
MethodDef 
Derivation 
Computation method 
4 
SDTM.IT.SITEID 
Tabulation 
ItemDef 
Variable 
Study site identifier 
5 
SDTM.IG.DM 
Tabulation 
ItemGroupDef 
Dataset 
Demographics dataset 
6 
ODM.IT.COMMON.SITEID 
Data 
Collection 
ItemDef 
Variable 
Study site identifier 
7 
ODM.IG.COMMON 
Data 
Collection 
ItemGroupDef 
Sub-form 
Common variables 
8 
ODM.F.DM 
Data 
Collection 
FormDef 
CRF 
Demographics form 
 
A hyperlink to an HTML rendering of each variable’s Trace-XML query can be included in the output generated by 
the Define-XML stylesheet to make reviewing traceability easier for reviewers and decision makers. The image 
below (Figure 4) shows a partial view of a Define-XML that lists the vital signs analysis dataset ADVS with links to 
the individual variable traceability queries shown in the Source/Derivation/Comment column. These links provide 
data reviewers access to the detailed traceability information returned by a Trace-XML query that reaches back to 
the original source variable. 
 
Figure 4. Links to variable queries are added to Define-XML in the Source/Derivation/Comment column 
 
Using the graph and DFS-based algorithms provided by Trace-XML, metadata validation can be extended beyond 
individual Define-XML documents to cover the full clinical research data lifecycle as a means to improve data 
integrity. Using Trace-XML, the ODM-XML and multiple Define-XML documents may be validated as one study 
to ensure end-to-end validity across the clinical research data lifecycle. Unreachable or untraceable nodes may be 
reported as validation errors so that the Define-XML or ODM-XML files can be corrected to more accurately reflect 
the complete data flow through the lifecycle.  
 
The GraphML standard used by Trace-XML can be rendered or analyzed using a number of open-source software 
tools, and Trace-XML can be configured to include GraphML extensions used by specific software packages. Open-
source software tools such as yEd and Gephi provide alternative ways of conducting exploratory metadata analysis 
162


### Page 6

 
using visual analytics to quickly access how all the variables used within a study are related to one another. They 
generate a wide variety of visualization layouts based on the same study graph to suit specific exploratory analysis 
preferences. These tools also often generate graph metrics useful for analyzing and comparing study graphs. The 
graph below (Figure 5) was created using the yEd software using the directed tree layout. Large, full-lifecycle 
graphs are useful for exploring high-level data flows and permit a reviewer to zoom in on a graph fragment for a 
more detailed analysis. 
 
Figure 5. Full lifecycle Trace-XML graph in a directed tree layout for 2 domains: demographics and vital signs 
Discussion 
Trace-XML’s layered framework enables the model to represent traceability at multiple levels of abstraction. The 
hierarchical nature of the framework provides data reviewers with a high-level, abstract view of the entire information 
manufacturing process in Layer 1 that is integrated with increasingly detailed views of traceability in the subsequent 
layers. The IP-MAP model in Layer 1 provides a conceptual visualization of an IP’s manufacturing process that aids 
information consumers in identifying how data is being captured, transformed, stored, and utilized prior to becoming 
available to the decision maker20, 21.  A high-level conceptual model has become increasingly important as new 
information sources and new validation mechanisms have been introduced into the clinical research lifecycle. For 
example, FDA draft guidance on the use of Electronic Health Record (EHR) data in Clinical Investigations 
recommends that sponsors include a diagram of the data flow between the EHR and the clinical research systems22. 
Layer 2 adds the detailed metadata from the CDISC standards models that represent the clinical research data artifacts. 
Layer 3 adds the relationships, or edges, that link the metadata together to represent the flow of the clinical research 
data lifecycle for a study. For example, the full-lifecycle view for a single variable generated using Trace-XML queries 
benefits data reviewers by enabling them to visualize the flow of the data through each state in the clinical research 
data lifecycle for that variable. It also enables them to drill down into the metadata details needed to understand how 
the data changes throughout the lifecycle of that variable. The integrated, hierarchical representation of traceability 
provided by Trace-XML improves the efficiency with which decision makers come to understand the IPs and permits 
them to drill into more detail as needed to answer specific questions about the data21. Trace-XML provides a 
comprehensive understanding of the clinical data by integrating the conceptual view, the clinical study artifact and 
data element view, and the graph view of the study metadata23.  
Validation of the Define-XML documents beyond mere XML schema validation has become a critical step in the 
regulatory submission process necessitating the development of validation rules and the engines to apply them24. Full 
lifecycle, or end-to-end, study metadata traceability validation is an immediate benefit provided by Trace-XML to 
improve the quality of study metadata. When study metadata is created as part of the study specification, traceability 
gaps identify analysis variables without appropriate inputs or collected data not being used in analysis datasets prior 
to study initiation. To effectively generate and validate traceability graphs for clinical research, new traceability rules 
must be created to establish end-to-end traceability requirements. For example, a variable that has multiple source 
variables should reference a method that describes the derivation or transformation used to create one result from 
multiple sources. This may be as simple as a concatenation to create a full date field or a calculation used to derive a 
result. This research project also added a rule to ensure that OIDs are unique within a Define-XML or ODM-XML 
file, and ideally OIDs would be unique across the entire study.  New traceability rules should be considered as 
additions to the existing CDISC standards and applied as validation rules that verify traceability quality within a study. 
The visualization and validation of CDISC standard traceability metadata can be extended to reference source data 
found in EHRs. The graphs (Figures 2, 3, 5) show a study data lifecycle that starts with data collection and ends with 
analysis datasets. This study data lifecycle could be extended to include links from data collection back to EHR 
electronic source data25. Additionally, the study data lifecycle could be extended to include links from analysis results 
163


### Page 7

 
metadata back to the analysis datasets using the Define-XML Analysis Results Metadata v1.0 extension. Trace-XML 
generated study graphs benefit data reviewers by providing the means to explore full-lifecycle traceability for a full 
study in order to quickly identify the variables extracted from an EHR and to assess the degree to which EHR data 
has been incorporated into a study.  
Trace-XML provides a computable traceability framework with a model developed from industry standard metadata. 
The existing hierarchical ODM-XML CRF metadata and the tabular Define-XML metadata provide nearly all the 
metadata needed to dynamically create the graph representation. The ability to make use of the existing standards 
while only requiring a small extension to the Define-XML metadata improves the implementation feasibility and is a 
benefit of the Trace-XML solution. This rationale supports the development Trace-XML based on technologies 
currently used by industry, regulators, and academics. This initial version of Trace-XML does not implement the W3C 
PROV or Open Provenance Model because these standards are not currently used in the CDISC standards or by 
regulators, but future versions will support these standards1. Other technologies of interest within healthcare, such as 
blockchain, also explicitly enable traceability, but they are not part of the existing technology infrastructure for clinical 
research.  Generalist model-based graphing libraries such as D3.js exist, as do tools that visualize biological 
relationships such as Cytoscape and Cytoscape.js, but these tools lack the out-of-the-box function of tracing metadata, 
and therefore data, conformant to CDISC standards across the full clinical research data lifecycle. To our knowledge, 
no tools exist that provide a traceability capability similar to Trace-XML. 
Conclusion 
Trace-XML contributes two features that immediately benefit data reviewers: the ability to validate traceability 
across a full study and the ability to query the complete trace for a variable across the entire lifecycle. Traceability 
improves a reviewer’s ability to understand a study, and has been identified as essential for a regulatory reviewer’s 
ability to assess a submission. Identifying the full trace for a variable in a CDISC study today is a manual process, or 
requires the development of custom-made tools. The ability to conduct an exploratory analysis of traceability for a 
study, or to compare the end-to-end data lifecycle for similar submissions has not been a common practice. The 
generation of full lifecycle study graphs makes this analysis possible. 
 
Future research will expand on the Trace-XML evaluation to include a qualitative assessment of the utility provided 
by Trace-XML to clinical data experts and reviewers. Future developments of Trace-XML will include support for 
existing, general use provenance standards such as W3C PROV. As EHRs and other electronic data sources from 
routine healthcare become data sources for clinical research integrating provenance data from these systems would 
provide a more complete view of traceability within a study. Although no alternative solutions are currently 
available, a comparison of Trace-XML to other possible technical approaches for establishing traceability, such as 
blockchain, is another area for future study. 
References 
1. Curcin V, Miles S, Danger R, Chen Y, Bache R, Taweel A. Implementing interoperable provenance in biomedical 
research. Future Generation Computer Systems. 2014;34:1-16. 
2. FDA. CDER common data standards issues document version 1.1. FDA; 2011. 
3. FDA. Study data technical conformance guide. In: CDER C, editor. FDA2016. 
4. Chhatre D, Malla A. CDER/CBER’s top 7 CDISC standards issues. FDA2012. 
5. Peterson T, Izard D. The 5 biggest challenges of ADaM NESUG 2010; Baltimore, MD: NESUG; 2010. 
6. Berkowitz D. The FDA and Slower Cures: The bureaucratic assault on cancer treatments. Wall Street Journal. 2011 
28-Feb-2011. 
7. van Valkenhoef G, Tervonen T, de Brock B, Hillege H. Deficiencies in the transfer and availability of clinical trials 
evidence: a review of existing systems and standards. BMC Medical Informatics and Decision Making. 2012;12(1):95. 
8. Dootson A. Tracing data elements through a standard data flow.  PhUSE 2011; Brighton, UK: PhUSE; 2011. 
9. Segalstad SH. International it regulations and compliance: quality standards in the pharmaceutical and regulated 
industries: John Wiley & Sons; 2008. 
10. CDISC. Clinical Data Interchange Standards Consortium: Clinical Data Interchange Standards Consortium; 2016 
[Available from: http://www.cdisc.org/. 
11. Carata L, Akoush S, Balakrishnan N, Bytheway T, Sohan R, Selter M, et al. A primer on provenance. 
Communications of the ACM. 2014;57(5):52-60. 
12. Davidson SB, Freire J, editors. Provenance and scientific workflows: challenges and opportunities. Proceedings 
of the 2008 ACM SIGMOD international conference on Management of data; 2008: ACM. 
164


### Page 8

 
13. Hevner A, March S, Park J, Ram S. Design science in information systems research. Mis Quarterly. 2004;28(1):75-
105. 
14. Simon H. The Sciences of the Artificial. 3rd ed: MIT Press; 1996. 
15. March ST, Smith GF. Design and natural science research on information technology. Decision support systems. 
1995;15(4):251-66. 
16. Nunamaker Jr JF, Chen M, editors. Systems development in information systems research. System Sciences, 1990, 
Proceedings of the Twenty-Third Annual Hawaii International Conference on; 1990: IEEE. 
17. Iivari J. A paradigmatic analysis of information systems as a design science. Scandinavian Journal of Information 
Systems. 2007;19(2):39. 
18. Shankaranarayan G, Ziad M, Wang RY. Managing data quality in dynamic decision environments: An information 
product approach. Journal of Database Management. 2003;14(4):14. 
19. Sedgewick R, Wayne K. Algorithms. Fourth Edition ed: Addison-Wesley; 2011. 
20. Shankaranarayanan G, Wang RY, Ziad M, editors. IP-MAP: Representing the manufacture of an information 
product. IQ; 2000. 
21. Chee C-H, Yeoh W, Gao S, editors. Enhancing business intelligence traceability through an integrated metadata 
framework. ACIS 2011 Proceedings; 2011; Sydney, Austrailia. 
22. FDA. Use of Electronic Health Record Data in Clinical Investigations: Guidance for Industry (Draft). In: Food 
and Drug Administration H, editor. 81 FR 30540 ed: FDA; 2016. p. 30540-1. 
23. Chee C-H, Yeoh W, Gao S, Richards G. Improving business intelligence traceability and accountability: An 
integrated framework of BI product and metacontent map. Journal of Database Management (JDM). 2014;25(3):28-
47. 
24. Hume S, Aerts J, Sarnikar S, Huser V. Current applications and future directions for the CDISC Operational Data 
Model standard: A methodological review. Journal of Biomedical Informatics. 2016. 
25. Erturkmen GBL, Bain L, Sinaci A. keyCRF: Using semantic metadata registries to populate an eCRF with EHR 
data.  International Semantic Web Conference 2014; Riva del Garda, Italy2014. 
 
165


---

