from skimage import io
import numpy as np
import matplotlib.pyplot as plt


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
    plt.imshow(img, cmap='gray')
    plt.colorbar()
    plt.title(f'shape={img.shape}, dtype={img.dtype}')
    plt.show()
    return


def guardar(img: np.array, compleja: bool) -> None:
    if compleja:
        img = np.log(1 + np.abs(img))
    plt.imsave(f"{input("Nombre para la imagen (sin extensión): ")}.jpg", np.abs(
        img*255).astype("float64"), cmap="gray")
    return
