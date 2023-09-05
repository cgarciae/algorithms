State = tuple[str, int, int]


def generate(n: int):
  states: list[State] = [("", n, n)]

  for _ in range(2 * n):
    next_states: list[State] = []

    for solution, left, right in states:
      if left > 0:
        next_states.append((solution + "(", left - 1, right))

      if right > left:
        next_states.append((solution + ")", left, right - 1))

    states = next_states

  return [state[0] for state in states]


for solution in generate(3):
  print(solution)
