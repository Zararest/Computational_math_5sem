from Plot import MyPlot
from Plot import PlotFunction 

import numpy as np 

def parse_file(file_name):
    data = np.array([])
    data = np.loadtxt(file_name, dtype=float)
    return data

class Newton:

    koefs = np.array([]) 
    initial_x = np.array([])
    initial_val = np.array([])
    # Возвращает значение ячейки и записывает промежуточные значения
    # нулевая вертикальная линия это f_i (i > 0)
    # нулевая горизонтальная линия это x_i (i > 0)
    # размер матрицы (n + 1)(n + 1)
    def calc_table_cell(table, i, j):
        if j == 0:
            return table[i, j]
        x_diff = table [0, j + i] - table[0, i]
        tmp_1 = Newton.calc_table_cell(table, i + 1, j - 1) 
        table[i, j] = (tmp_1 - table[i, j - 1]) / (x_diff)
        return table[i, j]

    # Возвращает набор коэффициентов многочлена
    # data[:, 0] - x_i
    # data[:, 1] - f(x_i)
    def fit_Newton(data):
        Newton.initial_x = np.copy(data[:, 0])
        Newton.initial_val = np.copy(data[:, 1])
        num_of_points = np.size(data[:, 0])
        table = np.full((num_of_points + 1, num_of_points + 1), 0.0)
        table[1 :, 0] = data[:, 1]
        table[0, 1 :] = data[:, 0]
        for it in range(num_of_points):
            Newton.koefs = np.append(Newton.koefs, Newton.calc_table_cell(table, 1, it))
        return Newton.koefs

    def calc_Newton(cur_x):
        num_of_points = np.size(Newton.initial_x)
        result = 0
        for i in range(num_of_points):
            x_polinom = 1
            for j in range(i):
                x_polinom = x_polinom * (cur_x - Newton.initial_x[j])
            result += Newton.koefs[i] * x_polinom
        return result

    def draw_Newton():
        #print(Newton.koefs)
        graph = PlotFunction()
        graph.create_continuous_function(Newton.calc_Newton, 1900, 2010)

        dots = PlotFunction()
        dots.set_arrayX(Newton.initial_x)
        dots.set_arrayY(Newton.initial_val)

        plot = MyPlot()
        plot.config_plot('Население США', 'Год', 'Население человек')
        plot.add_dots(dots)
        plot.add_function(graph)
        plot.draw_all()
        
