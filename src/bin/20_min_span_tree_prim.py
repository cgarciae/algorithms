from collections import defaultdict
from queue import PriorityQueue
from pprint import pprint
import heapq
from typing import Optional


Node = int
Weight = float
Label = int
G = dict[Node, set[tuple[Weight, Node]]]
F = G
Edge = tuple[Weight, Node]


class PQ(PriorityQueue[tuple[Weight, Node]]):

  def __init__(self, maxsize: int = 0) -> None:
    super().__init__(maxsize)
    self._priority: dict[Node, Weight] = {}

  def put(
      self, item: tuple[Weight, Node], block: bool = True, timeout: float | None = None
  ) -> None:
    weight, node = item
    self._priority[node] = weight
    return super().put(item, block, timeout)

  def get(
      self, block: bool = True, timeout: float | None = None
  ) -> tuple[Weight, Node]:
    weight, node = super().get(block, timeout)
    del self._priority[node]
    return weight, node

  def get_priority(self, node: Node) -> Weight:
    return self._priority[node]

  def decrease_key(self, key: Node, weight: Weight):
    for i, (_, node) in enumerate(self.queue):
      if node == key:
        self.queue[i] = (weight, node)
        self._priority[node] = weight
        heapq.heapify(self.queue)
        break
    else:
      raise KeyError()


def init_prim(graph: G, start: Node) -> tuple[dict[Node, Optional[Edge]], PQ]:
  priority = PQ()
  edge: dict[Node, Optional[Edge]] = {}

  for node in graph:
    if node == start:
      continue
    priority.put((float("inf"), node))
    edge[node] = None

  for w, node in graph[start]:
    edge[node] = (w, start)
    priority.decrease_key(node, w)

  return edge, priority


def loop_prim(
    graph: G, priority: PQ, edge: dict[Node, Optional[tuple[Weight, Node]]], start: Node
) -> F:
  spanning_tree: F = defaultdict(set)
  spanning_tree[start] = set()

  for _ in range(len(graph) - 1):
    _, node = priority.get()
    e = edge[node]
    assert e is not None
    w, neighbour = e

    spanning_tree[node].add((w, neighbour))
    spanning_tree[neighbour].add((w, node))

    for w, neighbour in graph[node]:
      if neighbour not in spanning_tree and priority.get_priority(neighbour) > w:
        edge[neighbour] = (w, node)
        priority.decrease_key(neighbour, w)

  return dict(spanning_tree)


def minimum_spanning_tree(graph: G) -> F:
  start = next(iter(graph))
  edge, priority = init_prim(graph, start)
  return loop_prim(graph, priority, edge, start)


edges: list[tuple[Node, Weight, Node]] = [
    (0, 8, 1),
    (0, 5, 2),
    (1, 10, 2),
    (1, 2, 3),
    (2, 3, 3),
    (1, 18, 4),
    (4, 12, 3),
    (4, 4, 6),
    (6, 14, 3),
    (6, 26, 5),
    (5, 30, 3),
    (5, 16, 2),
]
graph: G = defaultdict(set)
for a, w, b in edges:
  graph[a].add((w, b))
  graph[b].add((w, a))

spanning_tree = minimum_spanning_tree(graph)

pprint(spanning_tree)
