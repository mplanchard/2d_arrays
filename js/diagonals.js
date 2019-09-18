// Print the diagonals of a 2D array


class Point {
    constructor(x, y, value) {
        this.x = x;
        this.y = y;
        this.value = value;
    }
    static from_array_member(total_rows, row_idx, col_idx, val) {
        return new Point(
            col_idx,
            total_rows - row_idx - 1,
            val
        );
    }
}

class PointOnLineWithSlope {
    constructor(point, slope) {
        this.point = point;
        this.slope = slope;
    }

    x_intercept() {
        return -this.y_intercept() / this.slope;
    }

    y_intercept() {
        return this.point.y - (this.slope * this.point.x);
    }
}



const points_by_y_intercept = (accumulator, point_on_line) => {
    const y_intercept = point_on_line.y_intercept();
    return {
        ...accumulator,
        [y_intercept]: (
            [...accumulator[y_intercept] || [], point_on_line.point]
        )
    };
}

const array_to_points = (slope, array) => {
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

const print_diagonals = (slope, array) => {
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
    [
        []
    ],
];

[-1, 1, -2, 2].forEach(
    (slope) => test_arrays.forEach(
        (arr) => print_diagonals(slope, arr)
    )
)