import itertools
import numbers
import numpy
import numpy.linalg
import weakref

class ConstraintLayout:
  def __init__(self, axes_count):
    rect_count = axes_count + 1
    self.coord_count = 4 * rect_count

    coeffs_list = numpy.eye(self.coord_count, self.coord_count+1)
    length_exprs = [LengthExpr(self, coeffs) for coeffs in coeffs_list]

    self.figure = Rectangle(length_exprs[:4])
    self.axes = [Rectangle(length_expr_tuple) for
      length_expr_tuple in iterate_tuple(length_exprs[4:], 4)]

    self.lhs = numpy.empty((self.coord_count, self.coord_count))
    self.rhs = numpy.empty(self.coord_count)
    self.lhs[:2] = self.rhs[:2] = 0
    self.lhs[0, 0] = self.lhs[1, 1] = 1
    self.curr_constraint = 2

  @staticmethod
  def set_same_size(rects):
    first_rect = rects[0]
    for rect in rects[1:]:
      first_rect.dx.set_equal(rect.dx)
      first_rect.dy.set_equal(rect.dy)

  @staticmethod
  def place_on_grid(rects, nx, ny, sx, sy):
    if nx * ny != len(rects):
      raise ValueError('number of rectangles cannot fill grid')

    if isinstance(sx, str) or not hasattr(sx, '__iter__'):
      sx = [sx]
    if isinstance(sy, str) or not hasattr(sy, '__iter__'):
      sy = [sy]

    def delayed(iterable):
      yield None
      yield from iterable

    for i, sy_ in zip(range(ny), delayed(itertools.cycle(sy))):
      for j, sx_ in zip(range(nx), delayed(itertools.cycle(sx))):
        rect = rects[i*nx+j]
        if i > 0:
          above_rect = rects[(i-1)*nx+j]
          rect.x1.set_equal(above_rect.x1)
          rect.y1.set_equal(above_rect.y2 + sy_)
        elif j > 0:
          left_rect = rects[i*nx+(j-1)]
          rect.x1.set_equal(left_rect.x2 + sx_)
          rect.y1.set_equal(left_rect.y1)

  def add_constraint(self, lhs, rhs):
    if self.curr_constraint >= self.lhs.shape[0]:
      raise ValueError('too many constraints have been specified')

    self.lhs[self.curr_constraint] = lhs
    self.rhs[self.curr_constraint] = rhs
    self.curr_constraint += 1

  def solve(self):
    if self.curr_constraint < self.lhs.shape[0]:
      raise ValueError('{} more constraint(s) must be specified'
        .format(self.lhs.shape[0] - self.curr_constraint))

    try:
      singular_values = numpy.linalg.svd(self.lhs, compute_uv=False)
    except numpy.linalg.LinAlgError:
      raise ValueError('constraints are singular')
    else:
      if min(singular_values) / max(singular_values) < 1e-6:
        raise ValueError('constraints are ill-conditioned')

    try:
      solution = numpy.linalg.solve(self.lhs, self.rhs)
    except numpy.linalg.LinAlgError:
      raise ValueError('constraints are singular')

    self.coords = list(iterate_tuple(solution, 4))

    for n ,coords in enumerate(self.coords):
      print('{} | {:7.4f} {:7.4f} {:7.4f} {:7.4f} | {:7.4f} {:7.4f}'.format(
        '{:2d}'.format(n-1) if n > 0 else '  ',
        coords[0], coords[1], coords[2], coords[3],
        coords[2]-coords[0], coords[3]-coords[1]))

  def apply(self, figure=None):
    if not hasattr(self, 'coords'):
      self.solve()

    figure_dx, figure_dy = self.coords[0][2:]
    if figure:
      figure.set_size_inches(figure_dx, figure_dy, forward=True)
    else:
      from matplotlib import pyplot
      figure = pyplot.figure(figsize=(figure_dx, figure_dy))

    for x1, y1, x2, y2 in self.coords[1:]:
      figure.add_axes(
        (x1/figure_dx, 1-y2/figure_dy, (x2-x1)/figure_dx, (y2-y1)/figure_dy))

class Rectangle:
  def __init__(self, length_exprs):
    self.x1, self.y1, self.x2, self.y2 = length_exprs
    self.dx = self.x2 - self.x1
    self.dy = self.y2 - self.y1

class LengthExpr:
  def __init__(self, layout, coeffs):
    if isinstance(layout, weakref.ref):
      self.layout = layout
    else:
      self.layout = weakref.ref(layout)
    self.coeffs = coeffs

  def __pos__(self):
    return LengthExpr(self.layout, numpy.copy(self.coeffs))

  def __neg__(self):
    return LengthExpr(self.layout, -self.coeffs)

  def __add__(self, other):
    if isinstance(other, LengthExpr) and self.layout is other.layout:
      return LengthExpr(self.layout, self.coeffs + other.coeffs)
    elif isinstance(other, numbers.Number):
      coeffs = numpy.copy(self.coeffs)
      coeffs[-1] += other
      return LengthExpr(self.layout, coeffs)
    elif isinstance(other, str):
      return self + parse_length(other)
    return NotImplemented

  def __sub__(self, other):
    if isinstance(other, LengthExpr) and self.layout is other.layout:
      return LengthExpr(self.layout, self.coeffs - other.coeffs)
    elif isinstance(other, numbers.Number):
      coeffs = numpy.copy(self.coeffs)
      coeffs[-1] -= other
      return LengthExpr(self.layout, coeffs)
    elif isinstance(other, str):
      return self - parse_length(other)
    return NotImplemented

  def __mul__(self, other):
    if isinstance(other, numbers.Number):
      return LengthExpr(self.layout, self.coeffs * other)
    return NotImplemented

  def __truediv__(self, other):
    if isinstance(other, numbers.Number):
      return LengthExpr(self.layout, self.coeffs / other)
    return NotImplemented

  def __radd__(self, other):
    if isinstance(other, numbers.Number):
      return self + other
    elif isinstance(other, str):
      return self + parse_length(other)
    return NotImplemented

  def __rsub__(self, other):
    if isinstance(other, numbers.Number):
      return -self + other
    elif isinstance(other, str):
      return -self + parse_length(other)
    return NotImplemented

  def __rmul__(self, other):
    if isinstance(other, numbers.Number):
      return self * other
    return NotImplemented

  def set_equal(self, other):
    if isinstance(other, LengthExpr):
      coeffs = self.coeffs - other.coeffs
      self.layout().add_constraint(coeffs[:-1], -coeffs[-1])
    elif isinstance(other, numbers.Number):
      self.layout().add_constraint(self.coeffs[:-1], other - self.coeffs[-1])
    elif isinstance(other, str):
      return self.set_equal(parse_length(other))
    else:
      raise TypeError("length cannot be set equal to type '{}'"
        .format(type(other).__name__))

def iterate_tuple(iterable, count):
  return itertools.zip_longest(*[iter(iterable)] * count)

def parse_length(string):
  units = {'in': 1, 'cm': 1/2.54, 'pt': 1/72}
  string = string.rstrip()
  for unit, conversion in units.items():
    if string.endswith(unit):
      return float(string[:-len(unit)]) * conversion
  raise ValueError('string does not represent a length')
