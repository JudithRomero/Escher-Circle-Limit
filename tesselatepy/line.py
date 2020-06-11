from point import Point
from typing import Optional
from decimal_math import Decimal, atan2, pi, sqrt, copy_abs
from abc import ABC, abstractmethod
from scl import Scl
from circular_curve import CircularCurve


class Line(ABC):
  def __init__(self, a: Point, b: Point, is_straight: bool):
    self.a = a
    self.b = b
    self.is_straight = is_straight

  # reflect the point R thru the this line to get Q the returned point
  @abstractmethod
  def reflect(self, r: Point) -> Point:
    pass

  # append screen coordinates to the list in order to draw the line
  @abstractmethod
  def append_scl(self, scl: Optional[Scl], width: int, height: int) -> Scl:
    pass

  @staticmethod
  def new(a: Point, b: Point) -> 'CircleLine':
    den = a.x * b.y - b.x * a.y
    if copy_abs(den) == Decimal(0):
      return _StraightLine(a, b)
    return CircleLine(a, b, den)

class _StraightLine(Line):
  __slots__ = ('a', 'b', 'p', 'd')

  def __init__(self, a: Point, b: Point):
    super().__init__(a, b, True)
    self.p = a
    den = a.minusc(b).norm()
    self.d = Point((b.x - a.x) / den, (b.y - a.y) / den)

  def reflect(self, r: Point) -> Point:
    factor = Decimal(2) * ((r.x - self.p.x) * self.d.x + (r.y - self.p.y) * self.d.y)
    return Point(
      Decimal(2) * self.p.x + factor * self.d.x - r.x,
      Decimal(2) * self.p.y + factor * self.d.y - r.y
    )

  def append_scl(self, scl: Optional[Scl], width: int, height: int) -> Scl:
    x_center = width // 2
    y_center = height // 2
    radius = min(x_center, y_center)
    x: int = round(self.a.x * radius + x_center)
    y: int = round(self.a.y * radius + y_center)
    if not scl or x != scl.x or y != scl.y:
      scl = Scl(scl, x, y)
    x = round(self.b.x * radius + x_center)
    y = round(self.b.y * radius + y_center)
    if x != scl.x or y != scl.y:
      scl = Scl(scl, x, y)
    return scl

class CircleLine(Line):
  __slots__ = ('a', 'b', 'c', 'r')

  def __init__(self, a: Point, b: Point, den: Decimal):
    super().__init__(a, b, False)
    s1 = (Decimal(1) + a.norm_squared()) / Decimal(2)
    s2 = (Decimal(1) + b.norm_squared()) / Decimal(2)
    self.c = Point((s1 * b.y - s2 * a.y) / den, (a.x * s2 - b.x * s1) / den)
    self.r = sqrt(self.c.norm_squared() - Decimal(1))

  def reflect(self, r: Point) -> Point:
    factor = self.r * self.r / r.minusc(self.c).norm_squared()
    return Point(self.c.x + factor * (r.x - self.c.x), self.c.y + factor * (r.y - self.c.y))

  def append_scl(self, scl: Optional[Scl], width: int, height: int) -> Scl:
    x_center = width // 2
    y_center = height // 2
    radius = min(x_center, y_center)
    assert(not self.a.is_nan() and not self.b.is_nan())
    x: int = round(self.a.x * radius + x_center)
    y: int = round(self.a.y * radius + y_center)
    if not scl or x != scl.x or y != scl.y:
      scl = Scl(scl, x, y)
    alpha = atan2(self.a.y - self.c.y, self.a.x - self.c.x)
    beta = atan2(self.b.y - self.c.y, self.b.x - self.c.x)
    if copy_abs(beta-alpha) > pi:
      if beta < alpha:
        beta += Decimal(2) * pi
      else:
        alpha += Decimal(2) * pi
    curve = CircularCurve(self.c.x, self.c.y, self.r, x_center, y_center, radius)
    scl = curve.interpolate(scl, alpha, beta)
    return scl