class Spline:

    size_of_x_arr = -1
    A = np.array([])
    F = np.array([])
    h = np.array([]) #размер на 1 меньше чем точек 
    m = np.array([]) #вторые производные в точках (в первой и последней 0)
    init_x = np.array([])
    init_f = np.array([])
    #массивы коэффициентов сплайнов S_k(x) = [m_k * (x_{k+1} - x)^3 + m_{k + 1} * (x - x_k)^3] / [6(x_{k+1} - x_k)] + a_k * (x_{k+1} - x) + b_k * (x - x_k)
    a_coeff = np.array([]) #коэфф перед (x_{k + 1} -x)        
    b_coeff = np.array([]) #коэфф перед (x - x_k)

    def full_F(val_arr):
        size = Spline.size_of_x_arr - 2 #как и матрица на 2 меньше
        for i in range(size):
            cur_F = (val_arr[i + 2] - val_arr[i + 1]) / Spline.h[i + 1] - (val_arr[i + 1] - val_arr[i]) / Spline.h[i]
            Spline.F = np.append(Spline.F, cur_F)
        return Spline.F

    def full_h(x_arr):
        for i in range(Spline.size_of_x_arr - 1):
            Spline.h = np.append(Spline.h, x_arr[i + 1] - x_arr[i])
        return Spline.h

    def full_A():
        size = Spline.size_of_x_arr - 2                           #размер матрицы меньше на 2 крайние точки 
        Spline.A = np.full((size, size), 0.0)
        for i in range(size):
            Spline.A[i, i] = (Spline.h[i] + Spline.h[i + 1]) / 3
        for i in range(size - 1):
            Spline.A[i + 1, i] = Spline.h[i + 1] / 6
            Spline.A[i, i + 1] = Spline.h[i + 1] / 6
        return Spline.A

    def init(x_arr, val_arr):
        Spline.init_x = np.copy(x_arr)
        Spline.init_f = np.copy(val_arr)
        Spline.size_of_x_arr = np.size(x_arr)
        Spline.full_h(x_arr)
        Spline.full_A()
        Spline.full_F(val_arr)

    def calc_r(p):
        size = Spline.size_of_x_arr - 2 
        r = np.array([Spline.F[0] / Spline.A[0, 0]])
        for i in range(size - 1):
            k = i + 1               #тк начали не с первого 
            a = Spline.A[k, k - 1]
            b = Spline.A[k, k]
            cur_r = (Spline.F[k] - a * r[k - 1]) / (b - a * p[k - 1])
            r = np.append(r, cur_r)
        return r

    def calc_p():
        size = Spline.size_of_x_arr - 2 
        p = np.array([Spline.A[0, 1]] / Spline.A[0, 0])
        for i in range(size - 2):   #кроличество p на 1 меньше размера матрицы
            k = i + 1               #тк начали не с первого 
            c = Spline.A[k, k + 1]
            b = Spline.A[k, k]
            a = Spline.A[k, k - 1]
            cur_p = c / (b - a * p[k - 1])
            p = np.append(p, cur_p)
        return p

    def calc_m():
        size = Spline.size_of_x_arr - 2       #n - 2 где n + 1 - кол-во точек(n - номер последней)
        p = Spline.calc_p()
        r = Spline.calc_r(p)
        x = np.full(size, 0.0)
        x[size - 1] = r[size - 1]
        for k in range(size - 2, -1, -1):
            x[k] = r[k] - p[k] * x[k + 1]
        Spline.m = np.full(size + 2, 0.0)
        Spline.m[1 : -1] = x[:] 
        #Spline.m[1 : -1] =  np.linalg.solve(Spline.A, Spline.F)[:] #тестовый вариант
        return Spline.m

    def calc_a():
        size = Spline.size_of_x_arr - 1
        for i in range(size):
            cur_val = Spline.init_f[i] / Spline.h[i] - Spline.m[i] * Spline.h[i] / 6
            Spline.a_coeff = np.append(Spline.a_coeff, cur_val)
        return Spline.a_coeff
    
    def calc_b():
        size = Spline.size_of_x_arr - 1
        for i in range(size):
            cur_val = Spline.init_f[i + 1] / Spline.h[i] - Spline.m[i + 1] * Spline.h[i] / 6
            Spline.b_coeff = np.append(Spline.b_coeff, cur_val)
        return Spline.b_coeff

    #подсчет коэффициентов сплайнов
    def calc_coeff(): 
        Spline.calc_m()
        Spline.calc_a()
        Spline.calc_b()

    #подсчет значения кокретного сплайна
    def get_spline_val(spline_num, x):
        val = (Spline.m[spline_num] * (Spline.init_x[spline_num + 1] - x)**3 + Spline.m[spline_num + 1] * (x - Spline.init_x[spline_num])**3) / (6 * Spline.h[spline_num]) + \
            Spline.a_coeff[spline_num] * (Spline.init_x[spline_num + 1] - x) + Spline.b_coeff[spline_num] * (x - Spline.init_x[spline_num])
        return val

    def get_val(x):
        i = 0
        while x > Spline.init_x[i + 1] and i < (Spline.size_of_x_arr - 2):
            i += 1
        return Spline.get_spline_val(i, x)

    def draw_spline():
        graph = PlotFunction()
        graph.create_continuous_function(Spline.get_val, 1900, 2010)

        dots = PlotFunction()
        dots.set_arrayX(Spline.init_x)
        dots.set_arrayY(Spline.init_f)

        plot = MyPlot()
        plot.config_plot('Население США', 'Год', 'Население человек')
        plot.add_dots(dots)
        plot.add_function(graph)
        plot.draw_all()

    def test():
        print('Real m:', np.linalg.solve(Spline.A, Spline.F))
        print('My m:', Spline.m)
        print('coeff_a', Spline.a_coeff)
        print('coeff_b', Spline.b_coeff)
        print('val in 1910', Spline.get_spline_val(0, 1910))

def main():

    data = parse_file('Newton.txt')
    Newton.fit_Newton(data)
    Newton.draw_Newton()

    Spline.init(data[:, 0], data[:, 1])
    Spline.calc_coeff()
    Spline.draw_spline()
    #Spline.test()
    print('Экстраполяция на 2010 год:', Spline.get_val(2010))

    MyPlot.show_all()


if __name__ == '__main__':
    main()