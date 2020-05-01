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


version = 'covidphi v0.4'


class DangerousCovid:    
    def __init__(self, file='../doc/Department of Health/DOH COVID Data Drop Case Information.csv'):
        self.__file = file
        self.__data = []

        self.__read_csv('utf-8')

    def __read_csv(self, encode='utf-8'):
        """
        :param encode:
        :return: Save contains of csv file as a list of dict.
        """
        with open(self.__file, encoding=encode) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                self.__data.append(row)

    def unique_date(self):
        """
        :return: a list of unique date objects in ascending order.
        """
        ret = []
        for d in self.__data:
            date_conf = d['DateRepConf']
            date = datetime.strptime(date_conf, '%Y-%m-%d').date()
            ret.append(date)

        return sorted(list(set(ret)), reverse=False)
    
    def provinces(self):
        """
        :return: a list of provinces found in the data file.
        """
        ret = []
        for doh in self.__data:
            prov = doh['ProvRes']
            if prov == '':
                continue
            ret.append(prov)
        return sorted(list(set(ret)))
        
    def cases(self, province=None, days=None, cummulative=False):
        """
        :param province: province name
        :param days: number of days from latest
        :param cummulative: a total count which includes the previous counts
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
                date_dt = datetime.strptime(date_conf, '%Y-%m-%d').date()
                if (ud == date_dt and
                        (province is None or
                         province.lower() == doh['ProvRes'].lower())):
                    cnt += 1
            running_sum += cnt
            res.update({'Date': str(ud)})
            res.update({'Province': 'All provinces' if province is None else province})
            res.update({'Count': running_sum if cummulative else cnt})
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
    
    def deaths(self, province=None, days=None, cummulative=False):
        """
        :param province: province name
        :param days: number of days from latest
        :param cummulative: a total count which includes the previous counts
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
                if doh['RemovalType'] != 'Died':
                    continue
                date_rem = doh['DateRepRem']
                date_dt = datetime.strptime(date_rem, '%Y-%m-%d').date()
                if (ud == date_dt and
                        (province is None or
                         province.lower() == doh['ProvRes'].lower())):
                    cnt += 1
            running_sum += cnt
            res.update({'Date': str(ud)})
            res.update({'Province': 'All provinces' if province is None else province})
            res.update({'Count': running_sum if cummulative else cnt})
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
    
    def recoveries(self, province=None, days=None, cummulative=False):
        """
        :param province: province name
        :param days: number of days from latest
        :param cummulative: a total count which includes the previous counts
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
                if doh['RemovalType'] != 'Recovered':
                    continue
                date_rem = doh['DateRepRem']
                date_dt = datetime.strptime(date_rem, '%Y-%m-%d').date()
                if (ud == date_dt and
                        (province is None or
                         province.lower() == doh['ProvRes'].lower())):
                    cnt += 1
            running_sum += cnt
            res.update({'Date': str(ud)})
            res.update({'Province': 'All provinces' if province is None else province})
            res.update({'Count': running_sum if cummulative else cnt})
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

    def patients(self, date=True, cityortown=False, province=False):
        """
        :param date: if true, the date publicly announced as confirmed case will be extracted
        :param cityortown: if true, the city or municipality of patient will be extracted
        :param province: if true, the province of patient will be extraced
        :return: a list of dict [{'Patient': code, 'date: yyy-mm-dd ...}, {}, ...]
        """
        ret = []
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
            ret.append(info)

        # Sort by date in ascending order
        if date:
            ret = sorted(ret, key=lambda i: i['Date'], reverse=False)

        return ret
