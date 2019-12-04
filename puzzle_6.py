import pytest

from puzzle_5 import Line, Point, get_cross_points, get_wire


def distance(first: Point, second: Point) -> int:
    return abs(first.x - second.x) + abs(first.y - second.y)


def line_length(line: Line) -> int:
    return distance(line.start, line.end)


def is_point_on_line(point: Point, line: Line) -> bool:
    return (
        line.start.y == line.end.y == point.y
        and line.start.x <= point.x <= line.end.x
        or line.start.x == line.end.x
        and line.start.x == point.x
        and line.start.y <= point.y <= line.end.y
    )


def solution(value_1, value_2):
    wire_1_repr = value_1.split(",")
    wire_2_repr = value_2.split(",")

    wire_1 = get_wire(wire_1_repr)
    wire_2 = get_wire(wire_2_repr)
    cross_points = get_cross_points(wire_1, wire_2)

    distances = []

    for cross_point in cross_points:
        current_distance = 0

        for first_line in wire_1:
            current_distance += line_length(first_line)

            if is_point_on_line(cross_point, first_line):
                current_distance -= distance(first_line.second, cross_point)
                break

        for second_line in wire_2:
            current_distance += line_length(second_line)

            if is_point_on_line(cross_point, second_line):
                current_distance -= distance(second_line.second, cross_point)
                distances.append(current_distance)
                break

    return min(distances)


if __name__ == "__main__":
    import sys

    lines = sys.stdin.readlines()
    print(solution(lines[0], lines[1]))


@pytest.mark.parametrize(
    "value_1, value_2, output",
    [
        ("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83", 610),
        (
            "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
            "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
            410,
        ),
    ],
)
def test_solution(value_1, value_2, output):
    assert solution(value_1, value_2) == output


def test_is_point_on_line():
    assert not is_point_on_line(line=Line(Point(0, 0), Point(2, 0)), point=Point(-1, 0))
    assert is_point_on_line(line=Line(Point(0, 0), Point(2, 0)), point=Point(0, 0))
    assert is_point_on_line(line=Line(Point(0, 0), Point(2, 0)), point=Point(1, 0))
    assert is_point_on_line(line=Line(Point(0, 0), Point(2, 0)), point=Point(2, 0))
    assert not is_point_on_line(line=Line(Point(0, 0), Point(2, 0)), point=Point(1, 1))
    assert not is_point_on_line(line=Line(Point(0, 0), Point(2, 0)), point=Point(1, -1))

    assert not is_point_on_line(line=Line(Point(0, 0), Point(0, 2)), point=Point(0, 3))
    assert is_point_on_line(line=Line(Point(0, 0), Point(0, 2)), point=Point(0, 2))
    assert is_point_on_line(line=Line(Point(0, 0), Point(0, 2)), point=Point(0, 1))
    assert is_point_on_line(line=Line(Point(0, 0), Point(0, 2)), point=Point(0, 0))
    assert not is_point_on_line(line=Line(Point(0, 0), Point(0, 2)), point=Point(0, -1))
    assert not is_point_on_line(line=Line(Point(0, 0), Point(0, 2)), point=Point(1, 0))
    assert not is_point_on_line(line=Line(Point(0, 0), Point(0, 2)), point=Point(-1, 0))
