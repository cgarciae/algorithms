from functools import lru_cache
from typing import Optional


def optimal_change(nums: list[int], target: int) -> Optional[int]:
  @lru_cache(maxsize=target + max(nums))
  def _optimal_change(total: int) -> Optional[int]:
    print(total)
    if total == target:
      return 0
    elif total > target:
      return None

    solutions: list[int] = []
    for value in nums:
      solution = _optimal_change(total + value)
      if solution is not None:
        solutions.append(1 + solution)

    solution = min(solutions) if solutions else None
    return solution

  solution = _optimal_change(0)

  cache = _optimal_change.cache_info()
  print(f"{cache.hits=}")
  print(f"{cache.misses=}")

  return solution


nums = [2, 4, 7, 13, 28, 52, 91, 365]
target = 122

solution = optimal_change(nums, target)

print(f"{solution=}")
