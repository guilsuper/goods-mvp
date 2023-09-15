# Copyright 2023 Free World Certified -- all rights reserved.
"""Some hacking around to compare CATO and Freedom House.

"""
import argparse
import sys

import _cato
import _freedomhouse as _fh
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--all-labels", action="store_true")
args = parser.parse_args()


cato_iso = set(_cato.iso2score.keys())
fh_iso = set(_fh.iso2score.keys())
only_cato = cato_iso - fh_iso
only_fh = fh_iso - cato_iso

if len(only_cato) == 0:
    print("Freedom House has every place CATO covers.")
else:
    def cato_str(a2):
        return f"{a2} = {_cato.iso2score[a2]} = {_cato.iso2name[a2]}"
    print(f"Freeddom House is missing these {len(only_fh)} "
          f"places that CATO scores {', '.join(map(cato_str, only_cato))}.")

if len(only_fh) == 0:
    print("CATO has every place CATO covers.")
else:
    def fh_str(a2):
        return f"{a2} = {_fh.iso2score[a2]} = {_fh.iso2name[a2]}"
    print(f"CATO is missing these {len(only_fh)} "
          f"places that Freedom House scores {', '.join(map(fh_str, only_fh))}.")

countries_in_both = cato_iso.intersection(fh_iso)

x = []
y = []
labels = []
colors = []

red = "#FF0000"
blue = "#0000FF"
orange = "#FC6A03"

for a2 in sorted(_fh.iso2score.keys()):
    x.append(_fh.iso2score[a2])
    if a2 not in _cato.iso2score:
        not_in_cato = True
        y.append(8.9)
    else:
        not_in_cato = False
        y.append(_cato.iso2score[a2])
    if a2 in _fh.free_iso:
        colors.append(blue)
        if args.all_labels or not_in_cato or not (7.0 < _cato.iso2score[a2]):
            labels.append(_fh.iso2name[a2])
        else:
            labels.append(" ")

    elif a2 in _fh.partly_free_iso:
        colors.append(orange)
        if args.all_labels or not_in_cato or not (6.0 < _cato.iso2score[a2] <= 7.0):
            labels.append(_fh.iso2name[a2])
        else:
            labels.append(" ")

    elif a2 in _fh.not_free_iso:
        colors.append(red)
        if args.all_labels or not_in_cato or not (_cato.iso2score[a2] <= 6.0):
            labels.append(_fh.iso2name[a2])
        else:
            labels.append(" ")

    else:
        raise Exception("how did we get here?")

fig, ax = plt.subplots()
ax.scatter(x, y, c=colors, s=1)
ax.set_ylim([3, 9])
plt.title("CATO vs Freedom House scores")
plt.ylabel("CATO Score")
plt.xlabel("Freedom House Score")

ha_list = ["left", "center", "right"]
# va_list = ["top", "center", "baseline", "bottom"]
va_list = ["top", "bottom"]
for i, txt in enumerate(labels):
    ax.annotate(
        txt, (x[i], y[i]),
        rotation=45, size=3,
        rotation_mode="anchor",
        # horizontalalignment="center",
        verticalalignment="baseline",
        horizontalalignment=ha_list[i % len(ha_list)],
        # verticalalignment=va_list[i % len(va_list)],\
    )

# plt.show()
plt.savefig("cato-vs-freedomhouse.pdf", dpi=600)
sys.exit()
