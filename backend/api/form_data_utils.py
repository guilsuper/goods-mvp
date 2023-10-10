# Copyright 2023 Free World Certified -- all rights reserved.
"""Useful form data utility functions."""


def dict_to_form_data(data: dict, sep: str = "[{i}]") -> dict:
    """Converts dict data to multipart/form-data friendly dict.

    Args:
        data: raw python dictionary.
        sep: arrays separator (symbol to identify an array-like variable).

    Returns:
        Modified dictionary that supports multipart content-type.

    Examples:
        Converting the following dictionary:

        ```python
        data = {
            "name": "Abro",
            "status": {
                "code": "112",
                "desc": "why",
                "workers": [
                    {
                        "name": "1111"
                    }
                ]
            },
            "notes": ["1", "2"]
        }
        ```

        Using `dict_to_form_data(data)` results in the
        following multipart/form-data friendly dictionary:

        ```python
        {
            'name': 'Abro',
            'status.code': '112',
            'status.desc': 'why',
            'status.workers[0]name': '1111',
            'notes[0]': '1',
            'notes[1]': '2'
        }
        ```

    Reworked from code originally found here:
      https://gist.github.com/awbacker/ed0b29df769ccd0f886a

    """
    def inner(input: dict, inner_sep: str, result: dict, previous=None) -> dict:
        """Inner function to transform data as a recursive function."""
        # If inner element is a dictionary
        if isinstance(input, dict):
            if previous == "dict":
                inner_sep += "."
            for key, value in input.items():
                inner(value, inner_sep + key, result, "dict")
        # If inner element is array-like
        elif isinstance(input, (list, tuple)):
            for index, value in enumerate(input):
                inner(value, inner_sep + sep.format(i=index), result)
        else:
            result[inner_sep] = input

        return result

    return inner(data, "", {})
