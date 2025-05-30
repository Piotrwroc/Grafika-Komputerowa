#!/usr/bin/env python3

import ctypes
import sys

from glfw.GLFW import *
import glm
import numpy

from OpenGL.GL import *
from OpenGL.GLU import *

rendering_program = None
vertex_array_object = None
vertex_buffer = None

#P_matrix = None
global P_matrix

aspect_ratio = 400 / 400  # Dopasuj do rozmiaru okna (szerokość / wysokość)
fov = 45.0  # Kąt widzenia (Field of View)
near_plane = 0.1  # Bliska płaszczyzna
far_plane = 100.0  # Daleka płaszczyzna

P_matrix = glm.perspective(glm.radians(fov), aspect_ratio, near_plane, far_plane)

# # zad1
# def compile_shaders():
#     vertex_shader_source = """
#         #version 330 core
#
#         layout(location = 0) in vec4 position;
#
#         uniform mat4 M_matrix;
#         uniform mat4 V_matrix;
#         uniform mat4 P_matrix;
#
#         out vec4 vertex_color;
#
#         void main(void) {
#             gl_Position = P_matrix * V_matrix * M_matrix * position;
#             vertex_color = vec4(0.2, 0.9, 0.1, 1.0); // #zad1 Zielony kolor
#         }
#     """
#
#     fragment_shader_source = """
#        #version 330 core
#
#         in vec4 vertex_color;
#         out vec4 color;
#
#         void main(void) {
#             color = vertex_color; // #zad1 Przypisanie koloru przekazanego z shadera wierzchołków
#         }
#     """

# # zad2-3
# def compile_shaders():
#     vertex_shader_source = """
#         #version 330 core
#         layout(location = 0) in vec4 position;
#         layout(location = 1) in vec3 color;
#
#         uniform mat4 M_matrix;
#         uniform mat4 V_matrix;
#         uniform mat4 P_matrix;
#
#         out vec3 vertex_color;
#
#         void main(void) {
#             gl_Position = P_matrix * V_matrix * M_matrix * position;
#             vertex_color = color; // Przekazanie koloru do shadera fragmentów
#         }
#     """
#
#     fragment_shader_source = """
#         #version 330 core
#         in vec3 vertex_color;
#         out vec4 color;
#
#         void main(void) {
#             color = vec4(vertex_color, 1.0); // Użycie koloru z shadera wierzchołków
#         }
# #     """
#
#     vertex_shader = glCreateShader(GL_VERTEX_SHADER)
#     glShaderSource(vertex_shader, [vertex_shader_source])
#     glCompileShader(vertex_shader)
#     success = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS)
#
#     if not success:
#         print('Shader compilation error:')
#         print(glGetShaderInfoLog(vertex_shader).decode('UTF-8'))
#
#     fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
#     glShaderSource(fragment_shader, [fragment_shader_source])
#     glCompileShader(fragment_shader)
#     success = glGetShaderiv(fragment_shader, GL_COMPILE_STATUS)
#
#     if not success:
#         print('Shader compilation error:')
#         print(glGetShaderInfoLog(fragment_shader).decode('UTF-8'))
#
#     program = glCreateProgram()
#     glAttachShader(program, vertex_shader)
#     glAttachShader(program, fragment_shader)
#     glLinkProgram(program)
#     success = glGetProgramiv(program, GL_LINK_STATUS)
#
#     if not success:
#         print('Program linking error:')
#         print(glGetProgramInfoLog(program).decode('UTF-8'))
#
#     glDeleteShader(vertex_shader)
#     glDeleteShader(fragment_shader)
#
#     return program

