from numpy.lib.function_base import kaiser
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import math

# system representation
def f(vec, param):
  res = np.zeros(2);
  res[0] = vec[1]                                              # y1' = y2
  res[1] = - param * (vec[1] * ((vec[0]*vec[0] - 1) + vec[0])) # y2' =  -a(y2(y1^2-1)+y1))
  return res

def Rado_step(param, y, h):
  res = np.zeros(2)

  k1 = np.zeros(2)

  k1 = np.array((0, 0))
  k2 = np.array((0, 0))

  next = 1
  
  #just iterations 
  for i in range(10):
    next = 0
    k1 = f (y + h * (k1/4 - k2/4), param)
    k2 = f (y + h * (k1/4 + k2 * 5/12), param)

  return y + (k1/4 + 3/4 * k2) * h

def Rado(x0, y0, h ,param):
  current = [x0,y0]

  x = []
  y = []

  x.append(x0)
  y.append(y0)

  for i in range (1000000):
    current = Rado_step(param, current, h)
    x.append(current[0])
    y.append(current[1])
    print(current)

  plt.plot(x,y,".")
  return


for i in range(-2, 6):
  for j in range(0, 200, 50):
    pass#Rado((i - 2)/4, j - 100, 0.0001, 1000)

Rado(-1.5, 0, 0.0001, 1000)
plt.title("a = 10^3")
plt.show()