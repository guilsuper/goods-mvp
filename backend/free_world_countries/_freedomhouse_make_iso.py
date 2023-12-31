# Copyright 2023 Free World Certified -- all rights reserved.
"""Generate a CSV that assigns an two-letter ISO country code to each
row in freedomhouse.csv

"""
import csv

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
    "Congo (Brazzaville)",
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
    # "Gaza Strip": "PS",
    "West Bank": "PS",

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


# name_to_iso_alpha_2 = get_mapping()
# n2ia2_str = json.dumps(name_to_iso_alpha_2)
# n2ia2_str = n2ia2_str.replace("{", "{\n    ")
# n2ia2_str = n2ia2_str.replace(", ", ",\n    ")
# n2ia2_str = n2ia2_str.replace("'", '"')
# with open("freedomhouse_name_to_iso_alpha_2.py", "w") as fh:
#     fh.write("# Copyright 2023 Free World Certified -- all rights reserved.\n"
#              f'"""Generated by make_iso.py"""\nname_to_iso_alpha_2 = {n2ia2_str}')
