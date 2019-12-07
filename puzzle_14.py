from itertools import permutations
from typing import List

import pytest

from puzzle_10 import (INSTRUCTIONS, Instruction, InstructionCode,
                       MachineState, get_parameter_value)


class StopMachine(Exception):
    pass


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
        return MachineState.HALT, index + 2


class TotalHaltInstruction(Instruction):
    @staticmethod
    def call(
        instruction_code: InstructionCode, tape: List[int], index: int
    ) -> (MachineState, int):
        raise StopMachine


INSTRUCTIONS[3] = InputInstruction
INSTRUCTIONS[4] = OutputInstruction
INSTRUCTIONS[99] = TotalHaltInstruction


def run_phase(tape, permutation):
    global BUFFER
    last = 0
    BUFFER = [0]
    amp_indices = [0, 0, 0, 0, 0]
    amp_tapes = [tape.copy() for _ in range(5)]

    for amp_index, number in enumerate(permutation):
        BUFFER.append(number)
        amp_tapes[amp_index], amp_indices[amp_index] = run(
            amp_tapes[amp_index], INSTRUCTIONS, amp_indices[amp_index]
        )

    while True:
        try:
            for amp_index, number in enumerate(permutation):
                amp_tapes[amp_index], amp_indices[amp_index] = run(
                    amp_tapes[amp_index], INSTRUCTIONS, amp_indices[amp_index]
                )

            last = BUFFER[0]
        except StopMachine:
            break

    return last


def solution(tape):
    global BUFFER
    results = []

    for permutation in permutations([5, 6, 7, 8, 9]):
        result = run_phase(tape.copy(), permutation)
        results.append(result)

    return max(results)


def run(tape, instructions, index):
    while True:
        instruction_code = InstructionCode.from_instruction(tape[index])
        instruction = instructions[instruction_code.opcode]
        state, pointer = instruction.call(instruction_code, tape, index)
        index = pointer

        if state == MachineState.HALT:
            break

    return tape, index


if __name__ == "__main__":
    with open("inputs/input13.txt", "r") as content_file:
        content = content_file.read()

    value = list(map(int, content.split(",")))
    print(solution(value))


@pytest.mark.parametrize(
    "tape, permutation, output",
    [
        (
            [
                3,
                26,
                1001,
                26,
                -4,
                26,
                3,
                27,
                1002,
                27,
                2,
                27,
                1,
                27,
                26,
                27,
                4,
                27,
                1001,
                28,
                -1,
                28,
                1005,
                28,
                6,
                99,
                0,
                0,
                5,
            ],
            [9, 8, 7, 6, 5],
            139629729,
        ),
        (
            [
                3,
                52,
                1001,
                52,
                -5,
                52,
                3,
                53,
                1,
                52,
                56,
                54,
                1007,
                54,
                5,
                55,
                1005,
                55,
                26,
                1001,
                54,
                -5,
                54,
                1105,
                1,
                12,
                1,
                53,
                54,
                53,
                1008,
                54,
                0,
                55,
                1001,
                55,
                1,
                55,
                2,
                53,
                55,
                53,
                4,
                53,
                1001,
                56,
                -1,
                56,
                1005,
                56,
                6,
                99,
                0,
                0,
                0,
                0,
                10,
            ],
            [9, 7, 8, 5, 6],
            18216,
        ),
    ],
)
def test_run_phase(tape, permutation, output):
    assert run_phase(tape, permutation) == output
