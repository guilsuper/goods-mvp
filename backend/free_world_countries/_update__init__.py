# Copyright 2023 Free World Certified -- all rights reserved.
"""updates the free_world_countries/__init__.py file and also
generates JSON files with the free_world and not_free_world lists of
ISO 3166 two-letter country codes.

"""
import json

import free_world_countries._freedomhouse as _fh
from pkg_resources import resource_filename


def dump(something):
    return json.dumps(something, indent=4, sort_keys=True)


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("--generate-init", action="store_true")
    args = parser.parse_args()

    if not args.generate_init:
        sys.exit("must specify --generate-init, otherwise this does nothing.")

    else:
        # 2023-09-17: jrf: This is where we implement the decision to
        # define the "free world" by combining Freedom House "free"
        # and "partly free".
        free_world_set = _fh.free_iso.union(_fh.partly_free_iso)
        free_world_str = dump(sorted(free_world_set))
        not_free_str = dump(sorted(_fh.not_free_iso))

        fpath = resource_filename(__name__, "__init__.py")
        with open(fpath, "w") as fhio:
            print('''# Copyright 2023 Free World Certified -- all rights reserved.
"""Official sets of countries in the Free World and not free as
defined by the Free World Certification Board.  These strings are
two-letter country codes from ISO 3166.

"""

''', file=fhio)

            print(f"free_world = set({free_world_str})\n", file=fhio)
            print(f"not_free = set({not_free_str})", file=fhio)
        print("generated a new __init__.py file for this module")

        fpath = resource_filename(__name__, "free_world.js")
        with open(fpath, "w") as fhio:
            print("""/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

/** Official sets of countries in the Free World and not free as
  * defined by the Free World Certification Board.  These strings are
  * two-letter country codes from ISO 3166.
  */

""", file=fhio)

            print(f"free_world = {free_world_str};\n", file=fhio)
            print(f"not_free = {not_free_str};", file=fhio)

        print("generated a new free_world.js file")
