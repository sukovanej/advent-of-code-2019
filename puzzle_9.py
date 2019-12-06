from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

import pytest


class ParameterMode(Enum):
    POSITION = 0
    IMMEDIATE = 1


@dataclass
class InstructionCode:
    opcode: int
    first_mode: ParameterMode
    second_mode: ParameterMode
    third_mode: ParameterMode

    @classmethod
    def from_instruction(cls, number: int):
        return cls(
            number % 100,
            ParameterMode(number // 10 ** 2 % 10),
            ParameterMode(number // 10 ** 3 % 10),
            ParameterMode(number // 10 ** 4 % 10),
        )


class MachineState(Enum):
    HALT = "halt"
    CONTINUE = "continue"


class Instruction(ABC):
    @staticmethod
    @abstractmethod
    def call(
        instruction_code: InstructionCode, tape: List[int], index: int
    ) -> (MachineState, int):
        pass


def get_parameter_value(parameter_mode: ParameterMode, index: int, tape: List[int]):
    if parameter_mode == ParameterMode.IMMEDIATE:
        return tape[index]
    elif parameter_mode == ParameterMode.POSITION:
        return tape[tape[index]]


class AddInstruction(Instruction):
    @staticmethod
    def call(
        instruction_code: InstructionCode, tape: List[int], index: int
    ) -> (MachineState, int):
        left = get_parameter_value(instruction_code.first_mode, index + 1, tape)
        right = get_parameter_value(instruction_code.second_mode, index + 2, tape)
        result_position = tape[index + 3]
        tape[result_position] = left + right
        return MachineState.CONTINUE, index + 4


class MulInstruction(Instruction):
    @staticmethod
    def call(
        instruction_code: InstructionCode, tape: List[int], index: int
    ) -> MachineState:
        left = get_parameter_value(instruction_code.first_mode, index + 1, tape)
        right = get_parameter_value(instruction_code.second_mode, index + 2, tape)
        result_position = tape[index + 3]
        tape[result_position] = left * right
        return MachineState.CONTINUE, index + 4


class HaltInstruction(Instruction):
    @staticmethod
    def call(
        instruction_code: InstructionCode, tape: List[int], index: int
    ) -> (MachineState, int):
        return MachineState.HALT, index + 1


class InputInstruction(Instruction):
    @staticmethod
    def call(
        instruction_code: InstructionCode, tape: List[int], index: int
    ) -> (MachineState, int):
        result_pointer = tape[index + 1]
        tape[result_pointer] = int(input())
        return MachineState.CONTINUE, index + 2


class OutputInstruction(Instruction):
    PARAMS = 1

    @staticmethod
    def call(
        instruction_code: InstructionCode, tape: List[int], index: int
    ) -> MachineState:
        value = get_parameter_value(instruction_code.first_mode, index + 1, tape)
        print(value)
        return MachineState.CONTINUE, index + 2


INSTRUCTIONS: Dict[int, Instruction] = {
    1: AddInstruction,
    2: MulInstruction,
    3: InputInstruction,
    4: OutputInstruction,
    99: HaltInstruction,
}


def solution(tape, instructions=INSTRUCTIONS):
    index = 0

    while True:
        instruction_code = InstructionCode.from_instruction(tape[index])
        instruction = instructions[instruction_code.opcode]
        state, pointer = instruction.call(instruction_code, tape, index)

        if state == MachineState.HALT:
            break

        index = pointer

    return tape


if __name__ == "__main__":
    with open("inputs/input9.txt", "r") as content_file:
        content = content_file.read()

    value = list(map(int, content.split(",")))
    solution(value)


@pytest.mark.parametrize(
    "number, output",
    [
        (
            1002,
            InstructionCode(
                opcode=2,
                first_mode=ParameterMode.POSITION,
                second_mode=ParameterMode.IMMEDIATE,
                third_mode=ParameterMode.POSITION,
            ),
        ),
        (
            1102,
            InstructionCode(
                opcode=2,
                first_mode=ParameterMode.IMMEDIATE,
                second_mode=ParameterMode.IMMEDIATE,
                third_mode=ParameterMode.POSITION,
            ),
        ),
        (
            1132,
            InstructionCode(
                opcode=32,
                first_mode=ParameterMode.IMMEDIATE,
                second_mode=ParameterMode.IMMEDIATE,
                third_mode=ParameterMode.POSITION,
            ),
        ),
        (
            2,
            InstructionCode(
                opcode=2,
                first_mode=ParameterMode.POSITION,
                second_mode=ParameterMode.POSITION,
                third_mode=ParameterMode.POSITION,
            ),
        ),
        (
            1101,
            InstructionCode(
                opcode=1,
                first_mode=ParameterMode.IMMEDIATE,
                second_mode=ParameterMode.IMMEDIATE,
                third_mode=ParameterMode.POSITION,
            ),
        ),
    ],
)
def test_instruction_from(number, output):
    assert InstructionCode.from_instruction(number) == output


@pytest.mark.parametrize(
    "value, output",
    [
        ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
        # ([1, 0, 0, 1, 3, 5, 99], [1, 2, 0, 1, 3, 1, 99]),
        ([1101, 100, -1, 0, 99], [99, 100, -1, 0, 99]),
    ],
)
def test_solution(value, output):
    assert solution(value) == output
