#!/usr/bin/env python3
import sys
from math import *
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

N = 25

tab = [[[0] * 3 for i in range(N)] for j in range(N)]

# Tablice wartosci parametrow u i v
u, v = [], []

# Wyznaczamy n-elementowe tablice wartosci dla parametrow u i v
for i in range(N):
    u.append(i/(N-1))
    v.append(i/(N-1))

# Obliczamy wartosci x, y, z
for i in range(N):
    for j in range(N):
        tab[i][j][0] =  (-90 * u[i]**5 + 225 * u[i]**4 - 270 * u[i]**3 + 180 * u[i]*u[i] - 45*u[i]) * cos(pi * v[j])
        tab[i][j][1] = 160 * u[i] ** 4 - 320 * u[i] ** 3 + 160 * u[i] * u[i] - 5
        tab[i][j][2] =  (-90 * u[i]**5 + 225 * u[i]**4 - 270 * u[i]**3 + 180 * u[i]*u[i] - 45*u[i]) * sin(pi * v[j])

# Debugowanie
#print(u[N-1], v[N-1])

# Wyznaczamy tablice kolorow wierzcholkow trojkatow - dzieki temu nie bedzie migotania
# (brak zmian kolorow przy wielokrotnym wywolywaniu funkcji render)
a1, b1, c1, a2, b2, c2 = [], [], [], [], [], []
d1, e1, f1 = [], [], []

random.seed(None)

for i in range((N-1)*(N-1)):
    a1.append(random.randint(0,255)/255)
    b1.append(random.randint(0,255)/255)
    c1.append(random.randint(0,255)/255)
    a2.append(random.randint(0,255)/255)
    b2.append(random.randint(0,255)/255)
    c2.append(random.randint(0,255)/255)
    d1.append(random.randint(0,255)/255)
    e1.append(random.randint(0,255)/255)
    f1.append(random.randint(0,255)/255)


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

def startup():
    update_viewport(None, 700, 700)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time * 180 / 3.1415)

    axes()

    glColor3f(1, 1, 1)

    colorIndex = 0
    # Rysujemy trojkaty
    for i in range(N-1):
        for j in range(N-1):
            glBegin(GL_TRIANGLES)

            glColor3f(d1[colorIndex], e1[colorIndex], f1[colorIndex])
            glVertex3f(tab[i][j][0], tab[i][j][1], tab[i][j][2])

            glColor3f(a1[colorIndex], b1[colorIndex], c1[colorIndex])
            glVertex3f(tab[i+1][j][0], tab[i+1][j][1], tab[i+1][j][2])

            glColor3f(a2[colorIndex], b2[colorIndex], c2[colorIndex])
            glVertex3f(tab[i][j+1][0], tab[i][j+1][1], tab[i][j+1][2])

            glEnd()

            glBegin(GL_TRIANGLES)
            
            glColor3f(a2[colorIndex], b2[colorIndex], c2[colorIndex])
            glVertex3f(tab[i][j+1][0], tab[i][j+1][1], tab[i][j+1][2])

            glColor3f(a1[colorIndex], b1[colorIndex], c1[colorIndex])
            glVertex3f(tab[i+1][j][0], tab[i+1][j][1], tab[i+1][j][2])

            glColor3f(d1[colorIndex], e1[colorIndex], f1[colorIndex])
            glVertex3f(tab[i+1][j+1][0], tab[i+1][j+1][1], tab[i+1][j+1][2])

            glEnd()
            colorIndex += 1
    glFlush()


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
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(700, 700, __file__, None, None)
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
