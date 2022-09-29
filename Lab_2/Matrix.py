import numpy as np             
import matplotlib.pyplot as plt

n = 20
diag = 10

class Norm:

    def __get_first_norm(matrix):
        matr_size = matrix.shape
        if len(matr_size) != 1:
            print('Пока матрицы не поддерживаются')
            print('Shape:', matr_size)
            return -1
        return np.amax(np.abs(matrix))

    def get_norm(matrix):
        return Norm.__get_first_norm(matrix)

class UpperRelax:

    def __init__(self, A, f):
        self.A = A
        self.f = f
        self.teta = 1.5
        self.epsilon = 0.01
        matr_size = A.shape
        if (len(matr_size) != 2) or (matr_size[0] != matr_size[1]):
            print('Incorrect matrix')
        self.n = matr_size[0]
        self.r_arr = np.array([])

    def __get_initial_x(self):
        x = np.copy(self.f)
        return x

    #подсчет невязки
    def __calc_r(self, x):
        r = Norm.get_norm(np.matmul(self.A, x) - self.f)
        self.r_arr = np.append(self.r_arr, r)

    #концы включены
    #х - массив
    def __sum(self, start, end, x, j):
        sum = 0
        for k in range(end - start + 1):
            sum += self.A[j, start + k] / self.A[j, j] * x[start + k]
        return sum

    #индексация с 0
    def __iteration(self, x_prev):
        x_new = np.array([])
        for j in range(self.n):
            x_j = (-1) * self.teta * self.__sum(0, j - 1, x_new, j) + (1 - self.teta) * x_prev[j] \
                - self.teta * self.__sum(j + 1, self.n - 1, x_prev, j) + self.teta * self.f[j] / self.A[j, j]
            x_new = np.append(x_new, x_j)
        return x_new
    
    def calculate(self):
        num_of_iter = 0
        x_prev = self.__get_initial_x()
        x_new = np.array([])
        prev_error = np.Inf
        curr_error = 0
        while True:
            x_new = self.__iteration(x_prev)
            self.__calc_r(x_new)
            curr_error = Norm.get_norm(x_new - x_prev)
            if curr_error < self.epsilon:
                print('конечная разность:', Norm.get_norm(x_new - x_prev))
                break
            else:
                x_prev = x_new
            if prev_error < curr_error:
                print('Warning: on iteration', num_of_iter, 'error was', prev_error, ' and now', curr_error)
            prev_error = curr_error
            num_of_iter += 1
        return x_new




def get_line(line_num):
    line = np.array([])
    for j in range(n):
        if line_num == j:
            line = np.append(line, diag)
        else:    
            line = np.append(line, 1 / (line_num + j + 2))
    return line

def generate_matrix():
    matr = get_line(0)
    for i in range(n - 1):
        line = get_line(i + 1)
        matr = np.vstack((matr, line))
    return matr

def generate_rhs():
    rhs = np.array([])
    for i in range(n):
        rhs = np.append(rhs, 1 / (i + 1))
    return np.transpose(rhs)

def iteration_method(A, f):
    method = UpperRelax(A, f)
    method.calculate()

def main():
    A = generate_matrix()
    f = generate_rhs()
    method = UpperRelax(A, f)
    ans_iter = method.calculate()
    print('Ans:', ans_iter)
    print('Невязка:', method.r_arr)

if __name__ == '__main__':
    main()