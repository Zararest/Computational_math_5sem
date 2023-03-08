import numpy as np

e_param = np.e

# u = {y, z}
def f(u):
  res = np.copy(u)
  res[0] = u[1]
  res[1] = -e_param * (u[1] * (u[0] * u[0] - 1) + u[0])
  return res