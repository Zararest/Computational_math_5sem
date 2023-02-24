import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib as matplotlib

def color_map_color(value, cmap_name='Blues', vmin=0, vmax=1):
    # norm = plt.Normalize(vmin, vmax)
    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
    cmap = cm.get_cmap(cmap_name)  # PiYG
    rgb = cmap(norm(abs(value)))[:3]  # will return rgba, we take only first 3 so we get rgb
    color = matplotlib.colors.rgb2hex(rgb)
    return color

def initPlot():
  fig, ax = plt.subplots(figsize=(10, 7))
  return ax

def draw(res, ax, graph_color=color_map_color(0.5)):
  ax.plot(res[1, :], res[2, :], color=graph_color)  
  ax.set_xlabel('y')
  ax.set_ylabel('y\'')
  ax.set_title('Фазовая диаграмма ДУ')
  ax.grid()

def show():
  plt.show()
  