
import math
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image

N = 100

viewer = [0.0, 0.0, 10.0]

theta = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

current_texture = 0
textures = []

def load_texture(filename):
    try:
        image = Image.open(filename)
        image = image.convert("RGB")
        width, height = image.size
        data = image.tobytes("raw", "RGB", 0, -1)
        return width, height, data
    except FileNotFoundError:
        print(f"Error: Texture file '{filename}' not found.")
        sys.exit(1)  # Exit the program if the file isn't found

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

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_TEXTURE_2D)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR) # Dodano mipmapowanie dla lepszej jakości
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    textures.append(load_texture("tekstura.tga"))
    textures.append(load_texture("rat.tga"))

    switch_texture() # Inicjalizacja tekstury

def switch_texture():
    global current_texture
    current_texture = (current_texture + 1) % len(textures)
    width, height, data = textures[current_texture]
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
    # Generowanie mipmap
    glGenerateMipmap(GL_TEXTURE_2D)

def calculate_egg_points():
    points = [[[0.0, 0.0, 0.0] for _ in range(N)] for _ in range(N)]
    for i in range(N):
        u = i / (N - 1)
        for j in range(N):
            v = j / (N - 1)
            x = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.cos(math.pi * v)
            y = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5
            z = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.sin(math.pi * v)
            points[i][j] = [x, y, z]
    return points

def calculate_normals(points):
    normals = [[[0.0, 0.0, 0.0] for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            # Obliczanie wektorów stycznych i normalnych (uproszczone)
            u = i / (N - 1)
            v = j / (N - 1)

            # Pochodne cząstkowe (przybliżone)
            du_x = (-450 * u**4 + 900 * u**3 - 810 * u**2 + 360 * u - 45) * math.cos(math.pi * v)
            du_y = 640 * u**3 - 960 * u**2 + 320 * u
            du_z = (-450 * u**4 + 900 * u**3 - 810 * u**2 + 360 * u - 45) * math.sin(math.pi * v)

            dv_x = -math.pi * (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.sin(math.pi * v)
            dv_y = 0.0
            dv_z = math.pi * (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.cos(math.pi * v)

            # Iloczyn wektorowy (wektor normalny)
            nx = du_y * dv_z - du_z * dv_y
            ny = du_z * dv_x - du_x * dv_z
            nz = du_x * dv_y - du_y * dv_x

            # Normalizacja
            length = math.sqrt(nx**2 + ny**2 + nz**2)
            if length > 0:
                nx /= length
                ny /= length
                nz /= length

            normals[i][j] = [nx, ny, nz]
    return normals

def draw_egg_with_texture():
    points = calculate_egg_points()
    normals = calculate_normals(points)

    for i in range(N - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            s = j / (N - 1)
            t = i / (N - 1)

            glNormal3fv(normals[i][j])
            glTexCoord2f(s, t)
            glVertex3fv(points[i][j])

            glNormal3fv(normals[i + 1][j])
            glTexCoord2f(s, t + 1/(N-1))
            glVertex3fv(points[i + 1][j])
        glEnd()



def shutdown():
    pass


def render(time):
    global theta

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)

    # Przykład
    """"" 
    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-5.0, -5.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(5.0, -5.0, 0.0)
    glTexCoord2f(0.5, 1.0)
    glVertex3f(0.0, 5.0, 0.0)
    glEnd()
    """""
    # zad1
    """""
    glBegin(GL_TRIANGLES)
    
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-5.0, -5.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(5.0, -5.0, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-5.0, 5.0, 0.0)

    glTexCoord2f(1.0, 0.0)
    glVertex3f(5.0, -5.0, 0.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(5.0, 5.0, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-5.0, 5.0, 0.0)
    glEnd()
    """""

    # Zad2
    """""
    # Podstawa ostrosłupa 
    glBegin(GL_TRIANGLES)

    glTexCoord2f(0.0, 0.0)
    glVertex3f(-5.0, -5.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(5.0, -5.0, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-5.0, 5.0, 0.0)

    glTexCoord2f(1.0, 0.0)
    glVertex3f(5.0, -5.0, 0.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(5.0, 5.0, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-5.0, 5.0, 0.0)
    glEnd()

    # Wierzchołek ostrosłupa
    apex = (0.0, 0.0, 7.0)

    # Ściany trójkątne
    faces = [
        ((-5.0, -5.0, 0.0), (5.0, -5.0, 0.0)),  # Front
        ((5.0, -5.0, 0.0), (5.0, 5.0, 0.0)),   # Right
        ((5.0, 5.0, 0.0), (-5.0, 5.0, 0.0)),   # Back
        ((-5.0, 5.0, 0.0), (-5.0, -5.0, 0.0))  # Left
    ]

    for i, (v1, v2) in enumerate(faces):
        if show_face[i]:  
            glBegin(GL_TRIANGLES)
            glTexCoord2f(0.5, 0.5)
            glVertex3f(*apex)
            glTexCoord2f(0.0 if i % 2 == 0 else 1.0, 0.0)
            glVertex3f(*v1)
            glTexCoord2f(1.0 if i % 2 == 0 else 0.0, 0.0)
            glVertex3f(*v2)
            glEnd()
    """""
            
    # zad5
    draw_egg_with_texture()
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
    global show_face
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_SPACE and action == GLFW_PRESS:
        show_face[0] = not show_face[0]
    if key == GLFW_KEY_ENTER and action == GLFW_PRESS:
        switch_texture()
    
def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


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