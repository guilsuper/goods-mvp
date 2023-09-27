# Copyright 2023 Free World Certified -- all rights reserved.
"""Official judgments on countries as free and not free

"""
import csv

from _country_structs import Country
from _country_structs import Status
from pkg_resources import resource_filename

_statii = list(Status)

countries = {}

fpath = resource_filename(__name__, "_country_list.csv")
with open(fpath, "r", newline="") as i_fh:
    csv_reader = csv.reader(i_fh, quoting=csv.QUOTE_MINIMAL)
    for rec in csv_reader:
        vals = list(rec)
        vals[1] = Status(int(vals[1]))

        c = Country(*vals)
        countries[c.alpha_2] = c
