# Copyright 2023 Free World Certified -- all rights reserved.
"""Command-line tool for generating _country_list.csv

2023-09-24: The current strategy is as follows.  Following the pattern
of existing NGOs that make these kinds of lists, we will generate a
new list of countries each year.  The list gets generated early in the
year based on data from the previous year.  For example, we're in 2023
now, so we're operating on data from 2022.  We're late in the year
now, so in the future, hopefully, by this time of year we'd have
published the updated list.  If a country changes, then companies have
a year to react to the change.  If a country changes from not-free to
free, then companies importing from that country can update their
records to get the benefit.

If a country goes from free to not-free, then companies importing from
that country should get an *extra* year of grace period before their
report gets converted.  This requires some tinkers for companies that
have their reports expire shortly after we publish an update.

2023-09-27: wrote automatic_default, which uses simple rules to
generate _country_list.csv so it can be read by __init__.py

Next, we should finish building out functions like `judge_only_partly`
that give this file its name which will enable manually adjudicating
countries from the ISO list to generate a new CSV file.

"""
import csv
import os
from datetime import datetime

import _freedomhouse as _fh
import pycountry
from _country_structs import Country
from _country_structs import Status

override_names = {
    "BO": "Bolivia",  # Plurinational State of
    "CD": "Democratic Republic of Congo",  # The Democratic Republic of the
    "FM": "Micronesia",  # Federated States of
    "IR": "Iran",  # Islamic Republic of
    "KR": "South Korea",  # Republic of
    "LA": "Laos",  # Lao People's Democratic Republic
    "MD": "Moldova",   # Republic of
    "KP": "North Korea",  # Democratic People's Republic of
    "SY": "Syria",  # Syrian Arab Republic
    "TW": "Taiwan",  # not part of China!
    "TZ": "Tanzania",  # United Republic of
    "VE": "Venezuela",  # Bolivarian Republic of
}


def automatic_default(output_file_path, date, user):
    """Automatically generating output_file_path combining Freedom
    House's 'free' + 'partly free' to define our 'free'.

    """
    version = "v1.0"
    comment = "automatic FH F+PF --> F"
    print(automatic_default.__doc__)

    recs = {}
    for country in pycountry.countries:
        if country.alpha_2 in _fh.free_iso or country.alpha_2 in _fh.partly_free_iso:
            status = Status.Free
        elif country.alpha_2 in _fh.not_free_iso:
            status = Status.NotFree
        else:
            status = Status.Undetermined

        name = override_names.get(country.alpha_2, country.name)
        if status != Status.Undetermined and "," in name:
            sys.exit(f"Must override {country.alpha_2} --> {name}")

        recs[country.alpha_2] = Country(
            country.alpha_2,
            status,
            version, date,
            name,
            user, comment)

    with open(output_file_path, "w", newline="") as o_fh:
        csv_writer = csv.writer(o_fh, dialect="unix", quoting=csv.QUOTE_MINIMAL)
        for rec in recs.values():
            vals = list(rec)
            vals[1] = vals[1].value
            csv_writer.writerow(vals)
    print(f"Done writing {len(recs)} lines to {output_file_path}")


def judge_only_partly(output_file_path, date, user):
    """Copies Freedom House determinations for Free and Not Free, and
    requires manual adjudication on all Partly Free.

    """
    with open(output_file_path, "w") as o_fh:
        for a2 in _fh.iso2score:
            if a2 in _fh.free_iso:
                vote_worthy = 1
            elif a2 in _fh.not_free_iso:
                vote_worthy = 0
            else:
                print(f"{_fh.iso2name[a2]} is {_fh.iso2score[a2]}")
            print(f"{a2},{vote_worthy},{date},{user}", file=o_fh)


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("output_file_path")
    parser.add_argument("--automatic-default", action="store_true")
    parser.add_argument("--judge-only-partly", action="store_true")
    parser.add_argument("--date", default=datetime.utcnow().strftime("%Y-%m-%d"))
    parser.add_argument("--user", default=os.getlogin())
    args = parser.parse_args()

    if args.automatic_default:
        automatic_default(args.output_file_path, args.date, args.user)

    elif args.judge_only_partly:
        judge_only_partly(args.output_file_path, args.date, args.user)

    else:
        print("Must set either --automatic-default or --judge-only-partly")
