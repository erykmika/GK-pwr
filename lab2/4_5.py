#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

# Wspolrzedne oraz dlugosci bokow najwiekszego kwadratu
x = -80
y = -80
a = -2 * x
b = -2 * y


def startup():
    update_viewport(None, 800, 800)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    # Rysujemy najwiekszy kolorowy kwadrat
    glColor3f(0.71, 0.306, 0.169)
    draw_rectangle(x, y, a, b)
    # Rysujemy "dziury" wewnatrz kwadratu
    glColor3f(1, 1, 1)
    # Wykorzystujemy argument podany w wierszu polecen/terminalu
    draw_recursively(x, y, a, b, int(sys.argv[1]))


def draw_rectangle(x, y, a, b):

    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x + a, y)
    glVertex2f(x, y + b)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(x + a, y + b)
    glVertex2f(x + a, y)
    glVertex2f(x, y + b)
    glEnd()

    glFlush()


def draw_recursively(x, y, a, b, sim=1):

    # Warunek zakonczenia rekurencji
    if sim <= 0:
        return
    
    # 1/3 wymiarow wiekszego kwadratu
    new_width = 0.3333 * a
    new_height = 0.3333 * b

    draw_rectangle(x + new_width, y + new_height, new_width, new_height)
    
    # Wspolrzedne x to po kolei wspolrzedna x poczatku, 1/3 oraz 2/3 czesci boku wiekszego kwadratu

    # row 1 / wiersz 1 - od gory - wierzcholki kwadratow o wspolrzednych y w 2/3 czesci boku pionowego (y + 2*0.3333*b)
    draw_recursively(x,                 y + 2 * new_height, new_width, new_height, sim-1)
    draw_recursively(x + new_width,     y + 2 * new_height, new_width, new_height, sim-1)
    draw_recursively(x + 2 * new_width, y + 2 * new_height, new_width, new_height, sim-1)
    
    # row 2 / wiersz 2 - wierzcholki kwadratow o wspolrzednych y w 1/3 czesci boku pionowego (y + 0.3333*b)
    draw_recursively(x,                y + new_height, new_width, new_height, sim-1)
    # w srodku prostokat/kwadrat z poprzedniej iteracji
    draw_recursively(x + 2* new_width, y + new_height, new_width, new_height, sim-1)

    # row 3 / wiersz 3 - wierzcholki kwadratow o wspolrzednych y takich samych jak wiekszy kwadrat (y)
    draw_recursively(x,                y, new_width, new_height, sim-1)
    draw_recursively(x + new_width,    y, new_width, new_height, sim-1)
    draw_recursively(x + 2* new_width, y, new_width, new_height, sim-1)


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(800, 800, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
