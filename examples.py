from matplotlib import pyplot
import mpllayout

def example_1():
  layout = mpllayout.ConstraintLayout(1)

  layout.figure.dx.set_equal('10in')
  (layout.axes[0].x1 - layout.figure.x1).set_equal('1in')
  (layout.axes[0].y1 - layout.figure.y1).set_equal('0.5in')
  (layout.figure.x2 - layout.axes[0].x2).set_equal('1in')
  (layout.figure.y2 - layout.axes[0].y2).set_equal('0.5in')

  layout.axes[0].dy.set_equal(0.5 * layout.axes[0].dx)

  return layout

def example_2():
  layout = mpllayout.ConstraintLayout(8)
  main_axes = layout.axes[:len(layout.axes)//2]
  top_axes = layout.axes[len(layout.axes)//2:]

  layout.figure.dx.set_equal('10in')
  bx = layout.axes[0].x1 - layout.figure.x1
  by = layout.axes[0].y1 - layout.figure.y1
  bx.set_equal(by)
  (layout.figure.x2 - main_axes[-1].x2).set_equal(bx)
  (layout.figure.y2 - main_axes[-1].y2).set_equal(by)

  layout.set_same_size(main_axes)
  layout.set_same_size(top_axes)
  main_axes[0].dx.set_equal(0.4 * layout.figure.dx)
  main_axes[0].dy.set_equal(main_axes[0].dx)
  top_axes[0].x1.set_equal(main_axes[0].x1 + 0.2 * main_axes[0].dx)
  top_axes[0].x2.set_equal(main_axes[0].x2 - 0.2 * main_axes[0].dx)
  top_axes[0].dy.set_equal('0.3in')

  layout.place_on_grid(main_axes, 2, 2,
    0.5*bx,
    main_axes[0].y2 - top_axes[0].y1 + 0.5*by - main_axes[0].dy)
  layout.place_on_grid(top_axes, 2, 2,
    main_axes[0].dx + 0.5*bx - top_axes[0].dx,
    main_axes[0].y2 - top_axes[0].y1 + 0.5*by - top_axes[0].dy)
  top_axes[0].y2.set_equal(main_axes[0].y1 - '0.1in')

  return layout

def example_3():
  layout = mpllayout.ConstraintLayout(32)
  main_axes = layout.axes[:len(layout.axes)//2]
  bottom_axes = layout.axes[len(layout.axes)//2:]

  layout.figure.dx.set_equal('10in')
  (layout.axes[0].x1 - layout.figure.x1).set_equal('1in')
  (layout.axes[0].y1 - layout.figure.y1).set_equal('1in')
  (layout.figure.x2 - layout.axes[-1].x2).set_equal('1in')
  (layout.figure.y2 - layout.axes[-1].y2).set_equal('1in')

  layout.set_same_size(main_axes)
  layout.set_same_size(bottom_axes)
  main_axes[0].dy.set_equal(main_axes[0].dx)
  bottom_axes[0].dx.set_equal(main_axes[0].dx)
  bottom_axes[0].dy.set_equal(0.2 * main_axes[0].dy)

  layout.place_on_grid(main_axes, 4, 4,
    ['0in', '0.5in'], [bottom_axes[0].dy, bottom_axes[0].dy + '0.5in'])
  layout.place_on_grid(bottom_axes, 4, 4,
    ['0in', '0.5in'], [main_axes[0].dy, main_axes[0].dy + '0.5in'])
  bottom_axes[0].x1.set_equal(main_axes[0].x1)
  bottom_axes[0].y1.set_equal(main_axes[0].y2)

  return layout

def example_4():
  layout = mpllayout.ConstraintLayout(16)

  layout.figure.dx.set_equal('10in')
  layout.figure.dy.set_equal('10in')
  (layout.axes[0].x1 - layout.figure.x1).set_equal(0.1 * layout.figure.dx)
  (layout.axes[0].y1 - layout.figure.y1).set_equal(0.1 * layout.figure.dy)
  (layout.figure.x2 - layout.axes[-1].x2).set_equal(0.1 * layout.figure.dx)
  (layout.figure.y2 - layout.axes[-1].y2).set_equal(0.1 * layout.figure.dy)

  layout.set_same_size(layout.axes[0::8] + layout.axes[2::8])
  layout.set_same_size(layout.axes[1::8] + layout.axes[3::8])
  layout.set_same_size(layout.axes[4::8] + layout.axes[6::8])
  layout.set_same_size(layout.axes[5::8] + layout.axes[7::8])
  layout.axes[1].dx.set_equal(0.6 * layout.axes[0].dx)
  layout.axes[1].dy.set_equal(layout.axes[0].dy)
  layout.axes[4].dx.set_equal(layout.axes[0].dx)
  layout.axes[4].dy.set_equal(0.4 * layout.axes[0].dy)
  layout.axes[5].dx.set_equal(0.6 * layout.axes[0].dx)
  layout.axes[5].dy.set_equal(0.4 * layout.axes[0].dy)

  layout.place_on_grid(layout.axes, 4, 4, 0, 0)

  return layout

def example_5():
  layout = mpllayout.ConstraintLayout(9)

  layout.figure.dx.set_equal('10in')
  bx = layout.axes[0].x1 - layout.figure.x1
  by = layout.axes[0].y1 - layout.figure.y1
  bx.set_equal(by)
  (layout.figure.x2 - layout.axes[5].x2).set_equal(bx)
  (layout.figure.y2 - layout.axes[-1].y2).set_equal(by)

  layout.set_same_size(layout.axes)
  layout.axes[0].dx.set_equal('2in')
  layout.axes[0].dy.set_equal(layout.axes[0].dx)

  sx = 0.2 * layout.axes[0].dx
  sy = 0.2 * layout.axes[0].dy
  layout.place_on_grid(layout.axes[0:3], 3, 1, sx, 0)
  layout.place_on_grid(layout.axes[3:6], 3, 1, sx, 0)
  layout.place_on_grid(layout.axes[6:9], 3, 1, sx, 0)
  layout.axes[3].x1.set_equal(layout.axes[0].x1 + 0.5 * layout.axes[0].dx)
  layout.axes[3].y1.set_equal(layout.axes[0].y2 + sy)
  layout.axes[6].x1.set_equal(layout.axes[0].x1)
  layout.axes[6].y1.set_equal(layout.axes[3].y2 + sy)

  return layout

def show_example(layout):
  layout.apply(pyplot.gcf())
  for n, axes in enumerate(pyplot.gcf().axes):
    pyplot.sca(axes)
    pyplot.annotate(str(n), xy=[0.5, 0.5], ha='center', va='center')
    pyplot.xticks([])
    pyplot.yticks([])
  pyplot.show()

if __name__ == '__main__':
  show_example(example_1())
  show_example(example_2())
  show_example(example_3())
  show_example(example_4())
  show_example(example_5())
