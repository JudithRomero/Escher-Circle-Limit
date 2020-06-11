from poincare_disk import PoincareDisk, DiskParams
from polygon import get_scl
from PIL import Image
from PIL import ImageDraw
from time import monotonic


params = DiskParams(n=5, k=6, layers=4, width=640, height=480)
disk = PoincareDisk.new(params)
im = Image.new('RGB', (params.width, params.height))
draw = ImageDraw.Draw(im)

total = 0
amount = len(disk.polys)
report_seconds = 3
insignificants = 0
start_time = monotonic()
current_time = start_time
print('total polys:', amount)

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
im.show()
