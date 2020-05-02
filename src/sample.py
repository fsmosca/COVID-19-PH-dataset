"""
Filename:
    sample.py

Description:
    Examples on how to get info using covidphi module.
"""


import covidphi


def main():
    covid = covidphi.DangerousCovid()

    # (1) Confirmed cases in the last 7 days
    print(f'Confirmed cases in the last 7 days:')
    confirmed = covid.cases(days=7)
    for c in confirmed:
        print(f'{c["Date"]}, {c["Count"]}')
            
    # (2) Deaths
    print('Deaths in the last 7 days:')
    death = covid.deaths(days=7)
    for d in death:
        print(f'{d["Date"]}, {d["Count"]}')
            
    # (3) Recovered
    print('Recoveries in the last 7 days:')
    recovered = covid.recoveries(days=7)
    for r in recovered:
        print(f'{r["Date"]}, {r["Count"]}')

    # (4) Print all provinces that are available in the database file.
    print('Provinces of confirmed cases:')
    for p in covid.provinces():
        print(p)

    # (5) Print confirmed cases in Bulacan in the last 30 days.
    days, prov = 30, 'Bulacan'
    print(f'Confirmed cases in {prov} in the last {days} days:')
    cc = covid.cases(province=prov, days=days)
    for c in cc:
        print(f'{c["Date"]}, {c["Province"]}, {c["Count"]}')

    # (6) Print confirmed cases in NCR for all days with records.
    days, place = 14, 'NCR'
    print(f'Confirmed cases in {place}:')
    cc = covid.cases(province=place, days=None)
    for c in cc:
        print(f'{c["Date"]}, {c["Count"]}')

    # (7) Print Cumulative confirmed cases in Bulacan.
    prov = 'Bulacan'
    print(f'Cumulative confirmed cases in {prov}:')
    cc = covid.cases(province=prov, days=None, cumulative=True)
    for c in cc:
        print(f'{c["Date"]}, {c["Count"]}')

    # (8) Print Cumulative confirmed cases in Philippines.
    print(f'Cumulative confirmed cases in Philippines')
    cc = covid.cases(province=None, days=None, cumulative=True)
    for c in cc:
        print(f'{c["Date"]}, {c["Count"]}')

    # (9) Cumulative recoveries in NCR in the last 14 days
    print('Cumulative recoveries in NCR in the last 14 days:')
    recovered = covid.recoveries(province='NCR', days=14, cumulative=True)
    for r in recovered:
        print(f'{r["Date"]}, {r["Count"]}')

    # (10) Cumulative deaths in NCR
    print('Cumulative deaths in NCR:')
    death = covid.deaths(province='NCR', days=None, cumulative=True)
    for d in death:
        print(f'{d["Date"]}, {d["Count"]}')

    # (11) Print a list of patient case code and date confirmed, with city/town, province
    print('Patients case code with confirmation date, and address:')
    person = covid.patients(date=True, cityortown=True, province=True)
    for p in person:
        print(p)
        # {'Patient': 'C109005', 'Date': '2020-04-30', 'CityOrTown': 'Caluya', 'Province': 'Antique'}

    # (12) Print a list of patient case code, date confirmed and geo lat/lon
    print('Patients case code with confirmation date, and latitude/longitude:')
    persons = covid.patients(date=True, cityortown=False, province=False, geo=True)
    for p in persons:
        print(p)
        # {'Patient': 'C630867', 'Date': '2020-04-17', 'Latitude': 14.6760413, 'Longitude': 121.0437003}


if __name__ == '__main__':
    main()
