# Copyright 2023 Free World Certified -- all rights reserved.


def test_freedomhouse():
    from free_world_countries._freedomhouse import places, FreedomStatus
    usa = places["United States"]
    assert usa.score == 83

    china = places["China"]
    assert china.status == FreedomStatus.NotFree


def test_free_world_countries():
    from free_world_countries import countries
    from free_world_countries import Status

    assert "US" in countries
    assert countries["US"].name == "United States"
    assert countries["US"].status == Status.Free

    assert "CN" in countries
    assert countries["CN"].status == Status.NotFree
    assert countries["CN"].name == "China"

    assert "TW" in countries
    assert countries["TW"].status == Status.Free
    assert countries["TW"].name == "Taiwan"

    assert "VE" in countries
    assert countries["VE"].status == Status.NotFree
    assert countries["VE"].name == "Venezuela"

    assert "CI" in countries
    assert countries["CI"].status == Status.Free
    assert countries["CI"].name == "Côte d'Ivoire"
