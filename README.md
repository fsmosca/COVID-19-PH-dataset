# COVID-19 PH dataset
A collection of Philippine data for COVID-19 purposes.

### A. Data
#### 1. "DOH COVID Data Drop Case Information.csv"
Folder: [doc\Department of Health](https://github.com/fsmosca/COVID-19-PH-dataset/tree/master/doc/Department%20of%20Health)  
This file contains confirmed cases based from "DOH COVID Data Drop - 05 Case Information.csv" file.
More DOH data can be found at this [page](https://drive.google.com/drive/folders/10VkiUA8x7TS2jkibhSZK1gmWxFM-EoZP)  
DOH address: https://www.doh.gov.ph/

#### 2. "PSGC Publication Dec2019.csv"
Folder: [doc\Philippine Standard Geographic Code](https://github.com/fsmosca/COVID-19-PH-dataset/tree/master/doc/Philippine%20Standard%20Geographic%20Code)  
This file contains location code, name, geographic level [Region, Province, City and others], population and others. You can download the latest data in excel format in PSA (Philippine Statistics Authority) site.  
PSA address: https://psa.gov.ph/classification/psgc/

#### 3. "address reference.csv"
Folder: [doc\Others](https://github.com/fsmosca/COVID-19-PH-dataset/tree/master/doc/Others)  
This file contains basic geographic info such as main island, region, province, city, municipality, latitude/longitude of people with confirmed cases. The region, province, city, municipality and latitude/longitude data are mostly taken from [Google Maps Platform](https://cloud.google.com/maps-platform/?utm_source=google&utm_medium=cpc&utm_campaign=FY18-Q2-global-demandgen-paidsearchonnetworkhouseads-cs-maps_contactsal_saf&utm_content=text-ad-none-none-DEV_c-CRE_269762947808-ADGP_Hybrid+%7C+AW+SEM+%7C+BKWS+~+%5BMV%5D+%7C+PH+%7C+EN+%7C+BK+%7C+EXA+%7C+Google+Maps+Geo-KWID_43700030642350879-kwd-300650646186-userloc_1011154&utm_term=KW_google%20geocoding%20api-ST_google+geocoding+api&gclid=EAIaIQobChMI68rZqLeM6QIVt8EWBR24sw4KEAAYASAAEgJIavD_BwE) specifically the Geocoding API. Together with "DOH COVID Data Drop Case Information.csv" this file can be used to plot location on the map of confirmed cases for up to city and municipality level. I will try to update this daily when there is new confirmed cases reports from DOH.


### B. Credits
* Department of Health  
https://www.doh.gov.ph/
* Philippine Statistics Authority  
https://psa.gov.ph/classification/psgc/
