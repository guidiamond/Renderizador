# Desenvolvido por: Luciano Soares <lpsoares@insper.edu.br>
# Disciplina: Computação Gráfica
# Data: 28 de Agosto de 2020

import argparse     # Para tratar os parâmetros da linha de comando
import x3d          # Faz a leitura do arquivo X3D, gera o grafo de cena e faz traversal
import interface    # Janela de visualização baseada no Matplotlib
import gpu          # Simula os recursos de uma GPU

from numpy import array, empty, dot, concatenate
from render.point import Point
from render.line import Line
from render.triangle import Triangle
from math import sin, cos, tan

LARGURA = 400
ALTURA = 200

TRANSFORM_STACK = [[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]]
SCREEN_COORDS = array([[LARGURA/2, 0, 0, LARGURA/2],
                       [0, -ALTURA/2, 0, ALTURA/2],
                       [0, 0, 1, 0], [0, 0, 0, 1]])

def matrix_normalize(matrix):
    transv_matrix = matrix.T
    # 3x4 array gen
    new_mat = empty([3,4])
    for i in range(len(transv_matrix)):
        max_val =  transv_matrix[i][0] #start with max = first element
        for e in transv_matrix[i]:
            if e > max_val:
                max_val = e
        # divide every element of the matrix by the max val
        new_mat[i] = transv_matrix[i]/max_val # normalization
    return new_mat.T

def call_point(point, color):
    Point(point,color).render()

def call_line(lineSegments, color):
    Line(lineSegments, color).render()

def call_triangle(vertices, color):
    Triangle(vertices, color).render()

def triangleSet(point, color):
    for i in range(0,len(point),9):
        # p1
        p1 = array(point[i:i+3]+[1]).T
        p1 = dot(TRANSFORM_STACK[-1], p1)
        # p2
        p2 = array(point[i+3:i+6]+[1]).T
        p2 = dot(TRANSFORM_STACK[-1], p2)
        # p3
        p3 = array(point[i+6:i+9]+[1]).T
        p3 = dot(TRANSFORM_STACK[-1], p3)

        normalized_x = dot(SCREEN_COORDS, matrix_normalize(array([p1,p2,p3]).T)).T
        # normalized array flat and concat to use in the call_triangle function
        vertices = concatenate((normalized_x[0][0:2],normalized_x[1][0:2],normalized_x[2][0:2]), axis=None)
        call_triangle(vertices, color)

