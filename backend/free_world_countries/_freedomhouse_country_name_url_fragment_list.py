# Copyright 2023 Free World Certified -- all rights reserved.
"""Official judgments on countries as free and not free
"""
import csv

from pkg_resources import resource_filename

from ._country_structs import FreedomHouseCountryNameURLFragment

freedom_house_country_name_url_framents = {}

fpath = resource_filename(__name__, "_freedomhouse_country_name_url_fragment_list.csv")
with open(fpath, "r", newline="") as i_fh:
    csv_reader = csv.reader(i_fh, quoting=csv.QUOTE_MINIMAL)
    for rec in csv_reader:
        fhcnf = FreedomHouseCountryNameURLFragment(*rec)
        freedom_house_country_name_url_framents[fhcnf.alpha_2] = fhcnf
