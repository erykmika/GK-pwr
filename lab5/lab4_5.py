#!/usr/bin/env python3
import sys
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

N = 30

tab = [[[0] * 3 for i in range(N)] for j in range(N)]
normal = [[[0] * 3 for i in range(N)] for j in range(N)]

# Tablice wartosci parametrow u i v
u, v = [], []

# Wyznaczamy n-elementowe tablice wartosci dla parametrow u i v
for i in range(N):
    u.append(i/(N-1))
    v.append(i/(N-1))

#numOfZeroes = 0

# Obliczamy wartosci x, y, z
for i in range(N):
    for j in range(N):
        tab[i][j][0] =  (-90 * u[i]**5 + 225 * u[i]**4 - 270 * u[i]**3 + 180 * u[i]*u[i] - 45*u[i]) * cos(pi * v[j])
        tab[i][j][1] = 160 * u[i] ** 4 - 320 * u[i] ** 3 + 160 * u[i] * u[i] - 5
        tab[i][j][2] =  (-90 * u[i]**5 + 225 * u[i]**4 - 270 * u[i]**3 + 180 * u[i]*u[i] - 45*u[i]) * sin(pi * v[j])

        # Wektory normalne
        xu = (-450 * u[i]**4 + 900 * u[i]**3 - 810 * u[i]**2 + 360 * u[i] - 45) * cos(pi * v[j])
        xv = pi * (90 * u[i]**5 - 225 * u[i]**4 + 270 * u[i]**3 - 180 * u[i]**2 + 45 * u[i]) * sin(pi * v[j])
        yu = 640 * u[i]**3 - 960 * u[i]**2 + 320 * u[i]
        yv = 0
        zu = (-450 * u[i]**4 + 900 * u[i]**3 - 810 * u[i]**2 + 360 * u[i] - 45) * sin(pi * v[j])
        zv = -pi * (90 * u[i]**5 - 225 * u[i]**4 + 270 * u[i]**3 - 180 * u[i]**2 + 45 * u[i]) * cos(pi * v[j])

        a = yu * zv - zu * yv
        b = zu * xv - xu * zv
        c = xu * yv - yu * xv

        vector_length = sqrt(a*a+b*b+c*c)
        #numOfZeroes += 1 if vector_length==0 else 0

        normal[i][j][0] = a / vector_length if vector_length!=0 else 0 
        normal[i][j][1] = b / vector_length if vector_length!=0 else 0 
        normal[i][j][2] = c / vector_length if vector_length!=0 else 0


#print(numOfZeroes)

# Debugowanie
#print(u[N-1], v[N-1])

random.seed(None)

# Wyznaczamy tablice kolorow wierzcholkow trojkatow - dzieki temu nie bedzie migotania
# (brak zmian kolorow przy wielokrotnym wywolywaniu funkcji render)
a1, b1, c1, a2, b2, c2 = [], [], [], [], [], []
d1, e1, f1 = [], [], []

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

viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0
theta1 = 0.0
phi1 = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0
LIGHT_DISTANCE = 5
x_s = 0
y_s = 0
z_s = 0
light_choice = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

# Zrodlo swiatla 1
light_ambient1 = [0.02, 0.2, 0.0, 1.0]
light_diffuse1 = [1.0, 0.0, 1.0, 1.0]
light_specular1 = [1.0, 1.0, 1.0, 1.0]
light_position1 = [-10.0, 5.0, 0.0, 1.0]


att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def startup():
    update_viewport(None, 800, 800)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    # Zrodlo swiatla 0
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    # Zrodlo swiatla 1
    #glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient1)
    #glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse1)
    #glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular1)
    #glLightfv(GL_LIGHT1, GL_POSITION, light_position1)

    #glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    #glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    #glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    #glEnable(GL_LIGHT1)


def shutdown():
    pass


def render(time):
    global theta, phi, light_position, LIGHT_DISTANCE, x_s, y_s, z_s
    global theta1, phi1
    global light_choice

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    
    #if right_mouse_button_pressed:
    #    theta1 += delta_x * pix2angle
    #    phi1 += delta_y * pix2angle
    spin(time * 180 / 3.1415)
    colorIndex = 0
    for j in range(N-1):
        glBegin(GL_TRIANGLE_STRIP)
        for i in range(N-1):
            glColor3f(d1[colorIndex], e1[colorIndex], f1[colorIndex])
            glNormal(normal[i][j][0], normal[i][j][1], normal[i][j][2])
            glVertex3f(tab[i][j][0], tab[i][j][1], tab[i][j][2])
            glColor3f(a1[colorIndex], b1[colorIndex], c1[colorIndex])
            glNormal(normal[i+1][j][0], normal[i+1][j][1], normal[i+1][j][2])
            glVertex3f(tab[i+1][j][0], tab[i+1][j][1], tab[i+1][j][2])
            glColor3f(a2[colorIndex], b2[colorIndex], c2[colorIndex])
            glNormal(normal[i][j+1][0], normal[i][j+1][1], normal[i][j+1][2])
            glVertex3f(tab[i][j+1][0], tab[i][j+1][1], tab[i][j+1][2])
            glColor3f(d1[colorIndex], e1[colorIndex], f1[colorIndex])
            glNormal(normal[i+1][j+1][0], normal[i+1][j+1][1], normal[i+1][j+1][2])
            glVertex3f(tab[i+1][j+1][0], tab[i+1][j+1][1], tab[i+1][j+1][2])
            colorIndex+=1
        glEnd()
    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global light_choice
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_X and action == GLFW_PRESS:
        light_choice = not light_choice


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y
    global mouse_x_pos_old, mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos
    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed, right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0
    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(800, 800, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
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
