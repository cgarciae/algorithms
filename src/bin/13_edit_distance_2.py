from functools import lru_cache

calls = 0


def edit_distance(a: str, b: str) -> int:
    @lru_cache(maxsize=len(a) * len(b) + 100)
    def _edit_distance(i: int, j: int) -> int:
        global calls
        calls += 1

        if i == len(a):
            return len(b) - j

        if j == len(b):
            return len(a) - i

        insert = 1 + _edit_distance(i + 1, j)
        replace = int(a[i] != b[j]) + _edit_distance(i + 1, j + 1)
        delete = 1 + _edit_distance(i, j + 1)

        return min((insert, replace, delete))

    value = _edit_distance(0, 0)

    print(f"{_edit_distance.cache_info().hits=}")

    return value


answer = edit_distance("hola", "hols")

print(f"{answer=}")
print(f"{calls=}")
