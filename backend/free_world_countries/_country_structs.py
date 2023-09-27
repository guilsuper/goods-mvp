# Copyright 2023 Free World Certified -- all rights reserved.
"""Interface to our country judgments

"""
from enum import Enum
from typing import NamedTuple


class Status(Enum):
    NotFree = 0
    Free = 1
    Undetermined = 2

class Country(NamedTuple):
    alpha_2: str
    status: Status
    version: str
    date: str
    name: str
    user: str
    comment: str
