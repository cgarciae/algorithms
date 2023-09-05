from collections import defaultdict, deque
from typing import Iterable, Iterator, Literal
from itertools import chain


Edges = dict[int, set[int]]
Status = Literal["new", "active", "finished"]


def topological_sort(edges: Edges) -> deque[int]:
  status: dict[int, Status] = defaultdict(lambda: "new")

  def _topological_sort(vertex: int) -> Iterator[int]:
    status[vertex] = "active"

    for neighbour in edges[vertex]:
      status_neighbour = status[neighbour]
      if status_neighbour == "active":
        raise RuntimeError
      elif status_neighbour == "finished":
        continue

      yield from _topological_sort(neighbour)

    status[vertex] = "finished"
    yield vertex

  chains = deque()
  for vertex in list(edges.keys()):
    if status[vertex] == "new":
      chain = deque(reversed(deque(_topological_sort(vertex))))
      chain.extend(chains)
      chains = chain

  return chains


def create_edges(prerequisites: list[list[int]]) -> dict[int, set[int]]:
  edges = defaultdict(set)

  for [t, v] in prerequisites:
    edges[v].add(t)

  return edges


prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2], [2, 4]]
edges = create_edges(prerequisites)

print(topological_sort(edges))
