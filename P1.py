import Aux_Func as aux
from skimage import io
import matplotlib.pyplot as plt
import numpy as np


def padding(img: np.array, mode: str, L: int):
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


def aplicar_fft(imagen: np.array):
    transformada = np.fft.fft2(imagen)
    transformada = np.fft.fftshift(transformada)
    reescalada = np.log(1 + np.abs(transformada))
    aux.visualizar(reescalada)


if __name__ == "__main__":
    imagen = "cameraman.png"
    array_imagen = aux.cargar_imagen(imagen)
    # aux.visualizar(array_imagen)
    imagen_padded, pads = padding(array_imagen, "period", 512)
    # aux.visualizar(imagen_padded)
    aplicar_fft(imagen_padded)
