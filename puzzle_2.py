import pytest

from puzzle_1 import solution as solution_1


def solution(mass):
    fuel = solution_1(mass)

    if fuel <= 0:
        return 0

    return fuel + solution(fuel)


if __name__ == "__main__":
    import sys

    output = 0

    for line in sys.stdin:
        output += solution(int(line))

    print(output)


@pytest.mark.parametrize("mass, output", [(12, 2), (1969, 966), (100756, 50346)])
def test_solution(mass, output):
    assert solution(mass) == output
