//! Get the diagonals of a 2D array, using math
//!
//! See the Python implementation for lots more documentation.
//!


use fraction::Decimal;
use std::collections::HashMap;
use std::fmt::Debug;


#[derive(Debug)]
struct Point<'a, T: Debug> {
    x: usize,
    y: usize,
    value: &'a T,
}
impl<'a, T: Debug> Point<'a, T> {
    fn from_row_col_val(total_rows: usize, row_idx: usize, col_idx: usize, val: &'a T) -> Self {
        Self {
            x: col_idx,
            y: total_rows - row_idx - 1,
            value: val,
        }
    }
}


#[derive(Debug)]
struct PointOnLineWithSlope<'a, T: Debug> {
    point: &'a Point<'a, T>,
    slope: Decimal,
}
impl<'a, T: Debug> PointOnLineWithSlope<'a, T> {
    fn with_slope_from_point<S: Into<Decimal>>(slope: S, point: &'a Point<T>) -> Self {
        Self {
            slope: slope.into(),
            point,
        }
    }
    fn x_intercept(&self) -> Decimal {
        -self.y_intercept() / self.slope
    }
    fn y_intercept(&self) -> Decimal {
        Decimal::from(self.point.y) - (self.slope * self.point.x.into())
    }
}

fn array_to_points<T: Debug>(array: &Vec<Vec<T>>) -> Vec<Point<T>> {
    let array_len = array.len();
    let points = array
        .iter()
        .enumerate()
        .map(|(row_idx, sub_array)| {
            sub_array
                .into_iter()
                .enumerate()
                .map(move |(col_idx, val)| {
                    Point::from_row_col_val(array_len, row_idx, col_idx, val)
                })
        })
        .flatten()
        .collect();
    points
}

fn points_to_mapped_points<'a, T: Debug>(
    slope: Decimal,
    points: &'a Vec<Point<T>>,
) -> HashMap<Decimal, Vec<&'a Point<'a, T>>> {
    let points_on_line = points
        .iter()
        .map(|point| PointOnLineWithSlope::with_slope_from_point(slope, point));
    points_on_line.fold(HashMap::new(), |mut acc, point_on_line| {
        acc.entry(point_on_line.x_intercept())
            .and_modify(|point_list| {
                if slope < 0.into() {
                    point_list.push(point_on_line.point)
                } else {
                    point_list.insert(0, point_on_line.point)
                }
            })
            .or_insert(vec![point_on_line.point]);
        acc
    })
}

fn print_diagonals<T: Debug>(slope: Decimal, array: &Vec<Vec<T>>) {
    let points = array_to_points(&array);
    let mapped_points = points_to_mapped_points(slope, &points);
    let mut keys = mapped_points.keys().collect::<Vec<&Decimal>>();
    println!("Printing lines of slope {} for vec: {:?}", slope, array);
    keys.sort_by(|prev, next| prev.partial_cmp(next).unwrap());
    keys.iter().for_each(|key| {
        let points = mapped_points.get(key).unwrap();
        points.iter().for_each(|point| {
            print!("{:?} ", point.value);
        });
        print!("\n");
    });
    println!();
}

fn main() {
    #[rustfmt::skip]
    let test_arrays = vec![
        vec![
            vec![1,  2,  3,  4],
            vec![5,  6,  7,  8],
            vec![9, 10, 11, 12],
        ],
        vec![
            vec![ 1,  2,  3,  4, 5, 6, 7],
            vec![ 8,  9, 10, 11],
            vec![12, 13, 14, 15],
        ],
        vec![
            vec![1,  2, 3],
            vec![4,  5, 6, 7, 8],
            vec![9, 10],
        ],
        vec![
            vec![ 1,  2,  3, 4, 5, 6],
            vec![ 7,  8,  9],
            vec![10, 11, 12, 13, 14],
            vec![15, 16],
        ],
        vec![],
        vec![vec![]],
    ];

    // Print lines with a slope of -1
    test_arrays.iter().for_each(|arr| {
        print_diagonals(Decimal::from(-1), arr);
    });

    // Print lines with a slope of -1
    test_arrays.iter().for_each(|arr| {
        print_diagonals(Decimal::from(-2), arr);
    });

    // Print lines with a slope of 1
    test_arrays.iter().for_each(|arr| {
        print_diagonals(Decimal::from(1), arr);
    });

    // Print lines with a slope of 2
    test_arrays.iter().for_each(|arr| {
        print_diagonals(Decimal::from(2), arr);
    });
}
