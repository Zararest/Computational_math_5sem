import numpy as np

# {x}, {y, u} u = y'
# result: {y', u'}
def f(x, u):
  res = np.copy(u)
  res[0] = u[1]
  if (u[0] < 0):
    print("invalid root:")
    print("u = ", u)
  res[1] = x * np.sqrt(u[0])
  return res