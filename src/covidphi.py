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


version = 'covidphi v0.15'


class DangerousCovid:    
    def __init__(self,
                 doh_file='../doc/Department of Health/DOH COVID Data Drop Case Information.csv',
                 address_file='../doc/Others/address reference.csv',
                 psgc_file='../doc/Philippine Standard Geographic Code/PSGC Publication Dec2019.csv'):
        self.__address_file = address_file
        self.__psgc_file = psgc_file
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

    @staticmethod
    def save_to_file(output_file, data):
        """
        Save data to file in csv format.

        :param output_file: a csv filename to save the data
        :param data: a list of dict
        :return: None
        """
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        except PermissionError:
            print('Failed to write to csv file!')
            raise
        except Exception:
            print('Unexpected exception.')
            raise

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

    def regions(self):
        """
        Returns a list of all regions in Philippines.

        :return: a list of regions
        """
        ret = []

        for doh in self.__data:
            reg = doh['Region']
            if reg == '':
                continue
            ret.append(reg)

        return sorted(list(set(ret)))
    
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
            psgc = DangerousCovid.__read_csv(self.__psgc_file)
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

    def cities(self, covid=True):
        """
        Returns a list of cities depending on the parameter covid. If covid
        is true then cities with covid will be returned, otherwise cities
        without covid cases will be returned. Default covid is true.

        :covid: if true it will return cities with covid else without covid
        :return: a list of cities
        """
        ret = []

        if covid:
            for doh in self.__data:
                city = doh['City']
                if city == '':
                    continue
                ret.append(city)
        else:
            psgc = DangerousCovid.__read_csv(self.__psgc_file)
            for p in psgc:
                if p['Geographic Level'] == 'City':
                    psgc_city_name = p['Name']
                    found = False
                    for doh in self.__data:
                        if doh['City'].lower() == psgc_city_name.lower():
                            found = True
                            break
                    if not found:
                        psgc_city_name = psgc_city_name.title()
                        if 'City Of ' in psgc_city_name:
                            psgc_city_name = psgc_city_name.replace('City Of', 'City of')
                        ret.append(psgc_city_name)

        return sorted(list(set(ret)))

    def municipalities(self, covid=True):
        """
        Returns a list of municipalities depending on the parameter covid. If covid
        is true then municipalities with covid will be returned, otherwise municipalities
        without covid cases will be returned. Default covid is true.

        :covid: if true it will return municipalities with covid else without covid
        :return: a list of municipalities
        """
        ret = []

        if covid:
            for doh in self.__data:
                muni = doh['Municipality']
                if muni == '':
                    continue
                ret.append(muni)
        else:
            psgc = DangerousCovid.__read_csv(self.__psgc_file)
            for p in psgc:
                if p['Geographic Level'] == 'Mun':
                    psgc_mun_name = p['Name']
                    found = False
                    for doh in self.__data:
                        if doh['Municipality'].lower() == psgc_mun_name.lower():
                            found = True
                            break
                    if not found:
                        psgc_mun_name = psgc_mun_name.title()
                        ret.append(psgc_mun_name)

        return sorted(list(set(ret)))

    def data(self):
        """
        Returns all data in the case information database
        :return: a list of dict, where the key in dict is the header
        """
        return self.__data
        
    def cases(self, region=None, province=None, city=None, municipality=None,
              days=None, cumulative=False, active=False):
        """
        Returns a list of dict for confirmed cases. It can be filtered by
        region, province, city, last days, cumulative and whether or not it is active.
        If region, province and city name filters are all defined, only the region
        will be used. If province and city are defined, only the province is used.

        :param region: region name
        :param province: province name
        :param city: city name
        :param municipality: municipality name
        :param days: number of days from latest
        :param cumulative: a total count which includes the previous counts
        :param active: if true it will extract all cases except deaths and recoveries
        :return: a list of dict
        """
        ret = []
        running_sum = 0
        location_filter = None

        if region is not None:
            location_filter = 'region'
            if region.lower() not in [p.lower() for p in self.regions()]:
                print(f'Region {region} is not found in database.')
                print('Use regions() method of class DangerousCovid() to see acceptable region names.')
                print('Here is the list:')
                for p in self.regions():
                    print(p)
                return ret
        elif province is not None:
            location_filter = 'province'
            if province.lower() not in [p.lower() for p in self.provinces()]:
                print(f'Province {province} is not found in database.')
                return ret
        elif city is not None:
            location_filter = 'city'
            if city.lower() not in [p.lower() for p in self.cities()]:
                print(f'City {city} is not found in database.')
                print('Use the cities() method to get a list of cities.')
                return ret
        elif municipality is not None:
            location_filter = 'municipality'
            if municipality.lower() not in [p.lower() for p in self.municipalities()]:
                print(f'Municipality {municipality} is not found in database.')
                print('Use municipalities() method to get a list of municipalities.')
                return ret

        u_date = self.unique_date()

        for i, ud in enumerate(u_date):
            res, cnt = {}, 0
            for doh in self.__data:
                date_conf = doh['DateRepConf']

                # Filter date, region, province, city and active cases
                if (ud == date_conf and
                        (location_filter is None or
                        (location_filter == 'municipality' and municipality.lower() == doh['Municipality'].lower()) or
                        (location_filter == 'city' and city.lower() == doh['City'].lower()) or
                        (location_filter == 'province' and province.lower() == doh['Province'].lower()) or
                        (location_filter == 'region' and region.lower() == doh['Region'].lower()))):
                    # Active cases excludes deaths and recoveries
                    if not active:
                        cnt += 1
                    else:
                        if doh['RemovalType'] not in ['Died', 'Recovered']:
                            cnt += 1

            running_sum += cnt
            res.update({'Date': ud})
            if location_filter == 'municipality':
                res.update({'Municipality': municipality})
            if location_filter == 'city':
                res.update({'City': city})
            if location_filter == 'province':
                res.update({'Province': province})
            if location_filter == 'region':
                res.update({'Region': region})
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
    
    def deaths(self, region=None, province=None, days=None, cumulative=False):
        """
        :param region: region name
        :param province: province name
        :param days: number of days from latest
        :param cumulative: a total count which includes the previous counts
        :return: a list of dict
        """
        ret, running_sum, location_filter = [], 0, None

        if region is None and province is not None:
            location_filter = 'province'
            if province.lower() not in [p.lower() for p in self.provinces()]:
                print(f'Province {province} is not found in database.')
                return ret

        if region is not None:  # Ignore province
            location_filter = 'region'
            if region.lower() not in [p.lower() for p in self.regions()]:
                print(f'Region {region} is not found in database.')
                print('Use regions() method of class DangerousCovid() to see acceptable region names.')
                print('Here is the list:')
                for p in self.regions():
                    print(p)
                return ret

        u_date = self.unique_date(header='DateRepRem')

        for i, ud in enumerate(u_date):
            res, cnt = {}, 0
            for doh in self.__data:
                if doh['RemovalType'] != 'Died':
                    continue
                date_rem = doh['DateRepRem']
                if (ud == date_rem and
                        (location_filter is None or
                        (location_filter == 'province' and province.lower() == doh['Province'].lower()) or
                        (location_filter == 'region' and region.lower() == doh['Region'].lower()))):
                    cnt += 1
            running_sum += cnt
            res.update({'Date': ud})
            if location_filter == 'province':
                res.update({'Province': province})
            if location_filter == 'region':
                res.update({'Region': region})
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
    
    def recoveries(self, region=None, province=None, days=None, cumulative=False):
        """
        :param region: region name
        :param province: province name
        :param days: number of days from latest
        :param cumulative: a total count which includes the previous counts
        :return: a list of dict
        """
        ret, running_sum, location_filter = [], 0, None

        if region is None and province is not None:
            location_filter = 'province'
            if province.lower() not in [p.lower() for p in self.provinces()]:
                print(f'Province {province} is not found in database.')
                return ret

        if region is not None:  # Ignore province
            location_filter = 'region'
            if region.lower() not in [p.lower() for p in self.regions()]:
                print(f'Region {region} is not found in database.')
                print('Use regions() method of class DangerousCovid() to see acceptable region names.')
                print('Here is the list:')
                for p in self.regions():
                    print(p)
                return ret

        u_date = self.unique_date(header='DateRepRem')

        for i, ud in enumerate(u_date):
            res, cnt = {}, 0
            for doh in self.__data:
                if doh['RemovalType'] != 'Recovered':
                    continue
                date_rem = doh['DateRepRem']
                if (ud == date_rem and
                        (location_filter is None or
                        (location_filter == 'province' and province.lower() == doh['Province'].lower()) or
                        (location_filter == 'region' and region.lower() == doh['Region'].lower()))):
                    cnt += 1
            running_sum += cnt
            res.update({'Date': ud})
            if location_filter == 'province':
                res.update({'Province': province})
            if location_filter == 'region':
                res.update({'Region': region})
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
                info.update({'Date': doh['DateRepConf']})
            if cityortown:
                info.update({'CityOrTown': doh['CityOrMuni']})
            if province:
                info.update({'Province': doh['Province']})
            if geo:
                address_lookup = f'{doh["Address"]}'
                found = False
                for g in geo_data:
                    address = g['Address']
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
