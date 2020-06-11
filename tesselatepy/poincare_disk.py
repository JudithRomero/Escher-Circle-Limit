from random import choice
from typing import List, Tuple
from polygon import Polygon, construct_center_polygon, poly
from line import CircleLine, Line
from point import Point


Color = str

class DiskParams:
  def __init__(self, n: int, k: int, layers: int, size: int, colors: List[Color]):
    self.n = n
    self.k = k
    # algorithm depth
    # suggested max: 4
    self.layers = layers
    # image size
    self.width = size
    self.height = size
    self.colors = colors or flatcolors
    self._color_index = choice(range(len(self.colors)))

  def random_color(self) -> Color:
    result = self.colors[self._color_index]
    self._color_index = (self._color_index + 1) % len(self.colors)
    return result

class PoincareDisk:
  def __init__(self, n: int, polys: List[Polygon], rule: List[int], total: int, inner: int, colors: List[Color]):
    self.n = n
    self.polys = polys
    self.rule = rule
    self.total = total
    self.inner = inner
    self.colors = colors

  def draw(self):
    pass

  @staticmethod
  def new(params: DiskParams) -> 'PoincareDisk':
    inner, total = count_polys(params)
    return determine_polys(inner, total, params)

def count_polys(params: DiskParams) -> Tuple[int, int]:
  inner, total = 0, 1
  n = params.n
  k = params.k
  a = n * (k - 3)
  b = n
  next_a, next_b = 0, 0
  if k == 3:
    for layer in range(1, params.layers + 1):
      inner = total
      next_a = a + b
      next_b = (n - 6) * a + (n - 5) * b
      total += a + b
      a = next_a
      b = next_b
  else:
    for layer in range(1, params.layers + 1):
      inner = total
      next_a = ((n - 2) * (k - 3) - 1) * a + ((n - 3) * (k - 3) - 1) * b
      next_b = (n - 2) * a + (n - 3) * b
      total += a + b
      a = next_a
      b = next_b
  return inner, total

def determine_polys(inner: int, total: int, params: DiskParams) -> PoincareDisk:
  polys = [poly(0) for _ in range(total)]
  rule = [0] * total
  colors = [""] * total
  polys[0] = construct_center_polygon(params.n, params.k, False)
  colors[0] = params.random_color()
  # index of the next polygon to create
  j = 1
  for i in range(inner):
    j = apply_rule(i, j, rule, params, polys, colors)
  return PoincareDisk(params.n, polys, rule, total, inner, colors)

def apply_rule(i: int, j: int, rule: List[int], params: DiskParams, polys: List[Polygon], colors: List[Color]) -> int:
  is_alternating = params.k % 2 == 0
  r = rule[i]
  special = r == 1
  if special: r = 2
  start = 3 if r == 4 else 2
  quantity = params.n - r - 1 if params.k == 3 and r else params.n - r
  for s in range(start, start + quantity):
    # create a polygon adjacent to P[i]
    polys[j] = create_next_poly(polys[i], s % params.n, params.n)
    rule[j] = 4 if params.k == 3 and s == start and r else 3
    if is_alternating and j > 1:
      colors[j] = colors[1] if colors[i] == colors[0] else colors[0]
    else:
      colors[j] = params.random_color()
    j += 1
    m = 0
    if special: m = 2
    elif s==2 and r: m = 1
    for m in range(m, params.k - 3):
      # Create a polygon adjacent to P[j-1]
      polys[j] = create_next_poly(polys[j - 1], 1, params.n)
      rule[j] = 1 if params.n == 3 and m == params.k - 4 else 2
      if is_alternating:
        colors[j] = colors[1] if colors[j - 1] == colors[0] else colors[0]
      else:
        colors[j] = params.random_color()
      j += 1
  return j

# reflect P thru the point or the side indicated by the side s
# to produce the resulting polygon Q
def create_next_poly(p: Polygon, s: int, n: int) -> Polygon:
  q = poly(n)
  c = Line.new(p[s], p[(s + 1) % n])
  for i in range(n):
    j = (n + s - i + 1) % n
    q[j] = c.reflect(p[i])
  return q

# https://flatuicolors.com/palette/defo
flatcolors = [
  "#1abc9c",
  "#2ecc71",
  "#3498db",
  "#9b59b6",
  "#34495e",
  "#16a085",
  "#27ae60",
  "#2980b9",
  "#8e44ad",
  "#2c3e50",
  "#f1c40f",
  "#e67e22",
  "#e74c3c",
  "#ecf0f1",
  "#95a5a6",
  "#f39c12",
  "#d35400",
  "#c0392b",
  "#bdc3c7",
  "#7f8c8d",
]

def random_color() -> Color:
  return choice(flatcolors)
