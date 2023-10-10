# Copyright 2023 Free World Certified -- all rights reserved.
"""Module for testing functions in api/form_data_utils.py."""
import pytest
from api.form_data_utils import dict_to_form_data


@pytest.mark.parametrize(
    "input, output", [
        (dict(), dict()),
        ({"arr": [1, 2, 3]}, {"arr[0]": 1, "arr[1]": 2, "arr[2]": 3}),
        (
            {
                "data": [{"arr": "honey", "bruh": [1, "journey"]}, {"quick": {"karma": 7}}],
            }, {
                "data[0]arr": "honey",
                "data[0]bruh[0]": 1,
                "data[0]bruh[1]": "journey",
                "data[1]quick.karma": 7,
            },
        ),
        (
            {
                "name": "Abro",
                "status": {
                    "code": "112",
                    "desc": "why",
                    "workers": [
                        {
                            "name": "1111",
                        },
                    ],
                },
                "notes": ["1", "2"],
            }, {
                "name": "Abro",
                "status.code": "112",
                "status.desc": "why",
                "status.workers[0]name": "1111",
                "notes[0]": "1",
                "notes[1]": "2",
            },
        ),
    ],
)
def test_dict_to_form_data(input, output):
    """Tests dict_to_form_data utility."""
    assert dict_to_form_data(input) == output
