# COVID-19 PH dataset
A collection of Philippine data for COVID-19 purposes. It also includes python codes to retrieve certain data such confirmed cases and others.

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

### B. How to use this repository
##### 1. Download and install Python
    You may download python at https://www.python.org/downloads/

##### 2. Download this repo
    a. Press the button "Clone or Download" located at the top right of this page.  
    b. Select DOWNLOAD ZIP.  
    c. Uncompressed it on your computer.  
    d. Navigate to src folder.  
    e. You can place your python script in this src folder.  

### C. Python module
Folder: src  
Name: covidphi.py
#### Example 1: Get the Philippine COVID19 daily cases figure in the last 7 days
##### Code
```python
import covidphi

daily_info = covidphi.DangerousCovid()
cases = daily_info.cases(days=7)
print('Confirmed cases in the last 7 days:')
for c in cases:
    print(f'{c["Date"]}, {c["Count"]}')
```
##### Output
```
Confirmed cases in the last 7 days:
2020-04-30, 276
2020-04-29, 254
2020-04-28, 181
2020-04-27, 198
2020-04-26, 285
2020-04-25, 102
2020-04-24, 211
```

#### Example 2: Get cases in Bulacan province in the last 14 days
##### Code
```python
import covidphi

days, prov = 14, 'Bulacan'
print(f'Confirmed cases at {prov} in the last {days} days:')
daily_info = covidphi.DangerousCovid()
cc = daily_info.cases(province=prov, days=days)
for c in cc:
    print(f'{c["Date"]}, {c["Count"]}')
```
##### Output
```
Confirmed cases at Bulacan in the last 14 days:
2020-04-30, 1
2020-04-29, 1
2020-04-28, 1
2020-04-27, 3
2020-04-26, 3
2020-04-25, 0
2020-04-24, 1
2020-04-23, 2
2020-04-22, 2
2020-04-21, 0
2020-04-20, 2
2020-04-19, 1
2020-04-18, 2
2020-04-17, 3
```

#### Example 3: Cummulative deaths in Philippines
##### Code
```python
import covidphi

print('Cummulative deaths in Philippines:')
info = covidphi.DangerousCovid()
death = info.deaths(province=None, days=None, cummulative=True)
for d in death:
    print(f'{d["Date"]}, {d["Count"]}')
```
##### Output
```
Cummulative deaths in Philippines:
2020-04-30, 567
2020-04-29, 557
2020-04-28, 529
2020-04-27, 510
2020-04-26, 500
2020-04-25, 493
2020-04-24, 476
2020-04-23, 461
2020-04-22, 445
2020-04-21, 436
2020-04-20, 426
2020-04-19, 407
2020-04-18, 396
2020-04-17, 386
2020-04-16, 361
2020-04-15, 348
2020-04-14, 334
2020-04-13, 314
2020-04-12, 296
...
```

See module_info.txt or the module covidphi.py in src folder for other methods of DangerousCovid() class.


### D. Credits
* Department of Health  
https://www.doh.gov.ph/
* Philippine Statistics Authority  
https://psa.gov.ph/classification/psgc/
