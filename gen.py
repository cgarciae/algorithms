import typing as tp


class Mult(tp.Protocol):

  def __mul__(self, other: tp.Any, /) -> tp.Any:
    ...


A = tp.TypeVar("A", bound=Mult)
B = tp.TypeVar("B")


def times2(x: A) -> A:
  return x * 2


x = 10
a = times2(x)
print(a)

x = "hello"
b = times2(x)
print(b)


class Multiplier(tp.Generic[A, B]):

  def __init__(self, x: A, b: B) -> None:
    self.x = x
    self.b = b

  def prod(self, p: int) -> A:
    return self.x * p


class MultIntBytes(Multiplier[int, bytes]):
  pass


m = Multiplier(10, b"hello")
y = m.x
b = m.b

m2 = MultIntBytes(3.10, b"hello")
