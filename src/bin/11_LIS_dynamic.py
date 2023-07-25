import numpy as np


def lis_dynamic(nums: list[float]) -> int:
    n = len(nums)
    nums = [float("-inf")] + nums
    table = np.full((n + 1, n + 1), np.nan)

    table[:, n] = 0

    for j in range(n - 1, -1, -1):
        for i in range(j, -1, -1):
            skip = table[i, j + 1]
            take = 1 + table[j + 1, j + 1]
            if nums[j + 1] <= nums[i]:  # skip
                table[i, j] = skip
            else:
                table[i, j] = max(skip, take)

            print(table, "\n")

    return int(table[0, 0])


nums: list[float] = [8, 6, 7, 5, 3, 10, 9]
answer = lis_dynamic(nums)

print(answer)
