#!/usr/bin/env python3
import math
from re import A
import sys
from telnetlib import NEW_ENVIRON

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
import random


def startup():
    update_viewport(None, 400, 400)
    glClearColor(1, 1, 1, 1.0)


def shutdown():
    pass

#zad 1   
def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_TRIANGLES)
    glColor3f(1, 0, 0)
    glVertex2f(0.0, 0.0)
    glColor3f(0, 1, 0)
    glVertex2f(0.0, 50.0)
    glColor3f(0, 0, 1)
    glVertex2f(50.0, 0.0)
    glEnd()
    glFlush()

#zad 2

def draw_rectangle(x, y, a, b):

    bottom_left = (x - a / 2, y - b / 2)
    top_left = (x - a / 2, y + b / 2)
    top_right = (x + a / 2, y + b / 2)
    bottom_right = (x + a / 2, y - b / 2)
    glColor3f(1, 0, 0)
    glBegin(GL_TRIANGLES) 
    glVertex2f(*bottom_left)   
    glVertex2f(*top_left)
    glVertex2f(*bottom_right) 
    glVertex2f(*top_left)
    glVertex2f(*top_right)
    glVertex2f(*bottom_right)
    glEnd()

def render_rectangle():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_rectangle(0, 0, 100.0, 50.0)
    glFlush()

#zad 3
def draw_rectangle_random(x, y, a, b, d):

    a = a * (1 + random.uniform(-d,d))
    b = b * (1 + random.uniform(-d,d))

    bottom_left = (x - a / 2, y - b / 2)
    top_left = (x - a / 2, y + b / 2)
    top_right = (x + a / 2, y + b / 2)
    bottom_right = (x + a / 2, y - b / 2)

    
    glBegin(GL_TRIANGLES)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(*bottom_left)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(*top_left)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(*bottom_right)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(*top_left)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(*top_right)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(*bottom_right)
    glColor3f(random.random(), random.random(), random.random())
    glEnd()
   

def render_rectangle_random(random_seed):
    random.seed(random_seed)
    glClear(GL_COLOR_BUFFER_BIT)
    draw_rectangle_random(0, 0, 100.0, 50.0, 0.2)
    glFlush()

#zad 4
def carpet(x, y, a, b, depth):
    if depth == 0:
        draw_rectangle (x, y, a, b)
    else:
        new_a = a/3
        new_b = b/3
        for i in range(-1,2):
            for j in range (-1,2):
                if i==0 and j==0:
                    continue
                carpet(x+i*new_a, y+j*new_b, new_a, new_b, depth-1)

def render_carpet(depth):
    glClear(GL_COLOR_BUFFER_BIT)
    carpet(0, 0 ,300, 200, depth)
    glFlush()

#zad 5
def koch_curve(x, y, depth):
    if depth == 0:
        glColor3f(0.0, 0.3, 0.9) 
        glBegin(GL_LINES)
        glVertex2f(*x)
        glVertex2f(*y)
        glEnd()
    else:
        a1 = (2 * x[0] + 1 * y[0]) / 3
        b1 = (2 * x[1] + 1 * y[1]) / 3
        a2 = (1 * x[0] + 2 * y[0]) / 3
        b2 = (1 * x[1] + 2 * y[1]) / 3

        angle = math.radians(90)
        a3 = (a1 + a2) / 2 + (math.cos(angle) * (a2 - a1) / 2) - (math.sin(angle) * (b2 - b1) / 2)
        b3 = (b1 + b2) / 2 + (math.sin(angle) * (a2 - a1) / 2) + (math.cos(angle) * (b2 - b1) / 2)

        koch_curve(x, (a1, b1), depth - 1)
        koch_curve((a1, b1), (a3, b3), depth - 1)
        koch_curve((a3, b3), (a2, b2), depth - 1)
        koch_curve((a2, b2), y, depth - 1)

def render_koch(depth):
    glClear(GL_COLOR_BUFFER_BIT)
    

    cord_x = (45, 0)
    cord_y = (-45, 0)
    cord_z = (0, 90)
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 1.0, 1.0) 
    glVertex2f(*cord_x)
    glVertex2f(*cord_y)
    glVertex2f(*cord_z)
    glEnd()


    koch_curve(cord_x, cord_y, depth)
    koch_curve(cord_y, cord_z, depth)
    koch_curve(cord_z, cord_x, depth)
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

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    random_seed=random.randint(0, 100000000)
    
    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)
    

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        #render_rectangle()
        #render_rectangle_random(random_seed)
        #render_carpet(5)
        #render_koch(5)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()

if __name__ == '__main__':
    main()
