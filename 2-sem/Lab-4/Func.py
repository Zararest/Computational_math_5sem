import numpy as np

def k_a(x):
  return 0.125 * 0.125 # x + 1

def k_b(x):
  return 0.125 * 0.125 # x*x

def q(x):
  return 0.125 * 0.125 # x*x

def f(x):
  return np.cos(0.125) # np.cos(x)
