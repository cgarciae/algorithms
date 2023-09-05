from collections import defaultdict, deque
from typing import Iterable, Literal


Edges = dict[int, set[int]]
Status = Literal["new", "active", "finished"]


def _topological_sort(
    edges: Edges,
    status: dict[int, Status],
    vertex: int,
    output: deque[int],
):
  status[vertex] = "active"

  for neighbour in edges[vertex]:
    status_neighbour = status[neighbour]
    if status_neighbour == "active":
      raise RuntimeError
    elif status_neighbour == "finished":
      continue

    _topological_sort(edges, status, neighbour, output)

  status[vertex] = "finished"
  output.appendleft(vertex)


def topological_sort(edges: Edges) -> deque[int]:
  status: dict[int, Status] = defaultdict(lambda: "new")

  output: deque[int] = deque()

  for vertex in list(edges.keys()):
    if status[vertex] == "new":
      _topological_sort(edges, status, vertex, output)

  return output


def create_edges(prerequisites: list[list[int]]) -> dict[int, set[int]]:
  edges = defaultdict(set)

  for [t, v] in prerequisites:
    edges[v].add(t)

  return edges


prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]
edges = create_edges(prerequisites)

print(topological_sort(edges))
