#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
from math import *


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
    #glRotatef(theta1, 0.0, 1.0, 0.0)
    #glRotatef(phi1, 1.0, 0.0, 0.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 8, 8)
    gluDeleteQuadric(quadric)
    
    if left_mouse_button_pressed:
        theta -= delta_x * pix2angle
        phi -= delta_y * pix2angle
        x_s = LIGHT_DISTANCE * cos(pi*theta/180) * cos(pi*phi/180)
        y_s = LIGHT_DISTANCE * sin(pi*phi/180)
        z_s = LIGHT_DISTANCE * sin(pi*theta/180) * cos(pi*phi/180)

    glTranslatef(x_s, y_s, z_s)
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)
    glTranslatef(-x_s, -y_s, -z_s)
    #if light_choice:
    light_position[0] = x_s
    light_position[1] = y_s
    light_position[2] = z_s
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    #else:
    #    glLightfv(GL_LIGHT1, GL_POSITION, light_position)
    #glTranslatef(-x_s, -y_s, -z_s)
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
