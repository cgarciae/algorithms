from collections import deque
from typing import Set, Type, Union
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class Node:
  edges: list["Node"]

  def __init__(self) -> None:
    self.edges = []


# G = nx.watts_strogatz_graph(100, 4, 0.1)
A = np.random.uniform(size=(100, 100))
A = (A < 1 / (A.shape[0] * 0.75)).astype(np.int32)

nodes = [Node() for _ in range(A.shape[0])]

for i in range(A.shape[0]):
  node = nodes[i]
  for j in range(A.shape[1]):
    if A[i, j]:
      node.edges.append(nodes[j])


def graph_search(
    start: Node,
    end: Node,
    bag_type: Union[Type[list[Node]], Type[deque[Node]]] = list,
) -> bool:
  bag = bag_type()
  visited: Set[Node] = set()

  bag.append(start)

  while bag:
    if isinstance(bag, list):
      node = bag.pop()
    else:
      node = bag.popleft()

    if node is end:
      return True

    if node not in visited:
      visited.add(node)

      for edge in node.edges:
        if edge in visited:
          continue
        bag.append(edge)

  return False


start = nodes[0]
end = nodes[5]

answer = graph_search(start, end, bag_type=deque)

print(f"{answer = }")

# use networkx to plot the graph
# G = nx.from_numpy_array(A)
# Set the positions of the nodes
# pos = nx.spring_layout(G)
# nx.draw_networkx(G, pos=pos, with_labels=True, arrows=True)
# plt.show()
