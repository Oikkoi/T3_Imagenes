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
    alto, ancho = obtener_tamaño_imagen(img)
    pad_y_total = max(0, L - alto)
    pad_x_total = max(0, L - ancho)
    
    pad_top = pad_y_total // 2
    pad_bottom = pad_y_total - pad_top

    pad_left = pad_x_total // 2
    pad_right = pad_x_total - pad_left

    tupla_pad = ((pad_top, pad_bottom), (pad_left, pad_right))
    if mode == "zero":
        padded = np.pad(img, pad_width=tupla_pad, mode="constant")
    elif mode == "reflect":
        padded = np.pad(img, pad_width=tupla_pad, mode="reflect")
    elif mode == "edge":
        padded = np.pad(img, pad_width=tupla_pad, mode="edge")
    else:
        raise ValueError("modo inválido. Se espera 'zero', 'edge' o 'period'")
    return padded

if __name__ == "__main__":
    imagen = "cameraman.png"
    array_imagen = cargar_imagen(imagen) 
    # visualizar(array_imagen) 
    # imagen_padded = padding(array_imagen, "edge", 512)