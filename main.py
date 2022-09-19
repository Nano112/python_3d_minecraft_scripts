from turtle import width
import numpy as np
import pygame
from fxpmath import Fxp 

cube = [[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]]
adjacency = [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]]
identity_matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
binary_notation = [8, 7]

def get_scale_matrix(scale):
    return np.array([[scale, 0, 0], [0, scale, 0], [0, 0, scale]])

def get_rotation_matrix_x(angle):
    return np.array([[1, 0, 0], [0, np.cos(angle), -np.sin(angle)], [0, np.sin(angle), np.cos(angle)]])

def get_rotation_matrix_y(angle):
    return np.array([[np.cos(angle), 0, np.sin(angle)], [0, 1, 0], [-np.sin(angle), 0, np.cos(angle)]])

def get_rotation_matrix_z(angle):
    return np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])

def multiply_matrix(matrix, vector):
    return np.dot(matrix, vector)

def multiply_matrix_array(matrix, array):
    return [list(multiply_matrix(matrix, vector)) for vector in array]


def convert_to_binary_notation(number):
    return Fxp(number, signed=True, n_word=binary_notation[0] + binary_notation[1], n_frac=binary_notation[1]).bin(frac_dot=True)

def print_matrix_binary_notation(matrix):
    for row in matrix:
        print([convert_to_binary_notation(number) for number in row])
        
def print_array_binary_notation(array):
    for vector in array:
        print([convert_to_binary_notation(number) for number in vector])
        
def compose_matrix(matrix1, matrix2):
    return np.dot(matrix1, matrix2)

def project_cube_to_screen(cube):
    scaling = 16
    return [[scaling * vector[0] / vector[2], scaling * vector[1] / vector[2], scaling * vector[2] / vector[2]] for vector in cube]
    
def get_screen_cords(cube, width, height):
    projected_cube = project_cube_to_screen(cube)
    return [[(vector[0] + 1) * width / 2, (vector[1] + 1) * height / 2] for vector in projected_cube]

def draw_object(screen, vertices, faces, width, height):
    screen.fill((0, 0, 0))
    for face in faces:
        for i in range(len(face)):
            pygame.draw.line(screen, (255, 255, 255), get_screen_cords([vertices[face[i]]], width, height)[0], get_screen_cords([vertices[face[(i + 1) % len(face)]]], width, height)[0], 1)
    pygame.display.flip()
    
def draw_object_as_points(screen, vertices, width, height):
    screen.fill((0, 0, 0))
    for vertex in vertices:
        pygame.draw.circle(screen, (255, 255, 255), get_screen_cords([vertex], width, height)[0], 1)
    pygame.display.flip()

def get_obj_file(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        vertices = []
        faces = []
        for line in lines:
            if line[0] == 'v':
                vertices.append([float(number) for number in line.split()[1:]])
            elif line[0] == 'f':
                faces.append([int(number) - 1 for number in line.split()[1:]])
        return vertices, faces
    


pygame.init()
width = 128
height = 128
window = pygame.display.set_mode((width, height))
run = True
# scale the cube to fit the screen
scale_matrix = get_scale_matrix(2)
object, faces = get_obj_file('cube2.obj')
object = multiply_matrix_array(scale_matrix, object)
# rotate the cube
rotation_matrix_x = get_rotation_matrix_x(0.005) 
rotation_matrix_y = get_rotation_matrix_y(0.01)
# rotation_matrix_z = get_rotation_matrix_z(0.03)
# compose the rotation matrix
rotation_matrix = compose_matrix(rotation_matrix_x, rotation_matrix_y)
# rotation_matrix = compose_matrix(rotation_matrix, rotation_matrix_z)
object = multiply_matrix_array(rotation_matrix, object)
translate = np.array([0,0, 90])
frame_count = 0
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    translated_object = [[vector[0] + translate[0], vector[1] + translate[1], vector[2] + translate[2]] for vector in object]
    draw_object_as_points(window, translated_object, width, height)
    
    object = multiply_matrix_array(rotation_matrix, object)
    pygame.display.update()
    # save the frame to a file with the name of the frame number
    pygame.image.save(window, 'frames/' + str(frame_count) + '.png')
    frame_count += 1
    # stop after 360 frames
    if frame_count == 360:
        run = False
    # run = False
