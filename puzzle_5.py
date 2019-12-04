import math
from dataclasses import dataclass
from typing import List

import pytest


@dataclass
class Point:
    x: int
    y: int


class Line:
    def __init__(self, start: Point, end: Point):
        self.first = start
        self.second = end

        if start.y == end.y and start.x < end.x or start.x == end.x and start.y < end.y:
            self.start = start
            self.end = end
        else:
            self.end = start
            self.start = end

    def __repr__(self) -> str:
        return f"Line(start={self.start}, end={self.end})"


def get_cross_points_for_line(first: Line, second: Line) -> List[Point]:
    if (
        first.start.y == first.end.y
        and second.start.x == second.end.x
        and first.start.x <= second.start.x <= first.end.x
        and second.start.y <= first.start.y <= second.end.y
    ):
        return [Point(second.start.x, first.start.y)]

    if (
        first.start.x == first.end.x
        and second.start.y == second.end.y
        and first.start.y <= second.start.y <= first.end.y
        and second.start.x <= first.start.x <= second.end.x
    ):
        return [Point(first.start.x, second.start.y)]

    return []


def get_next_point(previous_point: Point, new_input: str) -> Point:
    direction = new_input[0]
    value = int(new_input[1:])

    if direction == "R":
        return Point(x=previous_point.x + value, y=previous_point.y)
    elif direction == "L":
        return Point(x=previous_point.x - value, y=previous_point.y)
    elif direction == "U":
        return Point(x=previous_point.x, y=previous_point.y + value)
    elif direction == "D":
        return Point(x=previous_point.x, y=previous_point.y - value)


def get_wire(wire_repr: str) -> List[Line]:
    wire = []
    previous_point = Point(x=0, y=0)

    for new_input in wire_repr:
        next_point = get_next_point(previous_point, new_input)
        wire.append(Line(previous_point, next_point))
        previous_point = next_point

    return wire


def get_cross_points(wire_1: List[Line], wire_2: List[Line]):
    cross_points = []

    for line_1 in wire_1:
        for line_2 in wire_2:
            cross_points.extend(
                [
                    point
                    for point in get_cross_points_for_line(line_1, line_2)
                    if point.x != 0 and point.y != 0
                ]
            )

    return cross_points


def solution(value_1, value_2):
    wire_1_repr = value_1.split(",")
    wire_2_repr = value_2.split(",")

    wire_1 = get_wire(wire_1_repr)
    wire_2 = get_wire(wire_2_repr)

    minimal_distance = math.inf

    for crossed_point in get_cross_points(wire_1, wire_2):
        distance = abs(crossed_point.x) + abs(crossed_point.y)

        if distance < minimal_distance:
            minimal_distance = distance

    return minimal_distance


if __name__ == "__main__":
    import sys

    lines = sys.stdin.readlines()
    print(solution(lines[0], lines[1]))


@pytest.mark.parametrize(
    "value_1, value_2, output",
    [
        ("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83", 159),
        (
            "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
            "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
            135,
        ),
    ],
)
def test_solution(value_1, value_2, output):
    assert solution(value_1, value_2) == output


@pytest.mark.parametrize(
    "line_1, line_2, points",
    [
        (
            Line(start=Point(1, 1), end=Point(3, 1)),
            Line(start=Point(2, 0), end=Point(2, 3)),
            [Point(2, 1)],
        ),
        (
            Line(start=Point(3, 1), end=Point(1, 1)),
            Line(start=Point(2, 0), end=Point(2, 3)),
            [Point(2, 1)],
        ),
        (
            Line(start=Point(2, 0), end=Point(2, 3)),
            Line(start=Point(1, 1), end=Point(3, 1)),
            [Point(2, 1)],
        ),
        (
            Line(start=Point(2, 0), end=Point(2, 3)),
            Line(start=Point(3, 1), end=Point(1, 1)),
            [Point(2, 1)],
        ),
    ],
)
def test_get_cross_points_for_line(line_1: Line, line_2: Line, points: List[Point]):
    assert get_cross_points_for_line(line_1, line_2) == points
