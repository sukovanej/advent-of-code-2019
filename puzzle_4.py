import sys

from puzzle_3 import solution as solution_3


def solution(value, desired):
    for i in range(len(value)):
        for j in range(len(value)):
            current = value.copy()
            current[1] = i
            current[2] = j
            result = solution_3(current)
            if result[0] == desired:
                return 100 * result[1] + result[2]


if __name__ == "__main__":
    value = list(map(int, sys.stdin.readlines()[0].split(",")))
    result = solution(value, 19690720)
    print(result)
