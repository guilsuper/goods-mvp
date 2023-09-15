# Copyright 2023 Free World Certified -- all rights reserved.

def test_freedomhouse():
    from free_world_countries._freedomhouse import places, FreedomStatus
    usa = places["United States"]
    assert usa.score == 83

    china = places["China"]
    assert china.status == FreedomStatus.NotFree


def test_free_world_countries():
    from free_world_countries import free_world
    assert "US" in free_world
