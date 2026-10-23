import Aux_Func as aux
from skimage import io
import matplotlib.pyplot as plt
import numpy as np


def padding(img: np.array, mode: str, L: int) -> np.array:
    """
    mode: Tipo de padding. 'zero' para rellenar con 0. 
    'reflect' para que se refleje desde el borde. 'edge' para repetir el valor del borde.
    L es un int que se refiere al tamaño objetivo de la imagen,
    """
    alto, ancho = aux.obtener_tamaño_imagen(img)
    pad_y_total = max(0, L - alto)
    pad_x_total = max(0, L - ancho)

    pad_top = pad_y_total // 2
    pad_bottom = pad_y_total - pad_top

    pad_left = pad_x_total // 2
    pad_right = pad_x_total - pad_left

    tupla_pad = ((pad_top, pad_bottom), (pad_left, pad_right))
    if mode == "zero":
        padded = np.pad(img, pad_width=tupla_pad, mode="constant")
    elif mode == "period":
        padded = np.pad(img, pad_width=tupla_pad, mode="reflect")
    elif mode == "edge":
        padded = np.pad(img, pad_width=tupla_pad, mode="edge")
    else:
        raise ValueError("modo inválido. Se espera 'zero', 'edge' o 'period'")
    return padded, (pad_top, pad_right, pad_bottom, pad_left)


def aplicar_fft(imagen: np.array) -> np.array:
    """
    Recibe el array de imagen, retorna la imagen en fourier tras hacer 
    el shift para poner el origen al centro
    """
    transformada = np.fft.fft2(imagen)
    transformada = np.fft.fftshift(transformada)
    return transformada


def crear_coords(espectro: np.array):
    """
    Entra la imagen en Fourier, sale la matriz de coordenadas en x 
    (cte vertical) e y (cte horizontal) respectivamente
    """
    alto, ancho = aux.obtener_tamaño_imagen(espectro)
    eje_x = np.arange(-ancho // 2, ancho // 2)
    eje_y = np.arange(-alto//2, alto//2)
    U, V = np.meshgrid(eje_x, eje_y)
    return U, V


def calculo_distancias(punto: tuple, matriz_distancias_x: np.array, matriz_distancias_y: np.array) -> tuple:
    u_0, v_0 = punto

    distancia_1 = np.sqrt((matriz_distancias_x - u_0) **
                          2 + (matriz_distancias_y - v_0)**2)
    distancia_2 = np.sqrt((matriz_distancias_x + u_0) **
                          2 + (matriz_distancias_y + v_0)**2)
    return (distancia_1, distancia_2)


def obtener_H(puntos: list[tuple], matriz_distancias_x: np.array, matriz_distancias_y: np.array, radio: int, notch: int) -> np.array:
    if notch not in (1, 2):
        raise ValueError("Se espera notch 1 o 2")
    H = np.ones(aux.obtener_tamaño_imagen(matriz_distancias_x))
    if notch == 1:
        for punto in puntos:
            distancia1, distancia2 = calculo_distancias(
                punto, matriz_distancias_x, matriz_distancias_y)
            H = H * (distancia1 > radio) * (distancia2 > radio)
    if notch == 2:
        for punto in puntos:
            distancia1, distancia2 = calculo_distancias(
                punto, matriz_distancias_x, matriz_distancias_y)
            H = H * (1 - np.exp(-(distancia1**2)/(2*radio**2))) * \
                (1 - np.exp(-(distancia2**2)/(2*radio**2)))
    return H


def aplicar_H(espectro: np.array, H: np.array) -> np.array:
    return espectro * H


def regresar_a_espacio(G: np.array) -> np.array:
    unshift = np.fft.ifftshift(G)
    espacial = np.fft.ifft2(unshift)
    g = np.real(espacial)
    return g


def unpadding(imagen_espacial: np.array, bordes: tuple) -> np.array:
    arriba, derecha, abajo, izquierda = bordes
    alto, ancho = aux.obtener_tamaño_imagen(imagen_espacial)
    imagen_terminada = imagen_espacial[arriba:(
        alto - abajo), izquierda:(ancho - derecha)]
    imagen_terminada = np.clip(imagen_terminada*255, 0, 255)
    imagen_terminada = imagen_terminada.astype("uint8")
    return imagen_terminada


def proceso_completo(radio: int, notch: int, imagen: str, objetivo_padding: int, lista_puntos: list[tuple]) -> np.array:
    array_imagen = aux.cargar_imagen(imagen)
    imagen_padded, pads = padding(array_imagen, "period", L)
    trans = aplicar_fft(imagen_padded)
    U, V = crear_coords(trans)
    H = obtener_H(lista_puntos, U, V, r, notch)
    G = aplicar_H(trans, H)
    g_padded = regresar_a_espacio(G)
    g = unpadding(g_padded, pads)
    return g


if __name__ == "__main__":
    r = 1
    notch = 2
    imagen = "cameraman.jpg"
    lista_puntos = [(0, 21), (0, 47), (0, 74), (0, 82), (0, 118),
                    (0, 135), (0, 145), (0, 185), (0, 204), (0, 223), (0, 234)]
    L = 512

    g = proceso_completo(r, notch, imagen, L, lista_puntos)
    aux.visualizar(g)
