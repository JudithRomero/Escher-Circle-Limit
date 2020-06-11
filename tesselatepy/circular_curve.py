from decimal_math import Decimal, cos, sin
from scl import Scl
from point import Point
from random import random


class CircularCurve:
  def __init__(self, x: Decimal, y: Decimal, r: Decimal, x_center: int, y_center: int, radius: int):
    self._x = x
    self._y = y
    self._r = r
    self.x_center = x_center
    self.y_center = y_center
    self.radius = radius

  def x(self, t: Decimal) -> Decimal:
    return self._x + self._r * cos(t)
  
  def y(self, t: Decimal) -> Decimal:
    return self._y + self._r * sin(t)

  def x_screen(self, t: Decimal) -> int:
    return round(self.x_center + self.radius * self.x(t))

  def y_screen(self, t: Decimal) -> int:
    return round(self.y_center + self.radius * self.y(t))
  
  def screen(self, t: Decimal) -> Point:
    return Point(Decimal(self.x_screen(t)), Decimal(self.y_screen(t)))

  # Determine if a curve between t=a and t=b is bent at t=c.
  # Say it is if C is outside a narrow ellipse.
  # If it is bent there, subdivide the interval.
  def bent(self, at: Decimal, bt: Decimal, ct: Decimal, scl: Scl) -> Scl:
    a = self.screen(at)
    b = self.screen(bt)
    c = self.screen(ct)
    excess = a.minusc(c).norm() + b.minusc(c).norm() - a.minusc(b).norm()
    if excess > 0.01:
      scl = self.interpolate(scl, at, ct)
      scl = self.interpolate(scl, ct, bt)
    return scl

  # Add to the list the coordinates of the curve (f(t),g(t)) for t
  # between a and b. It is assumed that the point (f(a),g(a)) is
  # already on the list. Enough points will be interpolated between a
  # and b so that the approximating polygon looks like the curve.
  # The last point to be included will be (f(b),g(b)).
  def interpolate(self, scl: Scl, at: Decimal, bt: Decimal) -> Scl:
    # first try bending it at the midpoint
    result = self.bent(at, bt, (at + bt) / Decimal(2), scl)
    if result != scl: return result
    # now try 4 random points
    for i in range(4):
      t = Decimal(random())
      result = self.bent(at, bt, t * at + (Decimal(1) - t) * bt, scl)
      if result != scl: return result
    # it's a straight line
    b1 = self.x_screen(bt)
    b2 = self.y_screen(bt)
    if scl.x != b1 or scl.y != b2:
      scl = Scl(scl, b1, b2)
    return scl
