from poincare_disk import PoincareDisk, DiskParams, random_color
from polygon import get_scl, Polygon, get_lines
from point import Point
from PIL import Image
from PIL import ImageDraw
from PIL.ImageOps import invert
from time import monotonic
from typing import List, Tuple, Optional, Set, cast
from decimal_math import Decimal, pi, atan2, sqrt
from random import choice


def is_similar_line_nondirectional(a: Tuple[Point, Point], b: Tuple[Point, Point]) -> bool:
  a0, a1 = a
  b0, b1 = b
  return max(a0.minusc(b0).norm_squared(), a1.minusc(b1).norm_squared()) < 1e-10

def is_similar_line(a: Tuple[Point, Point], b: Tuple[Point, Point]) -> bool:
  b0, b1 = b
  return is_similar_line_nondirectional(a, b) or is_similar_line_nondirectional(a, (b1, b0))

def get_unique_lines(polys: List[Polygon]) -> List[Tuple[Point, Point]]:
  points: List[Point] = []
  lines: Set[Tuple[int, int]] = set()
  total = 0
  prec = 1e-10
  for poly in polys:
    for line in get_lines(poly):
      ln = []
      total += 2
      for candidate in [line.a, line.b]:
        index = next((i for i, pt in enumerate(points) if pt.minusc(candidate).norm_squared() <= prec), -1)
        if index == -1:
          index = len(points)
          points.append(candidate)
        ln.append(index)
      lines.add(cast(Tuple[int, int], tuple(ln)))
  result: List[Tuple[Point, Point]] = []
  unique_lines: Set[Tuple[int, int]] = set()
  for (a_index, b_index) in lines:
    if (b_index, a_index) in unique_lines: continue
    unique_lines.add((a_index, b_index))
    pair = points[a_index], points[b_index]
    result.append(pair)
  return result

def invert_image(image: Image) -> Image:
  if image.mode == 'RGBA':
    r, g, b, a = image.split()
    rgb_image = Image.merge('RGB', (r, g, b))
    inverted_image = invert(rgb_image)
    r2, g2, b2 = inverted_image.split()
    return Image.merge('RGBA', (r2, g2, b2, a))
  else:
    return invert(image)

def monochrome(image: Image) -> Image:
  r, g, b, a = image.split()
  r2, g2, b2 = image.convert('1').convert('RGB').split()
  return Image.merge('RGBA', (r2, g2, b2, a))

def show_kleine_fishes(polys: List[Polygon], size: int, fishes: List['Image'], fname: str, face_color: Optional[str]):
  hs = size // 2
  offset = Point(Decimal(hs), Decimal(hs))
  im = Image.new('RGBA', (size, size))
  fish = fishes[0]
  fish_aspect = Decimal(fish.size[0] / fish.size[1])
  draw = ImageDraw.Draw(im)
  for poly in polys:
    pts = [p.times(Decimal(hs)).plusc(offset) for p in poly]
    pil_pts = [(pt.x, pt.y) for pt in pts]
    draw.polygon(pil_pts, fill=face_color or random_color())
  print('getting unique lines...')
  lines = get_unique_lines(polys)
  lines.sort(key=lambda a: a[0].minusc(a[1]).norm_squared())
  print('sorting...')
  for i, line in enumerate(lines):
    a, b = line
    start = a.times(Decimal(hs)).plusc(offset)
    end = b.times(Decimal(hs)).plusc(offset)
    # https://stackoverflow.com/a/1937202
    se = start.minusc(end)
    linelength = se.norm()
    angle = atan2(se.y, se.x)
    angle_deg = angle / pi * Decimal(180)
    thickness = linelength / fish_aspect
    if min(linelength, thickness) < 1: continue
    new_fish = choice(fishes)
    new_fish = new_fish.resize((linelength, thickness), Image.ANTIALIAS).rotate(180 - float(angle_deg), expand=True)
    ax, ay = 0, 0
    fx, fy = new_fish.size
    dx, dy = min(start.x, end.x), min(start.y, end.y)
    px = Decimal(-0.5) * thickness * (se.y / linelength)
    py = Decimal(0.5) * thickness * (se.x / linelength)
    dx = min(start.x + px, end.x + px, end.x - px, start.x - px)
    dy = min(start.y + py, end.y + py, end.y - py, start.y - py)
    # continue
    # draw.polygon([(dx, dy), (dx + fx, dy), (dx + fx, dy + fy), (dx, dy + fy)], outline='blue')
    try:
      im.paste(new_fish, (dx, dy), new_fish)
    except: continue
    r = 5
    # draw.ellipse((dx - r, dy - r, dx + r, dy + r), fill='red')
  fname = '' + fname
  print(f'Kleine model will be saved as: "{fname}"')
  if fname.endswith('.jpg'):
    im = im.convert('RGB')
  im.save(fname)
  im.show()

def main(params: DiskParams, face_color: Optional[str], fishes: List['Image'], output: str, poincare: bool):
  disk = PoincareDisk.new(params)
  im = Image.new('RGBA', (params.width, params.height))
  draw = ImageDraw.Draw(im)
  total = 0
  amount = len(disk.polys)
  report_seconds = 3
  insignificants = 0
  start_time = monotonic()
  current_time = start_time
  print('total polys:', amount)
  if not poincare:
    show_kleine_fishes(disk.polys, min(params.width, params.height), fishes, output, face_color)
    return
  for i, (poly, color) in enumerate(zip(disk.polys, disk.colors), 1):
    pts = get_scl(poly, params.width, params.height).points()
    current = len(pts)
    total += current
    if monotonic() > current_time + report_seconds:
      current_time = monotonic()
      print(f'[{i}/{amount}] points in poly: {current}, total: {total}, insignificants: {insignificants}')
    if current < 2:
      insignificants += 1
      continue
    draw.polygon(pts, fill=color)
  print(f'total points: {total}, insignificants: {insignificants}, elapsed: {round(monotonic() - start_time)}s')
  print(f'poincare model will be saved as: "{output}"')
  if output.endswith('.jpg'):
    im = im.convert('RGB')
  im.show()
  im.save(output)
