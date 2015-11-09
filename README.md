### Introduction

This Python module simplifies the task of setting up complex subplot arrangements in `matplotlib`.

The module requires Python 3.3 or later.

### Description

A figure in `matplotlib` refers to the entire plotting area, while a set of axes is the technical name for a subplot. (Note that the singular term 'axis' means either an _x_-axis or a _y_-axis, whereas the plural term 'axes' is understood to be the subplot spanned by two axes.) The positioning and sizing of the figure and the sets of axes are determined by the coordinates of their individual upper-left and lower-right corners, `(x1, y1)` and `(x2, y2)`. This module allows the user to place the figure and sets of axes by requiring the coordinates to satisfy certain linear relationships; the geometry of the figure and all sets of axes can be determined once a sufficient number of independent constraints are furnished.

### Examples

Suppose we would like to have two subplots side by side in a row. We first create a layout object for two sets of axes:

    import mpllayout
    layout = mpllayout.ConstraintLayout(2)

The module adopts a coordinate system in which the origin is at the upper-left corner of the figure, and the positive _x_- and _y_-directions are rightward and downward respectively. To have the subplots horizontally adjacent to each other with a gap in between, we specify the constraints

    layout.axes[1].x1.set_equal(layout.axes[0].x2 + '1in')
    layout.axes[1].y1.set_equal(layout.axes[0].y1)

The method `set_equal()` forces its argument to be equal to the object the method is bound to. The assignment operator `=` must not be used here since we are merely stating a constraint. Lengths can be given as numbers, in which case they are interpreted as in inches; they can also be strings, with a number followed by a unit chosen from `in`, `cm`, and `pt`.

If we want the two subplots to have the same size, we can say

    layout.set_same_size(layout.axes)

This is equivalent to

    layout.axes[1].dx.set_equal(layout.axes[0].dx)
    layout.axes[1].dy.set_equal(layout.axes[0].dy)

where `dx` and `dy` are shorthands for `x2 - x1` and `y2 - y1`.

The figure and the two sets of axes are described by 12 coordinates. The upper-left corner of the figure is always `(0, 0)`, hence there are only 10 free parameters. We can easily provide 6 more constraints:

    layout.figure.dx.set_equal('8in')
    layout.figure.dy.set_equal('6in')
    layout.axes[0].dx.set_equal('2in')
    layout.axes[0].dy.set_equal(layout.axes[0].dx)
    (layout.figure.x2 - layout.axes[-1].x2).set_equal(layout.axes[0].x1 - layout.figure.x1)
    (layout.figure.y2 - layout.axes[-1].y2).set_equal(layout.axes[0].y1 - layout.figure.y1)

We have created a figure of fixed size with two centered square subplots. The result can be displayed with

    layout.apply()
    from matplotlib import pyplot
    pyplot.show()

This may seem a lot of work for assembling two subplots, but this approach truly shines through when subplot placement is regular but non-trivial.

The file `examples.py` contains more advanced examples on how to use the module. It also demonstrates the use of another convenience method `place_on_grid()`, which spaces out sets of axes horizontally and vertically on a grid. The user can run the script and see the examples in action, or modify the examples for other use cases.

### Issues

A new layout object must be created if coordinates need to be updated in response to, say, a change in figure size.
