from itertools import permutations
from typing import List

import pytest

from puzzle_10 import (
    INSTRUCTIONS,
    Instruction,
    InstructionCode,
    MachineState,
    get_parameter_value,
)
from puzzle_10 import solution as solution_10

BUFFER = []


class InputInstruction(Instruction):
    @staticmethod
    def call(
        instruction_code: InstructionCode, tape: List[int], index: int
    ) -> (MachineState, int):
        global BUFFER
        result_pointer = tape[index + 1]
        tape[result_pointer] = BUFFER.pop()
        return MachineState.CONTINUE, index + 2


class OutputInstruction(Instruction):
    PARAMS = 1

    @staticmethod
    def call(
        instruction_code: InstructionCode, tape: List[int], index: int
    ) -> MachineState:
        global BUFFER
        value = get_parameter_value(instruction_code.first_mode, index + 1, tape)
        BUFFER.append(value)
        return MachineState.CONTINUE, index + 2


INSTRUCTIONS[3] = InputInstruction
INSTRUCTIONS[4] = OutputInstruction


def run_phase(tape, permutation):
    global BUFFER
    BUFFER = [0]

    for number in permutation:
        BUFFER.append(number)
        solution_10(tape, INSTRUCTIONS)

    return BUFFER.pop(0)


def solution(tape):
    results = []

    for permutation in permutations([0, 1, 2, 3, 4]):
        result = run_phase(tape.copy(), permutation)
        results.append(result)
        assert len(BUFFER) == 0

    return max(results)


if __name__ == "__main__":
    with open("inputs/input13.txt", "r") as content_file:
        content = content_file.read()

    value = list(map(int, content.split(",")))
    print(solution(value))


@pytest.mark.parametrize(
    "tape, permutation, output",
    [
        (
            [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0],
            [4, 3, 2, 1, 0],
            43210,
        ),
        (
            [
                3,
                23,
                3,
                24,
                1002,
                24,
                10,
                24,
                1002,
                23,
                -1,
                23,
                101,
                5,
                23,
                23,
                1,
                24,
                23,
                23,
                4,
                23,
                99,
                0,
                0,
            ],
            [0, 1, 2, 3, 4],
            54321,
        ),
        (
            [
                3,
                31,
                3,
                32,
                1002,
                32,
                10,
                32,
                1001,
                31,
                -2,
                31,
                1007,
                31,
                0,
                33,
                1002,
                33,
                7,
                33,
                1,
                33,
                31,
                31,
                1,
                32,
                31,
                31,
                4,
                31,
                99,
                0,
                0,
                0,
            ],
            [1, 0, 4, 3, 2],
            65210,
        ),
    ],
)
def test_run_phase(tape, permutation, output):
    assert run_phase(tape.copy(), permutation) == output
