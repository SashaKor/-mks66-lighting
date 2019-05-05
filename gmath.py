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
    ambient = calculate_ambient(ambient, areflect)
    diffuse = calculate_diffuse(light, dreflect, normal)
    specular = calculate_specular(light, sreflect, view, normal)
    #I= A+D+S
    #have to calculate intensity for r,g,b
    lighting =[limit_color(int(ambient[0]) + int(diffuse[0]) + int(specular[0])),
        limit_color(int(ambient[1]) + int(diffuse[1]) + int(specular[1])),
        limit_color(int(ambient[2]) + int(diffuse[2]) + int(specular[2]))]
    return lighting

def calculate_ambient(alight, areflect):
    ambient= [alight[0]*areflect[0], alight[1]*areflect[1], alight[2]*areflect[2]]
    return ambient


def calculate_diffuse(light, dreflect, normal):
    vals = [light[COLOR][0], light[COLOR][1], light[COLOR][2]]
    normalize(normal)
    constant = dot_product(normal, light[LOCATION])

    diffuse=[limit_color(vals[0]*constant*dreflect[0]),
    limit_color(vals[1]*constant*dreflect[1]),
    limit_color(vals[2]*constant*dreflect[2])]

    return diffuse

def calculate_specular(light, sreflect, view, normal):
    vals = [light[COLOR][0], light[COLOR][1], light[COLOR][2]]
    normalize(normal)
    constant = dot_product(normal, light[LOCATION])

    lst = normal[:]

    for i in range(0, 3):
        lst[i] *= 2 * constant
        lst[i] -= light[LOCATION][i]

    #specular exponent might be wonky
    specular= [limit_color(vals[0]*(sreflect[0]*dot_product(lst,view))** 3),
    limit_color(vals[1]*(sreflect[1]*dot_product(lst,view))** 3),
    limit_color(vals[2]*(sreflect[2]*dot_product(lst,view))** 3),
    ]
    return specular

def limit_color(color):
    #should always be between 0 and 255
    return max(min(color,255),0)

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

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
