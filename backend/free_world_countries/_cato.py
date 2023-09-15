# Copyright 2023 Free World Certified -- all rights reserved.
"""CATO Institute's Human Freedom Index

human-freedom-index-2022.csv

downloaded from https://www.cato.org/human-freedom-index/2022

See also the human-freedom-index-2022.pdf

The "Human Freedom Score" is between 0 and 10, and is the arithmetic
mean of their Personal Freedom Score and Economic Freedom Score.

"""
import csv

from pkg_resources import resource_filename
from pycountry import countries

skip_list = set([

    # same as China
    "Hong Kong SAR, China",
])

exceptions_list = {
    "Bahamas, The": "BS",

    "Congo, Dem. Rep.": "CD",
    "Congo, Rep.": "CG",

    "Egypt, Arab Rep.": "EG",
    "Gambia, The": "GM",
    "Iran, Islamic Rep.": "IR",
    "Korea, Rep.": "KR",   # South Korea
    "Lao PDR": "LA",
    "Taiwan": "TW",
    "Venezuela, RB": "VE",
    "Yemen, Rep.": "YE",
}

fpath = resource_filename(__name__, "human-freedom-index-2022.csv")

name2iso = {}
iso2score = {}
iso2name = {}
free_iso = set([])
partly_free_iso = set([])
not_free_iso = set([])


with open(fpath, "r") as fh:
    for rec in csv.reader(fh):
        year = rec[0]
        if year != "2020":
            continue
        name = rec[1]
        hf_score = float(rec[3])
        # print(f"{name} --> {hf_score}")

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
            iso2score[alpha_2] = hf_score
            iso2name[alpha_2] = name
            if 5.0 < hf_score:
                free_iso.add(alpha_2)
            elif 3.0 < hf_score:
                partly_free_iso.add(alpha_2)
            else:
                not_free_iso.add(alpha_2)
