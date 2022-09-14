#!usr/bin/python3

from array import array
import numpy as np             
import matplotlib
import matplotlib.pyplot as plt


class PlotFunction:

    def __init__(self):
        self.__arrayX = np.array([])
        self.__arrayY = np.array([])
        self.__config_line = '--'
        self.__line_dpi = 1000              #dpi - dots per interval

    @property                               #getters
    def config_line(self):
        return self.__config_line

    @property                               
    def arrayX(self):
        return self.__arrayX

    @property
    def arrayY(self):
        return self.__arrayY

    @property
    def line_dpi(self):
        return self.__line_dpi
    
    def set_line_dpi(self, line_dpi):           #setters
        self.__line_dpi = line_dpi

    def set_config_line(self, config_line):  
        self.__config_line = config_line

    def set_arrayX(self, array):                 
        self.__arrayX = array

    def set_arrayY(self, array):
        self.__arrayY = array


    def create_plot_function(self, func, left_bound, right_bound):
        np.delete(self.arrayY)
        np.delete(self.arrayX)
        step = (right_bound - left_bound) / self.line_dpi
        cur_pos = left_bound
        for i in range(self.__line_dpi):
            np.append(self.arrayY, func(cur_pos))
            np.append(self.arrayX, cur_pos)
            cur_pos += step

    def transformX(self, func):
        for it in self.arrayX:
            it = func(it)

    def transformY(self, func):
        for it in self.arrayY:
            it = func(it)

    def append_function(self, my_plot_func):
        np.append(self.arrayX, my_plot_func.arrayX)
        np.append(self.arrayY, my_plot_func.arrayY)

    def fit_data(self):
        pass
    


class MyPlot:

    __slots__ = ['__plot', '__functions', '__figure_name']     #запрет на доступ снаружи

    num_of_figures = 0

    def __init__(self):
        self.__plot = plt.figure(MyPlot.num_of_figures)
        self.__functions = list()
        self.__figure_name = MyPlot.num_of_figures
        MyPlot.num_of_figures += 1

    @property
    def functions(self):
        return self.__functions

    @property
    def figure_name(self):
        return self.__figure_name

    #Returns data set number number 
    def add_data(self, my_plot_func):
        self.functions.append(my_plot_func)
        return len(self.functions) - 1

    #Removes and returns data with specified number
    def remove_data(self, data_num):
        return list.pop([data_num])
    
    #Creates lines from each function
    def draw_all(self):
        plt.figure(self.figure_name)
        for it in self.functions:
            plt.plot(it.arrayX, it.arrayY, it.config_line)

    def config_plot(self, title, xlabel, ylabel):
        plt.figure(self.figure_name)
        plt.grid()
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

    def show_all():
        plt.show()




def test(func):
    myFunc = [func, func]
    myFunc[0]()    

def foo():
    print(1)

def main():
    obj1 = PlotFunction()
    obj2 = PlotFunction()

    obj1.set_arrayX([1, 2])
    obj1.set_arrayY([1, 2])

    obj2.set_arrayX([-1, -2])
    obj2.set_arrayY([-1, -2])

    plot = MyPlot()
    plot.add_data(obj1)
    plot.add_data(obj2)

    plot.config_plot('test', 'testX', 'testY')
    plot.draw_all()
    MyPlot.show_all()

if __name__ == '__main__':
    main()
    