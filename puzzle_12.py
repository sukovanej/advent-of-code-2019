from dataclasses import dataclass
from typing import List, Tuple

from puzzle_11 import Pair, Tree, str_to_pair_list


@dataclass
class WithParentTree(Tree):
    parent: object


def create_tree_with_parent(
    pair_list: List[Pair], current: str = "COM", parent: Tree = None
) -> (WithParentTree, WithParentTree, WithParentTree):
    tree_node = WithParentTree(value=current, parent=parent)
    santa_node = None
    you_node = None

    for pair in pair_list:
        if pair.center == current:
            _new_node, _sant_node, _you_node = create_tree_with_parent(
                pair_list, pair.orbit, tree_node
            )
            tree_node.leafs.append(_new_node)

            santa_node = santa_node or _sant_node
            you_node = you_node or _you_node

    if current == "SAN":
        santa_node = tree_node
    elif current == "YOU":
        you_node = tree_node

    return tree_node, santa_node, you_node


def calculate_length_between(
    tree_node: WithParentTree, previous_node: WithParentTree, santa_node: WithParentTree
) -> Tuple[bool, int]:
    parent_list = [tree_node.parent] if tree_node.parent else []
    possible_nodes = [n for n in tree_node.leafs + parent_list if n != previous_node]

    for node in possible_nodes:
        if node == santa_node:
            return True, 1

        found, length = calculate_length_between(node, tree_node, santa_node)

        if found:
            return True, 1 + length

    return False, 0


def solution(input_data):
    pair_list = str_to_pair_list(input_data)
    main_tree_node, santa_node, you_node = create_tree_with_parent(pair_list)
    return calculate_length_between(you_node, None, santa_node)[1] - 2


if __name__ == "__main__":
    with open("inputs/input11.txt", "r") as content_file:
        content = content_file.read()
        print(solution(content))


def test_solution():
    input_data = "COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN"
    assert solution(input_data) == 4
