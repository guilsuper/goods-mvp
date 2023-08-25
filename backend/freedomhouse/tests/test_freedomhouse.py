# Copyright 2023 Free World Certified -- all rights reserved.

def test_freedomhouse():
    from freedomhouse import places
    usa = places['United States']
    assert usa.score == 83
