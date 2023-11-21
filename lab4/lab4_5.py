#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from math import sin
from math import cos
from math import pi


viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0
pix2angle = 1.0
R = 1.0
x_eye = 0
y_eye = 0
z_eye = 10
MAX_DISTANCE = 3.0

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
key_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0
scale = 1.0


def startup():
    update_viewport(None, 800, 800)
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


def example_object():
    glColor3f(1.0, 1.0, 1.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)

    gluSphere(quadric, 1.5, 10, 10)

    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)

    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)

    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)

    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)

    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)


def render(time):
    global theta
    global phi
    global scale
    global R
    global x_eye
    global y_eye
    global z_eye
    global key_pressed

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    # Aktualizujemy wartosci, gdy klawisz wcisniety
    if right_mouse_button_pressed or key_pressed:
        phi += delta_y * pix2angle
        theta += delta_x * pix2angle
        R += delta_x * 0.015 * pix2angle
        if R < 1.0:
            R = 1.0
        if R > MAX_DISTANCE:
            R = MAX_DISTANCE
        phi%=360
        theta%=360
    if right_mouse_button_pressed:
        # Ruch kamery
        x_eye = R * cos(theta * (pi/180)) * sin(phi*(pi/180))
        y_eye = R * sin(phi*(pi/180))
        z_eye = R * sin(theta * (pi/180)) * cos(phi*(pi/180))
    elif key_pressed:
        #Obrocenie
        glRotatef(phi, 1.0, 0.0, 0.0)
        glRotatef(theta, 0.0, 1.0, 0.0)
    gluLookAt(x_eye, y_eye, z_eye, 0, 0, 0, 0, 1, 0)
    axes()
    example_object()

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
    global key_pressed
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    elif key == GLFW_KEY_X and action == GLFW_REPEAT:
        key_pressed = 1
    else:
        key_pressed = 0


def mouse_motion_callback(window, x_pos, y_pos):
    # Uzycie globalnych zmiennych
    global delta_x
    global mouse_x_pos_old
    global delta_y
    global mouse_y_pos_old
    
    # Zmiana polozenia x, y dla myszy
    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos
    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos



def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0


def main():
    global action
    global mvm
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
