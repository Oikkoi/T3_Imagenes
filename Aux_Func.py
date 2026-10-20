from skimage import io
import numpy as np
import matplotlib.pyplot as plt

def cargar_imagen(file_name:str):
    imagen = io.imread(file_name, as_gray="True")
    return imagen

def obtener_tamaño_imagen(array_imagen: np.array):
    return array_imagen.shape

def visualizar(img: np.array):
    plt.imshow(img, cmap='gray')
    plt.colorbar()
    plt.title(f'shape={img.shape}, dtype={img.dtype}')
    plt.show()
    return

if __name__ == "__main__":
    imagen = "cameraman.png"
    array_imagen = cargar_imagen(imagen) 
    # visualizar(array_imagen) 
    # obtener_tamaño_imagen(array_imagen)