import numpy as np

e_param = np.e

# u = {y, z}
def f(t, u):
  res = np.copy(u)
  res[0] = u[1]
  res[1] = u[1] * e_param * (1 - u[0]**2) - u[0]
  return res