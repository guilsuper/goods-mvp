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

from pkg_resources import resource_filename
from pycountry import countries


# 2023-09-15 these skips and exceptions are effectively an initial set
# of decisions for the not yet created FWC Advisory Board

skip_list = set([
    # conflict areas, skip them
    "Indian Kashmir",
    "Pakistani Kashmir",
    "Transnistria",
    "Nagorno-Karabakh",
    "Northern Cyprus",
    "South Ossetia",
    "Somaliland",

    "Hong Kong",  # not distinct from China

    # collides with a more primary area for the same country, see list
    # below
    "Crimea",
    "Eastern Donbas",
    "Gaza Strip",
    "Tibet",
    "Hong Kong",

    "Kosovo",    # special case, not part of Serbia, so wait.
    "Abkhazia",  # special case, not part of Georgia, so wait.

])


# some of these are just fuzzy search errors, and some are in-progress
# conflicts, see notes
exceptions_list = {
    "Congo (Brazzaville)": "CG",  # Rep. of Congo
    "Congo (Kinshasa)": "CD",     # DRC

    # Both of these are widely recognized as part of Ukraine, not
    # Russia, skip in favor of just Ukraine
    # "Crimea": "UA",
    # "Eastern Donbas": "UA",

    # These could be identified as part of Israel, because occupied
    # for 40+ years... but most countries recognize the State of
    # Palestine as a separate nation.
    # 2023-09-27: so we're not determining them at this time.
    # "Gaza Strip": "PS",
    # "West Bank": "PS",

    # string match errors:
    "Iran": "IR",
    "Laos": "LA",
    "St. Kitts and Nevis": "KN",
    "St. Lucia": "LC",
    "St. Vincent and the Grenadines": "VC",

    # Shining example of the Free World.
    "Taiwan": "TW",

    # Sadly taken over by a dictatorship.
    # "Tibet": "CN",
}


def _make_name2iso():
    name2iso = {}
    with open(resource_filename(__name__, "freedomhouse.csv"), "r") as filehandle:
        for name, region, country_or_territory, status_str, score_str in csv.reader(filehandle):
            if name in skip_list:
                continue
            if name in exceptions_list:
                alpha_2 = exceptions_list[name]
            else:
                hit = countries.get(name=name)
                if hit is not None:
                    alpha_2 = hit.alpha_2
                else:
                    try:
                        hits = countries.search_fuzzy(name)
                    except LookupError:
                        alpha_2 = "FIX THIS MANUALLY"
                    else:
                        if len(hits) == 1:
                            alpha_2 = hits[0].alpha_2
                        else:
                            alpha_2 = "FIX THIS MANUALLY"
            # print(f"{name},{alpha_2}")
            name2iso[name] = alpha_2
    return name2iso


name2iso = _make_name2iso()


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
            raise Exception(
                f"freedomhouse.csv contains unexpected data: "
                f"country_or_territory={country_or_territory}",
            )
        if status_str == "F":
            freedom_status = FreedomStatus.Free
        elif status_str == "PF":
            freedom_status = FreedomStatus.PartlyFree
        elif status_str == "NF":
            freedom_status = FreedomStatus.NotFree
        else:
            raise Exception(
                f"freedomhouse.csv contains unexpected data: "
                f"status_str={status_str}",
            )

        fhr = FreedomHouseRecord(
            name, region, is_country, is_territory,
            freedom_status, int(score_str),
        )
        places[fhr.name] = fhr

        if name not in name2iso:
            pass
            # print(f"'{name}' skipped, see free_world_countries/_make_iso.py.", file=sys.stderr)
        else:
            iso_alpha_2 = name2iso[name]
            iso2score[iso_alpha_2] = fhr.score
            iso2name[iso_alpha_2] = fhr.name
            if iso_alpha_2 in _seen_before:
                print(
                    f"uh oh, got code twice! {iso_alpha_2} --> {name} "
                    f"but already from {_seen_before[iso_alpha_2]}",
                )
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

        print(
            f"{fhr.name} is country={fhr.is_country} and territory={fhr.is_territory} "
            f"in {fhr.region} that "
            f"scored {fhr.score} out of 100 for data from 2022, "
            f"which makes it {fhr.status}",
        )