#zad 4
# def compile_shaders():
#     vertex_shader_source = """
#         #version 330 core
#
# layout(location = 0) in vec4 position;
# layout(location = 1) in vec4 color;
#
# out vec4 vertex_color;
#
# uniform mat4 V_matrix;
# uniform mat4 P_matrix;
# uniform float time;
#
# mat4 rotate(mat4 matrix, float angle, vec3 axis) {
#     float c = cos(angle);
#     float s = sin(angle);
#     float t = 1.0 - c;
#
#     vec3 a = normalize(axis);
#
#     mat4 rot = mat4(
#         vec4(t*a.x*a.x + c,     t*a.x*a.y + s*a.z, t*a.x*a.z - s*a.y, 0.0),
#         vec4(t*a.x*a.y - s*a.z, t*a.y*a.y + c,     t*a.y*a.z + s*a.x, 0.0),
#         vec4(t*a.x*a.z + s*a.y, t*a.y*a.z - s*a.x, t*a.z*a.z + c,     0.0),
#         vec4(0.0,               0.0,               0.0,                 1.0)
#     );
#
#     return rot * matrix;
# }
#
#
# void main(void) {
#     // Obliczanie transformacji na podstawie gl_InstanceID
#     int x = gl_InstanceID % 10 - 5;  // Pozycja X (od -5 do 4)
#     int y = gl_InstanceID / 10 - 5;  // Pozycja Y (od -5 do 4)
#
#     mat4 translation = mat4(1.0);
#     translation[3] = vec4(x, y, 0.0, 1.0);
#
#     mat4 rotation = rotate(mat4(1.0), time, vec3(1.0, 1.0, 0.0));
#     mat4 M_matrix = translation * rotation;
#     gl_Position = P_matrix * V_matrix * M_matrix * position;
#     vertex_color = color;
# }
#     """
#
#     fragment_shader_source = """
#         #version 330 core
#
#         in vec4 vertex_color;
#         out vec4 color;
#
#         void main(void) {
#             color = vertex_color;
#         }
#     """
#
#     vertex_shader = glCreateShader(GL_VERTEX_SHADER)
#     glShaderSource(vertex_shader, [vertex_shader_source])
#     glCompileShader(vertex_shader)
#     success = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS)
#
#     if not success:
#         print('Shader compilation error:')
#         print(glGetShaderInfoLog(vertex_shader).decode('UTF-8'))
#
#     fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
#     glShaderSource(fragment_shader, [fragment_shader_source])
#     glCompileShader(fragment_shader)
#     success = glGetShaderiv(fragment_shader, GL_COMPILE_STATUS)
#
#     if not success:
#         print('Shader compilation error:')
#         print(glGetShaderInfoLog(fragment_shader).decode('UTF-8'))
#
#     program = glCreateProgram()
#     glAttachShader(program, vertex_shader)
#     glAttachShader(program, fragment_shader)
#     glLinkProgram(program)
#     success = glGetProgramiv(program, GL_LINK_STATUS)
#
#     if not success:
#         print('Program linking error:')
#         print(glGetProgramInfoLog(program).decode('UTF-8'))
#
#     glDeleteShader(vertex_shader)
#     glDeleteShader(fragment_shader)
#
#     return program

#zad5
def compile_shaders():
    vertex_shader_source = """
        #version 330 core

        layout(location = 0) in vec4 position;
        layout(location = 1) in vec4 color;

        out vec4 vertex_color;

        uniform mat4 V_matrix;
        uniform mat4 P_matrix;
        uniform float time;

        // Pseudo-random number generator (Xorshift)
        uint xorshift(inout uint state) {
            state ^= state << 13;
            state ^= state >> 7;
            state ^= state << 17;
            return state;
        }

        mat4 rotate(mat4 matrix, float angle, vec3 axis) {
            float c = cos(angle);
            float s = sin(angle);
            float t = 1.0 - c;

            vec3 a = normalize(axis);

            mat4 rot = mat4(
                vec4(t*a.x*a.x + c,     t*a.x*a.y + s*a.z, t*a.x*a.z - s*a.y, 0.0),
                vec4(t*a.x*a.y - s*a.z, t*a.y*a.y + c,     t*a.y*a.z + s*a.x, 0.0),
                vec4(t*a.x*a.z + s*a.y, t*a.y*a.z - s*a.x, t*a.z*a.z + c,     0.0),
                vec4(0.0,               0.0,               0.0,                 1.0)
            );

            return rot * matrix; 
        }

        void main(void) {
            int x = gl_InstanceID % 10 - 5;
            int y = gl_InstanceID / 10 - 5;

            mat4 translation = mat4(1.0);
            translation[3] = vec4(x, y, 0.0, 1.0);

            mat4 rotation = rotate(mat4(1.0), time, vec3(1.0, 1.0, 0.0));
            mat4 M_matrix = translation * rotation;

            // Deformations based on gl_VertexID and gl_InstanceID
            uint instanceID = uint(gl_InstanceID); // Explicit cast to uint
            uint vertexID = uint(gl_VertexID);     // Explicit cast to uint
            uint state = instanceID * 100u + vertexID; // 'u' suffix for unsigned literal

            float randomX = float(xorshift(state)) / 4294967295.0 * 0.2 - 0.1; // Range -0.1 to 0.1
            float randomY = float(xorshift(state)) / 4294967295.0 * 0.2 - 0.1;
            float randomZ = float(xorshift(state)) / 4294967295.0 * 0.2 - 0.1;


            vec4 deformedPosition = position + vec4(randomX, randomY, randomZ, 0.0);

            gl_Position = P_matrix * V_matrix * M_matrix * deformedPosition;
            vertex_color = color;
        }
    """

    fragment_shader_source = """
        #version 330 core

        in vec4 vertex_color;
        out vec4 color;

        void main(void) {
            color = vertex_color;
        }
    """

    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader, [vertex_shader_source])
    glCompileShader(vertex_shader)
    success = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS)

    if not success:
        print('Shader compilation error:')
        print(glGetShaderInfoLog(vertex_shader).decode('UTF-8'))

    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader, [fragment_shader_source])
    glCompileShader(fragment_shader)
    success = glGetShaderiv(fragment_shader, GL_COMPILE_STATUS)

    if not success:
        print('Shader compilation error:')
        print(glGetShaderInfoLog(fragment_shader).decode('UTF-8'))

    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)
    success = glGetProgramiv(program, GL_LINK_STATUS)

    if not success:
        print('Program linking error:')
        print(glGetProgramInfoLog(program).decode('UTF-8'))

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return program


