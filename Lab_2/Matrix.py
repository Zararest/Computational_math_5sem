import numpy as np             
import matplotlib.pyplot as plt

n = 20
diag = 10


class UpperRelax:

    def __init__(self, A, f):
        self.A = A
        self.f = f
        self.teta = 1.5
        matr_size = A.shape
        if len(matr_size != 2) or (matr_size[0] != matr_size[1]):
            print('Incorrect matrix')
        self.n = matr_size[0]

    #концы включены
    #х - массив
    def __sum(self, start, end, x, j):
        sum = 0
        for k in range(end - start + 1):
            sum += self.A[j, k] / self.A[j, j] * x[k]
        return sum

    #индексация с 0
    def __iteration(self, x_prev, iter_num):
        x_new = np.array([])
        for j in range(self.n):
            x_j = -self.teta * self.__sum(0, j - 1, x_new, j) + (1 - self.teta) * x_prev[j] \
                - self.teta * self.__sum(j + 1, self.n - 1, x_prev, j) + self.teta * self.f[iter_num] / self.A[j, j]
            x_new = np.append(x_new, x_j)
    
    def calculate(self):
        pass





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
    print(A)
    print(f)

if __name__ == '__main__':
    main()