from typing import Any, Callable
import numpy as np
from collections import deque
import scipy
import scipy.special


class Array:

  def __init__(
      self, value: np.ndarray, *, children: tuple["Array", ...] = (), name: str = ""
  ):
    self.value = value
    self.children = children
    self.grad = np.zeros_like(self.value, dtype=np.float32)
    self.backward_fn: Callable[[], None] = lambda: None
    self.name = name

  @property
  def shape(self):
    return self.value.shape

  def backward(self):
    assert self.shape == ()
    self.grad = np.ones_like(self.value, dtype=np.float32)
    # implement topological sort
    sorted_arrays: deque[Array] = deque()
    visited: set[Array] = set()

    def dfs(array: Array):
      visited.add(array)

      for child in array.children:
        if child not in visited:
          dfs(child)

      # toposort = reverse postorder
      sorted_arrays.appendleft(array)

    # run topological sort
    dfs(self)

    # run backward_fn in topological order
    for array in sorted_arrays:
      array.backward_fn()

  def zero_grad(self):
    visited: set[Array] = set()

    def dfs(array: Array):
      array.grad = np.zeros_like(array.grad)
      visited.add(array)

      for child in self.children:
        if child not in visited:
          dfs(child)

    # run depth first search
    dfs(self)

  def __add__(self, other: "Array") -> "Array":
    return add(self, other)

  def __mul__(self, other: "Array") -> "Array":
    return mul(self, other)

  def __matmul__(self, other: "Array") -> "Array":
    return dot(self, other)

  def __repr__(self) -> str:
    return repr(self.value)


def broadcast(a: Array, shape: tuple[int, ...]):
  assert len(shape) >= len(a.shape)
  added_dims = len(shape) - len(a.shape)
  a_shape = (1,) * added_dims + a.shape
  reduce_axis: list[int] = []
  for i, (a_dim, b_dim) in enumerate(zip(a_shape, shape)):
    if a_dim != b_dim:
      if a_dim != 1:
        raise ValueError
      else:
        reduce_axis.append(i)

  out = Array(np.broadcast_to(a.value, shape), children=(a,), name="broadcast")

  def broadcast_backward():
    grad = np.sum(out.grad, axis=tuple(reduce_axis), keepdims=True)
    if added_dims:
      grad = np.squeeze(grad, axis=tuple(range(added_dims)))
    a.grad += grad

  out.backward_fn = broadcast_backward
  return out


def maybe_broadcast(a: Array, b: Array) -> tuple[Array, Array]:
  if a.shape == b.shape:
    return a, b

  broadcast_a = False
  broadcast_b = False

  shape_diff = abs(len(a.shape) - len(b.shape))

  if len(a.shape) > len(b.shape):
    b_shape = (1,) * shape_diff + b.shape
    a_shape = a.shape
  elif len(b.shape) > len(a.shape):
    a_shape = (1,) * shape_diff + a.shape
    b_shape = b.shape
  else:
    a_shape = a.shape
    b_shape = b.shape

  for a_dim, b_dim in zip(a_shape, b_shape):
    if a_dim != b_dim:
      if a_dim != 1 and b_dim != 1:
        raise ValueError
      if a_dim == 1:
        broadcast_a = True
      elif b_dim == 1:
        broadcast_b = True

  if broadcast_a:
    a = broadcast(a, b_shape)

  if broadcast_b:
    b = broadcast(b, a_shape)

  return a, b


def add(a: Array, b: Array):
  a, b = maybe_broadcast(a, b)

  out = Array(a.value + b.value, children=(a, b), name="add")

  def add_backward():
    a.grad += out.grad
    b.grad += out.grad

  out.backward_fn = add_backward

  return out


def mul(a: Array, b: Array):
  a, b = maybe_broadcast(a, b)

  out = Array(a.value * b.value, children=(a, b), name="mul")

  def mul_backward():
    a.grad += b.value * out.grad
    b.grad += a.value * out.grad

  out.backward_fn = mul_backward

  return out


