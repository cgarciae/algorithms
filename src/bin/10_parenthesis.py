def _generate(solution: str, left: int, right: int):
    if left == 0 and right == 0:
        yield solution

    if left > 0:
        yield from _generate(solution + "(", left - 1, right)

    if right > left:
        yield from _generate(solution + ")", left, right - 1)


def generate(n: int):
    return _generate("", n, n)


for solution in generate(3):
    print(solution)
