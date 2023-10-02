# Copyright 2023 Free World Certified -- all rights reserved.
"""Command-line tool for generating _freedomhouse_country_name_url_fragment_list.csv"""
import csv
import re
import sys
from pathlib import Path

import requests

#####################################################################
sys.path.append(str(Path(__file__).resolve().parent.parent))
from free_world_countries._country_list import countries  # noqa: E402
from free_world_countries._country_structs import FreedomHouseCountryNameURLFragment  # noqa: E402
from free_world_countries._country_structs import Status  # noqa: E402
from free_world_countries._freedomhouse import iso2name  # noqa: E402

override_fragments = {
    "CD": "democratic-republic-congo",
    "CG": "republic-congo",
}


def test_links(file_path):
    """Automatically verify that urls generated from file_path work"""

    fhc = {}
    with open(file_path, "r", newline="") as i_fh:
        csv_reader = csv.reader(i_fh, quoting=csv.QUOTE_MINIMAL)
        for rec in csv_reader:
            fhcnf = FreedomHouseCountryNameURLFragment(*rec)
            fhc[fhcnf.alpha_2] = fhcnf

    for country in fhc.values():
        url = f"https://freedomhouse.org/country/{country.fragment}/freedom-world/2023"

        response = requests.get(url)

        if response.status_code != requests.codes.ok:
            print(f"failed to fetch {country.alpha_2}:{country.fragment}")


def automatic_default(output_file_path):
    """Automatically generating output_file_path"""

    recs = {}
    for country in countries.values():
        if country.status in [Status.Undetermined]:
            continue
        elif country.alpha_2 in override_fragments:
            fragment = override_fragments[country.alpha_2]
        elif country.alpha_2 in iso2name:
            fragment = iso2name[country.alpha_2]
            fragment = fragment.lower()
            fragment = fragment.replace("'", "")
            fragment = re.sub(r"the ", "", fragment)
            fragment = re.sub(r"[\W]+", "-", fragment)
        else:
            sys.exit(f"no mapping for {country.alpha_2}:{country.name}")

        recs[country.alpha_2] = FreedomHouseCountryNameURLFragment(
            country.alpha_2,
            fragment
        )

    with open(output_file_path, "w", newline="") as o_fh:
        csv_writer = csv.writer(o_fh, dialect="unix", quoting=csv.QUOTE_MINIMAL)
        for rec in recs.values():
            csv_writer.writerow(rec)
    print(f"Done writing {len(recs)} lines to {output_file_path}")


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("output_file_path")
    parser.add_argument("--automatic-default", action="store_true")
    parser.add_argument("--test-links", action="store_true")
    args = parser.parse_args()

    if args.automatic_default:
        automatic_default(args.output_file_path)
    elif args.test_links:
        test_links(args.output_file_path)
    else:
        print("Must set --automatic-default")