def dot(a: Array, b: Array) -> Array:
  assert len(b.shape) == 2
  # (M, N) @ (N, K) = (M, K)
  out = Array(a.value @ b.value, children=(a, b), name="dot")

  def dot_backward():
    extra_dims = len(a.shape) - len(b.shape)
    grad = out.grad
    if extra_dims:  # vvvvv<--- Why do you use a mean here instead of sum???
      grad = np.mean(grad, axis=tuple(range(extra_dims)))
    # (B, M, N) = ((B, N, K) @ (K, M)).T
    a.grad += np.swapaxes(b.value @ grad.T, -1, -2)
    # (B, N, K) = (B, N, M) @ (M, K)
    b_grad = np.swapaxes(a.value, -1, -2) @ grad
    if extra_dims:
      b_grad = np.sum(b_grad, axis=tuple(range(extra_dims)))
    b.grad += b_grad

  out.backward_fn = dot_backward

  return out


def mean(a: Array) -> Array:
  out = Array(np.mean(a.value), children=(a,), name="mean")

  def mean_backward():
    a.grad += out.grad / np.prod(a.shape)

  out.backward_fn = mean_backward
  return out


def sum(a: Array) -> Array:
  out = Array(np.sum(a.value), children=(a,), name="sum")

  def sum_backward():
    a.grad += out.grad

  out.backward_fn = sum_backward
  return out


def cross_entropy_with_logits(logits: Array, labels: Array) -> Array:
  probs = scipy.special.softmax(logits.value, axis=-1)
  loss = -np.log(probs)
  loss = np.take_along_axis(loss, labels.value[..., None], axis=-1)[..., 0]

  out = Array(loss, children=(logits,), name="cross_entropy_with_logits")

  def cross_entropy_backwards():
    probs_true = np.take_along_axis(probs, labels.value[..., None], axis=-1)
    grad = probs.copy()
    np.put_along_axis(grad, labels.value[..., None], probs_true - 1, axis=-1)
    grad /= np.prod(labels.shape)
    logits.grad += grad

  out.backward_fn = cross_entropy_backwards

  return out


def relu(a: Array) -> Array:
  out = Array(np.maximum(0, a.value), children=(a,), name="relu")

  def relu_backward():
    a.grad += (a.value > 0) * out.grad

  out.backward_fn = relu_backward

  return out


class Module:

  def parameters(self):
    for value in vars(self).values():
      if isinstance(value, Array):
        yield value
      elif isinstance(value, Module):
        yield from value.parameters()


class Linear(Module):

  def __init__(self, din: int, dout: int):
    self.w = Array(np.random.uniform(0, 0.01, size=(din, dout)))
    self.b = Array(np.zeros((dout,)))

  def __call__(self, x: Array) -> Array:
    return x @ self.w + self.b


# ----------------------------------------
# example
# ----------------------------------------
import matplotlib.pyplot as plt


class Classifier(Module):

  def __init__(self, din: int, dmid: int, dout: int):
    self.linear1 = Linear(din, dmid)
    self.linear2 = Linear(dmid, dout)

  def __call__(self, x: Array) -> Array:
    x = self.linear1(x)
    x = relu(x)
    x = self.linear2(x)
    return x


# Generate sample data
N = 100  # number of points per class
D = 2  # dimensionality
K = 3  # number of classes
inputs = np.zeros((N * K, D))  # data matrix (each row = single example)
labels = np.zeros(N * K, dtype="uint8")  # class labels
for j in range(K):
  ix = range(N * j, N * (j + 1))
  r = np.linspace(0.0, 1, N)  # radius
  t = np.linspace(j * 4, (j + 1) * 4, N) + np.random.randn(N) * 0.2  # theta
  inputs[ix] = np.c_[r * np.sin(t), r * np.cos(t)]
  labels[ix] = j
# lets visualize the data:
plt.scatter(inputs[:, 0], inputs[:, 1], c=labels, s=40)
plt.show()


# initialize parameters randomly
inputs = Array(inputs)
labels = Array(labels)
model = Classifier(2, 64, K)
params = list(model.parameters())

# some hyperparameters
step_size = 1e-3

for i in range(10_000 + 1):
  logits = model(inputs)
  loss = mean(cross_entropy_with_logits(logits, labels))
  loss.backward()

  if i % 100 == 0:
    scores = model(inputs).value
    predicted_class = np.argmax(scores, axis=1)
    accuracy = np.mean(predicted_class == labels.value)
    print(f"iteration {i}: {loss.value = :.4f}, {accuracy = :.4f}")

  for p in model.parameters():
    p.value += -step_size * p.grad

  loss.zero_grad()

