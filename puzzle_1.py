import math

import pytest


def solution(mass):
    return math.floor(mass / 3) - 2


if __name__ == "__main__":
    import sys

    output = 0

    for line in sys.stdin:
        output += solution(int(line))

    print(output)


@pytest.mark.parametrize(
    "mass, output", [(12, 2), (14, 2), (1969, 654), (100756, 33583)]
)
def test_solution(mass, output):
    assert solution(mass) == output
