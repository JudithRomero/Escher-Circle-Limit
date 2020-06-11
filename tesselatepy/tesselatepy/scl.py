from typing import Optional, List, Tuple

class Scl:
  __slots__ = ('link', 'x', 'y')

  def __init__(self, link: Optional['Scl'] = None, x: int = 0, y: int = 0):
    self.link = link
    self.x = x
    self.y = y

  def points(self) -> List[Tuple[int, int]]:
    result: List[Tuple[int, int]] = []
    last: Optional[Scl] = self
    while last:
      result.append((last.x, last.y))
      last = last.link
    return result

  def __repr__(self) -> str:
    return f'Scl({len(self.points())} points)'
