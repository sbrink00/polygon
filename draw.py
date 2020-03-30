from display import *
from matrix import *
from transformations import *
from gmath import include

#0, 1, 2, 3, 4, 5, 6

def draw_lines(matrix, screen, color):
    length = int(len(matrix) / 2)
    for i in range(length):
      l1 = matrix[i * 2]
      l2 = matrix[i * 2 + 1]
      draw_line(round(l1[0]), round(l1[1]), round(l2[0]), round(l2[1]), screen, color)

def add_edge(matrix, x0, y0, z0, x1, y1, z1):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)

def add_point(matrix, x, y, z=0):
    matrix.append([x, y, z, 1])

def add_polygon_helper(x0, y0, z0, x1, y1, z1, x2, y2, z2):
  p0,p1,p2 = [x0, y0, z0, 1],[x1, y1, z1, 1],[x2, y2, z2, 1]
  points = findMiddle(p0, p1, p2)
  p0,p1,p2 = points[0],points[1],points[2]
  if p0[1] >= p1[1] and p2[1] >= p1[1]: return [[x for x in p1], [x for x in p2], [x for x in p0]]
  if p0[1] <= p1[1] and p2[1] <= p1[1]: return [[x for x in p1], [x for x in p0], [x for x in p2]]
  if p0[1] > p1[1] and p2[1] < p1[1]: return [[x for x in p1], [x for x in p0], [x for x in p2]]
  if p0[1] < p1[1] and p2[1] > p1[1]: return [[x for x in p1], [x for x in p2], [x for x in p0]]
  return [[x for x in p1], [x for x in p0], [x for x in p2]]

def add_polygon2(polygons, x0, y0, z0, x1, y1, z1, x2, y2, z2):
  polygons += add_polygon_helper(x0, y0, z0, x1, y1, z1, x2, y2, z2)

def add_polygon(polygons, x0, y0, z0, x1, y1, z1, x2, y2, z2):
  add_point(polygons, x0, y0, z0)
  add_point(polygons, x1, y1, z1)
  add_point(polygons, x2, y2, z2)

def draw_polygons(polygons, screen, color):
  length = int(len(polygons) / 3)
  for i in range(length):
    if include(polygons, i * 3):
      p0 = polygons[i * 3]
      p1 = polygons[i * 3 + 1]
      p2 = polygons[i * 3 + 2]
      draw_line(round(p0[0]), round(p0[1]), round(p1[0]), round(p1[1]), screen, color)
      draw_line(round(p1[0]), round(p1[1]), round(p2[0]), round(p2[1]), screen, color)
      draw_line(round(p2[0]), round(p2[1]), round(p0[0]), round(p0[1]), screen, color)

def findMiddle(a, b, c):
  points = [a, b, c]
  if points[0][0] > points[1][0]: points[0],points[1] = points[1],points[0]
  if points[1][0] > points[2][0]: points[2],points[1] = points[1],points[2]
  if points[2][0] < points[0][0]: points[0],points[2] = points[2],points[0]
  if points[0][0] > points[1][0]: points[0],points[1] = points[1],points[0]
  return [[x for x in points[0]], [x for x in points[1]], [x for x in points[2]]]


def add_square(matrix, x0, y0, x1, y1):
  add_edge(matrix, x0, y0, 0, x1, y0, 0)
  add_edge(matrix, x0, y0, 0, x0, y1, 0)
  add_edge(matrix, x0, y1, 0, x1, y1, 0)
  add_edge(matrix, x1, y0, 0, x1, y1, 0)

def add_circle(matrix, cx, cy, cz, r, steps):
  i = 0
  while i <= steps:
    t = 1.0 * i / steps
    x = r * cos(360 * t) + cx
    y = r * sin(360 * t) + cy
    z = cz
    add_point(matrix, x, y, z)
    if t != 0: add_point(matrix, x, y, z)
    i += 1
  add_point(matrix, r + cx, cy, cz)

def add_half_circle(matrix, cx, cy, cz, r):
  t = 0
  while t <= .5:
    x = r * cos(360 * t) + cx
    y = r * sin(360 * t) + cy
    z = cz
    add_point(matrix, x, y, z)
    if t != 0: add_point(matrix, x, y, z)
    t += TSTEP
  add_point(matrix, r + cx, cy, cz)

