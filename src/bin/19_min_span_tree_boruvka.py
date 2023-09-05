from collections import defaultdict
from pprint import pprint


Node = int
Weight = float
Label = int
G = dict[Node, set[tuple[Weight, Node]]]
F = G


def count_and_label(graph: F) -> tuple[dict[Node, Label], int]:
  component: dict[Node, Label] = {}

  def label_dfs(node: Node, label: Label):
    component[node] = label
    for _, neighbour in graph[node]:
      if neighbour not in component:
        label_dfs(neighbour, label)

  count = 0
  for node in graph:
    if node not in component:
      count += 1
      label_dfs(node, count)

  return component, count


def all_safe_edges(graph: G, spanning_tree: F, component: dict[Node, Label]):
  safe: dict[Label, tuple[Node, Weight, Node]] = {}

  for a in graph:
    for w, b in graph[a]:
      if component[a] != component[b]:
        if component[a] not in safe or w < safe[component[a]][1]:
          safe[component[a]] = (a, w, b)
        if component[b] not in safe or w < safe[component[b]][1]:
          safe[component[b]] = (a, w, b)

  for a, w, b in safe.values():
    spanning_tree[a].add((w, b))
    spanning_tree[b].add((w, a))


def minimum_spanning_tree(graph: G) -> F:
  spanning_tree: F = {node: set() for node in graph}

  component, count = count_and_label(spanning_tree)
  while count > 1:
    all_safe_edges(graph, spanning_tree, component)
    component, count = count_and_label(spanning_tree)

  return spanning_tree


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
