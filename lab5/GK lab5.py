#!/usr/bin/env python3
import math
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


viewer = [0.0, 0.0, 10.0]

theta = 0.0
pix2angle = 1.0
phi = 0.0
piy2angle = 1.0

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0
mouse_y_pos_old = 0
delta_y = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

light_ambient2 = [0.3, 0.3, 0.0, 1.0]   #zad1
light_diffuse2 = [0.0, 1.0, 0.7, 0.7]   #
light_specular2 = [0.5, 0.5, 0.5, 0.5]  #
light_position2 = [0.0, 10.0, 0.0, 1.0] #

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

current_component = 0  # 0 - ambient, 1 - diffuse, 2 - specular
key_up_pressed = False
key_down_pressed = False

R = 15.0
xs, ys, zs = 0.0, 0.0, 0.0

N = 50

show_normals = False

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    #glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient2)   #zad1
    #glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse2)   #
    #glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular2) #
    #glLightfv(GL_LIGHT1, GL_POSITION, light_position2) #

    #glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    #glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    #glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

def update_light():
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

def modify_light(component, index, delta):
    component[index] = max(0.0, min(1.0, component[index] + delta))
    print(f"Ambient: {light_ambient[:3]}, Diffuse: {light_diffuse[:3]}, Specular: {light_specular[:3]}")

def update_light_position():
    global light_position, xs, ys, zs
    light_position = [xs, ys, zs, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)    

def calculate_egg_points():
    tab = [[[0.0, 0.0, 0.0] for _ in range(N)] for _ in range(N)]
    for i in range(N):
        u = i / (N - 1)
        for j in range(N):
            v = j / (N - 1)
            x = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.cos(math.pi * v)
            y = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5
            z = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.sin(math.pi * v)
            tab[i][j] = [x, y, z]
    return tab

def calculate_normals(points):
    normals = [[[0.0, 0.0, 0.0] for _ in range(N)] for _ in range(N)]
    for i in range(N):
        u = i / (N - 1)
        for j in range(N):
            v = j / (N - 1)

            # Pochodne powierzchni po u i v
            xu = -450 * u**4 + 900 * u**3 - 810 * u**2 + 360 * u - 45
            yu = 640 * u**3 - 960 * u**2 + 320 * u
            zu = (-450 * u**4 + 900 * u**3 - 810 * u**2 + 360 * u - 45) * math.sin(math.pi * v)

            xv = math.pi * (90 * u**5 - 225 * u**4 + 270 * u**3 - 180 * u**2 + 45 * u) * math.sin(math.pi * v)
            yv = 0
            zv = -math.pi * (90 * u**5 - 225 * u**4 + 270 * u**3 - 180 * u**2 + 45 * u) * math.cos(math.pi * v)

            # Wektor normalny jako iloczyn wektorowy
            nx = yu * zv - zu * yv
            ny = zu * xv - xu * zv
            nz = xu * yv - yu * xv

            # Normalizacja wektora
            length = math.sqrt(nx**2 + ny**2 + nz**2)
            if length != 0:
                nx /= length
                ny /= length
                nz /= length

            # Odwracanie normalnych na drugiej połówce modelu
            
            if i > N // 2:
                nx *= -1
                ny *= -1
                nz *= -1
            
            # Zapis normalnej
            normals[i][j] = [nx, ny, nz]
    return normals

def draw_egg_triangle_strip(show_normals):
    points = calculate_egg_points()
    normals = calculate_normals(points)
    glColor3f(1.0, 1.0, 0.0)  # Kolor żółty dla jajka

    for i in range(N - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            # Górny wierzchołek            
            glNormal3fv(normals[i][j]) 
            glVertex3fv(points[i][j])

            # Dolny wierzchołek
            glNormal3fv(normals[i + 1][j])
            glVertex3fv(points[i + 1][j])
        glEnd()

    if show_normals:
        glColor3f(1.0, 0.0, 0.0)  # Czerwony kolor dla normalnych
        glBegin(GL_LINES)
        for i in range(N):
            for j in range(N):
                # Punkt początkowy (wierzchołek)
                glVertex3fv(points[i][j])
                # Punkt końcowy (wierzchołek + normalna)
                normal_endpoint = [
                    points[i][j][0] + normals[i][j][0],
                    points[i][j][1] + normals[i][j][1],
                    points[i][j][2] + normals[i][j][2],
                ]
                glVertex3fv(normal_endpoint)
        glEnd()

def shutdown():
    pass


def render(time):
    global theta, phi, xs, ys, zs, current_component, R, show_normals

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    
    

    if left_mouse_button_pressed:
        phi += delta_y * piy2angle
    if right_mouse_button_pressed:
        theta += delta_x * pix2angle    
    
    xs = R * math.cos(theta * math.pi / 180) * math.cos(phi * math.pi / 180)
    ys = R * math.sin(phi * math.pi / 180)
    zs = R * math.sin(theta * math.pi / 180) * math.cos(phi * math.pi / 180)
    update_light_position()

    
    if key_up_pressed:
        if current_component == 0:
            modify_light(light_ambient, 0, 0.1)
        elif current_component == 1:
            modify_light(light_diffuse, 0, 0.1)
        elif current_component == 2:
            modify_light(light_specular, 0, 0.1)
        update_light()
    elif key_down_pressed:
        if current_component == 0:
            modify_light(light_ambient, 0, -0.1)
        elif current_component == 1:
            modify_light(light_diffuse, 0, -0.1)
        elif current_component == 2:
            modify_light(light_specular, 0, -0.1)
        update_light()
     

    #glRotatef(theta, 0.0, 1.0, 0.0)
    
   
    glPushMatrix()
    glTranslate(xs, ys, zs)
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric
    glPopMatrix()


    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)
    

    draw_egg_triangle_strip(show_normals)
    glFlush()


def update_viewport(window, width, height):
    global pix2angle, piy2angle
    pix2angle = 360.0 / width
    piy2angle = 360.0 / height

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
    global key_up_pressed, key_down_pressed, current_component, show_normals

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_Q and action == GLFW_PRESS:   
       current_component = 0
       print("Changing ambient component")
    if key == GLFW_KEY_W and action == GLFW_PRESS:   
       current_component = 1  
       print("Changing diffuse component")
    if key == GLFW_KEY_E and action == GLFW_PRESS:   
       current_component = 2      
       print("Changing specular component")

    if key == GLFW_KEY_UP and (action ==GLFW_PRESS or GLFW_REPEAT):    
        key_up_pressed = action == GLFW_PRESS
    if key == GLFW_KEY_DOWN and (action ==GLFW_PRESS or GLFW_REPEAT):    
        key_down_pressed = action == GLFW_PRESS
 
    if key == GLFW_KEY_SPACE and action == GLFW_PRESS:
        show_normals = not show_normals 
      


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old
    global delta_y
    global mouse_y_pos_old

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

    window = glfwCreateWindow(400, 400, __file__, None, None)
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
