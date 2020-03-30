
"""
A matrix will be an N sized list of 4 element lists.
Each individual list will represent an [x, y, z, 1] point.
For multiplication purposes, consider the lists like so:
x0  x1      xn
y0  y1      yn
z0  z1  ... zn
1  1        1
"""
import math

#print the matrix such that it looks like
#the template in the top comment
def print_matrix( matrix ):
    s1 = ""
    s2 = ""
    s3 = ""
    s4 = ""
    for i in range(len(matrix)):
      s1 += str(matrix[i][0]) + " "
      s2 += str(matrix[i][1]) + " "
      s3 += str(matrix[i][2]) + " "
      s4 += str(matrix[i][3]) + " "
    s1 = s1[:-1] + "\n"
    s2 = s2[:-1] + "\n"
    s3 = s3[:-1] + "\n"
    s4 = s4[:-1]
    return s1 + s2 + s3 + s4

def print_transform(matrix):
  string = ""
  for i in matrix:
    for x in i:
      string += str(x) + " "
    string.strip()
    string += "\n"
  return string[:-1]

#turn the paramter matrix into an identity matrix
#you may assume matrix is square
def ident(matrix):
  while len(matrix) > 4:
    del matrix[-1]
  while len(matrix) < 4: matrix.append([])
  for i in range(len(matrix)): matrix[i] = [0] * 4
  length = len(matrix)
  for i in range(length):
    for x in range(length):
      if i != x: matrix[i][x] = 0
      else: matrix[i][x] = 1

#multiply m1 by m2, modifying m2 to be the product
#m1 * m2 -> m2

#I was unsure of the format for the multiplication
#because the edge matrices are formatted where the
#number of rows in the array is actumatrix[0][0] = xally the number
#of columns in the matrix it is representing.

#because m1 is usually going to be the transformation
#matrix, I figured that it would be formatted like a
#normal array, without the need to account for this by
#flipping the array.
def matrix_mult( m1, m2 ):
  for i in range(len(m2)):
    temp = [0, 0, 0, 0]
    temp[0] = (m1[0][0] * m2[i][0]) + (m1[0][1] * m2[i][1]) + (m1[0][2] * m2[i][2]) + (m1[0][3] * m2[i][3])
    temp[1] = (m1[1][0] * m2[i][0]) + (m1[1][1] * m2[i][1]) + (m1[1][2] * m2[i][2]) + (m1[1][3] * m2[i][3])
    temp[2] = (m1[2][0] * m2[i][0]) + (m1[2][1] * m2[i][1]) + (m1[2][2] * m2[i][2]) + (m1[2][3] * m2[i][3])
    temp[3] = (m1[3][0] * m2[i][0]) + (m1[3][1] * m2[i][1]) + (m1[3][2] * m2[i][2]) + (m1[3][3] * m2[i][3])
    m2[i] = temp

def transform_mult(t1, t2):
  for i in range(4):
    temp = [0, 0, 0, 0]
    temp[0] = (t1[0][0] * t2[0][i]) + (t1[0][1] * t2[1][i]) + (t1[0][2] * t2[2][i]) + (t1[0][3] * t2[3][i])
    temp[1] = (t1[1][0] * t2[0][i]) + (t1[1][1] * t2[1][i]) + (t1[1][2] * t2[2][i]) + (t1[1][3] * t2[3][i])
    temp[2] = (t1[2][0] * t2[0][i]) + (t1[2][1] * t2[1][i]) + (t1[2][2] * t2[2][i]) + (t1[2][3] * t2[3][i])
    temp[3] = (t1[3][0] * t2[0][i]) + (t1[3][1] * t2[1][i]) + (t1[3][2] * t2[2][i]) + (t1[3][3] * t2[3][i])
    for x in range(4):
      t2[x][i] = temp[x]

def new_matrix(rows = 4, cols = 4):
    m = []
    for c in range( cols ):
        m.append( [] )
        for r in range( rows ):
            m[c].append( 0 )
    return m
