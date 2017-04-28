# Data Files
## [single_claim.tsv](https://github.com/ReedJessen/IPStreetSemanticSearchValidation/blob/master/data/single_claim.tsv)
**Summary:**  A two column file containing a patent application number and single independant claim from the patent application. 

**Schema:** application number | random independent claim 

## [yes102.txt](https://github.com/ReedJessen/IPStreetSemanticSearchValidation/blob/master/data/yes102.txt)
**Summary:** A 12 column file containing data from US patent application which recieved at least 1 rejection under 35 U.S.C. § 102 during prosecution.

**Sechema:** application number | document number | priority date | file date | publication date | ipcr class | uspc class | art unit | NA | received a 102 rejection? (YES=1, NO=0) | NA | summary text


## [no102.txt](https://github.com/ReedJessen/IPStreetSemanticSearchValidation/blob/master/data/no102.txt)
**Summary:** A 12 column file containing data from US patent application which **did not** recieve a rejection under 35 U.S.C. § 102 during prosecution.

**Schema:** application number | document number | priority date | file date | publication date | ipcr class | uspc class | art unit | NA | received a 102 rejection? (YES=1, NO=0) | NA | summary text