#zad 1
# def startup():
#     global rendering_program
#     global vertex_array_object
#     global vertex_buffer
#
#     print("OpenGL {}, GLSL {}\n".format(
#         glGetString(GL_VERSION).decode('UTF-8').split()[0],
#         glGetString(GL_SHADING_LANGUAGE_VERSION).decode('UTF-8').split()[0]
#     ))
#
#     update_viewport(None, 400, 400)
#     glEnable(GL_DEPTH_TEST)
#
#     rendering_program = compile_shaders()
#
#     vertex_array_object = glGenVertexArrays(1)
#     glBindVertexArray(vertex_array_object)
#
#     vertex_positions = numpy.array([
#         -0.25, +0.25, -0.25,
#         -0.25, -0.25, -0.25,
#         +0.25, -0.25, -0.25,
#
#         +0.25, -0.25, -0.25,
#         +0.25, +0.25, -0.25,
#         -0.25, +0.25, -0.25,
#
#         +0.25, -0.25, -0.25,
#         +0.25, -0.25, +0.25,
#         +0.25, +0.25, -0.25,
#
#         +0.25, -0.25, +0.25,
#         +0.25, +0.25, +0.25,
#         +0.25, +0.25, -0.25,
#
#         +0.25, -0.25, +0.25,
#         -0.25, -0.25, +0.25,
#         +0.25, +0.25, +0.25,
#
#         -0.25, -0.25, +0.25,
#         -0.25, +0.25, +0.25,
#         +0.25, +0.25, +0.25,
#
#         -0.25, -0.25, +0.25,
#         -0.25, -0.25, -0.25,
#         -0.25, +0.25, +0.25,
#
#         -0.25, -0.25, -0.25,
#         -0.25, +0.25, -0.25,
#         -0.25, +0.25, +0.25,
#
#         -0.25, -0.25, +0.25,
#         +0.25, -0.25, +0.25,
#         +0.25, -0.25, -0.25,
#
#         +0.25, -0.25, -0.25,
#         -0.25, -0.25, -0.25,
#         -0.25, -0.25, +0.25,
#
#         -0.25, +0.25, -0.25,
#         +0.25, +0.25, -0.25,
#         +0.25, +0.25, +0.25,
#
#         +0.25, +0.25, +0.25,
#         -0.25, +0.25, +0.25,
#         -0.25, +0.25, -0.25,
#     ], dtype='float32')
#
#     vertex_buffer = glGenBuffers(1)
#     glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
#     glBufferData(GL_ARRAY_BUFFER, vertex_positions, GL_STATIC_DRAW)
#
#     glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
#     glEnableVertexAttribArray(0)

