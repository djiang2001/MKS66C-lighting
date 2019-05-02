import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    color = [0,0,0]
    
    normalize(normal)
    normalize(light[LOCATION])
    normalize(view)

    a = calculate_ambient(ambient, areflect)
    d = calculate_diffuse(light, dreflect, normal)
    s = calculate_specular(light, sreflect, view, normal)

    for index in range(len(color)):
        color[index] = a[index] + d[index] + s[index]
    return limit_color(color)

def calculate_ambient(alight, areflect):
    color = [0,0,0]
    for index in range(len(color)):
        color[index] = alight[index] * areflect[index]
    return limit_color(color)
    

def calculate_diffuse(light, dreflect, normal):
    color = [0, 0, 0]
    dot = dot_product( light[LOCATION], normal)
    for index in range(len(color)):
        color[index] = light[COLOR][index] * dreflect[index] * dot
    return limit_color(color)

def calculate_specular(light, sreflect, view, normal):
    color = [0,0,0]
    temp = [0,0,0]

    c = 2 * dot_product(light[LOCATION], normal)
    for index in range(len(temp)):
        temp[index] = normal[index] * c - light[LOCATION][index]

    c = (dot_product(temp, view))
    c = c if c > 0 else 0
    c = pow(c, SPECULAR_EXP)
    for index in range(len(color)):
        color[index] = light[COLOR][index] * sreflect[index] * c

    return limit_color(color)
    
    

def limit_color(color):
    for index in range(len(color)):
        color[index] = int(color[index])
        if color[index] > 255:
            color[index] = 255
        elif color[index] < 0:
            color[index] = 0
    return color

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude
    return vector

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
