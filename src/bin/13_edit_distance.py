from functools import lru_cache
from typing import Literal

calls = 0


def edit_distance(a: str, b: str) -> int:
  short, long = (a, b) if len(a) <= len(b) else (b, a)
  diff = len(long) - len(short)

  @lru_cache(maxsize=(len(short) + len(long)) * (diff + 1))
  def _edit_distance(i: int, j: int) -> int:
    global calls
    calls += 1

    if i == len(short) or j == len(long):
      return 0
    value = int(short[i] != long[j])
    values = [_edit_distance(i + 1, j + k + 1) for k in range(diff + 1 - (j - i))]
    value += min(values)
    return value

  values = [_edit_distance(0, k) for k in range(diff + 1)]
  value = min(values)

  print(f"{_edit_distance.cache_info().hits=}")

  return value + diff


answer = edit_distance("aaa", "cccccccc")

print(f"{answer=}")
print(f"{calls=}")

InnerLoopAggregation = Literal["last", "mean", "sum", "min", "max", "first"]

a: InnerLoopAggregation = "sum"