# #zad2-5
def startup():
    global rendering_program, vertex_array_object, vertex_buffer, color_buffer

    rendering_program = compile_shaders()

    vertex_array_object = glGenVertexArrays(1)
    glBindVertexArray(vertex_array_object)

    vertex_positions = numpy.array([
        # Tył sześcianu (Czerwony)
        -0.25, +0.25, -0.25,  # 0
        -0.25, -0.25, -0.25,  # 1
        +0.25, -0.25, -0.25,  # 2
        +0.25, -0.25, -0.25,  # 2
        +0.25, +0.25, -0.25,  # 3
        -0.25, +0.25, -0.25,  # 0

        # Prawa ściana (Zielony)
        +0.25, -0.25, -0.25,  # 2
        +0.25, -0.25, +0.25,  # 6
        +0.25, +0.25, -0.25,  # 3
        +0.25, -0.25, +0.25,  # 6
        +0.25, +0.25, +0.25,  # 7
        +0.25, +0.25, -0.25,  # 3

        # Przód (Niebieski)
        +0.25, -0.25, +0.25,  # 6
        -0.25, -0.25, +0.25,  # 4
        +0.25, +0.25, +0.25,  # 7
        -0.25, -0.25, +0.25,  # 4
        -0.25, +0.25, +0.25,  # 5
        +0.25, +0.25, +0.25,  # 7

        # Lewa ściana (Żółty)
        -0.25, -0.25, +0.25,  # 4
        -0.25, -0.25, -0.25,  # 1
        -0.25, +0.25, +0.25,  # 5
        -0.25, -0.25, -0.25,  # 1
        -0.25, +0.25, -0.25,  # 0
        -0.25, +0.25, +0.25,  # 5

        # Dół (Różowy)
        -0.25, -0.25, +0.25,  # 4
        +0.25, -0.25, +0.25,  # 6
        +0.25, -0.25, -0.25,  # 2
        +0.25, -0.25, -0.25,  # 2
        -0.25, -0.25, -0.25,  # 1
        -0.25, -0.25, +0.25,  # 4

        # Góra (Fioletowy)
        -0.25, +0.25, -0.25,  # 0
        +0.25, +0.25, -0.25,  # 3
        +0.25, +0.25, +0.25,  # 7
        +0.25, +0.25, +0.25,  # 7
        -0.25, +0.25, +0.25,  # 5
        -0.25, +0.25, -0.25,  # 0
    ], dtype='float32')

    vertex_colors = numpy.array([
        # Tył (Czerwony)
        1.0, 0.0, 0.0,  # 0
        1.0, 0.0, 0.0,  # 1
        1.0, 0.0, 0.0,  # 2
        1.0, 0.0, 0.0,  # 2
        1.0, 0.0, 0.0,  # 3
        1.0, 0.0, 0.0,  # 0

        # Prawa ściana (Zielony)
        0.0, 1.0, 0.0,  # 2
        0.0, 1.0, 0.0,  # 6
        0.0, 1.0, 0.0,  # 3
        0.0, 1.0, 0.0,  # 6
        0.0, 1.0, 0.0,  # 7
        0.0, 1.0, 0.0,  # 3

        # Przód (Niebieski)
        0.0, 0.0, 1.0,  # 6
        0.0, 0.0, 1.0,  # 4
        0.0, 0.0, 1.0,  # 7
        0.0, 0.0, 1.0,  # 4
        0.0, 0.0, 1.0,  # 5
        0.0, 0.0, 1.0,  # 7

        # Lewa ściana (Żółty)
        1.0, 1.0, 0.0,  # 4
        1.0, 1.0, 0.0,  # 1
        1.0, 1.0, 0.0,  # 5
        1.0, 1.0, 0.0,  # 1
        1.0, 1.0, 0.0,  # 0
        1.0, 1.0, 0.0,  # 5

        # Dół (Różowy)
        1.0, 0.0, 1.0,  # 4
        1.0, 0.0, 1.0,  # 6
        1.0, 0.0, 1.0,  # 2
        1.0, 0.0, 1.0,  # 2
        1.0, 0.0, 1.0,  # 1
        1.0, 0.0, 1.0,  # 4

        # Góra (Fioletowy)
        0.5, 0.0, 1.0,  # 0
        0.5, 0.0, 1.0,  # 3
        0.5, 0.0, 1.0,  # 7
        0.5, 0.0, 1.0,  # 7
        0.5, 0.0, 1.0,  # 5
        0.5, 0.0, 1.0,  # 0
    ], dtype='float32')

    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(GL_ARRAY_BUFFER, vertex_positions, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    # Włącz test głębi
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    # Kolory
    color_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
    glBufferData(GL_ARRAY_BUFFER, vertex_colors, GL_STATIC_DRAW)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
    glEnableVertexAttribArray(1)

def shutdown():
    global rendering_program
    global vertex_array_object
    global vertex_buffer

    glDeleteProgram(rendering_program)
    glDeleteVertexArrays(1, vertex_array_object)
    glDeleteBuffers(1, vertex_buffer)

# zad 1-2
# def render(time):
#     glClearBufferfv(GL_COLOR, 0, [0.0, 0.0, 0.0, 1.0])
#     glClearBufferfi(GL_DEPTH_STENCIL, 0, 1.0, 0)
#
#     M_matrix = glm.rotate(glm.mat4(1.0), time, glm.vec3(1.0, 1.0, 0.0))
#
#     V_matrix = glm.lookAt(
#         glm.vec3(0.0, 0.0, 1.0),
#         glm.vec3(0.0, 0.0, 0.0),
#         glm.vec3(0.0, 1.0, 0.0)
#     )
#
#     glUseProgram(rendering_program)
#
#     M_location = glGetUniformLocation(rendering_program, "M_matrix")
#     V_location = glGetUniformLocation(rendering_program, "V_matrix")
#     P_location = glGetUniformLocation(rendering_program, "P_matrix")
#
#     glUniformMatrix4fv(M_location, 1, GL_FALSE, glm.value_ptr(M_matrix))
#     glUniformMatrix4fv(V_location, 1, GL_FALSE, glm.value_ptr(V_matrix))
#     glUniformMatrix4fv(P_location, 1, GL_FALSE, glm.value_ptr(P_matrix))
#
#     glDrawArrays(GL_TRIANGLES, 0, 36)


# # #zad 3
# def render(time):
#     global P_matrix
#
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glUseProgram(rendering_program)
#
#     # Oddalenie kamery
#     V_matrix = glm.lookAt(
#         glm.vec3(0.0, 0.0, 10.0),  # Pozycja kamery
#         glm.vec3(0.0, 0.0, 0.0),  # Punkt, na który patrzy kamera
#         glm.vec3(0.0, 1.0, 0.0)   # Wektor "góry"
#     )
#
#     # Przekazanie macierzy do shadera
#     glUniformMatrix4fv(glGetUniformLocation(rendering_program, "P_matrix"), 1, GL_FALSE, glm.value_ptr(P_matrix))
#     glUniformMatrix4fv(glGetUniformLocation(rendering_program, "V_matrix"), 1, GL_FALSE, glm.value_ptr(V_matrix))
#
#
#     spacing = 0.6  # Odległość między obiektami
#
#     # Rysowanie planszy
#     for i in range(-5,5):
#         for j in range(-5,5):
#             # Macierz modelu (translacja wzdłuż X i Y)
#             translation = glm.translate(glm.mat4(1.0), glm.vec3(i * spacing, j * spacing, 0.0))
#             rotation  = glm.rotate(glm.mat4(1.0), time, glm.vec3(1.0, 1.0, 0.0))
#             M_matrix = translation * rotation
#
#             glUniformMatrix4fv(glGetUniformLocation(rendering_program, "M_matrix"), 1, GL_FALSE, glm.value_ptr(M_matrix))
#
#             # Narysowanie sześcianu
#             glDrawArrays(GL_TRIANGLES, 0, 36)  # 36 wierzchołków na sześcian
#
#     glFlush()

#zad 4-5
def render(time):
    glClearBufferfv(GL_COLOR, 0, [0.0, 0.0, 0.0, 1.0])
    glClearBufferfi(GL_DEPTH_STENCIL, 0, 1.0, 0)

    V_matrix = glm.lookAt(
        glm.vec3(0.0, 0.0, 8.0),
        glm.vec3(0.0, 0.0, 0.0),
        glm.vec3(0.0, 1.0, 0.0)
    )

    glUseProgram(rendering_program)

    V_location = glGetUniformLocation(rendering_program, "V_matrix")
    P_location = glGetUniformLocation(rendering_program, "P_matrix")
    time_location = glGetUniformLocation(rendering_program, "time")

    glUniformMatrix4fv(V_location, 1, GL_FALSE, glm.value_ptr(V_matrix))
    glUniformMatrix4fv(P_location, 1, GL_FALSE, glm.value_ptr(P_matrix))
    glUniform1f(time_location, time)

    glDrawArraysInstanced(GL_TRIANGLES, 0, 36, 100)



def update_viewport(window, width, height):
    global P_matrix

    aspect = width / height
    P_matrix = glm.perspective(glm.radians(70.0), aspect, 0.1, 1000.0)

    glViewport(0, 0, width, height)


def keyboard_key_callback(window, key, scancode, action, mods):
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)


def glfw_error_callback(error, description):
    print('GLFW Error:', description)


def main():
    glfwSetErrorCallback(glfw_error_callback)

    if not glfwInit():
        sys.exit(-1)

    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
    # Poniższą linijkę odkomentować w przypadku pracy w systemie macOS!
    # glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
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

