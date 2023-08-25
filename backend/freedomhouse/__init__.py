# Copyright 2023 Free World Certified -- all rights reserved.
'''Interface to key info from freedomhouse.org see README.md

'''
import csv
from enum import Enum
from pkg_resources import resource_filename
from typing import NamedTuple


class FreedomStatus(Enum):
    Free = 1
    PartiallyFree = 2
    NotFree = 3

class FreedomHouseRecord(NamedTuple):
    name: str
    region: str
    is_country: bool
    is_territory: bool
    status: FreedomStatus
    score: int

    
places = {}

with open(resource_filename(__name__, 'freedomhouse.csv'), 'r') as filehandle:
    for name, region, country_or_territory, status_str, score_str in csv.reader(filehandle):
        if country_or_territory == 't':
            is_country = False
            is_territory = True
        elif country_or_territory == 'c':
            is_country = True
            is_territory = False
        else:
            raise Exception(f'freedomhouse.csv contains unexpected data: '
                            f'country_or_territory={country_or_territory}')
        if status_str == 'F':
            freedom_status = FreedomStatus.Free
        elif status_str == 'PF':
            freedom_status = FreedomStatus.PartiallyFree
        elif status_str == 'NF':
            freedom_status = FreedomStatus.NotFree
        else:
            raise Exception(f'freedomhouse.csv contains unexpected data: '
                            f'status_str={status_str}')

        fhr = FreedomHouseRecord(name, region, is_country, is_territory, freedom_status, int(score_str))
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

        print(f'{fhr.name} is country={fhr.is_country} and territory={fhr.is_territory} in {fhr.region} that '
              f'scored {fhr.score} out of 100 for data from 2022, '
              f'which makes it {fhr.status}')
