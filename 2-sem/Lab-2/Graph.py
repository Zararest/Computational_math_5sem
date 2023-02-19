import matplotlib.pyplot as plt

def initPlot():
  fig, ax = plt.subplots(figsize=(10, 7))
  return ax

def draw(res, ax):
  ax.plot(res[1, :], res[2, :])  
  ax.set_xlabel('y')
  ax.set_ylabel('y\'')
  ax.set_title('Фазовая диаграмма ДУ')
  ax.grid()
  plt.show()