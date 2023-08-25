# Copyright 2023 Free World Certified -- all rights reserved.
'''Interface to key info from freedomhouse.org see README.md

'''
import csv
from pkg_resources import resource_filename
from collections import namedtuple

FreedomHouseRecord = namedtuple(
    'FreedomHouseRecord',
    'name,region,country_or_territory,status,score')

places = {}

with open(resource_filename(__name__, 'freedomhouse.csv'), 'r') as filehandle:
    for fhr in map(FreedomHouseRecord._make, csv.reader(filehandle)):
        fhr.score = int(fhr.score)
        places[fhr.name] = fhr


if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('place_name')
    args = parser.parse_args()

    if args.place_name not in places:
        all_names = ', '.join(sorted(places.keys()))
        sys.exit(f'The name "{args.place_name}" is not in {all_names}')

    else:
        fhr = places[args.place_name]
        c_or_t = (fhr.country_or_territory == "c" and "Country" or "Territory")
        if fhr.status == 'NF':
            freedom_status = 'not free.'
        elif fhr.status == 'PF':
            freedom_status = 'partially free.'
        else:
            freedom_status = 'FREE!'

        print(f'{fhr.name} is a {c_or_t} in {fhr.region} that '
              f'scored {fhr.score} out of 100 for data from 2022, '
              f'which makes it {freedom_status}')
