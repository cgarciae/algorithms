from collections import defaultdict
from typing import Iterator


def topological_sort(prerequisites: list[list[int]]) -> Iterator[int]:
  edges = get_edges(prerequisites)
  sources = get_sources(prerequisites)
  inflow_count = get_inflow_count(prerequisites)

  def topological_sort_dsf(node: int) -> Iterator[int]:
    if inflow_count[node] < 0:
      raise RuntimeError

    if inflow_count[node] == 0:
      yield node
      inflow_count[node] -= 1

      for neighbour in edges[node]:
        inflow_count[neighbour] -= 1
        yield from topological_sort_dsf(neighbour)

  for source in sources:
    yield from topological_sort_dsf(source)


def get_edges(prerequisites: list[list[int]]) -> dict[int, set[int]]:
  edges = defaultdict(set)

  for target, source in prerequisites:
    edges[source].add(target)

  return edges


def get_inflow_count(prerequisites: list[list[int]]) -> dict[int, int]:
  inflow_count = defaultdict(lambda: 0)

  for target, _ in prerequisites:
    inflow_count[target] += 1

  return inflow_count


def get_sources(prerequisites: list[list[int]]) -> set[int]:
  sources = set(source for _, source in prerequisites)
  targets = set(target for target, _ in prerequisites)
  return sources - targets


prerequisites = [
    [1, 0],
    [3, 1],
    [2, 0],
    [3, 2],
    [4, 1],
    [3, 4],
]

print(list(topological_sort(prerequisites)))
