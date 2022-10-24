#!usr/bin/python3

from distutils.command.build_scripts import first_line_re
import numpy as np    

epsilon = 0.001

def ostanov(prev_X, cur_X, q):
    return (np.abs(prev_X - cur_X) / (1 - q)) >= epsilon

def iter_method(func, q, initial_X):
    prev_X = initial_X + epsilon
    cur_X = initial_X
    while ostanov(prev_X, cur_X, q):
        prev_X = cur_X
        cur_X = func(prev_X)
    return cur_X

def first_func(X):
    return 10**(X / 4 - 1 / 2)

def first_func_diriv(X):
    return np.log(10) * 1 / 4 * first_func(X)

def calc_left_X():
    initial_X = 0.75
    return iter_method(first_func, first_func_diriv(initial_X), initial_X)

def second_func(X):
    return 4 * np.log(X) / np.log(10) + 2

def second_func_diriv(X):
    return 4 / (np.log(10) * X)

def calc_right_X():
    initial_X = 4.75
    return iter_method(second_func, second_func_diriv(initial_X), initial_X)

def calc_equation():
    ans = []
    ans.append(calc_left_X())
    ans.append(calc_right_X())
    return ans

def main():
    print('Result equation', calc_equation())

if __name__ == '__main__':
    main()