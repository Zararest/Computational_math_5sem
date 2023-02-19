import numpy as np

# u = {y, z}
def f(t, u):
  res = np.copy(u)
  res[0] = u[1]
  res[1] = u[1] * np.e * (1 - u[0]**2) - u[0]
  #print(res)
  return res