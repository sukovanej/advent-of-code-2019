import pytest


def solution(value):
    i = 0

    while True:
        if value[i] == 99:
            break
        elif value[i] == 1:
            value[value[i + 3]] = value[value[i + 1]] + value[value[i + 2]]
        elif value[i] == 2:
            value[value[i + 3]] = value[value[i + 1]] * value[value[i + 2]]

        i += 4

    return value


if __name__ == "__main__":
    import sys

    value = list(map(int, sys.stdin.readlines()[0].split(",")))
    value[1] = 12
    value[2] = 2
    output = solution(value)
    print(value[0])


@pytest.mark.parametrize(
    "value, output",
    [
        ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
    ],
)
def test_solution(value, output):
    assert solution(value) == output
