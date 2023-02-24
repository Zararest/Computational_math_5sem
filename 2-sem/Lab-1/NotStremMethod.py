import Graph as gr
import HeunMethod as hn
import Func

import numpy as np

#Returns vector {t, y, z}^T
def NistremFunc(h = 0.001, iter_num = 100000, initial_pos = np.zeros((2, 1), np.float64)):
  result = hn.HeunFunc(h, 4, initial_pos)[1 : 3, :]
  t = np.linspace(0, h * iter_num, iter_num)
  for i in range(iter_num - 4):
    cur_t = i * h
    u_0 = np.reshape(result[:, -4], (2, 1))
    u_1 = np.reshape(result[:, -3], (2, 1))
    u_2 = np.reshape(result[:, -2], (2, 1))
    u_3 = np.reshape(result[:, -1], (2, 1))
    u_4 = u_2 + 1 / 3 * h * (8 * Func.f(cur_t + h * 3, u_3) \
                           - 5 * Func.f(cur_t + h * 2, u_2) \
                           + 4 * Func.f(cur_t + h * 1, u_1) \
                           - 1  * Func.f(cur_t + h * 0, u_0))
    result = np.hstack((result, u_4))
  return np.vstack((t, result))

# метод улетает в бесконечность

def main():
  print('Решение ДУ многошаговым методом Нистрема 4 порядка')
  init_pos = np.array([[4.0], [0]])
  res = NistremFunc(initial_pos=init_pos)
  print('Последняя точка: ', res[:, -1])
  gr.draw(res, gr.initPlot())
  gr.show()

if __name__ == '__main__':
    main()