def viewpoint(position, orientation, fieldOfView):
    close_dist = 0.5
    far_dist = 100
    position_matrix = array([[1, 0, 0, -position[0]],
                             [0, 1, 0, -position[1]],
                             [0, 0, 1, -position[2]],
                             [0, 0, 0, 1]])
    orientation_matrix = array([[1, 0, 0, 0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
    if orientation[0]:
        orientation_matrix[1] = [0, cos(orientation[3]), -sin(orientation[3]), 0]
        orientation_matrix[2] = [0, sin(orientation[3]), cos(orientation[3]), 0]

    elif orientation[1]:
        orientation_matrix[0] = [cos(orientation[3]), 0, sin(orientation[3]), 0]
        orientation_matrix[2] = [-sin(orientation[3]), 0, cos(orientation[3]), 0]

    elif orientation[2]:
        orientation_matrix[0] = [cos(orientation[3]), -sin(orientation[3]), 0, 0]
        orientation_matrix[1] = [sin(orientation[3]), cos(orientation[3]), 0, 0]

    matrix_view = dot(orientation_matrix, position_matrix)
    aspect_ratio = LARGURA/ALTURA
    #positions
    # top = -bottom
    top = close_dist * tan(fieldOfView)
    bottom = -top
    # right = -left
    right = top*aspect_ratio
    left = -right

    perspective_matrix = array([[close_dist / right, 0, 0, 0],
                                [0, close_dist / top, 0, 0],
                                [0, 0, -(far_dist+close_dist) / (far_dist-close_dist),
                                 -(2*far_dist*close_dist) / (far_dist-close_dist)],
                                  [0, 0, -1, 0]])
    TRANSFORM_STACK.append(dot(matrix_view, TRANSFORM_STACK[-1]))
    TRANSFORM_STACK.append(dot(perspective_matrix, TRANSFORM_STACK[-1]))



def transform(translation, scale, rotation):
    angle = rotation[3]
    translation_matrix = array([[1, 0, 0, translation[0]],
                                [0, 1, 0, translation[1]],
                                [0, 0, 1, translation[2]],
                                [0, 0, 0, 1]])
    scale_matrix = array([[scale[0], 0, 0, 0],
                          [0, scale[1], 0, 0],
                          [0, 0, scale[2], 0],
                          [0, 0, 0, 1]])
    if rotation[0]:
        rotation_matrix = array([[1, 0, 0, 0],
                                 [0, cos(angle), -sin(angle), 0],
                                 [0, sin(angle), cos(angle), 0],
                                 [0, 0, 0, 1]])
    elif rotation[1]:
        rotation_matrix = array([[cos(angle), 0, sin(angle), 0],
                                 [0, 1, 0, 0],
                                 [-sin(angle), 0, cos(angle), 0],
                                 [0, 0, 0, 1]])
    elif rotation[2]:
        rotation_matrix = array([[cos(angle), -sin(angle), 0, 0],
                                 [sin(angle), cos(angle), 0, 0],
                                 [0, 0, 1 ,0],
                                 [0, 0, 0, 1]])

    m = dot(dot(translation_matrix, scale_matrix), rotation_matrix)
    TRANSFORM_STACK.append(dot(TRANSFORM_STACK[-1], m))

def _transform():
    TRANSFORM_STACK.pop()

def triangleStripSet(point, stripCount, color):
    p_idx=0
    for _ in range(int(stripCount[0]-2)):
        point1=point[p_idx:p_idx+3]
        point2=point[p_idx+3:p_idx+6]
        point3=point[p_idx+6:p_idx+9]
        
        points=point1+point2+point3
        p_idx+=3

        triangleSet(points,color)

def indexedTriangleStripSet(point, index, color):
    pts = [point[3*i:3*(i+1)] for i in range(len(index))]

    for i in range(len(index)-3):
        point1 = pts[index[i]]
        point2 = pts[index[i+1]]
        point3 = pts[index[i+2]]

        pointList=point1+point2+point3
        triangleSet(pointList,color)

def box(size, color):
    x = size[0] / 2
    y = size[1] / 2
    z = size[2] / 2

    ps = [[-x, y, z], [-x, -y, z],
          [x, y, z], [x, -y, z],
          [x, y, -z], [x, -y, -z],
          [-x, y, -z], [-x, -y, -z]]

    # gen points
    triangleStripSet(ps[0]+ps[1]+ps[2]+ps[3], [4], color)
    triangleStripSet(ps[1]+ps[7]+ps[3]+ps[5], [4], color)
    triangleStripSet(ps[2]+ps[3]+ps[4]+ps[5], [4], color)
    triangleStripSet(ps[4]+ps[5]+ps[6]+ps[7], [4], color)
    triangleStripSet(ps[6]+ps[7]+ps[0]+ps[1], [4], color)
    triangleStripSet(ps[6]+ps[0]+ps[4]+ps[2], [4], color)

if __name__ == '__main__':

    # Valores padrão da aplicação
    width = LARGURA
    height = ALTURA

    x3d_file = "exemplo6.x3d"
    image_file = "tela.png"

    # Tratando entrada de parâmetro
    parser = argparse.ArgumentParser(add_help=False)   # parser para linha de comando
    parser.add_argument("-i", "--input", help="arquivo X3D de entrada")
    parser.add_argument("-o", "--output", help="arquivo 2D de saída (imagem)")
    parser.add_argument("-w", "--width", help="resolução horizonta", type=int)
    parser.add_argument("-h", "--height", help="resolução vertical", type=int)
    parser.add_argument("-q", "--quiet", help="não exibe janela de visualização", action='store_true')
    args = parser.parse_args() # parse the arguments
    if args.input: x3d_file = args.input
    if args.output: image_file = args.output
    if args.width: width = args.width
    if args.height: height = args.height

    # Iniciando simulação de GPU
    gpu.GPU(width, height, image_file)

    # Abre arquivo X3D
    scene = x3d.X3D(x3d_file)
    scene.set_resolution(width, height)

    # funções que irão fazer o rendering
    x3d.X3D.render["Polypoint2D"] = call_point
    x3d.X3D.render["Polyline2D"] = call_line
    x3d.X3D.render["TriangleSet2D"] = call_triangle
    x3d.X3D.render["TriangleSet"] = triangleSet
    x3d.X3D.render["Viewpoint"] = viewpoint
    x3d.X3D.render["Transform"] = transform
    x3d.X3D.render["_Transform"] = _transform
    x3d.X3D.render["TriangleStripSet"] = triangleStripSet
    x3d.X3D.render["IndexedTriangleStripSet"] = indexedTriangleStripSet
    x3d.X3D.render["Box"] = box
    x3d.X3D.render["IndexedFaceSet"] = indexedFaceSet



    # Se no modo silencioso não configurar janela de visualização
    if not args.quiet:
        window = interface.Interface(width, height)
        scene.set_preview(window)

    scene.parse() # faz o traversal no grafo de cena

    # Se no modo silencioso salvar imagem e não mostrar janela de visualização
    if args.quiet:
        gpu.GPU.save_image() # Salva imagem em arquivo
    else:
        window.image_saver = gpu.GPU.save_image # pasa a função para salvar imagens
        window.preview(gpu.GPU._frame_buffer) # mostra janela de visualização
