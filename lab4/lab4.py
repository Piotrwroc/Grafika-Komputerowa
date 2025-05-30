#!/usr/bin/env python3
from re import X
import sys
import math
from winreg import KEY_WOW64_32KEY

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


viewer = [0.0, 0.0, 10.0]

theta = 0.0
pix2angle = 1.0
phi = 0.0
piy2angle = 1.0
scale = 1.0
R = 10.0
move_object_mode = False
first_person_mode = False
key_w_pressed = False
key_s_pressed = False
key_a_pressed = False
key_d_pressed = False
camera_position = [0.0, 0.0, 0.0]
look_direction = [0.0, 0.0, -1.0]
up_vector = [0.0, 1.0, 0.0]
move_speed = 0.02
mouse_sensitivity = 0.1

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0

right_mouse_button_pressed = 0
mouse_y_pos_old = 0
delta_y = 0


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
    global theta, phi, scale, R, camera_position, look_direction

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if first_person_mode:

        if right_mouse_button_pressed:
            theta += delta_x * mouse_sensitivity
            phi -= delta_y * mouse_sensitivity

            # Ograniczenie kąta phi, aby nie wychodził poza zakres
            if phi > 90:
                phi = 90
            elif phi < -90:
                phi = -90

        # Oblicz kierunek patrzenia kamery (wektory x_look, y_look, z_look)
        x_look = math.cos(phi * math.pi / 180) * math.sin(theta * math.pi / 180)
        y_look = math.sin(phi * math.pi / 180)
        z_look = math.cos(phi * math.pi / 180) * math.cos(theta * math.pi / 180)

        look_direction = [x_look, y_look, z_look]

        # Oblicz wektor "prawo-lewo" względem kierunku patrzenia
        x_right = math.sin((theta + 90) * math.pi / 180)
        z_right = math.cos((theta + 90) * math.pi / 180)

        # Ustawienie kamery w trybie first-person
        gluLookAt(camera_position[0], camera_position[1], camera_position[2],
                camera_position[0] + look_direction[0],
                camera_position[1] + look_direction[1],
                camera_position[2] + look_direction[2],
                up_vector[0], up_vector[1], up_vector[2])

        # Ruch kamery w przód/tył wzdłuż osi Z
        if key_w_pressed:
            camera_position[0] += move_speed * x_look   # Ruch "do przodu" wzdłuż osi X
            camera_position[1] += move_speed * y_look   # Ruch "do przodu" wzdłuż osi Y
            camera_position[2] += move_speed * z_look   # Ruch "do przodu" wzdłuż osi Z

        if key_s_pressed:
            camera_position[0] -= move_speed * x_look   # Ruch "do tyłu" wzdłuż osi X
            camera_position[1] -= move_speed * y_look   # Ruch "do tyłu" wzdłuż osi Y
            camera_position[2] -= move_speed * z_look   # Ruch "do tyłu" wzdłuż osi Z

        # Ruch kamery w lewo/prawo (odpowiadający przesunięciu w osi X)
        if key_a_pressed:
            camera_position[0] += move_speed * x_right  # Ruch w lewo wzdłuż osi X
            camera_position[2] += move_speed * z_right  # Ruch w lewo wzdłuż osi Z

        if key_d_pressed:
            camera_position[0] -= move_speed * x_right  # Ruch w prawo wzdłuż osi X
            camera_position[2] -= move_speed * z_right  # Ruch w prawo wzdłuż osi Z

    elif move_object_mode:
        gluLookAt(viewer[0], viewer[1], viewer[2],     
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        if left_mouse_button_pressed:
            phi += delta_y * piy2angle  
        if right_mouse_button_pressed:
            theta += delta_x * pix2angle       
        glRotatef(theta, 0.0, 1.0, 0.0)    
        glRotatef(phi, 1.0, 0.0, 0.0)      
    else:   
        xeye = R * math.cos(phi * math.pi / 180) * math.sin(theta * math.pi / 180)
        yeye = R * math.sin(phi * math.pi / 180)
        zeye = R * math.cos(phi * math.pi / 180) * math.cos(theta * math.pi / 180)

        gluLookAt(xeye, yeye, zeye,     
                0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        if left_mouse_button_pressed:
            #theta += delta_x * pix2angle   #przykład
            #phi += delta_y * piy2angle     #zad 1
            R += delta_y * 0.1              
            if R < 2.0:         # Ograniczenie zasiegu oddalenia
                R = 2.0
            elif R > 50.0:
               R = 50    

        if right_mouse_button_pressed:
            #scale += delta_y * 0.01         #zad 2
            theta += delta_x * pix2angle
            phi += delta_y - piy2angle
            if phi> 90: 
                phi = 90
            elif phi <-90: 
                phi = -90  

    #glScalef(scale, scale, scale)      #zad 2
    #glRotatef(theta, 0.0, 1.0, 0.0)    #przykład
    #glRotatef(phi, 1.0, 0.0, 0.0)      #zad 1

    axes()
    example_object()

    glFlush()

   

def update_viewport(window, width, height):
    global pix2angle
    global piy2angle
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
    global move_object_mode, first_person_mode, key_w_pressed, key_s_pressed, key_a_pressed, key_d_pressed
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_SPACE and action == GLFW_PRESS:   
        move_object_mode = not move_object_mode
    if key == GLFW_KEY_ENTER and action == GLFW_PRESS:   
        first_person_mode = not first_person_mode    

    if key == GLFW_KEY_W:
        key_w_pressed = action in (GLFW_PRESS, GLFW_REPEAT)
    if key == GLFW_KEY_S:
        key_s_pressed = action in (GLFW_PRESS, GLFW_REPEAT)
    if key == GLFW_KEY_A:
        key_a_pressed = action in (GLFW_PRESS, GLFW_REPEAT)
    if key == GLFW_KEY_D:
        key_d_pressed = action in (GLFW_PRESS, GLFW_REPEAT)     


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
