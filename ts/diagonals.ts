// Print the diagonals of a 2D array


class Point {
    constructor(public x: number, public y: number, public value: any) { }
    static from_array_member(total_rows: number, row_idx: number, col_idx: number, val: any): Point {
        return { x: col_idx, y: total_rows - row_idx - 1, value: val };
    }
}

class PointOnLineWithSlope {
    constructor(public point: Point, public slope: number) { }

    x_intercept(): number {
        return -this.y_intercept() / this.slope;
    }

    y_intercept(): number {
        return this.point.y - (this.slope * this.point.x);
    }
}


interface PointsByIntercept {
    [index: number]: Array<Point>
}


const points_by_y_intercept = (
    accumulator: PointsByIntercept,
    point_on_line: PointOnLineWithSlope,
): PointsByIntercept => {
    const y_intercept = point_on_line.y_intercept();
    return {
        ...accumulator,
        [y_intercept]: [...accumulator[y_intercept] || [], point_on_line.point]
    };
}

const array_to_points = (slope: number, array: Array<Array<any>>): PointsByIntercept => {
    const array_len = array.length;
    return array.map(
        (row, row_idx) => row.map(
            (val, col_idx) => Point.from_array_member(
                array_len, row_idx, col_idx, val
            )
        )
    ).reduce(
        (acc, val) => acc.concat(val), []
    ).map(
        (point) => new PointOnLineWithSlope(point, slope)
    ).reduce(
        points_by_y_intercept, {}
    );
}

const print_diagonals = (slope: number, array: Array<Array<any>>): void => {
    const points = array_to_points(slope, array);

    const sorter = (slope < 1) ? undefined : (first, second) => second - first;
    const reverser = (slope < 1) ? (x) => x : (x) => x.reverse()

    console.log(`Diagonals with slope ${slope} for`, array);
    Object.keys(points).sort(sorter).forEach((
        (y_intercept) => {
            console.log(
                reverser(
                    points[y_intercept]
                ).map((point) => `${point.value}`).join(" ")
            );
        }
    ));
    console.log();
}


const test_arrays = [
    [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
    ],
    [
        ["a", "b", "c", "d", "e", "f", "g"],
        ["h", "i", "j", "k"],
        ["l", "m", "n", "o"],
    ],
    [
        [0, 1, 2],
        [3, 4, 5, 6],
        [7, 8]
    ],
    [
        ["a", "b", "c"],
        ["d", "e"],
        ["f", "g", "h", "i", "j"],
        ["k", "l", "m"]
    ],
    [
        [0, 1, 2, 3, 4, 5],
        [6, 7],
        [8, 9, 10, 11, 12],
        [13, 14, 15],
        [16, 17, 18, 19, 20, 21, 22, 23, 24]
    ],
    [],
    [[]],
];

[-1, 1, -2, 2].forEach(
    (slope) => test_arrays.forEach(
        (arr) => print_diagonals(slope, arr)
    )
)