def add_bezier(matrix, x0, y0, x1, y1, x2, y2, x3, y3):
  ax = (3 * x1 + x3 - x0 - 3 * x2)
  bx = (3 * x0 + 3 * x2 - 6 * x1)
  cx = (3 * x1 - 3 * x0)
  dx = x0
  ay = (3 * y1 + y3 - y0 - 3 * y2)
  by = (3 * y0 + 3 * y2 - 6 * y1)
  cy = (3 * y1 - 3 * y0)
  dy = y0
  t = 0
  while t <= 1:
    x = dx + t * (cx + t * (bx + t * ax))
    y = dy + t * (cy + t * (by + t * ay))
    add_point(matrix, x, y)
    if t != 0 and t < 1: add_point(matrix, x, y)
    t += TSTEP
  del matrix[-1]

def add_hermite(matrix, x0, y0, x1, y1, rx0, ry0, rx1, ry1):
  ax = (2 * x0 + rx0 + rx1 - 2 * x1)
  bx = (3 * x1 - 3 * x0 - 2 * rx0 - rx1)
  cx = rx0
  dx = x0
  ay = (2 * y0 + ry0 + ry1 - 2 * y1)
  by = (3 * y1 - 3 * y0 - 2 * ry0 - ry1)
  cy = ry0
  dy = y0
  t = 0
  while t <= 1:
    x = dx + t * (cx + t * (bx + t * ax))
    y = dy + t * (cy + t * (by + t * ay))
    add_point(matrix, x, y)
    if t != 0 and t < 1: add_point(matrix, x, y)
    t += TSTEP
  del matrix[-1]

  # ====================
  # Generates all the points along the surface
  # of a sphere with center (cx, cy, cz) and
  # radius r.
  # Returns a matrix of those points
  # ====================
def generate_sphere2( points, cx, cy, cz, r, fistep, thetastep):
  matrix = []
  fi = 0
  while fi < 1:
    theta = 0
    x0 = r * cos(180 * theta) + cx
    y0 = r * sin(180 * theta) * cos(360 * fi) + cy
    z0 = r * sin(180 * theta) * sin(360 * fi) + cz
    while theta < 1:
      x1 = r * cos(180 * theta) + cx
      y1 = r * sin(180 * theta) * cos(360 * fi) + cy
      z1 = r * sin(180 * theta) * sin(360 * fi) + cz
      add_edge(matrix, x0, y0, z0, x1, y1, z1)
      x0,y0,z0 = x1,y1,z1
      theta += thetastep
    fi += fistep
  return matrix

def generate_sphere(cx, cy, cz, r, steps):
  matrix = []
  rot = 0
  circ = 0
  while rot < steps:
    circ = 0
    fi = 1.0 * rot / steps
    while circ < steps:
      theta = 1.0 * circ / steps
      x0 = r * cos(180 * theta) + cx
      y0 = r * sin(180 * theta) * cos(360 * fi) + cy
      z0 = r * sin(180 * theta) * sin(360 * fi) + cz
      add_point(matrix, x0, y0, z0)
      #add_point(matrix, x0, y0, z0)
      circ += 1
    rot += 1
  return matrix

  # ====================
  # adds all the points for a sphere with center
  # (cx, cy, cz) and radius r to points
  # should call generate_sphere to create the
  # necessary points
  # ====================

def add_sphere(points, cx, cy, cz, r, steps):
  matrix = generate_sphere(cx, cy, cz, r, steps)
  for i in range(len(matrix) - 1):
      points.append(matrix[i])
      points.append(matrix[i + 1])
      points.append(matrix[(i + steps + 1) % len(matrix)])
      if i % steps != 0 and i % steps != steps - 1:
        points.append(matrix[i])
        points.append(matrix[(i + steps + 1) % len(matrix)])
        points.append(matrix[(i + steps) % len(matrix)])

  # ====================
  # Generates all the points along the surface
  # of a torus with center (cx, cy, cz) and
  # radii r0 and r1.
  # Returns a matrix of those points
  # ====================
def generate_torus(cx, cy, cz, r0, r1, steps):
  matrix = []
  rot = 0
  circ = 0
  while rot < steps:
    fi = 1.0 * rot / steps
    circ = 0
    while circ < steps:
      theta = 1.0 * circ / steps
      x0 = cos(360 * fi) * (r0 * cos(360 * theta) + r1) + cx
      y0 = r0 * sin(360 * theta) + cy
      z0 = (-1 * sin(360 * fi)) * (r0 * cos(360 * theta) + r1) + cz
      add_point(matrix, x0, y0, z0)
      circ += 1
    rot += 1
  return matrix

  # ====================
  # adds all the points for a torus with center
  # (cx, cy, cz) and radii r0, r1 to points
  # should call generate_torus to create the
  # necessary points
  # ====================
