import typing as tp


def _longest_subsequence(nums: list[int], current: list[int], longest: list[int]):
    if not nums:
        return

    elem = nums[0]
    nums = nums[1:]

    # with element
    if not current or elem > current[-1]:
        current.append(elem)
        if len(current) > len(longest):
            longest[:] = current
        _longest_subsequence(nums, current, longest)
        current.pop()

    # without element
    _longest_subsequence(nums, current, longest)


def longest_subsequence(nums: list[int]) -> list[int]:
    longest = []
    current = []
    _longest_subsequence(nums, current, longest)
    return longest


nums = list(range(10))

longest = longest_subsequence(nums)

print(longest)
