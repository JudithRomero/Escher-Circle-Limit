from point import Point
from typing import List, Optional, cast
from scl import Scl
from decimal_math import Decimal, sin, pi, cos, sqrt
from line import Line


Polygon = List[Point]

def construct_center_polygon(n: int, k: int, quasiregular: bool) -> Polygon:
  # Initialize P as the center polygon in an n-k regular or quasiregular tiling.
  # Let ABC be a triangle in a regular (n,k0-tiling, where
  #    A is the center of an n-gon (also center of the disk),
  #    B is a vertex of the n-gon, and
  #    C is the midpoint of a side of the n-gon adjacent to B.
  angle_a = pi / n
  angle_b = pi / k
  angle_c = pi / 2
  # For a regular tiling, we need to compute the distance s from A to B.
  sin_a = sin(angle_a)
  sin_b = sin(angle_b)
  s = sin(angle_c - angle_b - angle_a) / sqrt(Decimal(1) - sin_b * sin_b - sin_a * sin_a)
  # But for a quasiregular tiling, we need the distance s from A to C.
  if quasiregular:
    s = (s * s + Decimal(1)) / (Decimal(2) * s * cos(angle_a))
    s = s - sqrt(s * s - Decimal(1))
  # Now determine the coordinates of the n vertices of the n-gon.
  # They're all at distance s from the center of the Poincare disk.
  poly = [Point(s, s) for _ in range(n)]
  for i, pt in enumerate(poly):
    pt.x *= cos(Decimal(3 + 2 * i) * angle_a)
    pt.y *= sin(Decimal(3 + 2 * i) * angle_a)
  return poly

def get_lines(poly: Polygon) -> List[Line]:
  n = len(poly)
  return [Line.new(pt, poly[(i + 1) % n]) for i, pt in enumerate(poly)]

def get_scl(poly: Polygon, width: int, height: int) -> Scl:
  scl: Optional[Scl] = None
  for line in get_lines(poly):
    scl = line.append_scl(scl, width, height)
  return cast(Scl, scl)

def poly(n: int) -> Polygon:
  zero = Decimal(0)
  return [Point(zero, zero) for _ in range(n)]

def is_not_nan(poly: Polygon) -> bool:
  return not any(x.is_nan() for x in poly)
