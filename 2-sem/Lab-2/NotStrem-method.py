import Graph as gr
import HeunMethod as hn
import Func

import numpy as np

#Returns vector {t, y, z}^T
def NistremFunc(h = 0.0001, iter_num = 100, initial_pos = np.zeros((2, 1), np.float64)):
  cur_res = hn.HeunFunc(h, 3, initial_pos)[1 : 3, :] #calculating first 3 values (with initial) (without t line)
  result = np.copy(cur_res)
  #print(result)
  t = np.linspace(0, h * iter_num, iter_num)
  for i in range(3, iter_num):
    u_2 = cur_res[:, 0] + 2 * h * Func.f(t[i - 2], cur_res[:, 1])
    u_3 = cur_res[:, 1] + 1 / 3 * h * (7 * Func.f(t[i - 1], cur_res[:, 2]) - 2 * Func.f(t[i - 2], cur_res[:, 1]) + Func.f(t[i - 3], cur_res[:, 0]))
    cur_res = np.transpose((np.copy(cur_res[:, 1]), u_2, u_3))
    #result[:, -1] = u_2
    result = np.hstack((result, u_3.reshape(2, 1)))
    print(cur_res)
  return np.vstack((t, result)) 

# метод улетает в бесконечность

def main():
  print('Решение ДУ многошаговым методом Нистрема 3 порядка')
  init_pos = np.array([[4.0], [0]])
  res = NistremFunc(initial_pos=init_pos)
  print('Последняя точка: ', res[:, -1])
  gr.draw(res, gr.initPlot())

if __name__ == '__main__':
    main()