import pytest


def check_criteria(value):
    found_double = False
    previous = 0

    for n in list(map(int, str(value))):
        if n < previous:
            return False

        if n == previous:
            found_double = True

        previous = n

    return found_double


def solution(value_min, value_max, check_criteria_fn=check_criteria):
    counter = 0
    for i in range(value_min, value_max + 1):
        if check_criteria_fn(i):
            counter += 1

    return counter


if __name__ == "__main__":
    import sys

    values = sys.stdin.readlines()[0].split("-")
    output = solution(int(values[0]), int(values[1]))
    print(output)


@pytest.mark.parametrize(
    "value, expected", [(111111, True), (223450, False), (123789, False)]
)
def test_check_criteria(value, expected):
    assert check_criteria(value) == expected
