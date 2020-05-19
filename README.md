# COVID-19 PH dataset
A collection of Philippine data for COVID-19 purposes. It also includes python module to retrieve certain data such as confirmed cases and others. Here is some basic interactive [Philippine covid-19 plots](https://fsmosca.github.io/COVID-19-PH-dataset/) built using bokeh.

#### Cases Recoveries and Deaths
![covid19 bokeh cases](https://i.imgur.com/RaaAPtH.png)

#### Provinces and Metro Manila total cases, Cities and Municipalities daily cases in the last 14 days
![covid19 bokeh cities](https://i.imgur.com/eUcOvNV.png)

#### No. of days doubling of cases history in the last 30 days
![covid19 bokeh doubling](https://i.imgur.com/GdSMfU4.png)

### A. Data
#### 1. "DOH COVID Data Drop Case Information.csv"
Folder: [doc\Department of Health](https://github.com/fsmosca/COVID-19-PH-dataset/tree/master/doc/Department%20of%20Health)  
This file contains confirmed cases based from "DOH COVID Data Drop - 05 Case Information.csv" file. There are added columns in this file for covidphi module purposes. More DOH data can be found at this google [page](https://drive.google.com/drive/folders/10VkiUA8x7TS2jkibhSZK1gmWxFM-EoZP)  
DOH address: https://www.doh.gov.ph/

#### 2. "PSGC Publication Dec2019.csv"
Folder: [doc\Philippine Standard Geographic Code](https://github.com/fsmosca/COVID-19-PH-dataset/tree/master/doc/Philippine%20Standard%20Geographic%20Code)  
This file contains location code, name, geographic level [Region, Province, City and others], population and others. You can download the latest official data in excel format in PSA (Philippine Statistics Authority) site. You can also find the last 2 updates in excel format in this repo at [doc/Philippine Standard Geographic Code/Rererences](https://github.com/fsmosca/COVID-19-PH-dataset/tree/master/doc/Philippine%20Standard%20Geographic%20Code/References)   
PSA address: https://psa.gov.ph/classification/psgc/

#### 3. "address reference.csv"
Folder: [doc\Others](https://github.com/fsmosca/COVID-19-PH-dataset/tree/master/doc/Others)  
This file contains basic geographic info such as island group [Luzon, Visaya, Mindanao], region, province, city, municipality, latitude/longitude of people with confirmed cases. The latitude/longitude data are taken from [Google Maps Platform](https://cloud.google.com/maps-platform/?utm_source=google&utm_medium=cpc&utm_campaign=FY18-Q2-global-demandgen-paidsearchonnetworkhouseads-cs-maps_contactsal_saf&utm_content=text-ad-none-none-DEV_c-CRE_269762947808-ADGP_Hybrid+%7C+AW+SEM+%7C+BKWS+~+%5BMV%5D+%7C+PH+%7C+EN+%7C+BK+%7C+EXA+%7C+Google+Maps+Geo-KWID_43700030642350879-kwd-300650646186-userloc_1011154&utm_term=KW_google%20geocoding%20api-ST_google+geocoding+api&gclid=EAIaIQobChMI68rZqLeM6QIVt8EWBR24sw4KEAAYASAAEgJIavD_BwE) specifically the Geocoding API. Together with "DOH COVID Data Drop Case Information.csv" this file can be used to plot location on the map of confirmed cases for up to city and municipality level. I will try to update this daily when there is new confirmed cases reports from DOH.

### B. How to use this repository
##### 1. Download and install Python
    You may download python at https://www.python.org/downloads/. Latest version like 3.8.2 is better.

##### 2. Download this repo
    a. Press the button "Clone or Download" located at the top right of this page.  
    b. Select DOWNLOAD ZIP.  
    c. Uncompressed it on your computer.  
    d. Navigate to src folder and run/experiment with sample.py.  
    e. You can also place your python script in src folder.  

### C. Module covidphi.py
Folder: [src](https://github.com/fsmosca/COVID-19-PH-dataset/tree/master/src)  
This module is using the data file "DOH COVID Data Drop Case Information.csv" and "PSGC Publication Dec2019.csv" to return info based on the methods called. covid19phi class and methods info can be found [here](https://github.com/fsmosca/COVID-19-PH-dataset/blob/master/src/module_info.txt).

#### Example 1: Daily Confirmed cases in the last 7 days
##### Code
```python
import covidphi

covid = covidphi.DangerousCovid()
cases = covid.cases(days=7)
print('Daily Confirmed cases in the last 7 days:')
for c in cases:
    print(f'{c["Date"]}, {c["Count"]}')
```
##### Output
```
Daily Confirmed cases in the last 7 days:
2020-05-18, 205
2020-05-17, 208
2020-05-16, 214
2020-05-15, 215
2020-05-14, 258
2020-05-13, 268
2020-05-12, 264
```

#### Example 1.1: Cumulative confirmed cases
##### Code
```python
import covidphi

covid = covidphi.DangerousCovid()
print(f'Cumulative confirmed cases:')
cc = covid.cases(province=None, days=None, cumulative=True)
for c in cc:
    print(f'{c["Date"]}, {c["Count"]}')
```

##### Output
```
Cumulative confirmed cases:
2020-05-18, 12718
2020-05-17, 12513
2020-05-16, 12305
2020-05-15, 12091
2020-05-14, 11876
2020-05-13, 11618
2020-05-12, 11350
2020-05-11, 11086
2020-05-10, 10794
2020-05-09, 10610
...
```

#### Example 1.2 Daily recoveries
##### Code
```python
import covidphi

covid = covidphi.DangerousCovid()
print('Daily Recoveries:')
rec = covid.recoveries(region=None, province=None, days=None, cumulative=False)
for r in rec:
print(f'{r["Date"]}, {r["Count"]}')
```

##### Output
```
Daily Recoveries:
2020-05-18, 94
2020-05-17, 74
2020-05-16, 101
2020-05-15, 123
2020-05-14, 86
2020-05-13, 145
2020-05-12, 107
2020-05-11, 75
2020-05-10, 82
2020-05-09, 108
...
```

#### Example 1.3: Daily deaths
##### Code
```python
import covidphi

covid = covidphi.DangerousCovid()
print('Daily Deaths:')
dea = covid.deaths(region=None, province=None, days=None, cumulative=False)
for d in dea:
    print(f'{d["Date"]}, {d["Count"]}')
```

##### Output
```
Daily Deaths:
2020-05-18, 7
2020-05-17, 7
2020-05-16, 11
2020-05-15, 16
2020-05-14, 18
2020-05-13, 21
2020-05-12, 25
2020-05-11, 7
2020-05-10, 15
2020-05-09, 8
...
```

#### Example 2: Confirmed cases at Bulacan in the last 14 days
##### Code
```python
import covidphi

covid = covidphi.DangerousCovid()
days, prov = 14, 'Bulacan'
print(f'Confirmed cases at {prov} in the last {days} days:')
cc = covid.cases(province=prov, days=days)
for c in cc:
    print(f'{c["Date"]}, {c["Count"]}')
```
##### Output
```
Confirmed cases at Bulacan in the last 14 days:
2020-05-18, 0
2020-05-17, 1
2020-05-16, 2
2020-05-15, 2
2020-05-14, 3
2020-05-13, 0
2020-05-12, 1
2020-05-11, 4
2020-05-10, 1
2020-05-09, 1
2020-05-08, 0
2020-05-07, 2
2020-05-06, 1
2020-05-05, 0
```

#### Example 2.1: Cumulative confirmed cases at Bulacan in the last 14 days
##### Code
```python
import covidphi

covid = covidphi.DangerousCovid()
days, prov = 14, 'Bulacan'
print(f'Cumulative confirmed cases at {prov} in the last {days} days:')
cc = covid.cases(province=prov, days=days, cumulative=True)
for c in cc:
    print(f'{c["Date"]}, {c["Count"]}')
```

##### Output
```
Cumulative confirmed cases at Bulacan in the last 14 days:
2020-05-18, 151
2020-05-17, 151
2020-05-16, 150
2020-05-15, 148
2020-05-14, 146
2020-05-13, 143
2020-05-12, 143
2020-05-11, 142
2020-05-10, 138
2020-05-09, 137
2020-05-08, 136
2020-05-07, 136
2020-05-06, 134
2020-05-05, 133
```

#### Example 3: Cumulative deaths in Philippines
##### Code
```python
import covidphi

covid = covidphi.DangerousCovid()
print('Cumulative deaths in Philippines:')
death = covid.deaths(province=None, days=None, cumulative=True)
for d in death:
    print(f'{d["Date"]}, {d["Count"]}')
```
##### Output
```
Cumulative deaths in Philippines:
2020-05-04, 623
2020-05-03, 607
2020-05-02, 603
2020-05-01, 579
2020-04-30, 568
2020-04-29, 558
2020-04-28, 530
...
```

#### Example 4: Get patient info with latitude/longitude
##### Code
```python
import covidphi

covid = covidphi.DangerousCovid()
print(f'Patients info with geo location:')
persons = covid.patients(date=True, cityortown=False, province=False, geo=True)
for p in persons:
    print(p)
```
##### Output
```
Patients info with geo location:
{'Patient': 'C404174', 'Date': '2020-01-30', 'Latitude': 9.3129297, 'Longitude': 123.3021299}
{'Patient': 'C462688', 'Date': '2020-02-03', 'Latitude': 9.3129297, 'Longitude': 123.3021299}
{'Patient': 'C387710', 'Date': '2020-02-05', 'Latitude': 9.573142899999999, 'Longitude': 123.7629465}
{'Patient': 'C377460', 'Date': '2020-03-06', 'Latitude': 14.5176184, 'Longitude': 121.0508645}
{'Patient': 'C498051', 'Date': '2020-03-06', 'Latitude': 14.5864844, 'Longitude': 121.114876}
{'Patient': 'C130591', 'Date': '2020-03-07', 'Latitude': 14.5864844, 'Longitude': 121.114876}
{'Patient': 'C178743', 'Date': '2020-03-08', 'Latitude': 14.554729, 'Longitude': 121.0244452}
...
```

#### Example 6: Cumulative active confirmed cases in Philippines
##### Code
```python
import covidphi

covid = covidphi.DangerousCovid()
print(f'Cumulative active confirmed cases in Philippines:')
print('Active means excluding deaths and recoveries.')
cc = covid.cases(province=None, days=None, cumulative=True, active=True)
for c in cc:
    print(f'{c["Date"]}, {c["Count"]}')
```

##### Output
```
Cumulative active confirmed cases in Philippines:
Active means excluding deaths and recoveries.
2020-05-05, 7639
2020-05-04, 7443
2020-05-03, 7182
2020-05-02, 6891
2020-05-01, 6735
2020-04-30, 6456
2020-04-29, 6186
...
```

#### Example 7: Cumulative active confirmed cases in Metro Manila or NCR in the last 7 days
##### Code
```python
import covidphi

covid = covidphi.DangerousCovid()
print(f'Cumulative active confirmed cases in Metro Manila or NCR in the last 7 days:')
print('Active means excluding deaths and recoveries.')
region_name = 'National Capital Region (NCR)'
cc = covid.cases(region=region_name, province=None, days=7, cumulative=True, active=True)
for c in cc:
    print(c)
```

##### Output
```
Cumulative active confirmed cases in Metro Manila or NCR in the last 7 days:
Active means excluding deaths and recoveries.
{'Date': '2020-05-04', 'Region': 'National Capital Region (NCR)', 'Count': 4892}
{'Date': '2020-05-03', 'Region': 'National Capital Region (NCR)', 'Count': 4770}
{'Date': '2020-05-02', 'Region': 'National Capital Region (NCR)', 'Count': 4653}
{'Date': '2020-05-01', 'Region': 'National Capital Region (NCR)', 'Count': 4604}
{'Date': '2020-04-30', 'Region': 'National Capital Region (NCR)', 'Count': 4475}
{'Date': '2020-04-29', 'Region': 'National Capital Region (NCR)', 'Count': 4325}
{'Date': '2020-04-28', 'Region': 'National Capital Region (NCR)', 'Count': 4131}
```

#### Example 8: Provinces without COVID19 cases
##### Code
```python
import covidphi

covid = covidphi.DangerousCovid()
date_today = datetime.today().strftime('%Y-%m-%d')
print(f'Provinces without COVID19 cases as of {date_today}:')
for p in covid.provinces(covid=False):
    print(p)
```

##### Output
```
Provinces without COVID19 cases as of 2020-05-19:
Agusan Del Sur
Apayao
Aurora
Basilan
Batanes
Biliran
Dinagat Islands
Eastern Samar
Kalinga
Masbate
Mountain Province
Quirino
Sarangani
Siquijor
Sorsogon
Southern Leyte
Surigao Del Norte
Surigao Del Sur
Tawi-Tawi
Zamboanga Del Norte
Zamboanga Sibugay
```

#### Example 9: Get all region names, this can be used as filter on cases, deaths and recoveries methods
##### Code
```python
import covidphi

covid = covidphi.DangerousCovid()
print('Regions:')
regions = covid.regions()
for r in regions:
    print(r)
```

##### Output
```
Regions:
Bangsamoro Autonomous Region in Muslim Mindanao (BARMM)
Cordillera Administrative Region (CAR)
MIMAROPA Region
National Capital Region (NCR)
Region I (Ilocos Region)
Region II (Cagayan Valley)
Region III (Central Luzon)
Region IV-A (CALABARZON)
Region IX (Zamboanga Peninsula)
Region V (Bicol Region)
Region VI (Western Visayas)
Region VII (Central Visayas)
Region VIII (Eastern Visayas)
Region X (Northern Mindanao)
Region XI (Davao Region)
Region XII (SOCCSKSARGEN)
Region XIII (Caraga)
```

#### Example 10: Get all data from the source database of case information and save it to a file
##### Code
```python
import covidphi

covid = covidphi.DangerousCovid()
all_data = covid.data()  # a list of dict
covid.save_to_file('mycopy.csv', all_data)
```

#### Example 11: Cities with confirmed cases
##### Code
```python
import covidphi

covid = covidphi.DangerousCovid()
ct = covid.cities(covid=True)
print('Cities with confirmed cases:')
for c in ct:
    print(c)
```

##### Output
```
Cities with confirmed cases:
Batangas City
City of Alaminos
City of Angeles
City of Antipolo
City of Bacolod
City of Bacoor
City of Baguio
...
```

#### Example 12: Cities without confirmed cases
##### Code
```python
import covidphi

covid = covidphi.DangerousCovid()
ct = covid.cities(covid=False)
print('Cities without confirmed cases:')
for c in ct:
    print(c)
```

##### Output
```
Cities without confirmed cases:
City of Bago
City of Bayawan
City of Baybay
City of Bayugan
City of Bislig
City of Bogo
City of Borongan
City of Cabadbaran
...
```

#### Example 13: Cumulative confirmed cases in Quezon city in the last 14 days
##### Code
```python
import covidphi

covid = covidphi.DangerousCovid()
print('Cumulative confirmed cases in Quezon city in the last 14 days:')
cc = covid.cases(city='quezon city', days=14, cumulative=True)
for c in cc:
    print(f'{c["Date"]}, {c["Count"]}')
```
##### Output
```
Cumulative confirmed cases in Quezon city in the last 14 days:
2020-05-04, 1367
2020-05-03, 1351
2020-05-02, 1341
2020-05-01, 1340
2020-04-30, 1326
2020-04-29, 1308
2020-04-28, 1280
2020-04-27, 1245
2020-04-26, 1217
2020-04-25, 1199
2020-04-24, 1183
2020-04-23, 1167
2020-04-22, 1147
2020-04-21, 1138
```


See sample.py in src folder for more examples.

### D. sample.py
Folder: [src](https://github.com/fsmosca/COVID-19-PH-dataset/tree/master/src)  
This file contains example codes on how to use the module covidphi.

### E. Credits
* Department of Health  
https://www.doh.gov.ph/
* Philippine Statistics Authority  
https://psa.gov.ph/classification/psgc/
* Bokeh  
https://bokeh.org/
