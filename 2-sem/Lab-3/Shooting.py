import numpy as np
import Rosenbrock as solve
import Integral as integral
import Graph as gr

initial_y = 0.03
initila_x = 0
final_x = 1
integral_value = 1

# calcs deviation of initial condition depends on cur solution
# condition = {y, u} u = y'
def calc_deviation(y_arr, h):
  return integral.calc(initila_x, h, y_arr) - integral_value

# calcs system with initiali condition y'_0 = alpha
# returns array of y
def calc_system(alpha, h):
  initial_cond = np.array([[initial_y], [alpha]])
  iter_num = int((final_x - initila_x) / h)
  solution = solve.Rosenbrock(h=h, iter_num=iter_num, initial_pos=initial_cond, 
                                                      initial_x=initila_x)
  return solution[1, :]

def infinit_bin_search(alpha, prev_alpha, cur_sign, prev_sign, max_alpha_is_infinit):
  if (alpha == 0):
    return 1
  if (max_alpha_is_infinit and (cur_sign == prev_sign)):
    return 2 * alpha
  
  if (cur_sign == prev_sign):
    return alpha + (alpha - prev_alpha) / 2 
  else:
    return alpha - (alpha - prev_alpha) / 2 


# boundary value problem solver
def solve_edge(h = 1e-3, epsilon = 0.0001):
  # array of current solutions y(x, alpha)
  y_arr = np.array([])
  end_solution_deviation = epsilon
  max_alpha_is_infinit = True
  alpha = 0
  prev_alpha = 0
  while abs(end_solution_deviation) >= epsilon: 
    y_arr = calc_system(alpha, h)
    deviation = calc_deviation(y_arr, h)
    prev_deviation_sign = np.sign(end_solution_deviation)
    end_solution_deviation = deviation
    tmp_prev_alpha = alpha
    alpha = infinit_bin_search(alpha, prev_alpha, np.sign(deviation), prev_deviation_sign, 
                               max_alpha_is_infinit)
    prev_alpha = tmp_prev_alpha
    if (max_alpha_is_infinit and prev_alpha > alpha):
      max_alpha_is_infinit = False
    print("cur epsilon: ", end_solution_deviation)
    print("cur alpha = ", alpha)
  return y_arr

def main():
  print("Решение краевой задачи методом стрельбы")
  h = 1e-3
  y_arr = solve_edge(h)
  step_num = int((final_x - initila_x) / h) 
  x_arr = np.linspace(initila_x, final_x, step_num)
  gr.draw(np.vstack((x_arr, y_arr)), gr.initPlot())
  gr.show()

if __name__ == '__main__':
    main()