import numpy as np

def Symp(x, f):
  res = 0
  h = x[1] - x[0] 
  N = np.size(x)
  for i in range(0, N - 2, 2):
    res += ((f[i] + 4*f[i+1] + f[i+2]) / 6) * h*2
  return res

def calc(x_beg, x_step, y_arr):
  end = x_beg + np.size(y_arr) * x_step
  x_arr = np.linspace(x_beg, end, np.size(y_arr))
  return Symp(x_arr, y_arr) 