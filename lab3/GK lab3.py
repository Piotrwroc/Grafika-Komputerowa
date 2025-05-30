#!/usr/bin/env python3
import sys
import numpy as np
import random
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

N = 50

#zad1

def calculate_egg_points():
    tab = np.zeros((N, N, 3))
    u = np.linspace(0.0, 1.0, N)
    v = np.linspace(0.0, 1.0, N)
    for i in range(N):
        for j in range(N):
            u_val = u[i]
            v_val = v[j]
            
            x = (-90 * u_val**5 + 225 * u_val**4 - 270 * u_val**3 + 180 * u_val**2 - 45 * u_val) * np.cos(np.pi * v_val)
            y = 160 * u_val**4 - 320 * u_val**3 + 160 * u_val**2 - 5
            z = (-90 * u_val**5 + 225 * u_val**4 - 270 * u_val**3 + 180 * u_val**2 - 45 * u_val) * np.sin(np.pi * v_val)
            tab[i][j] = [x, y, z]

    return tab

def draw_egg():
    tab = calculate_egg_points()
    glColor3f(1.0, 1.0, 0.0) # Kolor żółty 

    glBegin(GL_POINTS)
    for i in range(N):
        for j in range(N):
            glVertex3fv(tab[i][j])
    glEnd()
            
#zad2

def draw_egg_lines():
    tab = calculate_egg_points()
    glColor3f(1.0, 1.0, 0.0) # Kolor żółty 
    glBegin(GL_POINTS)
    for i in range(N):
        for j in range(N):
            glVertex3fv(tab[i][j])
    glEnd()
    glBegin(GL_LINES)
    for i in range (N-1):
        for j in range(N-1):
            glVertex3fv(tab[i][j])
            glVertex3fv(tab[i][j+1])
            
            glVertex3fv(tab[i][j])
            glVertex3fv(tab[i+1][j])
    for i in range (N-1):
        glVertex3fv(tab[i][N-1])
        glVertex3fv(tab[i+1][N-1])
    for j in range (N-1):    
        glVertex3fv(tab[N-1][j])
        glVertex3fv(tab[N-1][j+1])        
    glEnd()

#zad3

def draw_egg_triangles(random_seed):
    random.seed(random_seed)
    tab = calculate_egg_points()
    glBegin(GL_TRIANGLES)
    

    for i in range(N - 1):
        for j in range(N - 1):
            glColor3f(random.random(), random.random(), random.random())
            glVertex3fv(tab[i][j]) 
            glColor3f(random.random(), random.random(), random.random())
            glVertex3fv(tab[i][j + 1]) 
            glColor3f(random.random(), random.random(), random.random())
            glVertex3fv(tab[i + 1][j]) 

            glColor3f(random.random(), random.random(), random.random())
            glVertex3fv(tab[i + 1][j]) 
            glColor3f(random.random(), random.random(), random.random())
            glVertex3fv(tab[i][j + 1]) 
            glColor3f(random.random(), random.random(), random.random())
            glVertex3fv(tab[i + 1][j + 1])

    glEnd()   

#zad4
def draw_egg_triangle_strip(random_seed):
    random.seed(random_seed)
    tab = calculate_egg_points()

    for i in range(N - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            glColor3f(random.random(), random.random(), random.random())
            glVertex3fv(tab[i][j]) # Wierzchołek z aktualnego wiersza
            glColor3f(random.random(), random.random(), random.random())
            glVertex3fv(tab[i + 1][j]) # Wierzchołek z następnego wiersza
        glEnd()

#zad5
def draw_sierpinski_pyramid(vertices, depth):
    glColor3f(1.0, 1.0, 0.0) # Kolor żółty 
    if depth == 0:
        glBegin(GL_TRIANGLES)
        
        # Rysowanie czterech ścian piramidy
        glVertex3fv(vertices[0])
        glVertex3fv(vertices[1])
        glVertex3fv(vertices[2])
        
        glVertex3fv(vertices[0])
        glVertex3fv(vertices[1])
        glVertex3fv(vertices[3])
        
        glVertex3fv(vertices[1])
        glVertex3fv(vertices[2])
        glVertex3fv(vertices[3])
        
        glVertex3fv(vertices[0])
        glVertex3fv(vertices[2])
        glVertex3fv(vertices[3])
         
        glEnd()
    else:
        # Obliczanie punktów środkowych
        mid_points = [
            (vertices[0] + vertices[1]) / 2,
            (vertices[1] + vertices[2]) / 2,
            (vertices[2] + vertices[0]) / 2,
            (vertices[0] + vertices[3]) / 2,
            (vertices[1] + vertices[3]) / 2,
            (vertices[2] + vertices[3]) / 2
        ]
        
        # Tworzenie nowych wierzchołków 
        new_vertices = [
            vertices[0],        # Wierzchołek główny
            mid_points[0],      # Środek między vertices[0] i vertices[1]
            mid_points[1],      # Środek między vertices[1] i vertices[2]
            mid_points[3],      # Środek między vertices[0] i vertices[3]
            mid_points[2]       # Środek między vertices[2] i vertices[0]
        ]
        
        # Rekurencyjne rysowanie mniejszych piramid
        draw_sierpinski_pyramid([vertices[0], mid_points[0], mid_points[2], mid_points[3]], depth - 1)
        draw_sierpinski_pyramid([mid_points[0], vertices[1], mid_points[1], mid_points[4]], depth - 1)
        draw_sierpinski_pyramid([mid_points[2], mid_points[1], vertices[2], mid_points[5]], depth - 1)
        draw_sierpinski_pyramid([mid_points[3], mid_points[4], mid_points[5], vertices[3]], depth - 1)

def spin(angle):
	glRotatef(angle, 1.0, 0.0, 0.0)
	glRotatef(angle, 0.0, 1.0, 0.0)
	glRotatef(angle, 0.0, 0.0, 1.0)

def startup():
    update_viewport(None, 400, 400)
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


def render(time, random_seed):

    vertices = np.array([
    [0.0, 4.0, 0.0], # Wierzchołek
    [-5.0, 0.0, 5.0], # Wierzchołek podstawy
    [5.0, 0.0, 5.0], # Wierzchołek podstawy
    [5.0, 0.0, -5.0], # Wierzchołek podstawy
    [-5.0, 0.0, -5.0] # Wierzchołek podstawy
    ], dtype=np.float32)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time * 180 / 3.1415)
    axes()
    #draw_egg()
    #draw_egg_lines()
    #draw_egg_triangles(random_seed)
    #draw_egg_triangle_strip(random_seed)
    draw_sierpinski_pyramid(vertices, 3)
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
        render(glfwGetTime(), random_seed)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
