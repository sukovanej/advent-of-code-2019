from typing import List

from puzzle_9 import (
    INSTRUCTIONS,
    Instruction,
    InstructionCode,
    MachineState,
    get_parameter_value,
    solution,
)


class JumpIfTrueInstruction(Instruction):
    @staticmethod
    def call(
        instruction_code: InstructionCode, tape: List[int], index: int
    ) -> (MachineState, int):
        condition = get_parameter_value(instruction_code.first_mode, index + 1, tape)
        new_position = get_parameter_value(
            instruction_code.second_mode, index + 2, tape
        )

        if condition != 0:
            return MachineState.CONTINUE, new_position
        else:
            return MachineState.CONTINUE, index + 3


class JumpIfFalseInstruction(Instruction):
    @staticmethod
    def call(
        instruction_code: InstructionCode, tape: List[int], index: int
    ) -> (MachineState, int):
        condition = get_parameter_value(instruction_code.first_mode, index + 1, tape)
        new_position = get_parameter_value(
            instruction_code.second_mode, index + 2, tape
        )

        if condition == 0:
            return MachineState.CONTINUE, new_position
        else:
            return MachineState.CONTINUE, index + 3


class LessThanInstruction(Instruction):
    @staticmethod
    def call(
        instruction_code: InstructionCode, tape: List[int], index: int
    ) -> (MachineState, int):
        left = get_parameter_value(instruction_code.first_mode, index + 1, tape)
        right = get_parameter_value(instruction_code.second_mode, index + 2, tape)
        result_position = tape[index + 3]

        if left < right:
            tape[result_position] = 1
            return MachineState.CONTINUE, index + 4
        else:
            tape[result_position] = 0
            return MachineState.CONTINUE, index + 4


class EqualsInstruction(Instruction):
    @staticmethod
    def call(
        instruction_code: InstructionCode, tape: List[int], index: int
    ) -> (MachineState, int):
        left = get_parameter_value(instruction_code.first_mode, index + 1, tape)
        right = get_parameter_value(instruction_code.second_mode, index + 2, tape)
        result_position = tape[index + 3]

        if left == right:
            tape[result_position] = 1
            return MachineState.CONTINUE, index + 4
        else:
            tape[result_position] = 0
            return MachineState.CONTINUE, index + 4


INSTRUCTIONS[5] = JumpIfTrueInstruction
INSTRUCTIONS[6] = JumpIfFalseInstruction
INSTRUCTIONS[7] = LessThanInstruction
INSTRUCTIONS[8] = EqualsInstruction


if __name__ == "__main__":
    with open("inputs/input9.txt", "r") as content_file:
        content = content_file.read()

    value = list(map(int, content.split(",")))
    solution(value, INSTRUCTIONS)