def add_torus(points, cx, cy, cz, r0, r1, steps):
  matrix = generate_torus(cx, cy, cz, r0, r1, steps)
  for i in range(len(matrix) - 1):
    points.append(matrix[i])
    points.append(matrix[(i + steps) % len(matrix)])
    points.append(matrix[(i + steps + 1) % len(matrix)])
    points.append(matrix[i])
    points.append(matrix[(i + steps + 1) % len(matrix)])
    points.append(matrix[i + 1])


  # ====================
  # add the points for a rectagular prism whose
  # upper-left corner is (x, y, z) with width,
  # height and depth dimensions.
  # ====================

def add_box(points, x, y, z, w, h, d):
  x1,y1,z1 = x + w,y - h,z - d
  #top
  add_polygon(points, x, y, z, x1, y, z, x, y, z1)
  add_polygon(points, x1, y, z, x1, y, z1, x, y, z)

  #bottom
  add_polygon(points, x, y1, z1, x, y1, z, x1, y1, z)
  add_polygon(points, x, y1, z1, x1, y1, z, x1, y1, z1)

  #left
  add_polygon(points, x, y, z1, x, y1, z1, x, y1, z)
  add_polygon(points, x, y, z1, x, y1, z, x, y, z)

  #right
  add_polygon(points, x1, y, z1, x1, y1, z1, x1, y1, z)
  add_polygon(points, x1, y, z1, x1, y1, z, x1, y, z)

  #front
  add_polygon(points, x, y, z, x, y1, z, x1, y, z)
  add_polygon(points, x1, y1, z, x1, y, z, x, y1, z)

  #back
  add_polygon(points, x, y1, z1, x1, y, z1, x, y, z1)
  add_polygon(points, x, y1, z1, x1, y1, z1, x1, y, z1)

  #add_edge(points, x, y, z, x + w, y, z)
  # add_edge(points, x, y, z, x, y, z - d)
  # add_edge(points, x + w, y, z, x + w, y, z - d)
  # add_edge(points, x, y, z - d, x + w, y, z - d)
  # add_edge(points, x, y, z, x, y - h, z)
  # add_edge(points, x, y, z - d, x, y - h, z - d)
  # add_edge(points, x + w, y, z - d, x + w, y - h, z - d)
  # add_edge(points, x + w, y, z, x + w, y - h, z)
  # add_edge(points, x, y - h, z, x + w, y - h, z)
  # add_edge(points, x, y - h, z, x, y - h, z - d)
  # add_edge(points, x + w, y - h, z, x + w, y - h, z - d)
  # add_edge(points, x, y - h, z - d, x + w, y - h, z - d)



def draw_line(x0, y0, x1, y1, screen, color):
  x1,y1,x0,y0 = int(x1),int(y1),int(x0),int(y0)
  undefined,a,b,m = findABM(x0, y0, x1, y1)
  if 0 <= m and m <= 1:
    if y1 < y0: x0,y0,x1,y1 = x1,y1,x0,y0
    x = x0
    y = y0
    undefined,a,b,m = findABM(x0, y0, x1, y1)
    d = 2 * a + b
    while x <= x1:
      plot(screen, color, x, y)
      if d > 0:
        y += 1
        d += 2 * b
      x += 1
      d += 2 * a
    return
  if m > 1 or undefined:
    if y1 < y0: x0,y0,x1,y1 = x1,y1,x0,y0
    x = x0
    y = y0
    undefined,a,b,m = findABM(x0, y0, x1, y1)
    d = 2 * a + b
    while y <= y1:
      plot(screen, color, x, y)
      if d < 0:
        x += 1
        d += 2 * a
      y += 1
      d += 2 * b
    return
  if m < 0 and m >= -1:
    if y1 > y0: x0,y0,x1,y1 = x1,y1,x0,y0
    x = x0
    y = y0
    undefined,a,b,m = findABM(x0, y0, x1, y1)
    d = 2 * a + b
    while x <= x1:
      plot(screen, color, x, y)
      if d < 0:
        y -= 1
        d -= 2 * b
      x += 1
      d += 2 * a
    return
  if m < -1:
    if y1 > y0: x0,y0,x1,y1 = x1,y1,x0,y0
    x = x0
    y = y0
    undefined,a,b,m = findABM(x0, y0, x1, y1)
    d = 2 * a + b
    while y >= y1:
      plot(screen, color, x, y)
      if d > 0:
        x += 1
        d += 2 * a
      y -= 1
      d -= 2 * b
    return

def findABM(x0, y0, x1, y1):
  undefined = False
  a = y1 - y0
  b = -1 * (x1 - x0)
  if b == 0: return True,a,b,-1
  m = -1.0 * a / b
  return undefined,a,b,m
