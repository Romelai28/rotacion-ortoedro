import pygame
import math
import numpy as np
from sys import exit

# COLORES:
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
ROSA = (255, 0, 255)
CIAN = (0, 255, 255)
NARANJA = (255, 128, 0)
BLANCO_SUAVE = (200, 200, 200)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

pygame.init()

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600

scalar = 100
shift_x = WINDOW_WIDTH / 2
shift_y = WINDOW_HEIGHT / 2
FPS = 60

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("3D cube")
clock = pygame.time.Clock()

# CONFIGURACIONES INICIALES
# Ángulos iniciales
ang_x = 1
ang_y = 2
ang_z = 3
# Velocidades constantes
vel_x = 0.03 * 0.5
vel_y = 0.1 * 0.5
vel_z = 0.01 * 0.5
# Puntos por componente (Su valor absoluto) y eje de rotación
x_i = -2
x_f = 1
y_i = -2
y_f = 1
z_i = -1
z_f = 2

points = []
for x in range(x_i, x_f):
    for y in range(y_i, y_f):
        for z in range(z_i, z_f):
            points.append(np.matrix([x, y, z]))

# CUADRADO DE LxMxN
l_lados = abs(x_f - x_i) - 1
m_lados = abs(y_f - y_i) - 1
n_lados = abs(z_f - z_i) - 1

p_matrix = np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 0]])

aristas = [0, n_lados,
           m_lados*(n_lados+1), (m_lados+1)*(n_lados+1)-1,
           l_lados * (m_lados + 1) * (n_lados + 1), l_lados*(m_lados+1)*(n_lados+1) + n_lados,
           (l_lados+1)*(m_lados+1)*(n_lados+1)-1 - n_lados, (n_lados+1)*(m_lados+1)*(l_lados+1)-1]

lista_caras = [
    (aristas[0], aristas[1], aristas[3], aristas[2], AZUL),
    (aristas[4], aristas[6], aristas[7], aristas[5], ROJO),
    (aristas[2], aristas[6], aristas[4], aristas[0], VERDE),
    (aristas[5], aristas[1], aristas[0], aristas[4], AMARILLO),
    (aristas[3], aristas[2], aristas[6], aristas[7], BLANCO),
    (aristas[7], aristas[5], aristas[1], aristas[3], ROSA)
]


def unir_puntos(a, b):
    pygame.draw.aaline(WINDOW, BLANCO_SUAVE,
                       (matrix_proyectada[a].item(0) * scalar + shift_x,
                        matrix_proyectada[a].item(1) * scalar + shift_y),
                       (matrix_proyectada[b].item(0) * scalar + shift_x,
                        matrix_proyectada[b].item(1) * scalar + shift_y), 15)


def dibujar_una_cara(a, b, c, d, color):
    pygame.draw.polygon(WINDOW, color,
                        [(matrix_proyectada[a].item(0) * scalar + shift_x,
                          matrix_proyectada[a].item(1) * scalar + shift_y),
                         (matrix_proyectada[b].item(0) * scalar + shift_x,
                          matrix_proyectada[b].item(1) * scalar + shift_y),
                         (matrix_proyectada[c].item(0) * scalar + shift_x,
                          matrix_proyectada[c].item(1) * scalar + shift_y),
                         (matrix_proyectada[d].item(0) * scalar + shift_x,
                          matrix_proyectada[d].item(1) * scalar + shift_y)])


def dibujar_contorno_exterior():
    # CARA UNO:
    unir_puntos(aristas[0], aristas[1])
    unir_puntos(aristas[0], aristas[2])
    unir_puntos(aristas[1], aristas[3])
    unir_puntos(aristas[2], aristas[3])

    # CARA DOS:
    unir_puntos(aristas[4], aristas[6])
    unir_puntos(aristas[6], aristas[7])
    unir_puntos(aristas[4], aristas[5])
    unir_puntos(aristas[5], aristas[7])

    # RESTO:
    unir_puntos(aristas[0], aristas[4])
    unir_puntos(aristas[1], aristas[5])
    unir_puntos(aristas[3], aristas[7])
    unir_puntos(aristas[2], aristas[6])


def dibujar_todas_caras():
    lista_ordenada_z = ordenar()
    for n in range(len(lista_caras)):
        for indice in range(4):
            if lista_caras[n][indice] == lista_ordenada_z[0][0]:
                dibujar_una_cara(
                    lista_caras[n][0],
                    lista_caras[n][1],
                    lista_caras[n][2],
                    lista_caras[n][3],
                    lista_caras[n][4]
                )
                break


def mostrar_enumeracion(elementos):
    font1 = pygame.font.SysFont(str(elementos), 30)
    img1 = font1.render(str(elementos), True, ROJO)
    WINDOW.blit(img1, (x_component * scalar + shift_x, y_component * scalar + shift_y))


def sort_second(val):
    return val[1]


def ordenar():
    lista_z = []
    for arista in aristas:
        z_tupla = [arista, matrix_sin_proyectar[arista].item(2)]  # Primer valor el n-arista y el segundo su valor de z.
        lista_z.append(z_tupla)

    # lista_z.sort(key=sort_second)
    lista_z.sort(key=sort_second, reverse=True)
    return lista_z


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    WINDOW.fill(NEGRO)

    rotation_x = np.matrix([
        [1, 0, 0],
        [0, math.cos(ang_x), -math.sin(ang_x)],
        [0, math.sin(ang_x), math.cos(ang_x)]
    ])

    rotation_y = np.matrix([
        [math.cos(ang_y), 0, math.sin(ang_y)],
        [0, 1, 0],
        [-math.sin(ang_y), 0, math.cos(ang_y)]
    ])

    rotation_z = np.matrix([
        [math.cos(ang_z), -math.sin(ang_z), 0],
        [math.sin(ang_z), math.cos(ang_z), 0],
        [0, 0, 1]
    ])

    matrix_sin_proyectar = []
    matrix_proyectada = []

    for i in range(len(points)):
        # Tomo un vector de la matriz:
        vector_rotado_1 = np.matrix(np.dot(rotation_x, points[i].reshape(3, 1)))  # Aplico transformación en x.
        vector_rotado_2 = np.matrix(np.dot(rotation_y, vector_rotado_1))  # Aplico transformación en y.
        vector_rotado_3 = np.matrix(np.dot(rotation_z, vector_rotado_2))  # Aplico transformación en z. Vector final.

        # Lo proyecto al vector final a dos dimensiones.
        vector_proyectado_2d = np.matrix(np.dot(p_matrix, vector_rotado_3))

        matrix_sin_proyectar.append(vector_rotado_3)
        matrix_proyectada.append(vector_proyectado_2d)

    # El for loop, el x_component, y_component son necesarios para mostrar puntos, enunmerar aristas y resaltar aristas.
    for i in range(len(matrix_proyectada)):

        x_component = matrix_proyectada[i].item(0)
        y_component = matrix_proyectada[i].item(1)

        # MOSTRAR PUNTOS
        # pygame.draw.circle(WINDOW, ROJO, (x_component * scalar + shift_x, y_component * scalar + shift_y), 2)

        # ENUMERAR ARISTAS
        # if i in aristas:
        #     mostrar_enumeracion(i)

        # RESALTAR ARISTAS
        # if i in aristas:
        #     pygame.draw.circle(WINDOW, CIAN, (x_component * scalar + shift_x, y_component * scalar + shift_y), 7)

    dibujar_contorno_exterior()
    dibujar_todas_caras()

    ang_x += vel_x
    ang_y += vel_y
    ang_z += vel_z

    pygame.display.update()
    clock.tick(FPS)
