
# S02 - Onboard Architecture specifications Version 2.1.1

```diff
- Note There is a new version of the specifications available
```

This it the github repository for the ITxPT S02 specifications. It contains example files complementing the actual specifications
as well as JSON schemas and XSDs to use for validation purposes. 

The specifications can be found under https://wiki.itxpt.org/index.php?title=ITxPT_Technical_Specifications.

This repository contains only officially released data. The development history is only accessable to TC members. Each branch reflects a specific version. The head of each branch is the latest officially made available version of files for the corresponding release. 


## Know Issues List ##

Known issues for the S02 Specifications are documented in [KnownIssues.md](KnownIssues.md)

## Client Development Guide ##

The [Client Development Guide](guidelines/ClientDevelopmentGuide.md) lists some some advice for customer implementations. 

## Schemas ## 

Schemas and examples are currently available for each of the following services:

- Inventory
- GNSSLocation
- FMStoIP
- VEHICLEtoIP
- AVMS
- APC
- MADT

### Purpose of schema files ###
XML Schema Definitions (XSDs) or JSON schemas are the standard for describing XML and JSON structured data. Schemas should be used during software development as a tool to validate XML/JSON data structures against the ITxPT specifications. 

### Report an issue/question related to the schema files ###
To report any issue found during implementation or question you have regarding the content of this repository, please use GitHub's Issue system. 

## Report an issue/question related to an ITxPT specification ###
To report any issue found during implementation or question you have regarding the content of the specification, please use the dedicated form: https://forms.gle/tMRgxTXSF1Mahpq27
