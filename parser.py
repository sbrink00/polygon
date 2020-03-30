import sys
from matrix import *
from draw import *
from display import *
from transformations import *


def genLines(file):
  f = open(file, "r")
  lines = f.readlines()
  for i in range(len(lines)): lines[i] = lines[i][:-1]
  if sys.argv[-1] == "nodisplay": lines = [x for x in lines if x != "display"]
  f.close()
  return lines

steps_2d = 100
steps_3d = 20

def parse_file(file, edge, polygons, transform, screen, color):
  lines = genLines(file)
  ident(transform)
  x = 0
  while x < len(lines):
    if lines[x] == "line":
      p = [int(y) for y in lines[x + 1].split(" ")]
      add_edge(edge, p[0], p[1], p[2], p[3], p[4], p[5])
      x += 1
    elif lines[x] == "circle":
      p = [int(y) for y in lines[x + 1].split(" ")]
      add_circle(edge, p[0], p[1], p[2], p[3], 10000)
      x += 1
    elif lines[x] == "triangle":
      p = [int(y) for y in lines[x + 1].split(" ")]
      add_polygon(polygons, p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8])
      x += 1
    elif lines[x] == "hermite":
      p = [int(y) for y in lines[x + 1].split(" ")]
      add_hermite(edge, p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7])
      x += 1
    elif lines[x] == "bezier":
      p = [int(y) for y in lines[x + 1].split(" ")]
      add_bezier(edge, p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7])
      x += 1
    elif lines[x] == "torus":
      p = [int(y) for y in lines[x + 1].split(" ")]
      add_torus(edge, p[0], p[1], p[2], p[3], p[4], steps_3d)
      x += 1
    elif lines[x] == "sphere":
      p = [int(y) for y in lines[x + 1].split(" ")]
      add_sphere(polygons, p[0], p[1], p[2], p[3], steps_3d)
      x += 1
    elif lines[x] == "box":
      p = [int(y) for y in lines[x + 1].split(" ")]
      add_box(polygons, p[0], p[1], p[2], p[3], p[4], p[5])
      x += 1
    elif lines[x] == "ident":
      ident(transform)
    elif lines[x] == "scale":
      f = [int(y) for y in lines[x + 1].split(" ")]
      s = []
      scale(s, f[0], f[1], f[2])
      transform_mult(s, transform)
      x += 1
    elif lines[x] == "move":
      f = [int(y) for y in lines[x + 1].split(" ")]
      move = []
      translate(move, f[0], f[1], f[2])
      transform_mult(move, transform)
      x += 1
    elif lines[x] == "rotate":
      f = lines[x + 1].split(" ")
      r = []
      rotate(r, f[0], int(f[1]))
      transform_mult(r, transform)
      x += 1
    elif lines[x] == "apply":
      matrix_mult(transform, edge)
      matrix_mult(transform, polygons)
    elif lines[x] == "display":
      draw_lines(edge, screen, DRAW_COLOR)
      display(screen)
    elif lines[x] == "clear":
      edge.clear()
    elif lines[x] == "save":
      draw_lines(edge, screen, DRAW_COLOR)
      draw_polygons(polygons, screen, DRAW_COLOR)
      save_extension(screen, lines[x + 1])
      print("File name: " + lines[x + 1])
      x += 1
    x += 1
