import numpy as np
import Matrix as solve
import Func

A = 0.435866521508459 #?
BETA = A * (6 * A * A - 3 * A + 2) / (6 * A * A - 6 * A + 1)

B21 = -A
B31 = -A
B32 = BETA - A

P1 = A
P3 = (6 * A * A - 6 * A + 1) / (6 * A * (BETA - A))
P2 = (1 - 2 * A - 2 * BETA * P3) / (2 * A)

# returns column of partial deriv
def calc_deriv(y_n, x_n, var_num, h):
  h_col = np.zeros((y_n.size, 1), y_n.dtype)
  h_col[var_num, 0] = h
  h2_col = np.zeros((y_n.size, 1), y_n.dtype)
  h2_col[var_num, 0] = 2 * h
  return 4 / 3 * (Func.f(x_n, y_n + h_col) - Func.f(x_n, y_n - h_col)) / (2 * h) \
       - 1 / 3 * (Func.f(x_n, y_n + h2_col) - Func.f(x_n, y_n - h2_col)) / (4 * h)

def calc_J_stupid(y_n, x_n, h):
  J = np.zeros((2, 2))
  J[0, 1] = 1
  if y_n[0] == 0 and x_n == 0:
    J[1, 0] = 1 / 2
  else:
    J[1, 0] = 1 / 2 * x_n / np.sqrt(y_n[0]) 
  return J

# calcs derivative for each combination of {y, y'}
def calc_J(y_n, x_n, h):
  return calc_J_stupid(y_n, x_n, h)
  size = y_n.size
  res = calc_deriv(y_n, x_n, 0, h)
  for var_num in range(size - 1):
    res = np.hstack((res, calc_deriv(y_n, x_n, var_num, h)))
  return res

def calc_matr(y_n, x_n, h):
  diff_h = h / 10
  return np.eye(y_n.size, dtype=y_n.dtype) + A * h * calc_J(y_n, x_n, diff_h)

# f - column
def solve_system(A, f):
  correct_f = np.zeros(f[:, 0].size, dtype=f.dtype)
  correct_f[:] = f[:, 0]
  method = solve.UpperRelax(A, correct_f)
  return method.calculate()

def calc_system(A, y, x, h):
  return np.reshape(solve_system(A, h * Func.f(x, y)), (y.size, 1))

# initial_pos = {y, y'}^T
# returns: {x, y, y'}^T array
def Rosenbrock(h = 1e-5, iter_num = 10000, initial_pos = np.zeros((2, 1), dtype=np.float128),
                                           initial_x = 0):
  result = np.copy(initial_pos)
  y_n = np.copy(initial_pos)
  x = np.linspace(initial_x, h * iter_num, iter_num)
  for i in range(iter_num - 1):
    A = calc_matr(y_n, x[i], h)
    K1 = calc_system(A, y_n, x[i], h)
    K2 = calc_system(A, y_n + B21 * K1, x[i], h)
    K3 = calc_system(A, y_n + B31 * K1 + B32 * K2, x[i], h)
    y_n = y_n + P1 * K1 + P2 * K2 + P3 * K3
    result = np.hstack((result, y_n))
  return np.vstack((x, result))