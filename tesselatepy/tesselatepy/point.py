from decimal_math import Decimal, sqrt, is_nan


class Point:
  __slots__ = ('x', 'y')

  def __init__(self, x: Decimal, y: Decimal):
    self.x = x
    self.y = y

  def is_nan(self) -> bool:
    return is_nan(self.x) or is_nan(self.y)

  def __repr__(self) -> str:
    return f'({self.x}, {self.y})'

  def inner_product(self, other: 'Point') -> Decimal:
    return other.x * self.x + other.y * self.y

  def norm_squared(self) -> Decimal:
    return self.inner_product(self)
  
  def norm(self) -> Decimal:
    return sqrt(self.norm_squared())

  def conjugate(self) -> 'Point':
    return Point(self.x, -self.y)

  def negation(self) -> 'Point':
    return Point(-self.x, self.y)

  def plusc(self, w: 'Point') -> 'Point':
    return Point(self.x + w.x, self.y + w.y)

  def plus(self, t: Decimal) -> 'Point':
    return Point(self.x + t, self.y)

  def minusc(self, w: 'Point') -> 'Point':
    return Point(self.x - w.x, self.y - w.y)

  def minus(self, t: Decimal) -> 'Point':
    return self.plus(-t)

  @staticmethod
  def sub2c(z: 'Point', w: 'Point') -> 'Point':
    return Point(z.x - w.x, z.y - w.y)

  @staticmethod
  def subc(t: Decimal, w: 'Point') -> 'Point':
    return Point(t - w.x, -w.y)

  @staticmethod
  def csub(z: 'Point', t: Decimal) -> 'Point':
    return Point(z.x - t, z.y)

  @staticmethod
  def add2c(z: 'Point', w: 'Point') -> 'Point':
    return Point(z.x + w.x, z.y + w.y)

  @staticmethod
  def cadd(t: Decimal, w: 'Point') -> 'Point':
    return Point(t + w.x, w.y)
  
  @staticmethod
  def addc(z: 'Point', t: Decimal) -> 'Point':
    return Point(z.x, z.y + t)

  def timesc(self, w: 'Point') -> 'Point':
    return Point(self.x * w.x - self.y * w.y, self.y * w.x + self.x * w.y)

  def times(self, t: Decimal) -> 'Point':
    return Point(t * self.x, t * self.y)

  @staticmethod
  def mul2c(z: 'Point', w: 'Point') -> 'Point':
    return Point(z.x * w.x - z.y * w.y, z.y * w.x + z.x * w.y)

  @staticmethod
  def cmul(t: Decimal, w: 'Point') -> 'Point':
    return Point(t * w.x, t * w.y)

  def reciprocal(self) -> 'Point':
    norm = self.norm_squared()
    return Point(self.x / norm, -self.y / norm)

  def overc(self, w: 'Point') -> 'Point':
    norm = self.norm_squared()
    return Point((self.x * w.x + self.y * w.y) / norm, (self.y * w.x - self.x * w.y) / norm)
  
  def over(self, t: Decimal) -> 'Point':
    return Point(self.x / t, self.y / t)

  @staticmethod
  def div2c(z: 'Point', w: 'Point') -> 'Point':
    norm = w.norm_squared()
    return Point((z.x * w.x + z.y * w.y) / norm, (z.y * w.x - z.x * w.y) / norm)

  @staticmethod
  def divc(t: Decimal, w: 'Point') -> 'Point':
    norm = w.norm_squared()
    return Point(t * w.x / norm, -t *w.y / norm)

  @staticmethod
  def cdiv(z: 'Point', t: Decimal) -> 'Point':
    return Point(z.x / t, z.y / t)


  # Reflect the point A through this point B to get the returned point C.
  # The rule for computing A thru B (as complex numbers) is: |
  #
  #            B - t A	         where t = (1+BB')/2, and
  # A |> B = -----------               B' is the complex
  #           t -  A B'                conjugate of B
  #
  def reflect(self, w: 'Point') -> 'Point':
    t = (Decimal(1) + self.norm_squared()) / Decimal(2)
    numerator = self.minusc(w.times(t))
    denominator = Point.subc(t, w.timesc(self.conjugate()))
    return numerator.overc(denominator)
