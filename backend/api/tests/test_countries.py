# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains tests for countries in our database
"""
import pytest
from api.models import Country


@pytest.mark.django_db()
def test_country_usa():
    us = Country.objects.get(pk="US")
    assert us.alpha_2 == "US"
    assert us.alpha_3 == "USA"
    assert us.name == "United States"
    assert us.official_name == "United States of America"
    assert us.free


@pytest.mark.django_db()
def test_country_china():
    china = Country.objects.get(pk="CN")
    assert china.alpha_2 == "CN"
    assert china.alpha_3 == "CHN"
    assert china.name == "China"
    assert china.official_name == "People's Republic of China"
    assert not china.free
