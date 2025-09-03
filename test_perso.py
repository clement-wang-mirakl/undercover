from time import time

from player import speak, vote

arguments = [
    5,
    3,
    "conservative",
    ["mistress", "disabled", "fulfill", "puke", "conservative"],
    [1, 2, 5, 4, 3],
    {},
]


# print(vote(*arguments))

arguments_2 = [
    7,
    4,
    "sideways",
    [
        "canoe",
        "stuffed",
        "urgent",
        "cooperative",
        "pantry",
        "stewardess",
        "flaky",
        "genus",
        "San Francisco",
        "pomegranate",
        "champion",
        "gravel",
        "worse",
        "deflate",
        "rainbow",
        "do not",
        "ledge",
        "fray",
        "timeline",
        "establish",
        "firecracker",
        "gift",
    ],
    [1, 5, 2, 6, 3, 4, 7, 5, 7, 6, 3, 4, 2, 4, 7, 3, 2, 5, 3, 4, 2, 7],
    {1: "U", 6: "C", 5: "U"},
]

print(vote(*arguments_2))
