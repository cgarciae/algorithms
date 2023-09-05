from functools import lru_cache


def subset_sum(nums: list[float], target: int) -> bool:
  n = len(nums)

  @lru_cache
  def _subset_sum(i: int, total: int) -> bool:
    if total == target:
      return True
    if i == n:
      return False

    skip = _subset_sum(i + 1, total)

    if nums[i] + total <= target:
      take = _subset_sum(i + 1, nums[i] + total)
    else:
      take = False

    return skip or take

  value = _subset_sum(0, 0)

  cache = _subset_sum.cache_info()
  print(f"{cache.hits=}")
  print(f"{cache.misses=}")

  return value


nums: list[float] = [8, 6, 7, 5, 3, 10, 9]
answer = subset_sum(nums, 15)

print(f"{answer=}")
