"""
Filename:
    covidphi.py

Description:
    A module that can be used to return specific Philippine COVID info. The info
    are based from DOH (Department of Health) at https://www.doh.gov.ph/.

Database source:
    DOH:
        https://drive.google.com/drive/folders/10VkiUA8x7TS2jkibhSZK1gmWxFM-EoZP
    On this Repository:
        "doc/Department of Health/DOH COVID Data Drop Case Information.csv"

Example:
    Print a list of dict in the last 7 days confirmed cases in PHI.

import covidphi

covid = covidphi.DangerousCovid()
cases = covid.cases(days=7)
print(cases)
print('Confirmed cases in the last 7 days:')
for c in cases:
    print(f'{c["Date"]}, {c["Count"]}')

See sample.py for more examples.
"""


import csv
from datetime import datetime


version = 'covidphi v0.8'


class DangerousCovid:    
    def __init__(self,
                 doh_file='../doc/Department of Health/DOH COVID Data Drop Case Information.csv',
                 address_file='../doc/Others/address reference.csv'):
        self.__address_file = address_file
        self.__data = DangerousCovid.__read_csv(doh_file, 'utf-8')

    @staticmethod
    def __read_csv(csvfile, encode='utf-8'):
        """
        :param csvfile: the filename of file
        :param encode: encoding
        :return: a list of dict
        """
        ret = []
        with open(csvfile, encoding=encode) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                ret.append(row)

        return ret

    def unique_date(self, header='DateRepConf'):
        """
        When calculating confirmed cases, use the DateRepConf column. For
        recoveries use the DateRepRem. For deaths use DateRepRem too.

        :header: name of column with dates to use, default is confirmed date
        :return: a list of unique string date ordered in ascending order
        """
        ret = []
        for d in self.__data:
            date = d[header]
            if date == '':
                continue
            ret.append(date)

        return sorted(list(set(ret)), reverse=False)
    
    def provinces(self, covid=True):
        """
        Returns a list of provinces depending on the parameter covid. If covid
        is true then provinces with covid will be extracted, otherwise provinces
        without covid cases will be extracted. Default covid is true.

        :covid: if true it will return provinces with covid else without covid
        :return: a list of provinces
        """
        ret = []

        if covid:
            for doh in self.__data:
                prov = doh['Province']
                if prov == '':
                    continue
                ret.append(prov)
        else:
            psgc_file = '../doc/Philippine Standard Geographic Code/PSGC Publication Dec2019.csv'
            psgc = DangerousCovid.__read_csv(psgc_file)
            for p in psgc:
                if p['Geographic Level'] == 'Prov':
                    psgc_prov_name = p['Name']
                    found = False
                    for doh in self.__data:
                        if doh['Province'].lower() == psgc_prov_name.lower():
                            found = True
                            break
                    if not found:
                        ret.append(psgc_prov_name.title())

        return sorted(list(set(ret)))
        
    def cases(self, province=None, days=None, cumulative=False, active=False):
        """
        Returns a list of dict for confirmed cases. It can be filtered by
        province, last days, cumulative and whether or not it is active.

        :param province: province name
        :param days: number of days from latest
        :param cumulative: a total count which includes the previous counts
        :param active: if true it will extract all cases except deaths and recoveries
        :return: a list of dict
        """
        ret = []
        running_sum = 0

        if province is not None:
            if province.lower() not in [p.lower() for p in self.provinces()]:
                print(f'Province {province} is not found in database.')
                return ret

        u_date = self.unique_date()

        for i, ud in enumerate(u_date):
            res, cnt = {}, 0
            for doh in self.__data:
                date_conf = doh['DateRepConf']

                # Filter date, province and active cases
                if (ud == date_conf and
                        (province is None or
                         province.lower() == doh['ProvRes'].lower())):

                    # Active cases excludes deaths and recoveries
                    if not active:
                        cnt += 1
                    else:
                        if doh['RemovalType'] not in ['Died', 'Recovered']:
                            cnt += 1

            running_sum += cnt
            res.update({'Date': ud})
            res.update({'Province': 'All provinces' if province is None else province})
            res.update({'Count': running_sum if cumulative else cnt})
            ret.append(res)

        ret = sorted(ret, key=lambda i: i['Date'], reverse=True)  # Descending

        if days is not None:
            ret2 = []
            for i, n in enumerate(ret):
                ret2.append(n)
                if i >= days - 1:
                    break
            return ret2

        return ret
    
    def deaths(self, province=None, days=None, cumulative=False):
        """
        :param province: province name
        :param days: number of days from latest
        :param cumulative: a total count which includes the previous counts
        :return: a list of dict
        """
        ret = []
        running_sum = 0

        if province is not None:
            if province.lower() not in [p.lower() for p in self.provinces()]:
                print(f'Province {province} is not found in database.')
                return ret

        u_date = self.unique_date(header='DateRepRem')

        for i, ud in enumerate(u_date):
            res, cnt = {}, 0
            for doh in self.__data:
                if doh['RemovalType'] != 'Died':
                    continue
                date_rem = doh['DateRepRem']
                if (ud == date_rem and
                        (province is None or
                         province.lower() == doh['ProvRes'].lower())):
                    cnt += 1
            running_sum += cnt
            res.update({'Date': ud})
            res.update({'Province': 'All provinces' if province is None else province})
            res.update({'Count': running_sum if cumulative else cnt})
            ret.append(res)

        ret = sorted(ret, key=lambda i: i['Date'], reverse=True)  # Descending

        if days is not None:
            ret2 = []
            for i, n in enumerate(ret):
                ret2.append(n)
                if i >= days - 1:
                    break
            return ret2

        return ret
    
    def recoveries(self, province=None, days=None, cumulative=False):
        """
        :param province: province name
        :param days: number of days from latest
        :param cumulative: a total count which includes the previous counts
        :return: a list of dict
        """
        ret = []
        running_sum = 0

        if province is not None:
            if province.lower() not in [p.lower() for p in self.provinces()]:
                print(f'Province {province} is not found in database.')
                return ret

        u_date = self.unique_date(header='DateRepRem')

        for i, ud in enumerate(u_date):
            res, cnt = {}, 0
            for doh in self.__data:
                if doh['RemovalType'] != 'Recovered':
                    continue
                date_rem = doh['DateRepRem']
                if (ud == date_rem and
                        (province is None or
                         province.lower() == doh['ProvRes'].lower())):
                    cnt += 1
            running_sum += cnt
            res.update({'Date': ud})
            res.update({'Province': 'All provinces' if province is None else province})
            res.update({'Count': running_sum if cumulative else cnt})
            ret.append(res)

        ret = sorted(ret, key=lambda i: i['Date'], reverse=True)  # Descending

        if days is not None:
            ret2 = []
            for i, n in enumerate(ret):
                ret2.append(n)
                if i >= days - 1:
                    break
            return ret2

        return ret

    def patients(self, date=True, cityortown=False, province=False, geo=False):
        """
        Returns patient info including address and geo data i.e latitude/longitude.

        :param date: if true, the date publicly announced as confirmed case will be extracted
        :param cityortown: if true, the city or municipality of patient will be extracted
        :param province: if true, the province of patient will be extracted
        :param geo: if true, the latitude and longitude of patient will be extracted
        :return: a list of dict [{'Patient': code, 'date: yyy-mm-dd ...}, {}, ...]
        """
        ret = []

        # Read the "address reference.csv" file if geo is true.
        if geo:
            geo_data = DangerousCovid.__read_csv(self.__address_file, 'utf-8')

        for doh in self.__data:
            info = {}
            info.update({'Patient': doh['CaseCode']})
            if date:
                date_dt = datetime.strptime(doh['DateRepConf'], '%Y-%m-%d').date()
                info.update({'Date': str(date_dt)})
            if cityortown:
                info.update({'CityOrTown': doh['CityMunRes']})
            if province:
                info.update({'Province': doh['ProvRes']})
            if geo:
                address_lookup = f'{doh["CityMunRes"]}, {doh["ProvRes"]}'
                found = False
                for g in geo_data:
                    address = g['DOHCityMunProvRes']
                    if address == address_lookup:
                        info.update({'Latitude': float(g['Latitude'])})
                        info.update({'Longitude': float(g['Longitude'])})
                        found = True
                        break
                if not found:
                    info.update({'Latitude': None})
                    info.update({'Longitude': None})
            ret.append(info)

        # Sort by date in ascending order
        if date:
            ret = sorted(ret, key=lambda i: i['Date'], reverse=False)

        return ret
