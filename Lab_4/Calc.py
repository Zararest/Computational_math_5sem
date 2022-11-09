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
        print(Newton.koefs)
        graph = PlotFunction()
        graph.create_continuous_function(Newton.calc_Newton, 1900, 2001)

        dots = PlotFunction()
        dots.set_arrayX(Newton.initial_x)
        dots.set_arrayY(Newton.initial_val)

        plot = MyPlot()
        plot.config_plot('Население США', 'Год', 'Население человек')
        plot.add_dots(dots)
        plot.add_function(graph)
        plot.draw_all()
        
class Spline:

    A = np.array([])
    F = np.array([])
    h = np.array([]) #размер на 1 меньше чем точек 
    m = np.array([]) #вторые производные в точках (в первой и последней 0)
    init_x = np.array([])
    init_f = np.array([])
    #массивы коэффициентов сплайнов S(x) = a x^3 + b x^2 + c (x - x_k) + d (x - x_{k + 1})
    a_coeff = np.array([]) #коэфф перед 3 производной       
    b_coeff = np.array([]) #коэфф перед 2 производной
    c_coeff = np.array([]) #коэфф перед (x - x_k)
    d_coeff = np.array([]) #коэфф перед (x - x_{k + 1})

    def full_F(val_arr):
        size = np.size(val_arr) - 2 #как и матрица на 2 меньше
        for i in range(size):
            cur_F = (val_arr[i + 2] - val_arr[i + 1]) / Spline.h[1] - (val_arr[i + 1] - val_arr[i]) / Spline.h[0]
            Spline.F = np.append(Spline.F, cur_F)
        return Spline.F

    def full_h(x_arr):
        for i in range(np.size(x_arr) - 1):
            Spline.h = np.append(Spline.h, x_arr[i + 1] - x_arr[0])
        return Spline.h

    def full_A(x_arr):
        size = np.size(x_arr) - 2                           #размер матрицы меньше на 2 крайние точки 
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
        Spline.full_h(x_arr)
        Spline.full_A(x_arr)
        Spline.full_F(val_arr)

    def calc_r(p):
        size = np.size(Spline.A[:, 0])
        r = np.array([Spline.F[0] / Spline.A[0, 0]])
        for i in range(size - 1):
            k = i + 1               #тк начали не с первого 
            a = Spline.A[k, k - 1]
            b = Spline.A[k, k]
            cur_r = (Spline.F[k] - a * r[k - 1]) / (b - a * p[k - 1])
            r = np.append(r, cur_r)
        return r

    def calc_p():
        p = np.array([Spline.A[0, 1]])
        size = np.size(Spline.A[:, 0])
        for i in range(size - 2):   #кроличество p на 1 меньше размера матрицы
            k = i + 1               #тк начали не с первого 
            c = Spline.A[k, k + 1]
            b = Spline.A[k, k]
            a = Spline.A[k, k - 1]
            cur_p = c / (b - a * p[k - 1])
            p = np.append(p, cur_p)
        return p

    def calc_m():
        size = np.size(Spline.A[:, 0])      #n - 2 где n - кол-во точек
        p = Spline.calc_p()
        r = Spline.calc_r(p)
        x = np.full(size, 0.0)
        x[size - 1] = r[size - 1]
        for i in range(size - 1):
            k = i + 1               #идем с конца 
            x[size - 1 - k] = r[size - 1 - k] - p[size - 1 - k] * x[size - k]
        Spline.m = np.full(size + 2, 0.0)
        Spline.m[1 : -1] = x[:] 
        return Spline.m

    def calc_a(k):
        return (Spline.m[k + 1] - Spline.m[k]) / (6 * Spline.h[k + 1])

    def calc_b(k):
        return (Spline.m[k] * Spline.init_x[k + 1] - Spline.m[k + 1] * Spline.init_x[k]) / (2 * Spline.h[k + 1])
    
    def calc_c(k):
        S_val = Spline.init_f[k + 1]
        cur_x = Spline.init_x[k + 1]
        numerator = S_val - Spline.a_coeff[k] * (cur_x ** 3) - Spline.b_coeff[k] * (cur_x ** 2)
        denominator = cur_x - Spline.init_x[k]
        return numerator / denominator
    
    def calc_d(k):
        S_val = Spline.init_f[k]
        cur_x = Spline.init_x[k]
        numerator = S_val - Spline.a_coeff[k] * (cur_x ** 3) - Spline.b_coeff[k] * (cur_x ** 2)
        denominator = cur_x - Spline.init_x[k + 1]
        return numerator / denominator

    def calc_d(k):
        pass

    #подсчет коэффициентов сплайнов
    def calc_coeff(): 
        num_of_spl = np.size(Spline.h)
        Spline.calc_m()
        for i in range(num_of_spl):
            Spline.a_coeff = np.append(Spline.a_coeff, Spline.calc_a(i))
            Spline.b_coeff = np.append(Spline.b_coeff, Spline.calc_b(i))
            Spline.c_coeff = np.append(Spline.c_coeff, Spline.calc_c(i))
            Spline.d_coeff = np.append(Spline.d_coeff, Spline.calc_d(i))

    def get_val(x):
        pass

def main():

    data = parse_file('Newton.txt')
    Newton.fit_Newton(data)
    Newton.draw_Newton()

    Spline.init(data[:, 0], data[:, 1])
    Spline.calc_coeff()
    #MyPlot.show_all()


if __name__ == '__main__':
    main()