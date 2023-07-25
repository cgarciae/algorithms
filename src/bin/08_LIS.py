import typing as tp


def longest_subquence(
    nums: list[int],
    prev: tp.Optional[int] = None,
) -> int:
    if len(nums) == 0:
        return 0

    elem = nums[0]
    nums = nums[1:]

    if prev is not None and prev >= elem:
        return longest_subquence(nums, prev)

    return max(
        1 + longest_subquence(nums, elem),  # with element
        longest_subquence(nums, prev),  # skip element
    )


nums = [8, 6, 7, 5, 3, 10, 9]
answer = longest_subquence(nums)
print(f"{answer=}")
