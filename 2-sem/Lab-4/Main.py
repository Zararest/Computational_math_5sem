import Progon as solver
import Func as func

import numpy as np
import math as mh
import matplotlib.pyplot as plt

# singularity is between alpha and alpha + 1
def calc_coefs(h, x_0, x_L, alpha):
  size = mh.ceil((x_L - x_0) / h) + 1
  A = np.zeros((size, size))
  for l in range(1, alpha):
    x_l = x_0 + l * h
    a = func.k_a(x_l + 1/2 * h)
    b = -(func.k_a(x_l + 1/2 * h) + func.k_a(x_l - 1/2 * h) + func.q(x_l) * h*h)
    c = func.k_a(x_l - 1/2 * h)
    A[l][l - 1] = c
    A[l][l] = b
    A[l][l + 1] = a 
  # u{alpha} = u{beta}
  A[alpha][alpha] = 1
  A[alpha][alpha + 1] = -1
  # edge condition
  A[alpha + 1][alpha] = func.k_a(x_0 + alpha * h)
  A[alpha + 1][alpha - 1] = -func.k_a(x_0 + alpha * h)
  beta = alpha + 1
  A[alpha + 1][beta + 1] = -func.k_b(x_0 + beta * h)
  A[alpha + 1][beta] = func.k_b(x_0 + beta * h)
  for l in range(alpha + 2, size - 1):
    x_l = x_0 + l * h
    a = func.k_b(x_l + 1/2 * h)
    b = -(func.k_b(x_l + 1/2 * h) + func.k_b(x_l - 1/2 * h) + func.q(x_l) * h*h)
    c = func.k_b(x_l - 1/2 * h)
    A[l][l - 1] = c
    A[l][l] = b
    A[l][l + 1] = a
  A[0][0] = 1 
  A[-1][-1] = 1
  return A
  
def calc_heterogeneity(h, x_0, x_L, u_0, u_L, alpha):
  size = mh.ceil((x_L - x_0) / h) + 1
  f = np.zeros(size)
  for l in range(1, size):
    x_l = x_0 + l * h
    f[l] = -(func.f(x_l)) * h*h
  f[alpha] = 0
  f[alpha + 1] = 0
  f[0] = u_0
  f[-1] = u_L
  return f 

def draw(u, x):
  fig, ax = plt.subplots(figsize=(10, 7))
  ax.plot(x, u)
  ax.set_xlabel('x')
  ax.set_ylabel('y')
  ax.set_title('Решение ДУ')
  ax.grid()
  plt.show()  

def main():
  print('Решение уравнения теплопроводности с помощью встречной прогонки')
  u_0 = 1
  u_L = 0
  x_0 = 0
  x_L = 1
  x_singul = 0.125
  h = 0.01
  alpha = int(x_singul / h)
  k_alpha = func.k_a(x_0 + alpha * h)
  k_beta = func.k_b(x_0 + (alpha + 1) * h)
  A = calc_coefs(h, x_0, x_L, alpha) # size includes edge points
  f = calc_heterogeneity(h, x_0, x_L, u_0, u_L, alpha) # f[0], f[-1] - edge points()
  u = solver.solve(A, f, alpha, k_alpha, k_beta)
  x = np.linspace(x_0, x_L, mh.ceil((x_L - x_0) / h) + 1)
  print('res:', u)
  draw(u, x)

if __name__ == '__main__':
  main()