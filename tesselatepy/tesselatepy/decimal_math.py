import math
from decimal import Decimal, ExtendedContext, setcontext, getcontext


setcontext(ExtendedContext)
getcontext().prec = 30

pi = Decimal(math.pi)

def atan2(y: Decimal, x: Decimal) -> Decimal:
  return Decimal(math.atan2(y, x))

def sqrt(x: Decimal) -> Decimal:
  return x.sqrt()

def is_nan(x: Decimal) -> bool:
  return x.is_nan()

def cos(x: Decimal) -> Decimal:
    getcontext().prec += 2
    i, lasts, s, fact, num, sign = 0, Decimal(0), Decimal(1), 1, Decimal(1), 1
    while s != lasts:
        lasts = s
        i += 2
        fact *= i * (i-1)
        num *= x * x
        sign *= -1
        s += num / fact * sign
    getcontext().prec -= 2
    return +s

def copy_abs(x: Decimal) -> Decimal:
  return x.copy_abs()

def sin(x: Decimal) -> Decimal:
    getcontext().prec += 2
    i, lasts, s, fact, num, sign = 1, Decimal(0), x, 1, x, 1
    while s != lasts:
        lasts = s
        i += 2
        fact *= i * (i-1)
        num *= x * x
        sign *= -1
        s += num / fact * sign
    getcontext().prec -= 2
    return +s
