from functools import lru_cache


def lis(nums: list[float]) -> int:
  nums = [float("-inf")] + nums
  n = len(nums)

  @lru_cache(maxsize=n**2)
  def _lis_recursive(i: int, j: int) -> int:
    if j == n:
      return 0

    skip = _lis_recursive(i, j + 1)

    if nums[j] > nums[i]:
      take = 1 + _lis_recursive(j, j + 1)
    else:
      take = 0

    return max(skip, take)

  value = _lis_recursive(0, 1)

  cache = _lis_recursive.cache_info()
  print(f"{cache.hits=}")
  print(f"{cache.misses=}")

  return value


nums: list[float] = [8, 6, 7, 5, 3, 10, 9]
answer = lis(nums)

print(f"{answer=}")
