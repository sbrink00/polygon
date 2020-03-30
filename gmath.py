import math
from display import *



#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
  pass

#Return the dot porduct of a . b
def dot_product(a, b):
  return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

def findVector(a, b):
  return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):
  v1 = findVector(polygons[i], polygons[i + 1])
  v2 = findVector(polygons[i], polygons[i + 2])
  crossProduct = findCrossProduct(v1, v2)
  return crossProduct

def findCrossProduct(a, b):
  zero = a[1] * b[2] - a[2] * b[1]
  one = a[2] * b[0] - a[0] * b[2]
  two = a[0] * b[1] - a[1] * b[0]
  return [zero, one, two]

def include(polygons, i):
  normal = calculate_normal(polygons, i)
  view = [0, 0, 1]
  cosTheta = dot_product(normal, view)
  if cosTheta >0: return True
  return False
