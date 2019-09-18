# 2d_arrays

Solutions to the 2D array problem

## Algorithm

All of the solutions here make use of a correspondence between the 2D
array and the x-y coordinate system to collect the points in the array
into a hash map, keyed by their y-intercept values.

This is a nice solution, because it's relatively easy to convert the
2D array into a 2D array of coordinate points. If we imagine a 2D
array in terms of `(row_idx, col_idx)`, for a square array of length 3,
we see something like:

```raw
(0, 0) (0, 1) (0, 2)
(1, 0) (1, 1) (1, 2)
(2, 0) (2, 1) (2, 2)
```

If we imagine the origin of the cartesian plane at the bottom left,
and looking at standard (x, y) notation for points, we see:

```raw
(0, 2) (1, 2) (2, 2)
(0, 1) (1, 1) (2, 1)
(0, 0) (1, 0) (2, 0)
```

So, if we want to convert a `(row_idx, col_idx)` 2-tuple to an (x, y) point,
we can start by saying that `x == col_idx`. For the y coordinate, we can
see that our `row_idx` and our y coordinates are reversed in the vertical
plane, i.e. the first row's index is 0, but it corresponds to a y-value
of 2, while the third row's index is 2, but it corresponds to a y-value
of 0. We can express this relationship as `y == len(array) - 1 - row_idx`.

Okay, easy enough, but what does putting our 2D array in terms of the
Cartesian plane give us?

The problem at hand is to print the diagonals. If we label the first
diagonal line as 0, the next as 1, and so on, and each point on each line
in the order it should be printed, e.g. 0.0, 0.1, 0.2, etc.:

```raw
2.0 3.0 4.0
1.0 2.1 3.1
0.0 1.1 2.2
```

Putting these lines on the coordinate plane allows us to describe them
with standard equations. In this case, hearkening back to highschool
geometry, the equation of a line is _y = mx + b_.

These lines in particular are lines with a slope of -1 (slope is rise/run,
and these go down one, over one, or -1/1).

So, the question becomes, can we use the fact that every line has a
mathematically inescapable _invariant_, which is that all points on the
line MUST conform to the equation of the line, to accomplish our goal?

It turns out we can! The trick is to recognize that since we want to print
our lines going from left to right, we are also printing them in increasing
order of y-intercept. In the case we're considering above, we would
print the points on the line with its y-intercept at 0, then the line
with its y-intercept at 1, then the line with its y-intercept at 2.

This pattern applies _regardless of how many items are in the array_, and
_regardless of how many items are in any given sub-array_. This means that
if we can base out solution on the intercept, we can free ourselves from
complicated iteration patterns entirely.

So, how do we do it? The first step is to convert the array to series of
points, where each point contains its x coordinate, its y coordinate, and
the value at that position in the original array.

So, if we imagine an array like this:

```raw
[
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]
```

we know that its `(row_idx, col_idx)` pairs look like this:

```raw
(0, 0) (0, 1) (0, 2)
(1, 0) (1, 1) (1, 2)
(2, 0) (2, 1) (2, 2)
```

and its (x, y) pairs look like this:

```raw
(0, 2) (1, 2) (2, 2)
(0, 1) (1, 1) (2, 1)
(0, 0) (1, 0) (2, 0)
```

So we can convert it into a series of Points, where Points are of the form
Point(x, y, value):

```raw
[
    [Point(0, 2, 1), Point(1, 2, 2), Point(2, 2, 3)],
    [Point(0, 1, 4), Point(1, 1, 5), Point(2, 1, 6)],
    [Point(0, 0, 7), Point(1, 0, 8), Point(2, 0, 9)],
]
```

Since each point now encapsulates its location within the original array,
we don't need to keep the nested structure anymore, so it's easiest here
to flatten the array into a 1D array of points:

```raw
[
    Point(0, 2, 1), Point(1, 2, 2), Point(2, 2, 3),
    Point(0, 1, 4), Point(1, 1, 5), Point(2, 1, 6),
    Point(0, 0, 7), Point(1, 0, 8), Point(2, 0, 9),
]
```

Now, for each Point, we have the value of _x_ and the value of _y_. This
leaves only _m_, the slope, and _b_, the y-intercept remaining in the
canonical equation of a line, which means that if we have one, we can
calculate the other.

Now, we're almost there! We could now write a function like
`y_intercept(slope: float, point: Point) -> float`.

With that function in hand, we can reduce our list of Points down to a
hash map whose keys are y-intercepts, and whose values are lists of
Points.

Now, we've got a hash map that looks like this:

```raw
{
    0: [points...],
    1: [points...],
    2: [points...],
    3: [points...],
    4: [points...],
}
```

Where the points are only those points that lie on the line with the
y-intercept specified by the key. This means we're basically done.
We can sort the keys of the hash map, and for each key, print the
point values in order.

What's superb here is that all we need to do to support any slope at all
is to recognize that for _positive_ slopes we want to walk our y-intercepts
in descending order, while for _negative_ slopes we walk in ascending
order. So, we choose a sorting strategy appropriately. From there,
because we mapped over the arrays from "top left" to "bottom right"
when constructing our points, we can keep them in their order of insertion
for negative slopes, or reverse them for positive slopes. Easy!

What's particularly nice about this solution is that it's entirely
resilient to most or all of the edge/corner cases that trip up most
solutions. Because we're not assuming anything about the length of the
outer array or any sub-arrays, it is completely amenable to sub-arrays
of different lengths. It also correctly does nothing for an empty
outer array or empty inner array. Finally, it supports slopes of different
magnitudes. Changing the -1 to a 1 gets us lines going from bottom left
to top right, rather than top left to bottom right. It even has no
trouble with slopes like 1/2.

## Complexity

How does it do on time complexity? To some degree, this depends on the
language. In JavaScript, for example, where all array operations return
new arrays, it involves a fairly large number of iterations over the
2D array. In Python, on the other hand, where array operations return
generators, it involves only one full loop over the members of the 2D
array. The Rust solution is able to use a mix of generators and vectors,
and is also quite fast. Once the hash map is generated, the keys must
be sorted. The speed of that will depend on the sorting algorithm
used by the language, but in any case, the maximum number of y-intercepts
is _n_, where _n_ is the length of the subarray of a 2D array containing
only one array, or any number of sub-arrays whose lengths are all 1.
If we assume this worst case, and the language does not maintain insertion
order in hash maps, the sorting of the array keys brings us to _O(n log n)_,
but the average case will be much better than this, because the number of
y-intercepts decreases non-linearly relative to the total number of
elements the longer the outer array is.

Space complexity is also highly language-dependent. All languages require
the construction of a Point for each element of the array, which will
take the amount of memory for the array element's value plus integers
for the x and y coordinates. In Rust, this and all further operations are
accomplished with a direct reference to the original array, making the
requisite space quite small. Regardless, though, the space complexity does
not grow at a greater rate than the input array, and so is probably _O(n)_.
