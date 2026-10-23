from skimage import io
import numpy as np
import matplotlib.pyplot as plt
import os


def cargar_imagen(file_name: str) -> np.array:
    """
    Recibe un str y retorna el array de la imagen Gray
    """
    imagen = io.imread(file_name, as_gray=True)
    return imagen


def obtener_tamaño_imagen(array_imagen: np.array) -> tuple:
    """
    Función que retorna el tamaño del array de la imagen
    """
    return array_imagen.shape


def visualizar(img: np.array, compleja: bool = False) -> None:
    """
    Recibe un array de imagen, luego la muestra con una colorbar activa
    No retorna nada
    """
    if compleja:
        img = np.log(1 + np.abs(img))
    img = np.clip(np.divide(img, np.max(img)), 0, 1)
    plt.imshow(img, cmap='gray')
    plt.colorbar()
    plt.title(f'shape={img.shape}, dtype={img.dtype}')
    plt.show()
    return


def guardar(img: np.array, compleja: bool, nombre_archivo: str, nombre_experimento: str) -> None:
    """
    Recibe un array de numpy (la imagen que se quiere guardar), un booleano para hacer visibles las imágenes que son complejas,
    el nombre del archivo (Importante: con su extensión!) y el nombre del experimento en proceso (para nombrar la carpeta)
    """
    ruta = os.path.join(os.path.dirname(__file__),
                        f"Resultados_{nombre_experimento}")
    file_name = os.path.join(ruta, nombre_archivo)
    os.makedirs(f"Resultados_{nombre_experimento}", exist_ok=True)
    if compleja:
        img = np.log(1 + np.abs(img))
    img = np.clip(np.divide(img, np.max(img)), 0, 1)
    plt.imsave(file_name, img, cmap="gray")
    return
