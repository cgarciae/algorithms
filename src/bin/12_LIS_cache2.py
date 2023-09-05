from functools import lru_cache


def lis(nums: list[float]) -> int:
  nums = [float("-inf")] + nums
  n = len(nums)

  @lru_cache(maxsize=len(nums))
  def _lis_recursive(i: int) -> int:
    value = 0
    for j in range(i, n):
      if nums[j] > nums[i] and 1 + _lis_recursive(j) > value:
        value = 1 + _lis_recursive(j)
    return value

  return _lis_recursive(0)


nums: list[float] = [8, 6, 7, 5, 3, 10, 9]
answer = lis(nums)

print(answer)
