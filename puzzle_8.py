import pytest

from puzzle_7 import solution


def check_criteria_extended(value):
    found_double = False
    previous = 0

    current_number, current_counter = 0, 0

    for n in list(map(int, str(value))):
        if n != current_number:
            if current_counter == 2:
                found_double = True

            current_number, current_counter = n, 1
        else:
            current_counter += 1

        if n < previous:
            return False

        previous = n

    return current_counter == 2 or found_double


if __name__ == "__main__":
    import sys

    values = sys.stdin.readlines()[0].split("-")
    output = solution(
        int(values[0]), int(values[1]), check_criteria_fn=check_criteria_extended
    )
    print(output)


@pytest.mark.parametrize(
    "value, expected",
    [
        (111111, False),
        (223450, False),
        (123789, False),
        (112233, True),
        (123444, False),
        (111122, True),
    ],
)
def test_check_criteria(value, expected):
    assert check_criteria_extended(value) == expected
