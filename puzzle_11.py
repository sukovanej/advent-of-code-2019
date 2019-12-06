from dataclasses import dataclass, field
from typing import List

import pytest


@dataclass
class Tree:
    value: str
    parent: object = None
    leafs: List = field(default_factory=list)


@dataclass
class Pair:
    center: str
    orbit: str


def create_tree(pair_list: List[Pair], current: str = "COM", parent=None) -> Tree:
    tree_node = Tree(current, parent)

    for pair in pair_list:
        if pair.center == current:
            tree_node.leafs.append(create_tree(pair_list, pair.orbit, tree_node))

    return tree_node


def str_to_pair_list(input_data):
    result = []
    for line in input_data.strip().split("\n"):
        value = line.split(")")
        result.append(Pair(value[0], value[1]))
    return result


def calculate_length(tree_node: Tree, length=-1):
    return (
        length + 1 + sum(calculate_length(node, length + 1) for node in tree_node.leafs)
    )


def solution(input_data):
    pair_list = str_to_pair_list(input_data)
    main_tree_node = create_tree(pair_list)
    return calculate_length(main_tree_node)


if __name__ == "__main__":
    with open("inputs/input11.txt", "r") as content_file:
        content = content_file.read()
        print(solution(content))


@pytest.mark.parametrize(
    "pair_list, output",
    [
        (
            [Pair("A", "B"), Pair("COM", "A"), Pair("COM", "C"), Pair("B", "D")],
            Tree("COM", [Tree("A", [Tree("B", [Tree("D")])]), Tree("C")]),
        ),
    ],
)
def test_create_tree(pair_list, output):
    assert create_tree(pair_list) == output


def test_solution():
    input_data = "COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L"
    assert solution(input_data) == 42
