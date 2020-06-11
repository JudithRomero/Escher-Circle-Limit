from argparse import ArgumentParser
from sys import argv as sys_argv
from poincare_disk import DiskParams
from typing import List, Optional
from PIL import Image
from main import main


class Args:
  def __init__(self, params: DiskParams, face_color: Optional[str], fishes: List['Image'], output: str, poincare: bool):
    self.params = params
    self.face_color = face_color
    self.fishes = fishes
    self.output = output
    self.poincare = poincare

  @staticmethod
  def parse(argv: List[str]) -> Optional['Args']:
    parser = ArgumentParser()
    parser.add_argument('--output', '-o', help='output image filename, i.e "tesselation.png"', required=True)
    parser.add_argument('--color', help='face color, i.e "#3d3d3d"; if none given random color will be used')
    parser.add_argument('--poincare', help='draw poincare model instead of klein', action='store_true')
    parser.add_argument('--layers', type=int, help='algorithm recursion depth, default: 4', default=4)
    parser.add_argument('--size', type=int, help='output image width and height, default: 800px', default=800)
    parser.add_argument('--edge', '-e', nargs='*', help='image filename, that will be used randomly on edges', required=True)
    parser.add_argument('--vertices', '-p', type=int, help='number of vertices of each polygon, (p-2)(q-2) must be > 4', required=True)
    parser.add_argument('--adjacency', '-q', type=int, help='number of polygons adjacent to each vertex, (p-2)(q-2) must be > 4', required=True)
    parsed = parser.parse_args(argv)
    p = parsed.vertices
    q = parsed.adjacency
    fst_image = None
    images = []
    allowed_extensions = ['.png', '.jpg', '.bmp']
    if not any(map(parsed.output.endswith, allowed_extensions)):
      print('output filename should have one of these extensions:', ', '.join(allowed_extensions))
      return None
    if (p - 2) * (q - 2) <= 4:
      print('(p-2)(q-2) must be > 4')
      return None
    for edge in parsed.edge:
      try:
        image = load_image(edge)
        if not fst_image:
          fst_image = image
        if image.size != fst_image.size:
          print('All edge images must be equal size')
          return None
        images.append(image)
      except Exception as e:
        print(f"Can't load image '{edge}': {e}")
        return None
    params = DiskParams(p, q, parsed.layers, parsed.size)
    return Args(params, parsed.color, images, parsed.output, parsed.poincare)

def load_image(path: str) -> 'Image':
  return Image.open(path).convert('RGBA')

if __name__ == '__main__':
  args = Args.parse(sys_argv[1:])
  if not args:
    exit(1)
  else:
    main(args.params, args.face_color, args.fishes, args.output, args.poincare)
