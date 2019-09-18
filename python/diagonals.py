#!/usr/bin/env python3
"""A mathematical solution to the 2D arrays problem using Python."""

import typing as t
from functools import partial, reduce
from itertools import chain
from typing import NamedTuple


# ######################################################################
# Functional Utilities
# ######################################################################

T = t.TypeVar("T")


def flatten(iterable: t.Iterable[t.Iterable[T]]) -> t.Iterable[T]:
    """Return a flattened iterator."""
    return chain.from_iterable(iterable)


U = t.TypeVar("U")


def for_each(fn: t.Callable[[U], t.Any], iterable: t.Iterable[U]) -> None:
    """Consume the iterator by calling `fn` on each item."""
    for item in iterable:
        fn(item)


V = t.TypeVar("V")


def identity(value: V) -> V:
    """Return the passed value."""
    return value


# ######################################################################
# Types
# ######################################################################


class Point(NamedTuple):
    """A point on the x-y coordinate system."""

    x: int
    y: int
    value: t.Any


class PointOnLineWithSlope(NamedTuple):
    """A point on a line.

    If we have a point on a line of the form y = mx + b, our only
    unknown variables are m, the slope, and b, the y-intercept. This
    class assumes we know the slope and provides methods to access
    the intercept(s).
    """

    point: Point
    slope: float

    @property
    def x_intercept(self) -> float:
        """Return the x-intercept for the line the point is on.

        The equation of a line is y = mx + b, where m is the slope, and
        b is the y-intercept. The y-intercept is the point on the y-axis
        at which x is 0, i.e. where y = b. The x-intercept is therefore
        the point on the x-axis at which y is 0:

            y = mx + b
            0 = mx + b
            mx = -b
            x = -b/m

        """
        return -self.y_intercept / self.slope

    @property
    def y_intercept(self) -> float:
        """Return the y-intercept for the line the point is on.

        We know that the line is y = mx + b, so the y-intercept is:

            y = mx + b
            b = y - mx

        We have all of these variables available and can solve directly.
        """
        return self.point.y - (self.slope * self.point.x)


# ######################################################################
# Type Constructors
# ######################################################################


def to_point(row_count: int, row_idx: int, col_idx: int, val: t.Any) -> Point:
    """Convert a member of a 2D array to a Point.

    :param row_count: the total number of rows in the array
    :param row_idx: the row index of the member being converted
    :param col_idx: the column index of the member being converted
    :param val: the value of the member
    """
    return Point(x=col_idx, y=row_count - row_idx - 1, value=val)


def to_point_on_line_with_slope(
    slope: int, point: Point
) -> PointOnLineWithSlope:
    """Convert a Point to a PointOnLineWithSlope."""
    return PointOnLineWithSlope(point=point, slope=slope)


# ######################################################################
# Utility Functions
# ######################################################################


def points_by_intercept(
    accumulator: t.Dict[float, t.List[Point]],
    point_on_line: PointOnLineWithSlope,
) -> t.Dict[float, t.List[Point]]:
    """Accumulate a Point into a dictionary, keyed by its x-intercept."""
    y_intercept = point_on_line.y_intercept
    return {
        **accumulator,
        y_intercept: [*accumulator.get(y_intercept, ()), point_on_line.point],
    }


def array_to_points(
    slope: float, array: t.List[t.List[t.Any]]
) -> t.Dict[float, t.List[Point]]:
    """Convert a 2D array to a dictionary of points, keyed by y-intercept."""
    array_len = len(array)

    # Convert the 2D array of values to a 2D array of points
    points = map(
        # For each row index of the array
        lambda row_idx: map(
            # For each column index of the row
            lambda col_idx: to_point(
                # Construct a point
                row_count=array_len,
                row_idx=row_idx,
                col_idx=col_idx,
                val=array[row_idx][col_idx],
            ),
            range(len(array[row_idx])),
        ),
        range(array_len),
    )

    # Flatten the 2D array into a 1D array, since our Points now contain
    # all of the x-y coordinate information we need.
    flattened = flatten(points)

    # Create a to_point_on_line function, which generates a
    # PointOnLineWithSlope with our specified slope
    to_point_on_line = partial(to_point_on_line_with_slope, slope)

    # Convert the Points to PointOnLineWithSlope instances
    points_on_line = map(to_point_on_line, flattened)

    # Accumulate them into a dict keyed by y-intercept
    return reduce(points_by_intercept, points_on_line, {})


def print_diagonals(slope: int, array: t.List[t.List[t.Any]]) -> None:
    """Print the diagonals of the lines with slope -1."""
    points = array_to_points(slope, array)

    printer = partial(print, sep=" ")

    # These two lines are code are all that we need to properly support
    # slopes of any value
    intercept_sorter = sorted if slope < 0 else partial(sorted, reverse=True)
    value_reverser = identity if slope < 0 else reversed

    print(f"Diagonals with slope {slope} for {array}:")
    for_each(
        lambda intercept: printer(
            *map(
                lambda p: p.value,
                value_reverser(points[intercept]),  # type: ignore
            )
        ),
        intercept_sorter(points),  # type: ignore
    )
    print()


def main():
    """Run all test cases and output solutions."""
    # fmt: off
    test_arrays = (
        # The standard square array:
        [
            [1,  2,  3,  4],
            [5,  6,  7,  8],
            [9, 10, 11, 12]
        ],
        # An array whose first sub-array is longer
        [
            ["a", "b", "c", "d", "e", "f", "g"],
            ["h", "i", "j", "k"],
            ["l", "m", "n", "o"],
        ],
        # An array with varying length sub-arrays
        [
            [0, 1, 2],
            [3, 4, 5, 6],
            [7, 8]
        ],
        # An array with "gaps" due to varying lengths
        [
            ["a", "b", "c"],
            ["d", "e"],
            ["f", "g", "h", "i", "j"],
            ["k", "l", "m"]
        ],
        # Another one, with multiple gaps
        [
            [ 0,  1,  2,  3,  4,  5],  # noqa
            [ 6,  7],  # noqa
            [ 8,  9, 10, 11, 12],  # noqa
            [13, 14, 15],
            [16, 17, 18, 19, 20, 21, 22, 23, 24]
        ],
        # Pathological case, empty array
        [],
        # Pathological case, empty array in array
        [[]],
        # Just one array
        [[1, 2, 3, 4]]
    )
    # fmt: on

    print("Slope: -1")
    for_each(lambda arr: print_diagonals(-1, arr), test_arrays)

    print("Slope: 1")
    for_each(lambda arr: print_diagonals(1, arr), test_arrays)

    print("Slope: -2")
    for_each(lambda arr: print_diagonals(-2, arr), test_arrays)

    print("Slope: 2")
    for_each(lambda arr: print_diagonals(2, arr), test_arrays)


if __name__ == "__main__":
    main()
