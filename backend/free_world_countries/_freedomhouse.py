# Copyright 2023 Free World Certified -- all rights reserved.
"""Interface to key info from freedomhouse.org see README.md

freedomhouse.FreedomHouse and freedomhouse.places are primary public
interface of the package.

"""
import csv
import pdb
import sys
from enum import Enum
from typing import NamedTuple

from free_world_countries._freedomhouse_make_iso import name2iso
from pkg_resources import resource_filename


class FreedomStatus(Enum):
    Free = 1
    PartlyFree = 2
    NotFree = 3


class FreedomHouseRecord(NamedTuple):
    name: str
    region: str
    is_country: bool
    is_territory: bool
    status: FreedomStatus
    score: int


places = dict()
free_iso = set()
partly_free_iso = set()
not_free_iso = set()
iso2score = dict()
iso2name = dict()

_seen_before = {}

with open(resource_filename(__name__, "freedomhouse.csv"), "r") as filehandle:
    for name, region, country_or_territory, status_str, score_str in csv.reader(filehandle):
        if country_or_territory == "t":
            is_country = False
            is_territory = True
        elif country_or_territory == "c":
            is_country = True
            is_territory = False
        else:
            raise Exception(f"freedomhouse.csv contains unexpected data: "
                            f"country_or_territory={country_or_territory}")
        if status_str == "F":
            freedom_status = FreedomStatus.Free
        elif status_str == "PF":
            freedom_status = FreedomStatus.PartlyFree
        elif status_str == "NF":
            freedom_status = FreedomStatus.NotFree
        else:
            raise Exception(f"freedomhouse.csv contains unexpected data: "
                            f"status_str={status_str}")

        fhr = FreedomHouseRecord(name, region, is_country, is_territory,
                                 freedom_status, int(score_str))
        places[fhr.name] = fhr

        if name not in name2iso:
            pass
            # print(f"'{name}' skipped, see free_world_countries/_make_iso.py.", file=sys.stderr)
        else:
            iso_alpha_2 = name2iso[name]
            iso2score[iso_alpha_2] = fhr.score
            iso2name[iso_alpha_2] = fhr.name
            if iso_alpha_2 in _seen_before:
                print(f"uh oh, got code twice! {iso_alpha_2} --> {name} "
                      f"but already from {_seen_before[iso_alpha_2]}")
                pdb.set_trace()
            _seen_before[iso_alpha_2] = name
            if freedom_status is FreedomStatus.Free:
                free_iso.add(iso_alpha_2)
            elif freedom_status is FreedomStatus.PartlyFree:
                partly_free_iso.add(iso_alpha_2)
            elif freedom_status is FreedomStatus.NotFree:
                not_free_iso.add(iso_alpha_2)
            else:
                raise Exception(f"how did we get {name} with {freedom_status}")


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("place-name")
    args = parser.parse_args()

    if args.place_name not in places:
        all_names = ", ".join(sorted(places.keys()))
        sys.exit(f"The name {args.place_name} is not in {all_names}")

    else:
        fhr = places[args.place_name]

        print(f"{fhr.name} is country={fhr.is_country} and territory={fhr.is_territory} "
              f"in {fhr.region} that "
              f"scored {fhr.score} out of 100 for data from 2022, "
              f"which makes it {fhr.status}")
