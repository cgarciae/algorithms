import dataclasses
import typing as tp


@dataclasses.dataclass
class Node:
  value: int
  left: tp.Optional["Node"] = None
  right: tp.Optional["Node"] = None

  def swap(self) -> None:
    self.left, self.right = self.right, self.left

  def _swap_refs(self, other: "Node") -> None:
    tmp = vars(self).copy()
    vars(self).update(vars(other))
    vars(other).update(tmp)

  def rotate_left(self):
    assert self.left is not None
    left = self.left
    left_right = left.right
    self._swap_refs(left)
    self.right = left
    left.left = left_right

  def rotate_right(self):
    assert self.right is not None
    right = self.right
    right_left = right.left
    self._swap_refs(right)
    self.left = right
    right.right = right_left

  def inorder(self) -> tp.Iterator[int]:
    if self.left is not None:
      yield from self.left.inorder()
    yield self.value
    if self.right is not None:
      yield from self.right.inorder()

  def sort(self):
    if self.left is None and self.right is None:
      return
    elif self.left is not None and self.right is None:
      self.left.sort()
      if self.left.value > self.value:
        self.swap()
    elif self.left is None and self.right is not None:
      self.right.sort()
      if self.right.value < self.value:
        self.swap()
    elif self.left is not None and self.right is not None:
      self.left.sort()
      self.right.sort()

      if self.left.value >= self.value >= self.right.value:
        self.swap()
      elif self.left.value > self.value:
        self.rotate_left()
        self.sort()
      elif self.right.value < self.value:
        self.rotate_right()
        self.sort()

    left = self.left
    right = self.right

    if left is not None and left.right is not None and left.right.value > self.value:
      self.rotate_left()
      assert self.right is not None
      self.right.sort()

    if right is not None and right.left is not None and right.left.value < self.value:
      self.rotate_right()
      assert self.left is not None
      self.left.sort()


root = Node(
    value=3,
    left=Node(value=1),
    right=Node(
        value=4,
        left=Node(value=5),
        right=Node(value=2),
    ),
)

root.sort()
root
