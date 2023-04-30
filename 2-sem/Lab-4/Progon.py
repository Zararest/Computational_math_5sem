import numpy as np

def print_matr(A):
  with open('matrix', 'w') as testfile:
    for row in A:
        testfile.write(' '.join([str(a) for a in row]) + '\n')

# ALPHA IS A -ALPHA IN ORDER TO GET Au=f FORM 

# u_l + a * u_{l+1} = bt
def straight(A, f, alpha, k_alpha, k_beta):
  size = np.size(f)
  B = np.zeros((size, size))
  f_B = np.zeros(size)
  u_0 = f[0]
  u_L = f[-1]
  
  B[0][0] = 1
  f_B[0] = u_0

  B[-1][-1] = 1
  f_B[-1] = u_L
  
  B[1][1] = 1
  B[1][2] = A[1][2] / A[1][1]
  f_B[1] = (f[1] - A[1][0] * u_0) / A[1][1]
  for l in range(2, alpha):
    a = A[l][l + 1] /                                 \
        (A[l][l] - A[l][l - 1] * B[l - 1][(l - 1) + 1])
    b = (f[l] - A[l][l - 1] * f_B[l - 1]) /             \
        (A[l][l] - A[l][l - 1] * B[l - 1][(l - 1) + 1])
    B[l][l] = 1
    B[l][l + 1] = a
    f_B[l] = b

  B[size - 2][size - 2] = 1
  B[size - 2][size - 3] = A[size - 2][size - 3] / \
                          A[size - 2][size - 2]
  f_B[size - 2] = (f[size - 2] - A[size - 2][size - 3] * u_L) / \
                  A[size - 2][size - 2]
  for l in reversed(range(alpha + 2, size - 1)):
    a = A[l][l - 1] / \
        (A[l][l] - A[l][l + 1] * B[l + 1][(l + 1) - 1])
    b = (f[l] - A[l][l + 1] * f_B[l + 1]) / \
        (A[l][l] - A[l][l + 1] * B[l + 1][(l + 1) - 1])
    B[l][l] = 1
    B[l][l - 1] = a
    f_B[l] = b
  beta = alpha + 1
  u_alpha = (k_alpha * f_B[alpha - 1] + k_beta * f_B[beta + 1]) / \
            (k_alpha * (1 + B[alpha - 1][(alpha - 1) + 1]) + \
             k_beta * (1 + B[beta + 1][(beta + 1) - 1]))
  B[alpha][alpha] = 1
  B[beta][beta] = 1
  f_B[alpha] = u_alpha
  f_B[beta] = u_alpha
  return B, f_B

def back(A, f, alpha):
  size = np.size(f)
  u = np.zeros(size)
  u[0] = f[0]
  u[-1] = f[-1]
  u[alpha] = f[alpha]
  u[alpha + 1] = f[alpha + 1]
  for l in reversed(range(1, alpha)):
    a = A[l][l + 1]
    u[l] = -a * u[l + 1] + f[l]
  for l in range(alpha + 2, size - 1): 
    a = A[l][l - 1]
    u[l] = -a * u[l - 1] + f[l]
  return u

# solver for system  with singularity between alpha and alpha + 1
# u_l{alpha} = u_l{alpha+1}
# (k_alpha)_l_{alpha} (u_l_{alpha} - u_l_{alpha-1}) 
#   = (k_alpha)_l_{alpha+1} (u_l_{alpha+2} - u_l_{alpaha+1})
# k_alpha and k_beta - value in heterogeneity point
# f[0] = u_0 f[-1] = u_L
def solve(A, f, alpha, k_alpha, k_beta):
  B, f_B = straight(A, f, alpha, k_alpha, k_beta)
  return back(B, f_B, alpha)
  