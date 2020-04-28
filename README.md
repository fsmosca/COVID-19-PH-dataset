# COVID-19 PH dataset
A collection of Philippine data for COVID-19 purposes.

### A. Data
* [COVID-19 data](https://drive.google.com/drive/folders/10VkiUA8x7TS2jkibhSZK1gmWxFM-EoZP) is shared by [DOH](https://www.doh.gov.ph/) and is updated daily.  
Minor revision of Case information in csv format can also be found in doc/Department of Health folder in this repo. Revision includes converting the dates into ISO 8601 format that is (YYYY-MM-DD).
* [PSA](https://psa.gov.ph/classification/psgc/) has standard codes for Philippine geographical data, visit the site for updates and get the full file in excel format.  
There is a csv file in doc/Philippine Standard Geographic Code in this repo with minor modification such as moving the text strings in population column into the new Notes column. Only numbers are retained in the population column.
* There is a file "address reference.csv" in doc\Others folder of this repo which contains basic geographic info of people with confirmed cases. Together with "DOH Data Drop Case Information.csv" this file can be used to plot location on the map of confirmed cases for up to city and municipality level.


### B. Credits
* Department of Health  
https://www.doh.gov.ph/
* Philippine Statistics Authority  
https://psa.gov.ph/classification/psgc/
