import Graph as gr
import Func
import numpy as np

#Returns vector {t, y, z}^T
def HeunFunc(h = 0.001, iter_num = 100000, initial_pos = np.zeros((2, 1), np.float64)):
  print('Параметры:')
  print('Шаг:', h)
  print('Начальная точка:')
  print(initial_pos)
  result = np.copy(initial_pos)
  cur_res = initial_pos
  t = np.linspace(0, h * iter_num, iter_num)
  for i in range(iter_num - 1):
    cur_t = i * h
    K1 = h * Func.f(cur_t, cur_res)
    K2 = h * Func.f(cur_t + h / 3, cur_res + K1 / 3)
    K3 = h * Func.f(cur_t + 2 * h / 3, cur_res + 2 * K2 / 3)
    cur_res = cur_res + K1 / 4 + 3 * K3 / 4
    result = np.hstack((result, cur_res))
  return np.vstack((t, result))


def main():
  print('Решение ДУ методом Хойна 3 порядка')
  init_pos = np.array([[4.0], [0]])
  res = HeunFunc(initial_pos=init_pos)
  print('Последняя точка: ', res[:, -1])
  gr.draw(res, gr.initPlot())

if __name__ == '__main__':
    main()