from collections import defaultdict, deque
from itertools import groupby
from pprint import pprint
from tokenize import group


Graph = dict[str, set[str]]


def rev(graph: Graph) -> Graph:
  rev_graph: Graph = defaultdict(set)

  for a, edges in graph.items():
    for b in edges:
      rev_graph[b].add(a)

  return rev_graph


def strong_components(graph: Graph):
  rev_graph = rev(graph)
  visited = set[str]()
  queue = deque[str]()
  node_label = dict[str, int]()

  def postorder_dfs(node: str):
    visited.add(node)

    for neighbour in rev_graph[node]:  # REVERSE
      if neighbour not in visited:
        postorder_dfs(neighbour)

    queue.appendleft(node)

  for node in graph:
    if node not in visited:
      postorder_dfs(node)

  def label_dfs(node: str, label: int):
    node_label[node] = label

    for neighbour in graph[node]:  # FORWARD
      if neighbour not in node_label:
        label_dfs(neighbour, label)

  label = 0
  for node in queue:
    if node not in node_label:
      label_dfs(node, label)
      label += 1

  components = sorted((label, node) for node, label in node_label.items())
  components = groupby(components, key=lambda t: t[0])
  return {label: [n for l, n in group] for label, group in components}


graph: Graph = {
    "a": {"b"},
    "b": {"f"},
    "c": {"h"},
    "d": {"c"},
    "e": {"f", "i"},
    "f": {"g", "l"},
    "g": {"c", "a"},
    "h": {"l", "d"},
    "i": {"n"},
    "j": {"k", "m"},
    "k": {"h", "l"},
    "l": {"o", "p"},
    "m": {"i"},
    "n": {"j", "o"},
    "o": {"k"},
    "p": set(),
}

pprint(strong_components(graph))
