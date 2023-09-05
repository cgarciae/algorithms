import typing as tp


def all_subquences(
    nums: list[int], seq: tuple[int, ...]
) -> tp.Iterator[tuple[int, ...]]:
  if not nums:
    yield seq
    return

  elem = nums[0]
  nums = nums[1:]

  yield from all_subquences(nums, seq)  # skip

  if not seq or seq[-1] < elem:
    yield from all_subquences(nums, (*seq, elem))  # add


nums = [8, 6, 7, 5, 3, 10, 9]

for subsequences in all_subquences(nums, ()):
  print(f"seq={subsequences}, len={len(subsequences)}")
