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


version = 'covidphi v0.1'


class DangerousCovid:    
    def __init__(self, file='../doc/Department of Health/DOH COVID Data Drop Case Information.csv'):
        self.file = file
        self.data = []

        self.read_csv('utf-8')

    def read_csv(self, encode='utf-8'):
        """
        :param encode:
        :return: Save contains of csv file as a list of dict.
        """
        with open(self.file, encoding=encode) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                self.data.append(row)

    def unique_date(self):
        """
        :return: a list of unique date objects
        """
        ret = []
        for d in self.data:
            date_conf = d['DateRepConf']
            date = datetime.strptime(date_conf, '%Y-%m-%d').date()
            ret.append(date)

        return sorted(list(set(ret)), reverse=True)
    
    def provinces(self):
        """
        :return: a list of provinces found in the data file.
        """
        ret = []
        for doh in self.data:
            prov = doh['ProvRes']
            if prov == '':
                continue
            ret.append(prov)
        return sorted(list(set(ret)))
        
    def cases(self, province=None, days=None):
        """
        :param province: province name
        :param days: number of days from latest
        :return: a list of dict
        """
        ret = []

        if province is not None:
            if province.lower() not in [p.lower() for p in self.provinces()]:
                print(f'Province {province} is not found in database.')
                return ret

        u_date = self.unique_date()

        for i, ud in enumerate(u_date):
            res, cnt = {}, 0
            for doh in self.data:
                date_conf = doh['DateRepConf']
                date_dt = datetime.strptime(date_conf, '%Y-%m-%d').date()
                if (ud == date_dt and
                        (province is None or
                         province.lower() == doh['ProvRes'].lower())):
                    cnt += 1
            res.update({'Date': str(ud)})
            res.update({'Province': 'All provinces' if province is None else province})
            res.update({'Count': cnt})            
            ret.append(res)

            if days is None:
                continue

            if i >= days - 1:
                break

        return ret
    
    def deaths(self, province=None, days=None):
        """
        :param province: province name
        :param days: number of days from latest
        :return: a list of dict
        """
        ret = []

        if province is not None:
            if province.lower() not in [p.lower() for p in self.provinces()]:
                print(f'Province {province} is not found in database.')
                return ret

        u_date = self.unique_date()

        for i, ud in enumerate(u_date):
            res, cnt = {}, 0
            for doh in self.data:
                if doh['RemovalType'] != 'Died':
                    continue
                date_rem = doh['DateRepRem']
                date_dt = datetime.strptime(date_rem, '%Y-%m-%d').date()
                if (ud == date_dt and
                        (province is None or
                         province.lower() == doh['ProvRes'].lower())):
                    cnt += 1
            res.update({'Date': str(ud)})
            res.update({'Province': 'All provinces' if province is None else province})
            res.update({'Count': cnt})
            ret.append(res)

            if days is None:
                continue

            if i >= days - 1:
                break

        return ret
    
    def recovered(self, province=None, days=None):
        """
        :param province: province name
        :param days: number of days from latest
        :return: a list of dict
        """
        ret = []

        if province is not None:
            if province.lower() not in [p.lower() for p in self.provinces()]:
                print(f'Province {province} is not found in database.')
                return ret

        u_date = self.unique_date()

        for i, ud in enumerate(u_date):
            res, cnt = {}, 0
            for doh in self.data:
                if doh['RemovalType'] != 'Recovered':
                    continue
                date_rem = doh['DateRepRem']
                date_dt = datetime.strptime(date_rem, '%Y-%m-%d').date()
                if (ud == date_dt and
                        (province is None or
                         province.lower() == doh['ProvRes'].lower())):
                    cnt += 1
            res.update({'Date': str(ud)})
            res.update({'Province': 'All provinces' if province is None else province})
            res.update({'Count': cnt})
            ret.append(res)

            if days is None:
                continue

            if i >= days - 1:
                break

        return ret