# plot decision boundary
x = np.linspace(inputs.value[:, 0].min(), inputs.value[:, 0].max(), 100)
y = np.linspace(inputs.value[:, 1].min(), inputs.value[:, 1].max(), 100)
xx, yy = np.meshgrid(x, y)
grid_inputs = np.stack([xx, yy], axis=-1)
grid_preds = model(Array(grid_inputs)).value
grid_labels = np.argmax(grid_preds, axis=-1)
plt.contourf(xx, yy, grid_labels)
# scatter with black borders
plt.scatter(
    inputs.value[:, 0], inputs.value[:, 1], c=labels.value, s=40, edgecolors="k"
)
plt.show()

# ----------------------------------------
# tests
# ----------------------------------------
import jax.numpy as jnp
import jax
import optax


def test_mean():
  a = Array(np.arange(5, dtype=np.float32))
  loss = mean(a)

  loss.backward()

  # jax
  def f(x):
    return jnp.mean(x)

  grad = jax.grad(f)(jnp.arange(5, dtype=jnp.float32))

  np.testing.assert_allclose(a.grad, grad)


def test_sum():
  a = Array(np.arange(5, dtype=np.float32))
  loss = sum(a)

  loss.backward()

  # jax
  def f(x):
    return jnp.sum(x)

  grad = jax.grad(f)(jnp.arange(5, dtype=jnp.float32))

  np.testing.assert_allclose(a.grad, grad)


def test_broadcast():
  a = Array(np.arange(5, dtype=np.float32))
  b = broadcast(a, (2, 5))
  loss = sum(b)

  loss.backward()

  # jax
  def f(x):
    return jnp.sum(jnp.broadcast_to(x[None], (2, 5)))

  grad = jax.grad(f)(jnp.arange(5, dtype=jnp.float32))

  np.testing.assert_allclose(a.grad, grad)


def test_dot():
  a = Array(np.random.uniform(size=(5, 3, 4)))
  b = Array(np.random.uniform(size=(4, 2)))
  c = a @ b
  loss = sum(c)

  loss.backward()

  # jax
  def f(t):
    a, b = t
    c = a @ b
    return jnp.sum(c)

  grad_a, grad_b = jax.grad(f)((jnp.array(a.value), jnp.array(b.value)))

  np.testing.assert_allclose(a.grad, grad_a, rtol=1e-5)
  np.testing.assert_allclose(b.grad, grad_b, rtol=1e-5)


def test_linear():
  x = Array(np.random.uniform(size=(5, 3, 4)), name="x")
  w = Array(np.random.uniform(size=(4, 2)), name="w")
  b = Array(np.random.uniform(size=(2,)), name="b")
  y = x @ w + b
  loss = sum(y)

  loss.backward()

  # jax
  def f(params, x):
    w, b = params
    y = x @ w + b
    return jnp.sum(y)

  grad_w, grad_b = jax.grad(f)(
      (jnp.array(w.value), jnp.array(b.value)), jnp.array(x.value)
  )

  np.testing.assert_allclose(w.grad, grad_w, rtol=1e-5)
  np.testing.assert_allclose(b.grad, grad_b, rtol=1e-5)


def test_cross_entropy_with_logits():
  logits = Array(np.random.uniform(size=(5, 10)))
  labels = Array(np.random.randint(0, 10, size=(5,)))

  loss = mean(cross_entropy_with_logits(logits, labels))
  loss.backward()

  def f(logits, labels):
    return jnp.mean(optax.softmax_cross_entropy_with_integer_labels(logits, labels))

  loss_jax, grad = jax.value_and_grad(f)(logits.value, labels.value)

  np.testing.assert_allclose(loss.value, loss_jax, rtol=1e-5)
  np.testing.assert_allclose(logits.grad, grad, rtol=1e-5)


def run_tests():
  test_mean()
  test_sum()
  test_broadcast()
  test_dot()
  test_linear()
  test_cross_entropy_with_logits()


run_tests()
